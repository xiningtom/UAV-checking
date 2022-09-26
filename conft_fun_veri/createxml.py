from __future__ import print_function

import os
import sys

import pycparser

project = "pycparser"
sys.path.append(os.getcwd().split(project)[0] + project)
sys.path.extend(['.', '..'])
from pycparser import parse_file, c_parser, c_generator, c_ast
from xml.dom.minidom import Document
from xml.dom.minidom import parse

global_decl=[] #avoid avariable rename
globalv_list = [] #list of global avariable
global_dic = {} #function and global avariable mapping

#each varible have be processed, incleding typedef,decl and function name

"""Add all global variable in global"""

def find_ID(st,l):
    for i in st:
        if (i==None):
            break
        #elif type(i)==c_ast.ID and type(st)!=c_ast.StructRef:
        elif type(i) == c_ast.ID:
            idname=i.name
            if type(st)==c_ast.StructRef:
                if st.field.name==idname:
                    continue
                else:
                    if i.name in globalv_list and i.name not in l:
                        l.append(i.name)


            if i.name in globalv_list and i.name not in l:
                l.append(i.name)
            #globalfv_list.append(i.name)
            find_ID(i,l)
        else:
            find_ID(i,l)
Type_List=['size_t','__int8_t','__uint8_t','__int16_t','__uint16_t','__int32_t','__uint32_t',
               '__int64_t','__uint64_t','int','float','double','bool','int16_t','uint16_t','uint32_t',
               'uint8_t','int8_t','Enum','uint64_t','char','int64_t','int32_t']

def deal_global_variable(ast):
    """ Simply use the c_generator module to emit a parsed AST.
    """
    """record all global variable in ast"""
    for func in ast.ext:
        if type(func) == c_ast.Decl and type(func.type) != c_ast.FuncDecl and func.name not in globalv_list:
            globalv_list.append(func.name)
    """record each function's global variable"""
    for fun in ast.ext:
        if type(fun) == c_ast.FuncDef:
            l = []
            fun111 = fun.body.block_items
            if fun111 is None:
                continue
            find_ID(fun111, l)
            global_dic[fun.decl.name] = l

def deal_decls(decls,nodes,generator):
    for j in decls:
        if type(j.type) == c_ast.TypeDecl:
            node1 = doc.createElement("variable")
            node1.setAttribute("name", str(j.name))
            if j.quals == ['const']:
                node1.setAttribute("quals", "const")
            if type(j.type.type) == c_ast.Struct or type(j.type.type)==c_ast.Union:
                # print(generator.visit(i))
                # print("continue+1111111111")
                # print(i)
                continue
            else:
                if type(j.type.type) == c_ast.Enum:
                    node1.setAttribute("type", j.type.type.name)
                    node1.setAttribute("Enum", "y")
                    e = j.type.type.name


                    node1.setAttribute("level", "L")
                    nodes[1].appendChild(node1)
                    # print(generator.visit(i))
                    # print("continue+2222222222")
                    # print(i)
                    continue
                te = str(j.type.type.names)
                e = te[2:-2]
                node1.setAttribute("type", e)
                if e in Type_List:
                    node1.setAttribute("level", "L")
                else:
                    node1.setAttribute("ref", e)
                nodes[1].appendChild(node1)
        elif type(j.type) == c_ast.PtrDecl and type(j.type.type) == c_ast.FuncDecl:
            continue
        elif type(j.type) == c_ast.PtrDecl and type(j.type.type) == c_ast.TypeDecl:
            node1 = doc.createElement("variable")
            node1.setAttribute("name", str(j.name))
            if j.quals == ['const']:
                node1.setAttribute("quals", "const")
            if type(j.type.type.type) == c_ast.Struct:
                e = j.type.type.type.name

                node1.setAttribute("type", e)
                node1.setAttribute("ptr", '*')
                if e in Type_List:
                    node1.setAttribute("level", "L")
                else:
                    node1.setAttribute("ref", e)
                nodes[1].appendChild(node1)
                # print(generator.visit(i))
                # print("continue+3333333333")
                # print(i)
                continue
            else:
                te = str(j.type.type.type.names)
                e = te[2:-2]
                node1.setAttribute("type", e)
                node1.setAttribute("ptr", '*')
                if e in Type_List:
                    node1.setAttribute("level", "L")
                else:
                    node1.setAttribute("ref", e)
                nodes[1].appendChild(node1)

        elif type(j.type) == c_ast.ArrayDecl:
            if type(j.type.type.type) == c_ast.Struct:
                # print(generator.visit(i))
                # print("continue+4444444444")
                # print(i)
                continue
            if type(j.type.type) == c_ast.ArrayDecl:
                # print(generator.visit(i))
                # print("continue+1313131313")
                # print(i)
                continue
            if type(j.type.type.type)==c_ast.Enum:
                continue
            if type(j.type.type) == c_ast.PtrDecl:
                node1 = doc.createElement("variable")
                node1.setAttribute("name", str(j.name))
                if j.quals == ['const']:
                    node1.setAttribute("quals", "const")
                if type(j.type.type.type.type) == c_ast.Struct:
                    e = str(j.type.type.type.type.name)
                else:
                    te = str(j.type.type.type.type.names)
                    e = te[2:-2]
                node1.setAttribute("ptr", "*")
                node1.setAttribute("type", e)
                node1.setAttribute("arr", j.type.dim.value)
                if e in Type_List:
                    node1.setAttribute("level", "L")
                else:
                    node1.setAttribute("ref", e)
                nodes[1].appendChild(node1)
                continue

            node1 = doc.createElement("variable")
            node1.setAttribute("name", str(j.name))
            if j.quals == ['const']:
                node1.setAttribute("quals", "const")
            te = str(j.type.type.type.names)
            e = te[2:-2]
            node1.setAttribute("type", e)
            if type(j.type.dim)==c_ast.ID:
                node1.setAttribute("arr", j.type.dim.name)
            elif type(j.type.dim)==c_ast.BinaryOp:
                value = generator.visit(j.type.dim)
                node1.setAttribute("arr", value)
            else:
                node1.setAttribute("arr", j.type.dim.value)
            if e in Type_List:
                node1.setAttribute("level", "L")
            else:
                node1.setAttribute("ref", e)
            nodes[1].appendChild(node1)

