import os


def del_const(path_c):
    path_c_list = os.listdir(path_c)
    for file in path_c_list:
        if os.path.splitext(file)[1]==".c" or os.path.splitext(file)[1]==".h":
            name=os.path.basename(file)
            path1=path_c+"/"+name
            with open(path1, "r") as f:
                lines = f.readlines()
                f.close()
            with open(path1, "w") as f:
                for line in lines:
                    if "const" in line:
                        line = line.replace("const", "")
                    f.write(line)
                f.close()


if __name__ == '__main__':
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()
    name1='../../Project/'+pro_name+'/meta_data/Source_copy'
    name2='../../Project/'+pro_name+'/pilot_src/Source'
    del_const(name1)
    del_const(name2)