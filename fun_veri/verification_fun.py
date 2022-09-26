import datetime
import os
import subprocess
import sys
import threading
from xml.dom.minidom import parse


# project = "pycparser"
# sys.path.append(os.getcwd().split(project)[0] + project)

from pycparser import parse_file, c_ast

def read_6line(file):
    with open(file) as f:
        txt = f.readlines()
    keys = [k for k in range(0, len(txt))]
    result = {k: v for k, v in zip(keys, txt[::-1])}
    list = []
    for i in range(6):
        temp = result[i].replace("\n", " ")
        list.append(temp)

    list.reverse()
    for i in range(4):
        print(list[i])

def read_3line(file):
    with open(file) as f:
        txt = f.readlines()
    keys = [k for k in range(0, len(txt))]
    result = {k: v for k, v in zip(keys, txt[::-1])}
    list = []
    for i in range(3):
        temp = result[i].replace("\n", " ")
        list.append(temp)

    list.reverse()
    for i in range(3):
        print(list[i])

def test_thread(command,i):
    (status, output) = subprocess.getstatusoutput(command)

    # print("================")
    # print(status)
    path =r"../../result/"+ i + ".txt"
    path1=os.path.abspath(path)
    # print(path1)
    if status != 0:
        mon=open(path,"w")
        mon.write(output)
        if status==10:
            print("function:"+i+"验证存在安全缺陷，具体为：\n")
            read_6line(path1)

            print("请到路径 "+path1+"下查看相应的反例和更多的信息.")
            #print(i + ":验证结束")
        else:
            print("function:" + i + "验证异常，具体为：\n")
            read_3line(path1)

            print("请到路径 " + path1 + "下查看异常信息.")

    else:
        print("function:"+i+"")
        #print("验证安全\n")
        print(i + ":验证结束")


def verification(fun_list):
    print(fun_list+":开始验证")
    c_filename = []
    function_name = fun_list
    fp = open("../../../path/project.txt")
    line = fp.readline().strip()
    path = r'../../Project/'+line+'/pilot_src/Source'
    path1=os.path.abspath(path)
    path_list = os.listdir(path1)

    for file in path_list:
        if os.path.splitext(file)[1] == '.c':
            name_c = os.path.basename((file))
            # print(name_c+"  "+name)
            c_filename.append(name_c)

    temp_command = 'cbmc '
    for i in c_filename:
        temp_command = temp_command + i + ' '
    temp_command = temp_command + "--32 --function "

    unwind = " --unwind 1 --no-unwinding-assertions"
    os.chdir(path)

    command = temp_command + function_name+ unwind
    print(command)
    temp_file = "temp.xml"


    t = threading.Thread(target=test_thread, args=(command,function_name,))
    t.start()
    t.join(int(sys.argv[3]))
    
    exit()
    # print("join")


def main():
    file=sys.argv[1]
    filename=file+".c"
    list=sys.argv[2]
    # for i in range(1, len(sys.argv)):
    #     list.append(sys.argv[i])
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()
    path1 = r'../../Project/'+pro_name+'/pilot_src/Source/'+filename
    with open(path1, "r") as f:
        lines = f.readlines()
        size = len(lines)
        i = 0
        for line in lines:
            i = i + 1

            if list in line:
                break

        if i >= size:
            print("相应的自合成函数不存在,请先自合成.")
            exit()
    verification(list)


if __name__ == "__main__":
    main()






