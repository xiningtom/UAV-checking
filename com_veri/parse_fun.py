import os
import sys
from xml.dom.minidom import Document, parse

project = "pycparser"
sys.path.append(os.getcwd().split(project)[0] + project)
from pycparser import parse_file, c_ast

def parse_fun(function):
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()
    path = r'../../Project/'+pro_name+'/meta_data/file.xml'
    path1=os.path.abspath(path)
    if not os.path.exists(path1):
        print(path1+" is a intermediate file for \"generate XML file\" ,Please operate \'generate XML file\' first.")
    doc = parse(path1)
    root = doc.documentElement

    fun = root.getElementsByTagName('function')

    input_fun={}
    out_fun={}

    for f in function:
        in_param_list = []
        out_parm_list = []
        for ff in fun:
            if ff.getAttribute("name")==f:
                if ff.hasAttribute("Returntype"):
                    ree=ff.getElementsByTagName("return_value")
                    #print(ree)
                    for i in ree:
                        ret=i.getAttribute("type")
                        #print(ret)
                        if i.hasAttribute("ptr"):
                            ret1 = "out0 (* " + ret + ")"
                        else:
                            ret1 = "out0 " + "(" + ret + ")"
                            #print(ret1)
                    
                        out_parm_list.append(ret1)

                param=ff.getElementsByTagName("params")
                i=0
                j=0
                for p in param:
                    i=i+1
                    Type=p.getAttribute("type")
                    if p.hasAttribute("ptr"):
                        ty = "* " + Type
                        j = j + 1
                        in_param_list.append("in" + str(i) + " (" + ty + ")")
                        out_parm_list.append("out" + str(j) + " (" + ty + ")")

                    else:
                        in_param_list.append("in" + str(i) + " (" + Type + ")")

                input_fun[f] = in_param_list
                out_fun[f] = out_parm_list
                break
    #print(input_fun)
    #print(out_fun)


    """generate xml file"""
    doc=Document()
    root=doc.createElement("root")
    doc.appendChild(root)
    nodes={0:root}

    fun_list=doc.createElement("func_list")
    fun_list.setAttribute("len",str(len(function)))
    nodes[0].appendChild(fun_list)
    nodes[1]=fun_list
    for i in function:
        func=doc.createElement("func")
        func.setAttribute("name",i)
        nodes[1].appendChild(func)

    for i in function:
        out_in=doc.createElement("out_in")
        out_in.setAttribute("name",i)
        nodes[0].appendChild(out_in)
        nodes[1]=out_in
        Out=doc.createElement("Out")
        out_list=out_fun[i]
        Out.setAttribute("len",str(len(out_list)))
        nodes[1].appendChild(Out)
        nodes[2]=Out
        for o in out_list:
            out=doc.createElement("out")
            out.setAttribute("name",o)
            nodes[2].appendChild(out)
        Input= doc.createElement("Input")
        in_list=input_fun[i]
        Input.setAttribute("len",str(len(in_list)))
        nodes[1].appendChild(Input)
        nodes[2]=Input
        for p in in_list:
            input=doc.createElement("input")
            input.setAttribute("name",p)
            nodes[2].appendChild(input)

    temp_file=r'../../Project/'+pro_name+'/meta_data/com_veri/temp.xml'
    with open(temp_file,"w") as f:
        f.write(doc.toprettyxml(indent=' '))

        f.close()


if __name__ == '__main__':
    fun_list=[]
    for i in range(1,len(sys.argv)):
        fun_list.append(sys.argv[i])
    parse_fun(fun_list)
