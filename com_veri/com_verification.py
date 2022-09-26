import os
import sys
from xml.dom.minidom import parse

project="pycparser"
sys.path.append(os.getcwd().split(project)[0]+project)


def suc_output():
    print("Verification Successful")

def recur(arg_list,level,decl,type):
    """

    :param arg_list:
    :param level:
    :param strucst:
    :return:
    """
    len1 = len(arg_list)

    for d in decl:
        if d.getAttribute("name")==type:
            struct=d
            variable=struct.getElementsByTagName("variable")

            for v in variable:
                level=level+1
                if (level>len1):
                    break
                if v.getAttribute("name")==arg_list[level-1] and v.hasAttribute("ref") and level==len1:
                    return 0
                elif v.getAttribute("name")==arg_list[level-1] and v.hasAttribute("level") and level==len1:
                    sec_level=v.getAttribure("level")
                    return  sec_level
                elif v.getAttribute("name")==arg_list[level-1] and level<len1:
                    type=v.getAttribute("ref")
                    recur(arg_list,level,decl,type)
            break




def com_verification( fun_list):
    """
    :param com_file: the file or com_relation
    :param fun_list: the list of funciotn need to verify,according to the list to get relative xml file
    :return:
    """
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()

    com_relation='../../Project/'+pro_name+'/meta_data/com_veri/com.xml'
    doc_com=parse(com_relation)
    relation = doc_com.getElementsByTagName("ralation")

    dom_list={}
    for f in fun_list:
        path='../../Project/'+pro_name+'/meta_data/com_veri/sec_cert/'+f+'.xml'
        if os.path.exists(path):
            doc=parse(path)
            dom_list[f]=doc
        else:
            print("please generete "+ f+".xml first.")
            exit()


    index=0
    for r in relation:
        index=index+1
        out_fun=r.getAttribute("out_fun")
        out_arg=r.getAttribute("output_arg")
        """ accroding to structs's level, out_arg is a list"""
        out_list = out_arg.split(":")
        # print("3333")
        # print(out_list)

        out_xml1=dom_list[out_fun]

        out_xml=out_xml1.getElementsByTagName("root")


        input_fun=r.getAttribute("input_fun")
        input_arg=r.getAttribute("input_arg")
        input_list = input_arg.split(":")

        input_xml=dom_list[input_fun]

        output=(out_xml[0].getElementsByTagName("function"))[0].getElementsByTagName("output")
        out=output[0].getElementsByTagName(out_list[0])

        if len(out_list)==1 and out[0].hasAttribute("ref"):
            print("属性:"+out_fun+" "+out_arg+"  "+input_fun+" "+input_arg+" 验证结束!")
            continue
        elif len(out_list)>1 and out[0].hasAttribute("ref"):
            type = out[0].getAttribute("ref")
            decl=out_xml[0].getElementsByTagName("decl")
            arg_list=out_list[1:]
            level=0
            result=recur(arg_list,level,decl,type)
            if result==0:
                print("属性:"+out_fun+" "+out_arg+"  "+input_fun+" "+input_arg+" 验证结束!")
                continue
            else:
                input = input_xml.getElementsByTagName("function")[0].getElementsByTagName("input")
                inp = input[0].getElementsByTagName(input_list[0])
                in_level = (inp[0].getAttribute("level"))
                if result == "L" and in_level == "H":
                    index=index-1

                    print("属性:"+out_fun+" "+out_arg+"  "+input_fun+" "+input_arg +" 存在安全缺陷!")
                    print(out_arg + "'s level:" + result)
                    print(input_arg + "'s level:" + in_level)
                    """Verification fail"""
                    break
                else:
                    print(
                        "属性:" + out_fun + " " + out_arg + "  " + input_fun + " " + input_arg + " 验证结束!")
                    """successful"""
                    continue

        elif len(out_list)==1 and out[0].hasAttribute("level"):
            out_level=(out[0].getAttribute("level"))
            input=input_xml.getElementsByTagName("function")[0].getElementsByTagName("input")
            inp=input[0].getElementsByTagName(input_list[0])
            in_level=(inp[0].getAttribute("level"))
            if out_level=="L" and in_level=="H":
                index=index-1
                """fail"""
                print(
                    "属性:" + out_fun + " " + out_arg + "  " + input_fun + " " + input_arg + " 存在安全缺陷!")

                print(out_arg+" 的安全级别为:"+out_level)
                print(input_arg+" 的安全级别为:"+in_level)

            else:
                print("属性:"+out_fun+" "+out_arg+"  "+input_fun+" "+input_arg+" 验证结束!")
                """successful"""
                continue

    #
    # if index==len(relation):
    #     suc_output()


if __name__ == "__main__":
    # re_file=sys.argv[1]
    # fun_list=[]
    # for i in range(2,len(sys.argv)):
    #     fun_list.append(sys.argv[i])
    # fun_list=['RC_Channel_set_radio_in','RC_Channel_get_radio_in','RC_Channel_pwm_to_range_dz']
    fun_list=[ 'RC_Channel_set_radio_in', 'RC_Channel_get_radio_in', 'RC_Channel_pwm_to_range_dz']
    com_verification(fun_list)
    # file_name = "/home/rraa/pycparser/examples/com_verification/zheshu2.xml"
    # R = getXmlData(file_name)
    # for x in R:
    #     print(x)
    #     pass
