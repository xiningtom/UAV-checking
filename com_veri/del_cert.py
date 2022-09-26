import os
import sys

if __name__ == '__main__':
    funname=sys.argv[1]
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()
    dir='../../Project/'+pro_name+'/meta_data/com_veri/sec_cert'

    path_list = os.listdir(dir)

    for file in path_list:

        name = os.path.basename((file))
        base_name=name[0:-4]
        # print(base_name)
        if base_name == funname:
            os.remove(dir+"/"+file)
            break
