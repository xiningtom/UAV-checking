import sys
import xml.dom.minidom as xmldom
import os




def writeStruct(type,dom,structDic,strList,root):
    element = dom.createElement('decl')
    element.setAttribute('name', type)
    element.setAttribute('type', 'Struct')
    for i in range(len(structDic[type])):
        element.appendChild(structDic[type][i])
        types = structDic[type][i].getAttribute('type')
        if types in structDic.keys() and types not in strList:
            strList.append(types)
            writeStruct(types,dom,structDic,strList,root)
    root.appendChild(element)


def writeEnum(type,dom,enumDic,enumList,root):
    element = dom.createElement('decl')
    element.setAttribute('name', type)
    element.setAttribute('type', 'Enum')
    element.setAttribute("level",'H')
    root.appendChild(element)




#函数
#构造函数
def writeFunc(name,paramElem,dom,structDic,retElem,root,enumDic):
    if name in paramElem.keys():
        element = dom.createElement('function')
        element.setAttribute('name', name)
        element_in = dom.createElement('input')
        element_out = dom.createElement('output')
        num_out = 0
        ret_flag = False
        ##输入:element_in
        for i in range(len(paramElem[name])):
            num_in = str(i+1)
            str_in = "in" + num_in
            elem = dom.createElement(str_in)
            type = paramElem[name][i].getAttribute('type')
            if type in structDic.keys() or type in enumDic.keys():
                elem.setAttribute('ref', type)
            else:
                level = paramElem[name][i].getAttribute('level')
                elem.setAttribute('level', level)
            element_in.appendChild(elem)
            #添加返回值（如果有的话）
            if name in retElem.keys() and ret_flag == False:
                ret_flag = True
                str_out = "out"+str(0)
                elem_out = dom.createElement(str_out)
                if retElem[name][0].getAttribute('ptr') == '*':
                    elem_out.setAttribute('ref', retElem[name][0].getAttribute('type'))
                elif retElem[name][0].getAttribute('type') in enumDic.keys() : 
                    elem_out.setAttribute('ref', retElem[name][0].getAttribute('type'))
                    elem_out.setAttribute('type', 'ret_var')
                else:
                    elem_out.setAttribute('level', retElem[name][0].getAttribute('level'))
                    elem_out.setAttribute('type', 'ret_var')
                element_out.appendChild(elem_out)
            str_out = "out"
            if paramElem[name][i].getAttribute('ptr') == "*":
                num_out =num_out + 1
                str_out += str(num_out)
                elem_out = dom.createElement(str_out)
                if type in structDic.keys():
                    elem_out.setAttribute('ref', type)
                else:
                    level = paramElem[name][i].getAttribute('level')
                    elem_out.setAttribute('level', level)
                element_out.appendChild(elem_out)
        #输出:element_out
        element.appendChild(element_in)
        element.appendChild(element_out)
        root.appendChild(element)





def autoGenerator(funcName,paramElem,structDic,dom,strList,root,retElem,enumDic,enumList):
    for item in paramElem[funcName]:
        name = item.getAttribute('type')
        if name in structDic.keys():
            writeStruct(name,dom,structDic,strList,root)
        elif name in enumDic.keys():
            writeEnum(name,dom,enumDic,enumList,root)
    if funcName in  retElem.keys():
        for item in retElem[funcName]:
            name = item.getAttribute('type')
            if name in enumDic.keys():
                writeEnum(name,dom,enumDic,enumList,root)

    writeFunc(funcName,paramElem,dom,structDic,retElem,root,enumDic)



def main():
    
    fp = open("../../../path/project.txt")
    pro_name = fp.readline().strip()
    pro_name_path = '../../Project/'+pro_name+'/meta_data/'
    xml_filepath = os.path.abspath(pro_name_path+"file.xml")
    # 文件对象
    dom_obj = xmldom.parse(xml_filepath)

    # 得到元素对象
    elem_obj = dom_obj.documentElement
    # sub_elem_obj Nodelist 对象（有 getElementsByTagName方法得到NodeList对象）
    struct_sub_elem_obj = elem_obj.getElementsByTagName("decl")
    func_sub_elem_obj = elem_obj.getElementsByTagName("function")
    # 存储所有结构体类型的列表
    strctList = []
    enumList = []
    for var in struct_sub_elem_obj:
        type = var.getAttribute('type')
        if type == 'Struct':
            strctList.append(var)
        if type == 'Enum':
            enumList.append(var)

    # 存储所有（结构体，所含所有变量Nodelist） 字典
    structDic = {}
    for item in strctList:
        names = item.getAttribute('name')
        if names not in structDic.keys():
            structDic[names] = item.getElementsByTagName('variable')

    #存储所有枚举
    enumDic = {}
    for item in enumList:
        name = item.getAttribute('name')
        if names not in enumDic.keys():
            enumDic[name] = item.getElementsByTagName('variable')

    # 函数名列表
    funcNames = []
    for var in func_sub_elem_obj:
        if var not in funcNames:
            funcNames.append(var)

    # 函数名-参数字典
    paramElem = {}
    # 函数名-返回值字典
    retElem = {}
    for item in funcNames:
        name = item.getAttribute('name')
        ret = item.getElementsByTagName('return_value')
        if name not in paramElem.keys():
            paramElem[name] = item.getElementsByTagName('params')
        if name not in retElem.keys() and len(ret) > 0:
            retElem[name] = ret

    dom = xmldom.getDOMImplementation().createDocument(None, 'root', None)
    root = dom.documentElement

    writenList = []

    # 输出所有函数中的结构体
    strList = []
    funcName = sys.argv[1]
    autoGenerator(funcName,paramElem,structDic,dom,strList,root,retElem,enumDic,enumList)
    filename='../../Project/'+pro_name+'/meta_data/com_veri/sec_cert/'+funcName+'.xml'
    #filename_new = funcName+'.xml'
    filename1=os.path.abspath(filename)
    # print(filename1)
    with open(filename1, 'w', encoding='utf-8') as f:
        dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')
    pass

if __name__ == '__main__':
    main()
    print("generate successful")
