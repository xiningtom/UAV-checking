import os
import sys

def pro_process():
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()
    """read object dictory,extract filename"""
    filename_c_list=[]
    filename_list=[]
    path = '../../Project/'+pro_name+'/meta_data/Source_copy'
    path_list = os.listdir(path)
    for file in path_list:
        if os.path.splitext(file)[1]==".c" or os.path.splitext(file)[1]==".h":
            name=os.path.basename(file)
            path1=path+"/"+name
            with open(path1, "r") as f:
                lines = f.readlines()
                f.close()
            with open(path1, "w") as f:
                for line in lines:
                    if "const" in line:
                        line = line.replace("const", "")
                    f.write(line)
                f.close()
    for file in path_list:
        if os.path.splitext(file)[1] == '.c':
            print(os.path.basename(file))
            name_c=os.path.basename((file))
            name=name_c[:-2]
            print(name_c+"  "+name)
            filename_c_list.append(name_c)
            filename_list.append(name)

    print(line)

    dirs1 = '../../Project/'+pro_name+'/meta_data/temp'
    dirs=os.path.abspath(dirs1)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    for file in filename_c_list:
        name_c=file
        index=filename_c_list.index(name_c)
        name=filename_list[index]
        dir=dirs+"/"+name
        os.system(
            "gcc -E %s/%s -I ../../utils/fake_libc_include >>%s" % (path,name_c,dir))

if __name__ == "__main__":
    #_zz_test_translate()
    #"""
    print("开始预处理")
    pro_process()
    print("预处理结束")
    #"""
