import os
import sys
from xml.dom.minidom import parse
project = "pycparser"
sys.path.append(os.getcwd().split(project)[0] + project)
from src.fun_veri.c_to_c4 import self_com
from src.fun_veri.verification_fun import verification



from pycparser import parse_file, c_ast



def fun_sel_com(filename,ffunname,line):
    xmlfile = r'../../Project/'+line+'/meta_data/file.xml'
    xmlfile1=os.path.abspath(xmlfile)
    if not os.path.isfile(xmlfile1):
        print("文件 "+xmlfile1+" 不存在, 请先生成xml文件并进行安全级配置.")
        exit()
    path1 = r'../../Project/'+line+'/meta_data/temp'
    basename = os.path.basename(filename)
    base_name=basename[0:-2]

    path_list1 = os.listdir(path1)
    doc = parse(xmlfile)
    root = doc.documentElement
    structs = root.getElementsByTagName('decl')
    function = root.getElementsByTagName('function')



    for file in path_list1:
        file_name=os.path.basename(file)
        if file_name==base_name:
            filepath = path1 + '/' + file
            objectname = os.path.basename(filepath)
            ast = parse_file(filepath)
            ast1=parse_file(filepath)
            # fun_list=[]
            # for i in range(0, len(ast.ext)):
            #     if (type(ast.ext[i]) == c_ast.FuncDef):
            #         fun_list.append(ast.ext[i].decl.name)
            #
            # for i in fun_list:
            #     print(i)
            # print("\n")
            # print("please choose a function\n")



            funname=ffunname

            for f in function:
                fun = f.getAttribute("name")
                if fun == funname:
                    func = f
                    break
            content = []

            fun_self = funname + "_self_com"

            print(funname+": 开始自合成")
            self_com(ast, ast1, func, structs, objectname, content)
            print(funname+": 自合成结束")



                





if __name__ == "__main__":
    """input the base path of c file and function's name"""
    fp = open("../../../path/project.txt")
    line = fp.readline().strip()
    filename='../../Project/'+line+'/pilot_src/RC_Channel/'+sys.argv[1]+".c"
    fun_list=sys.argv[2]
    # for i in range(2,len(sys.argv)):
    #     fun_list.append(sys.argv[i])

    fun_sel_com(filename,fun_list,line)
