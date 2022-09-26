import os
import re
import sys

def zhushi(path_1,path_2,file):
    rec = r"\s*\w*\s*\w*\s*[*]?\s*\w*\s*\("
    file1 = open(path_1 + "/" + file, "r", encoding='utf-8')
    file2 = open(path_2 + "/" + file, "w", encoding='utf-8')

    try:
        flag = False
        for line in file1.readlines():

            if flag == True:
                if ")" in line:
                    line = line.replace(line, "//" + line)
                    file2.write(line)
                    flag = False
                    continue
                else:
                    line = line.replace(line, "//" + line)
                    file2.write(line)
                    flag = True
                    continue

            if re.match(rec, line):
                if ")" in line:
                    line = line.replace(line, "//" + line)
                    file2.write(line)
                else:
                    line = line.replace(line, "//" + line)
                    file2.write(line)
                    flag = True
            else:
                file2.write(line)

    finally:
        file1.close()
        file2.close()
def copy(path1,path2):


    path_list1 = os.listdir(path1)
    for file in path_list1:
        name = os.path.basename(file)
        # print(name)
        if os.path.isdir(path1 + "/" + name):
            abp1 = path1 + "/" + name
            abp2 = path2 +"/"+name

            if name == "Inc":
                os.mkdir(abp2)
                pathlist2 = os.listdir(abp1)
                for f in pathlist2:
                    na=os.path.basename(f)
                    abp_1 = abp1 + "/" + na
                    abp_2 = abp2 + "/" + na
                    if os.path.isdir(abp1 + "/" + na):

                        os.system("cp -r %s %s" %(abp_1,abp_2))
                    else:
                        zhushi(abp1,abp2,na)




            else:
                os.system("cp -r %s %s" %(abp1,abp2))
        else:
            file1=path1 + "/"+ file
            file2 = path2 + "/" + file
            os.system("cp -r %s %s" %(file1,file2))













if __name__ == '__main__':
    path1="/home/raoxue/Downloads/jimi"
    path2="/home/raoxue/Desktop/jimi"
    # zhushi(path1,path2)
    copy(sys.argv[1],sys.argv[2])
    #copy(path1,path2)



