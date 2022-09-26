import os
import sys


def comp_c(path,str):

    with open(path, "r") as f:
        lines = f.readlines()
        f.close()
    with open(path, "w") as f:
        for line in lines:
            if str in line:
                line = line.replace(str, str(int(str)+2)
                print(line)
            f.write(line)
        f.close()



if __name__ == '__main__':
    path="/home/raoxue/Desktop/test_openssl/if_assume.c"

    for i in range(100):
        seed=3
        comp_c(path,str(seed))
        seed=seed+2
    # fp=open("result","w")
    # comp_c(path)
    # fp.close()