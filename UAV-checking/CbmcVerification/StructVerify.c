/*
 ============================================================================
 Name        : StructVerify.c
 Author      : rao
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */


#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <assert.h>

#define RCINPUT_UDP_NUM_CHANNELS 8
// used to pack structures
#define HAL_BOARD_SITL     3
# define EKF_ORIGIN_MAX_DIST_M         50000   // EKF origin and waypoints (including home) must be within 50km
#define LOCATION_SCALING_FACTOR 0.011131884502145034f

struct __attribute__((packed)) rc_udp_packet {
    uint32_t version;
    uint64_t timestamp_us;
    uint16_t sequence;
    uint16_t pwms[RCINPUT_UDP_NUM_CHANNELS];
};

#define PACKED __attribute__((__packed__))


typedef struct PACKED  {
    uint8_t relative_alt : 1;           // 1 if altitude is relative to home
    uint8_t unused1      : 1;           // unused flag (defined so that loiter_ccw uses the correct bit)
    uint8_t loiter_ccw   : 1;           // 0 if clockwise, 1 if counter clockwise
    uint8_t terrain_alt  : 1;           // this altitude is above terrain
    uint8_t origin_alt   : 1;           // this altitude is above ekf origin
    uint8_t loiter_xtrack : 1;          // 0 to crosstrack from center of waypoint, 1 to crosstrack from tangent exit location
}Location_Option_Flags;

typedef struct PACKED {

        Location_Option_Flags flags;                    ///< options bitmask (1<<0 = relative altitude)
        uint8_t options;                                /// allows writing all flags to eeprom as one byte

    // by making alt 24 bit we can make p1 in a command 16 bit,
    // allowing an accurate angle in centi-degrees. This keeps the
    // storage cost per mission item at 15 bytes, and allows mission
    // altitudes of up to +/- 83km
    int32_t alt:24;                                     ///< param 2 - Altitude in centimeters (meters * 100) see LOCATION_ALT_MAX_M
    int32_t lat;                                        ///< param 3 - Latitude * 10**7
    int32_t lng;                                        ///< param 4 - Longitude * 10**7
} Location;

enum EKF_TYPE {EKF_TYPE_NONE=0,
                   EKF_TYPE3=3,
                   EKF_TYPE2=2
#if CONFIG_HAL_BOARD == HAL_BOARD_SITL
                   ,EKF_TYPE_SITL=10
#endif
    };

uint8_t ekf_type(){
	int a = rand() % 10 - 6;
	return a;
}

const bool AP_AHRS_NavEKF_get_origin(Location *ret)
{
    switch (ekf_type()) {
    case EKF_TYPE_NONE:
        return false;

    case EKF_TYPE2:
    default:
        if (true) {//!EKF2.getOriginLLH(-1,ret)
            return false;
        }
        return true;

    case EKF_TYPE3:
        if (true) {//!EKF3.getOriginLLH(-1,ret)
            return false;
        }
        return true;

#if CONFIG_HAL_BOARD == HAL_BOARD_SITL
    case EKF_TYPE_SITL:
        if (!_sitl) {
            return false;
        }
        const struct SITL::sitl_fdm &fdm = _sitl->state;
        ret = fdm.home;
        return true;
#endif
    }
}


const Location AP_InertialNav_NavEKF_get_origin()
{
	 Location *ret;
     if (AP_AHRS_NavEKF_get_origin(ret)) {
         // initialise location to all zeros if EKF origin not yet set
         memset(&ret, 0, sizeof(ret));
     }
    return *ret;
}

float longitude_scale(const Location *loc)
{
    float scale =(float)rand(); //cosf(loc.lat * 1.0e-7f * DEG_TO_RAD);
    return scale;//constrain_float(scale, 0.01f, 1.0f);
}

float norm(const float first, const float second)
{
    return rand();//sqrtf(sq(first, second, parameters...));
}

float get_distance(const Location *loc1, const Location *loc2)
{
    float dlat              = (float)(loc2->lat - loc1->lat);
    float dlong             = ((float)(loc2->lng - loc1->lng)) * longitude_scale(loc2);
    return norm(dlat, dlong) * LOCATION_SCALING_FACTOR;
}



 bool Copter_far_from_EKF_origin( Location *loc,  Location *loc1)
{
	 loc1->alt=loc->alt;
	 loc1->lat=loc->lat;
	 loc1->lng=loc->lng;
	 loc1->options=loc->options;
    // check distance to EKF origin
    const Location ekf_origin = AP_InertialNav_NavEKF_get_origin();
    if (get_distance(&ekf_origin, loc) > EKF_ORIGIN_MAX_DIST_M) {
       return true;
    }

    const Location ekf_origin1 = AP_InertialNav_NavEKF_get_origin();
        if (get_distance(&ekf_origin1, loc1) > EKF_ORIGIN_MAX_DIST_M) {
           return true;
        }

        assert(loc1->alt==loc->alt);
        assert(loc1->lat==loc->lat);
        assert( loc1->lng==loc->lat);
        assert(loc1->options==loc->options);


    // close enough to origin
    return false;
}



int main(void) {
	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	return EXIT_SUCCESS;
}
