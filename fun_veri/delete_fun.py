import re
import sys


def delete_fun(filename,funname):
    with open(filename,"r") as f:
        lines=f.readlines()
        brace=[]
        # print(lines)
        start_end_line = []
        index=-1
        flag=0
        for line in lines:
            index = index + 1
            if funname in line and "{" in line:
                start_end_line.append(index)
                # print("111"+str(index))

                brace.append("{")
                # print(brace)
                flag=1

                continue
            elif funname in line:
                start_end_line.append(index)
                # print("222"+str(index))
                flag=1

                continue

            if len(start_end_line) and index>start_end_line[0]:
                if "{" in line:
                    brace.append("{")
                    # print(brace,index)




                if  '}' in line:
                    brace.pop()
                    if len(brace):

                        continue
                    else:
                        start_end_line.append(index)
                        break
        if flag:
            # print(start_end_line)
            time=start_end_line[1]-start_end_line[0]+1
            for i in range(0,time):
                lines.pop(start_end_line[0])
                # print(i)


        # for line in lines:
        #     index=lines.index(line)
        #     if index>start_end_line[0] and index<start_end_line[1]:
        #         lines.pop(index)
        f.close()
    with open(filename,"w") as f:
        for line in lines:
            f.write(line)


    #
    #         with open(filename,"w") as f1:
    #             for num, line in enumerate(f):
    #                 if num>=start_end_line[0] and num<=start_end_line[1]:
    #                     line =line.replace(line,"")
    #                     f1.write(line)
    #             f1.close()
    #
    # f.close()

if __name__ == "__main__":
    filename="./RC_Channel/AC_Fence.c"
    funname="AC_Fence_manual_recovery_start_self_com"
    delete_fun(filename,funname)
