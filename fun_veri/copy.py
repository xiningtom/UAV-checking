import os
import re
import sys


def zhushi(path1,path2):
    rec = r"\s*\w*\s*\w*\s*[*]?\s*\w*\s*\("

    path_list1 = os.listdir(path1)
    for file in path_list1:


        if os.path.splitext(file)[1] == ".c" :
            file1 = open(path1 + "/" + file, "r", encoding='utf-8')
            file2 = open(path2 + "/" + file, 'w', encoding='utf-8')

            try:
                for line in file1.readlines():

                    file2.write(line)

            finally:
                file1.close()
                file2.close()
        elif os.path.splitext(file)[1] == ".h":
            file1 = open(path1 + "/" + file, "r", encoding='utf-8')
            file2 = open(path2 + "/" + file, 'w', encoding='utf-8')

            try:
                flag=False
                for line in file1.readlines():

                    if flag==True:
                        if ")" in line:
                            line = line.replace(line, "//" + line)
                            file2.write(line)
                            flag=False
                            continue
                        else:
                            line = line.replace(line, "//" + line)
                            file2.write(line)
                            flag=True
                            continue

                    if re.match(rec, line):
                        if ")" in line:
                            line = line.replace(line, "//" + line)
                            file2.write(line)
                        else:
                            line=line.replace(line, "//" + line)
                            file2.write(line)
                            flag=True
                    else:
                        file2.write(line)

            finally:
                file1.close()
                file2.close()




if __name__ == '__main__':
    path1="/home/rraa/pycparser/examples/RC_Channel"
    path2="/home/rraa/Desktop/rc"
    # zhushi(path1,path2)
    zhushi(sys.argv[1],sys.argv[2])



