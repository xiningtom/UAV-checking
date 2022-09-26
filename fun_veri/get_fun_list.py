import os
import sys
# project = "pycparser"
# sys.path.append(os.getcwd().split(project)[0] + project)
from pycparser import parse_file, c_ast


def get_fun_list(filename,pro_name):
    path1 = r'../../Project/'+pro_name+'/meta_data/temp'
    basename = os.path.basename(filename)
    base_name = basename[0:-2]

    path_list1 = os.listdir(path1)

    for file in path_list1:
        file_name=os.path.basename(file)
        if file_name==base_name:
            filepath = path1 + '/' + file

            fun_list = []
            ast = parse_file(filepath)
            for i in range(0, len(ast.ext)):
                if (type(ast.ext[i]) == c_ast.FuncDef):
                    fun_list.append(ast.ext[i].decl.name)
            for f in fun_list:
                print(f)
            break


if __name__ == '__main__':
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()
    filename = '../../Project/'+pro_name+'/pilot_src/RC_Channel/' + sys.argv[1]+".c"
    get_fun_list(filename,pro_name)