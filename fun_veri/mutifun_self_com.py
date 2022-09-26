from __future__ import print_function
import os
import sys
# project = "pycparser"
# sys.path.append(os.getcwd().split(project)[0] + project)
from src.fun_veri.c_to_c4 import translate_to_cc


def main_entry(file_list):
    fp = open("../../../path/project.txt")
    line = fp.readline().strip()
    path=r'../../Project/'+line+'/meta_data/temp'
    xmlfile = r'../../Project/'+line+'/meta_data/file.xml'

    basename=file_list[:-2]
    content=[]
    path1=os.path.abspath(path)
    filepath=path1+"/"+basename
    # print(filepath+" 4444")

    translate_to_cc(filepath,xmlfile,content)



if __name__ == "__main__":
    file_list=sys.argv[1]
    # for i in range(1,len(sys.argv)):
    #     file_list.append(sys.argv[i])
    print(file_list+": 开始自合成")
    main_entry(file_list)
    print(file_list + ":自合成结束")