def createxml(ast,doc,root,flag,filename):
    structs = root.getElementsByTagName('decl')
    function = root.getElementsByTagName('function')
    processed_name=[]
    # if flag=="one":
    #     structs = root.getElementsByTagName('decl')
    #     function = root.getElementsByTagName('function')
    # else:
    #     structs=root[0].getElementsByTagName('decl')
    #     function=root[0].getElementsByTagName('function')
    for s in structs:
        name=s.getAttribute("name")
        processed_name.append(name)
    for f in function:
        name =f.getAttribute("name")
        processed_name.append(name)
    nodes = {0: root}
    # if flag=="one":
    #     nodes = {0:root}
    # else:
    #     nodes = {0: root[0]}


    for i in ast.ext:
        generator=c_generator.CGenerator()
        if type(i)==c_ast.Typedef or type(i)==c_ast.Decl:
            if type(i)==c_ast.Typedef and type(i.type)==c_ast.TypeDecl and type(i.type.type)==c_ast.Struct and \
                    hasattr(i.type.type,"decls") and i.type.type.decls is None:
                # print("don't copy+99889988")
                # print(generator.visit(i))
                continue
            print(generator.visit(i))
            print("every time")
            print(i)
            if type(i)==c_ast.Typedef and type(i.type)==c_ast.TypeDecl and type(i.type.type)==c_ast.IdentifierType:
                continue
            if type(i.type)==c_ast.Union:
                continue

            node = doc.createElement("decl")

            #need deal with
            if type(i.type)==c_ast.Enum:
                if i.type.name in processed_name:
                    continue
                if i.type.name in global_decl:
                    continue
                else:
                    global_decl.append(i.type.name)
                node.setAttribute("name",i.type.name)
                node.setAttribute("type",'Enum')
                nodes[0].appendChild(node)
                nodes[1] = node
                continue
            elif type(i.type)==c_ast.Struct:
                if i.type.name in processed_name:
                    continue
                if i.type.name in global_decl:
                    continue
                else :
                    global_decl.append(i.type.name)
                node.setAttribute("name", i.type.name)
                node.setAttribute("type", 'Struct')
                nodes[0].appendChild(node)
                nodes[1] = node
                if hasattr(i.type,"decls"):
                    decls = i.type.decls
                    if decls is not None:
                        deal_decls(decls,nodes,generator)
            elif type(i.type.type)==c_ast.Enum:
                if i.name in processed_name:
                    continue
                if i.name in global_decl:
                    continue
                else:
                    global_decl.append(i.name)
                node.setAttribute("name",i.name)
                node.setAttribute("type",'Enum')
                nodes[0].appendChild(node)
                nodes[1] = node
                continue

            else:
                if i.name in processed_name:
                    continue
                if i.name in global_decl:
                    continue
                else:
                    global_decl.append(i.name)

                node.setAttribute("name", i.name)

            if type(i.type)==c_ast.TypeDecl:
                if type(i.type.type)==c_ast.IdentifierType:
                    te = str(i.type.type.names)
                    e = te[2:-2]
                    node.setAttribute("type",e)
                elif type(i.type.type) == c_ast.Union:
                    node = doc.createElement("decl")
                    node.setAttribute("name",i.name)
                    node.setAttribute("type", "Union")
                    continue
                else:

                    te=str(type(i.type.type))
                    e=te[24:-2]
                    if e=='Enum':
                        node.setAttribute("type",i.type.type.name)
                    else:
                        node.setAttribute("type", e)
                nodes[0].appendChild(node)
                nodes[1]=node
                if hasattr(i.type.type,"decls"):
                    decls=i.type.type.decls
                    if decls is not None:
                        deal_decls(decls,nodes,generator)

                    else:
                        print(generator.visit(i))
                        print("continue+555555555555")
                        print(i)
                        continue
                else:
                    temp = node.getAttribute("type")
                    if temp in ["Struct","Enum"]:
                        no=doc.createElement("variable")
                        if i.type.type.values is None:
                            no.setAttribute("name",i.name)
                            no.setAttribute("type",temp)
                            no.setAttribute("Enum",'yes')
                            no.setAttribute("level","L")
                            continue

                            if temp in Type_List:
                                no.setAttribute("level", 'L')
                            else:
                                no.setAttribute("ref",temp)
                            nodes[1].appendChild(no)
                            continue

                        no.setAttribute("name",i.type.type.values.enumerators[0].name)
                        Type=i.type.type.values.enumerators[0].value.type
                        no.setAttribute("type",Type)
                        no.setAttribute("Enum",'yes')
                        if Type in Type_List:
                            node.setAttribute("level",'L')
                        else:
                            node.setAttribute("ref",Type)
                        nodes[1].appendChild(no)
                        continue
                    nodd=doc.createElement("variable")
                    nodd.setAttribute("name",i.name)

                    nodd.setAttribute("type",temp)
                    if temp in Type_List:
                        nodd.setAttribute("level","L")
                    else:
                        nodd.setAttribute("ref",temp)
                    nodes[1].appendChild(nodd)
                continue
            elif type(i.type)==c_ast.Enum:
                no=doc.createElement("variable")
                no.setAttribute("name", i.type.values.enumerators[0].name)

                no.setAttribute("Enum", 'yes')

                no.setAttribute("level", 'L')

                nodes[1].appendChild(no)
                continue
            elif type(i.type)==c_ast.PtrDecl or type(i.type)==c_ast.ArrayDecl:
                if type(i.type)==c_ast.PtrDecl:
                    if type(i.type.type)==c_ast.FuncDecl:
                        continue
                    if type(i.type.type.type)==c_ast.IdentifierType:
                        if str(i.type.type.type.names)[2:-2] == 'void':
                            continue
                        else:
                            nodd=doc.createElement("decl")
                            nodd.setAttribute("name",i.name)
                            nodd.setAttribute("type",str(i.type.type.type.names)[2:-2])
                            nodes[0].appendChild(nodd)
                            nodes[1]=nodd
                            no=doc.createElement("variable")
                            no.setAttribute("name",i.name)
                            no.setAttribute("type",str(i.type.type.type.names)[2:-2])
                            no.setAttribute("ptr","*")
                            temp=str(i.type.type.type.names)[2:-2]
                            if temp in Type_List:
                                no.setAttribute("level","L")
                            else:
                                no.setAttribute("ref",temp)
                            nodes[1].appendChild(no)
                            continue
                if type(i.type.type)==c_ast.PtrDecl:
                    node.setAttribute("type",str(i.type.type.type.type.names)[2:-2])

                elif type(i.type.type.type)==c_ast.Struct:
                    if type(i.type)==c_ast.PtrDecl:
                        node2=doc.createElement("decl")
                        node2.setAttribute("name",i.name)
                        node2.setAttribute("type",i.type.type.type.name)

                        nodes[0].appendChild(node2)
                        nodes[1] = node2
                        no = doc.createElement("variable")
                        no.setAttribute("name", i.name)
                        no.setAttribute("type", i.type.type.type.name)
                        no.setAttribute("ptr",'*')
                        # no.setAttribute("arr",i.type.dim.value)
                        temp = i.type.type.type.name
                        if temp in Type_List:

                            no.setAttribute("level", "L")
                        else:
                            no.setAttribute("ref", temp)
                        nodes[1].appendChild(no)
                        continue
                    t=i.type.type.type
                    node2=doc.createElement("decl")
                    node2.setAttribute("name",t.name)
                    node2.setAttribute("type","Struct")
                    nodes[0].appendChild(node2)
                    nodes[1]=node2
                    for j in t.decls:
                        no=doc.createElement("variable")
                        no.setAttribute("name",j.name)
                        no.setAttribute("type",str(j.type.type.names)[2:-2])
                        temp=str(j.type.type.names)[2:-2]
                        if temp in Type_List:
                            no.setAttribute("level","L")
                        else:
                            no.setAttribute("ref",temp)
                        nodes[1].appendChild(no)

                    node.setAttribute("type",t.name)
                    nodes[0].appendChild(node)
                    nodes[1]=node
                    node1 = doc.createElement("variable")
                    node1.setAttribute("name", i.name)

                    node1.setAttribute("type", t.name)
                    node1.setAttribute("ref",t.name)
                    node1.setAttribute("arr",i.type.dim.value)
                    nodes[1].appendChild(node1)
                    continue
                else:
                    print(i)
                    print(type(i.type))
                    print(type(i.type.type))
                    te = str(i.type.type.type.names)
                    e = te[2:-2]
                    node.setAttribute("type",e)
                    nodes[0].appendChild(node)
                    nodes[1] = node
                    nod=doc.createElement("variable")
                    nod.setAttribute("name",i.name)
                    nod.setAttribute("type",e)
                    if e in Type_List:
                        nod.setAttribute("level", "L")
                    else:
                        nod.setAttribute("ref", e)
                    if type(i.type)==c_ast.ArrayDecl:
                        if type(i.type.dim)==c_ast.BinaryOp:
                            value=generator.visit(i.type.dim)
                            nod.setAttribute("arr",value)
                        elif type(i.type.dim)==c_ast.ID:
                            nod.setAttribute("arr",i.type.dim.name)
                        elif i.type.dim is None:
                            pass
                        else:
                            print(type(i.type.dim))
                            nod.setAttribute("arr",i.type.dim.value)
                    nodes[1].appendChild(nod)
                    continue

                nodes[0].appendChild(node)
                nodes[1]=node
                temp=node.getAttribute("type")
                node1=doc.createElement("variable")
                node1.setAttribute("name",i.name)
                if type(i.type.type) == c_ast.PtrDecl:
                    node1.setAttribute("ptr",'*')
                    node1.setAttribute("arr",i.type.dim.value)
                node1.setAttribute("ptr",'*')

                node1.setAttribute("type",temp)
                if e in Type_List:
                    node1.setAttribute("level","L")
                else:
                    node1.setAttribute("ref",temp)
                nodes[1].appendChild(node1)
                continue
            else:
                print(generator.visit(i))
                print("continue+666666666")
                print(i)
                continue

        elif type(i) == c_ast.FuncDef:
            if i.decl.name in processed_name:
                continue
            if i.decl.name in global_decl:
                continue
            else:
                global_decl.append(i.decl.name)
            if i.body.block_items is None:
                continue
            node=doc.createElement("function")
            node.setAttribute("name",i.decl.name)
            if type(i.decl.type.type) ==c_ast.PtrDecl:
                print(generator.visit(i))
                print("continue+77777777777777")
                print(i)
                if type(i.decl.type.type.type.type)==c_ast.Struct:
                    e=str(i.decl.type.type.type.type.name)
                else:
                    te=str(i.decl.type.type.type.type.names)
                    e = te[2:-2]
                node.setAttribute("Returntype",e)
                node.setAttribute("ptr","*")
            elif type(i.decl.type.type.type)==c_ast.Enum:
                te=i.decl.type.type.type.name
                node.setAttribute("Returntype",te)
                node.setAttribute("Enum","y")
                print(generator.visit(i))
                print("continue+888888888888")
                print(i)

            else:
                te = str(i.decl.type.type.type.names)
                e = te[2:-2]
                node.setAttribute("Returntype",e)

            nodes[0].appendChild(node)
            nodes[1]=node

            """define function's global variable"""
            fun_global=global_dic[i.decl.name]
            for a in fun_global:
                no=doc.createElement("global")
                no.setAttribute("name",a)
                nodes[1].appendChild(no)
            returntype=node.getAttribute("Returntype")
            if returntype!='void':
                n1=doc.createElement("return_value")
                n1.setAttribute("name",'ret_self_com')
                if node.hasAttribute("ptr"):
                    n1.setAttribute("ptr","*")
                if node.hasAttribute("Enum"):
                    n1.setAttribute("Enum","y")
                n1.setAttribute("type",returntype)
                if returntype in Type_List:
                    n1.setAttribute("level",'L')
                elif node.hasAttribute("Enum"):
                    n1.setAttribute("level","L")
                else:
                    n1.setAttribute("ref",returntype)
                nodes[1].appendChild(n1)
            if i.decl.type.args is None:

                continue
            decls=i.decl.type.args.params
            if decls is not None:
                for j in decls:

                    if type(j)!=c_ast.Decl:
                        print(generator.visit(i))
                        print("continue+101010101010")
                        print(i)
                        continue
                    node1=doc.createElement("params")
                    node1.setAttribute("name",j.name)
                    if j.quals == ['const']:
                        node1.setAttribute("quals", "const")
                    if type(j.type)==c_ast.TypeDecl:

                        if type(j.type.type)==c_ast.Struct or type(j.type.type)==c_ast.Enum:
                            #node1.setAttribute("quals",j.type.quals)
                            node1.setAttribute("type",str(j.type.type.name))
                            if type(j.type.type)==c_ast.Enum:
                                node1.setAttribute("Enum","y")
                                node1.setAttribute("level","L")
                                nodes[1].appendChild(node1)
                                continue
                        else:

                            node1.setAttribute("type", str(j.type.type.names)[2:-2])
                    elif type(j.type)== c_ast.PtrDecl:
                        node1.setAttribute("ptr", "*")
                        if type(j.type.type.type)==c_ast.Struct:
                            node1.setAttribute("type", str(j.type.type.type.name))

                        else:
                            if type(j.type.type)==c_ast.PtrDecl:
                                print("two level poiter+=========")
                                continue
                            node1.setAttribute("type", str(j.type.type.type.names)[2:-2])
                    else:
                        print(generator.visit(i))
                        print("continue+9999999999")
                        print(i)
                    temp = node1.getAttribute("type")
                    if temp in Type_List:
                        node1.setAttribute("level","L")
                    else:
                        node1.setAttribute("ref",temp)
                    nodes[1].appendChild(node1)

            continue
        else:
            print(generator.visit(i))
            # print("continue+121212121212")
            print(i)
            continue


    with open(filename, 'w') as f:
        f.write(doc.toprettyxml(indent=' '))
        # if flag=="one":
        #     f.write(doc.toprettyxml(indent=' '))
        # else:
        #     doc.writexml(f,addindent=' ')
        f.close()



