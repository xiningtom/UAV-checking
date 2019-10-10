#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

typedef unsigned char      uint8_t;
typedef unsigned int       uint32_t;
typedef short              int16_t;
typedef int                int32_t;
typedef char               int8_t;


//AP_Motors_Class.h
typedef struct  {
        uint8_t armed              : 1;    // 0 if disarmed, 1 if armed
        uint8_t interlock          : 1;    // 1 if the motor interlock is enabled (i.e. motors run), 0 if disabled (motors don't run)
        uint8_t initialised_ok     : 1;    // 1 if initialisation was successful
    } AP_Motors_flags;

    AP_Motors_flags _flags;
bool                armed() { return _flags.armed; }
bool                get_interlock()  { return _flags.interlock; }
float get_throttle_hover()  { return 0.5f; }

float Copter_get_pilot_desired_throttle(int16_t throttle_control, float thr_mid)
{
    if (thr_mid <= 0.0f) {
        thr_mid = get_throttle_hover();
    }

    int16_t mid_stick = mid_stick-10; //get_throttle_mid()
    // protect against unlikely divide by zero
    if (mid_stick <= 0) {
        mid_stick = 500;
    }

    // ensure reasonable throttle values
    throttle_control = (0+1000)/2; //constrain_int16(throttle_control,0,1000)

    // calculate normalised throttle input
    float throttle_in;
    if (throttle_control < mid_stick) {
        // below the deadband
        throttle_in = ((float)throttle_control)*0.5f/(float)mid_stick;
    }else if(throttle_control > mid_stick) {
        // above the deadband
        throttle_in = 0.5f + ((float)(throttle_control-mid_stick)) * 0.5f / (float)(1000-mid_stick);
    }else{
        // must be in the deadband
        throttle_in = 0.5f;
    }

    float expo = (-0.5f+1.0f)/2;//constrain_float(-(thr_mid-0.5)/0.375, -0.5f, 1.0f)
    // calculate the output throttle using the given expo function
    float throttle_out = throttle_in*(1.0f-expo) + expo*throttle_in*throttle_in*throttle_in;
    return throttle_out;
}

float Copter_get_pilot_desired_throttle1(int16_t throttle_control, float thr_mid,int16_t throttle_control1, float thr_mid1)
{ 
    thr_mid=thr_mid1;
    throttle_control1=throttle_control;
    if (thr_mid <= 0.0f) {
        thr_mid = get_throttle_hover();
    }

    int16_t mid_stick = mid_stick-10; //get_throttle_mid()
    // protect against unlikely divide by zero
    if (mid_stick <= 0) {
        mid_stick = 500;
    }

    // ensure reasonable throttle values
    throttle_control = (0+1000)/2; //constrain_int16(throttle_control,0,1000)

    // calculate normalised throttle input
    float throttle_in;
    if (throttle_control < mid_stick) {
        // below the deadband
        throttle_in = ((float)throttle_control)*0.5f/(float)mid_stick;
    }else if(throttle_control > mid_stick) {
        // above the deadband
        throttle_in = 0.5f + ((float)(throttle_control-mid_stick)) * 0.5f / (float)(1000-mid_stick);
    }else{
        // must be in the deadband
        throttle_in = 0.5f;
    }

    float expo = (-0.5f+1.0f)/2;//constrain_float(-(thr_mid-0.5)/0.375, -0.5f, 1.0f)
    // calculate the output throttle using the given expo function
    float throttle_out = throttle_in*(1.0f-expo) + expo*throttle_in*throttle_in*throttle_in;

    if (thr_mid1 <= 0.0f) {
            thr_mid1 = get_throttle_hover();
        }

        int16_t mid_stick = mid_stick-10; //get_throttle_mid()
        // protect against unlikely divide by zero
        if (mid_stick <= 0) {
            mid_stick = 500;
        }

        // ensure reasonable throttle values
        throttle_control1 = (0+1000)/2; //constrain_int16(throttle_control1,0,1000)

        // calculate normalised throttle input
        float throttle_in;
        if (throttle_control1 < mid_stick) {
            // below the deadband
            throttle_in = ((float)throttle_control1)*0.5f/(float)mid_stick;
        }else if(throttle_control1 > mid_stick) {
            // above the deadband
            throttle_in = 0.5f + ((float)(throttle_control1-mid_stick)) * 0.5f / (float)(1000-mid_stick);
        }else{
            // must be in the deadband
            throttle_in = 0.5f;
        }

        float expo = (-0.5f+1.0f)/2;//constrain_float(-(thr_mid1-0.5)/0.375, -0.5f, 1.0f)
        // calculate the output throttle using the given expo function
        float throttle_out = throttle_in*(1.0f-expo) + expo*throttle_in*throttle_in*throttle_in;

        assert(throttle_control==throttle_control1);
        assert(thr_mid==thr_mid1);
    return throttle_out;
}

int main(){

	return 0;
}


