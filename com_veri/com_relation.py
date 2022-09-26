import os
import sys
from xml.dom.minidom import Document, parse
project = "pycparser"
sys.path.append(os.getcwd().split(project)[0] + project)

from src.com_veri.com_verification import com_verification




def main():
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()
    out_list=[]
    in_list=[]
    for i in range(1,len(sys.argv)):
        if i%2 == 1:
            outarg=sys.argv[i]
            out_list.append(outarg)
        else:
            inarg=sys.argv[i]
            in_list.append(inarg)
    doc=Document()
    com_relation=doc.createElement("com_relation")
    doc.appendChild(com_relation)
    nodes={0:com_relation}
    index=-1
    for i in out_list:
        index=index+1
        outarg=i
        out_split=outarg.split(".")
        relation=doc.createElement("ralation")
        relation.setAttribute("out_fun",out_split[0])
        relation.setAttribute("output_arg",out_split[1])
        # print(out_split)
        inarg=in_list[index]
        in_split=inarg.split(".")
        relation.setAttribute("input_fun",in_split[0])
        relation.setAttribute("input_arg",in_split[1])
        nodes[0].appendChild(relation)
    filename='../../Project/'+pro_name+'/meta_data/com_veri/com.xml'
    with open(filename, 'w') as f:

        f.write(doc.toprettyxml(indent=' '))

        f.close()

    dom=parse('../../Project/'+pro_name+'/meta_data/com_veri/temp.xml')
    root=dom.documentElement
    func=root.getElementsByTagName('func_list')
    fun_list=func[0].getElementsByTagName("func")
    function=[]
    for f in fun_list:
        function.append(f.getAttribute("name"))
    # print(function)
    com_verification(function)



    #     print(index)
    # print(out_list)
    # print(in_list)






if __name__ == "__main__":
    main()
    # if len(sys.argv) > 1:
    #     print('参数个数为:', len(sys.argv), '个参数。')
    #     print('参数列表:', str(sys.argv))
    #     print('脚本名为：', sys.argv[0])
    #     for i in range(1, len(sys.argv)):
    #         print('参数 %s 为：%s' % (i, sys.argv[i]))