#------------------------------------------------------------------------------
if __name__ == "__main__":
    #_zz_test_translate()
    #"""
    if len(sys.argv) > 1:
        filename=sys.argv[1]
        ast = parse_file(filename, use_cpp=True)
        deal_global_variable(ast)
        createxml(ast)
    else:
        fp = open("../../../path/project.txt")
        line = fp.readline().strip()
        print("开始生成安全策略文件")
        path_ree = r'../../Project/'+line+'/meta_data/temp'
        path=os.path.abspath(path_ree)
        path_list = os.listdir(path)
        f = './'+"temp.xml"
        for file in path_list:
            filename = path + '/' + file
            ast = parse_file(filename, use_cpp=True)
            deal_global_variable(ast)
            r=os.path.abspath(f)
            print(str(os.path.getsize(r))+"ffffffff")
            if os.path.getsize(r)>0:
                doc = parse(r)
                root = doc.documentElement
                # dom=Document()
                # dom.appendChild(root1)
                # root=dom.getElementsByTagName("root")
                flag="two"
                createxml(ast,doc,root,flag,r)
            else:
                flag="one"
                doc = Document()
                #create root node
                root = doc.createElement("root")
                doc.appendChild(root)
                createxml(ast,doc,root,flag,r)
        file='../../Project/'+line+'/meta_data/file.xml'
        file1 = open(r, "r", encoding='utf-8')
        file2 = open(file, 'w', encoding='utf-8')

        try:
            for line in file1.readlines():
                if line.split():
                    file2.write(line)
        finally:
            file1.close()
            file2.close()
        with open(r,"r+") as f:
            f.truncate()
        print("生成安全策略文件结束")
