from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import parse_file, c_parser, c_generator, c_ast

def get_decl():
    """get a decl node ast
    """
    s=r'''
void a(){
    float ret;
    int *a;
}
'''
    parser = c_parser.CParser()
    a_ast = parser.parse(s)
    a_decl=a_ast.ext[0].body.block_items
    return a_decl

def get_assign():
    """ get a assignment node ast
    """
    s = r'''
  void f(int a,int b){
   a=b;
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_assign = s_ast.ext[0].body.block_items[0]
    return s_assign

def get_return():
    s=r'''
  int f(int a){
return a;
}
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_return=s_ast.ext[0].body.block_items[0]
    return s_return

def get_goto():
    """ get a assignment node ast
    """
    s=r'''
  void f(){
   goto Second;
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_goto=s_ast.ext[0].body.block_items[0]
    return s_goto

def add_label(ast):
    label = get_label()
    ast.body.block_items.append(label)

def get_compound():
    """ get a compound and a assign statement
    """
    s=r'''
  void f(int a,int b){
   a=b;
   goto Second;

    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    #This is a compound body
    s_compound=s_ast.ext[0].body
    return s_compound

def get_label():
    """ get a assignment node ast
    """
    s=r'''
  void f(){
       Second:
        printf("\n");
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_label=s_ast.ext[0].body.block_items[0]
    return s_label



def find_return(st):
    """find all return statement and modify it and insert new statement
    """
#can't give a ast
    for child in st:
        if (st==None):
            break
        else:
            if (type(child)==c_ast.Return):
                if (type(st)==c_ast.Compound):
                    print(st)
                    #delete return statement
                    index=st.block_items.index(child)
                    assign=get_assign()
                    assign.lvalue.name='ret_self_com'
                    assign.rvalue=child.expr
                    goto = get_goto()
                    st.block_items.remove(child)

                    #insert assign statement
                    st.block_items.append(assign)
                    st.block_items.append(goto)
                else:
                    if type(st)==c_ast.Case or type(st)==c_ast.Default:
                        compound=get_compound()
                        assign = compound.block_items[0]
                        assign.lvalue.name = 'ret_self_com'
                        assign.rvalue = child.expr

                        print(st)
                        st.stmts[0] = compound
                        continue
                    compound=get_compound()
                    assign=compound.block_items[0]
                    assign.lvalue.name='ret_self_com'
                    assign.rvalue=child.expr

                    print(st)
                    st.iftrue=compound


                    #insert goto statement
                break
            print(type(child))
            find_return(child)

def deal_last_return(ast):
    st=ast.body.block_items
    for child in st:
        if (type(child)==c_ast.Return):
            assign=get_assign()
            assign.lvalue.name='ret_self_com'
            assign.rvalue=child.expr
            goto = get_goto()
            st.remove(child)
            ast.body.block_items.append(assign)
            ast.body.block_items.append(goto)
            break
        else:
            find_return(child)


def find_void_return(st):
    for child in st:
        if (st == None):
            break
        else:
            if (type(child) == c_ast.Return):
                if (type(st) == c_ast.Compound):
                    goto = get_goto()
                    st.block_items.remove(child)

                    st.block_items.append(goto)
                else:
                    if type(st) == c_ast.Case or type(st) == c_ast.Default:
                        goto=get_goto()

                        print(st)
                        st.stmts[0] = goto
                        continue
                    goto=get_goto()
                    st.iftrue = goto

                    # insert goto statement
                break
            print(type(child))
            find_void_return(child)


def deal_void_last_return(ast):
    st = ast.body.block_items
    for child in st:
        if (type(child) == c_ast.Return):
            goto = get_goto()
            st.remove(child)
            ast.body.block_items.append(goto)
            break
        else:
            find_void_return(child)


def deal_void_return(ast):
    deal_void_last_return(ast)
    add_label(ast)

def deal_return(rast):

    deal_last_return(rast)
    add_label(rast)
    s_return = get_return()
    s_return.expr.name = "ret_self_com"
    rast.body.block_items.append(s_return)

def deal_return1(rast):
    deal_last_return(rast)
    add_label(rast)
    s_return = get_return()
    s_return.expr.name = "ret_self_com"
    rast.body.block_items.append(s_return)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    #_zz_test_translate()
    #"""
    if len(sys.argv) > 1:
        filename=sys.argv[1]
        ast = parse_file(filename, use_cpp=True)
        deal_return(ast)
    else:
        funname="Copter_should_disarm_on_failsafe"
        #funname="millis"
        filename='/home/rraa/Desktop/Arducopter/tee'
        ast = parse_file(filename, use_cpp=True)
        ast1 = parse_file(filename, use_cpp=True)
        for i in range(0,len(ast.ext)):
            if(type(ast.ext[i])==c_ast.FuncDef and ast.ext[i].decl.name== funname):
                r_ast=ast.ext[i]
                m_ast=ast1.ext[i]
                deal_return(r_ast,m_ast)
                generator = c_generator.CGenerator()
                print(generator.visit(r_ast))
        # print("Please provide a filename as argument")
    #"""

