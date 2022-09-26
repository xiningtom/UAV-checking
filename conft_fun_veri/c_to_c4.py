#------------------------------------------------------------------------------
# pycparser: c-to-c.py
#
# Example of using pycparser.c_generator, serving as a simplistic translator
# from C to AST and back to C.
#
# Eli Bendersky [https://eli.thegreenplace.net/]
# License: BSD
#------------------------------------------------------------------------------
from __future__ import print_function

import os
import sys
import re
import random

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
from src.fun_veri.deal_return import deal_return, deal_return1, deal_void_return
from src.fun_veri.delete_fun import delete_fun

sys.path.extend(['.', '..'])
from pycparser import parse_file, c_parser, c_generator,c_ast
from xml.dom.minidom import parse

def get_assume():
    s = r'''
  void fun(float x){
  __CPROVER_assume(!isnan(x)&&!isinf(x));
  }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct = s_ast.ext[0].body.block_items[0]
    return s_struct

def get_assume_arr():
    s="""
    int fun(double a[2]){
for (int i=0;i<2;i++){
 __CPROVER_assume(!isnan(a[i])&&!isinf(a[i]));
}
}
    """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct = s_ast.ext[0].body.block_items[0]
    return s_struct

def get_assign():
    """ get a assignment node ast
    """
    s=r'''
  void f(int a,int b){
   a=b;
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_assign=s_ast.ext[0].body.block_items[0]
    return s_assign

def get_array():
    """ get a assignment node ast
    """
    s = r'''
  void f(int a,int b){
   int arr[10]; 
   int *arr1[10]; 
   int arr2[10]; 
   for (int i=0;i<10;i++){
      arr[i]=arr1[i];
    }
    for (int i=0;i<10;i++){
      assert(arr[i]==arr1[i]);
    }
    for(int i=0;i<2;i++){
      arr[i]=*arr1[i];
    }
    for(int i=0;i<2;i++){
      arr1[i]=&arr[i];
    }
    int *b[3];
    for(int i=0;i<2;i++){
      assert(*arr1[i]==*b[i]);
    }
    for(int i=0;i<3;i++){
     arr1[i]=(int*)malloc(sizeof(int));
    }
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_assign = s_ast.ext[0].body.block_items
    return s_assign
def get_strutref_arr():
    s = r'''
  typedef struct Node{
int a[2];
} Node;
void node_init(Node node, Node nnode1)
{   
    node1.a[i]=node.a[i];
 }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    body=s_ast.ext[1].body.block_items[0]
    return body

def get_basic_pointer_array():
    s="""
    void fun(){
	int a[2]={2,3};
	int *aa[2]={&a[0],&a[1]};
	int *a__1[2];
	int b[2];
	for (int i=0;i<2;i++){
		a__1[i]=&b[i];
}
	for (int i=0;i<2;i++){
		b[i]=*aa[i];
}
	for (int i=0;i<2;i++){
		assert(*aa[i]==*a__1[i]);

}
}
    """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct = s_ast.ext[0].body.block_items
    return s_struct

def get_compound_array():
    s = """
        typedef struct B{
        int c;
        int d;
    }B;
    void init(){
    B a[3]; 
    B b[3]; 
    a[0].c=b[0].c; 
    }
        """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct = s_ast.ext[1].body.block_items
    return s_struct

def get_ptr_struct_assign1():
    s = r'''
        typedef struct B{
    	int b1;
    	int *b2;
    }B;

    typedef struct A {
     int a;
     int *b;
     B e;
     B *f;
    }A;

    void fun(A basica){
        A basica__1;

        basica__1.e.b1=basica.e.b1;
    	assert(basica__1.e.b1==basica.e.b1);

    	B f1;
    	basica__1.f=&f1;
    	f1.b1=*(basica.f).b1;
    	assert(*(basica.f).b1==*(basica__1.f).b1);

    }

        '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    body = s_ast.ext[2].body.block_items

    # s_struct = s_ast.ext[1].body.block_items[1]
    return body

def get_ptr_struct_assign2():
    s = r'''
            typedef struct B{
        	int b1;
        	int *b2;
        }B;

        typedef struct A {
         int a;
         int *b;
         B e;
         B *f;
        }A;


        void fun1(A *ptra){
          A *ptra__1;
        	A ptrcopy;
        	ptra__1=&ptrcopy;

        	ptrcopy.e.b1=ptra->e.b1;
        	assert(ptra__1->e.b1==ptra->e.b1);


        	B f1;
        	ptrcopy.f=&f1;
        	*(f1.b1)=*(*(ptra->f)->b1);
        	assert(*(*(ptra->f)->b1)==*(*(ptra__1->f)->b1));
        }
            '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    body = s_ast.ext[2].body.block_items
    # s_struct = s_ast.ext[1].body.block_items[1]
    return body


def get_struct_assign():
    s=r'''
  typedef struct Node{
char key;
int level;
} Node;
  void node_init(Node* node, Node* n)
{
    node->key = n->key;
    node->level = 0;
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct=s_ast.ext[1].body.block_items[0]
    return s_struct

def get_structref_assign():
    s = r'''
  typedef struct Node{
char *key;
int level;
} Node;
  void node_init(Node node, Node *n)
{   
    Node node1;
    char a;
    a=*(node.key);
    node1.key=&a;
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    body=s_ast.ext[1].body.block_items
    return body

def get_struct_onestar_decl():
    s=r'''
  typedef struct Node{
char key;
int level;
} Node;
  void node_init(Node* node)
{
    Node* d; 
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct=s_ast.ext[1].body.block_items[0]
    return s_struct

def get_onestar_malloc():
    s=r'''
  typedef struct Node{
char key;
int level;
} Node;
  void node_init(Node* node)
{
    
    Node* d;
    d=(Node*)malloc(sizeof(Node));
    
    }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)

    s_struct=s_ast.ext[1].body.block_items[1]
    return s_struct

def get_assert():
    """get a assert node ast
    """
    s=r'''
void a(int a, int b){
    assert(a==b);
}
'''
    parser = c_parser.CParser()
    a_ast = parser.parse(s)

    #This is a assert node
    a_assert=a_ast.ext[0].body.block_items[0]
    return a_assert

def get_decl():
    """get a decl node ast
    """
    s=r'''
void a(){
    float ret;
    int *aa;
}
'''
    parser = c_parser.CParser()
    a_ast = parser.parse(s)
    a_decl=a_ast.ext[0].body.block_items
    return a_decl


def get_basic_pointer():
    s = r'''
  void fun(){
    char *a="nihao";
    char *b;
    char c;
    b=&c;
    c=*a;
    assert(*a==*b);

  }
  '''
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct = s_ast.ext[0].body.block_items

    return s_struct

def get_assume_poiter():
    s = r"""
    int fun(double *b){
__CPROVER_assume(!isnan(*b)&&!isinf(*b));
}
    """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    st = s_ast.ext[0].body.block_items[0]
    return st


def get_malloc_assign():
    """get a decl node ast
    """
    s=r'''
void a(){
    float ret;
    float *a;
    float *b;
    assert(*a==*b);
    a=&ret;
}
'''
    parser = c_parser.CParser()
    a_ast = parser.parse(s)
    a_decl=a_ast.ext[0].body.block_items
    return a_decl


def get_arr_recur():
    s = r"""
    typedef struct B{
    int b1;
    int *b2;
}B;
typedef struct A{
    int a;
    int *b;
    B e;
    B *f;
}A;
    void fun2(A array[],int n){
	A array__1[n];

	for (int i=0;i<n;i++){
		array_1[i].a=array[i].a;
	}
	for (int i=0;i<n;i++){
		assert(array_1[i].a==array[i].a);
	}
    array_1[0].a=array[0].a;
	for (int i=0;i<n;i++){
		array__1[i].e.b1=array[i].e.b1;
	}
}

    """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct = s_ast.ext[2].body.block_items
    return s_struct


def tese():
    s = r"""
    enum GPS_Status
{
    NO_GPS,                                     
    NO_FIX,                                      

};
enum GPS_Status status;

    """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    st = s_ast.ext[1]
    return st


def get_arr_related():
    s = """
    typedef struct B{
    int b1;
    int *b2;
}B;
typedef struct A{
    int a;
    int *b;
    int *d[2];
    B e;
    B *f;
    B bb[2];
}A;

void function(A basica){
  A basica__1;
    basica__1.bb[0].b=basica.bb[0].b;
    basica__1.bb[1].b=basica.bb[1].b;
    int d1[2];
	for (int i=0;i<2;i++){
		ptrcopy.d[i]=&d1[i];
	}
	for (int i=0;i<2;i++){
		d1[i]=*(ptra->d[i]);
	}
	for (int i=0;i<2;i++){
		assert(*(ptra->d[i])==*(ptra__1->d[i]));
	}	
	for (int i=0;i<2;i++){
		ptrcopy.c[i]=ptra->c[i];
	}
	for (int i=0;i<2;i++){
		assert(ptra->c[i]==ptra__1->c[i]);	
	}
}
    """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    s_struct = s_ast.ext[2].body.block_items
    return s_struct

def get_poiter_arr_assume():
    s = r"""
    int fun(double *b[]){
	for (int i=0;i<2;i++){
 __CPROVER_assume(!isnan(*b[i])&&!isinf(*b[i]));
}
}
    """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    st = s_ast.ext[0].body.block_items[0]
    return st

def get_assume_parr():
    s = r"""
    typedet struct A{
    int a;
    }
    int fun(){
A arr[2];
for (int i=0;i<2;i++){
__CPROVER_assume(!isnan(arr[i].a)&&!isinf(arr[i].a));
}
    """
    parser = c_parser.CParser()
    s_ast = parser.parse(s)
    st = s_ast.ext[0].body.block_items[1]
    return st


def merge_ast(rast,mast):
    """merge two ast and modify it
    """
    body= mast.body.block_items
    for i in body:
        rast.body.block_items.append(i)
    return rast

def recur(structs,rname,newname,nname,isptr,ty,rast,record,mast,funtype,depth):
    print("44444444444444444")
    for s in structs:
        if s.getAttribute("name") == ty:
            if s.getAttribute("type")=="Union":
                break
            var1 = s.getElementsByTagName("variable")
            if not var1:
                break
            else:
                for ii in var1:
                    if ii.hasAttribute("quals"):
                        continue
                    ran=random.randint(1,1000)
                    if ii.hasAttribute("level"):
                        if isptr:
                            if ii.hasAttribute("ptr") and ii.hasAttribute("arr"):

                                subname = ii.getAttribute("name")
                                subnewname = subname + "_"+str(ran)
                                if type(rname) == c_ast.StructRef or type(rname)==c_ast.ArrayRef:

                                    name ="self_"
                                    subnewname = name + "_" + subnewname
                                else:
                                    subnewname = rname + "_" + subnewname
                                Type = ii.getAttribute("type")
                                ty1 = re.findall('(.*[a-zA-Z0-9_])', Type)
                                arr_size=ii.getAttribute("arr")

                                if Type == "float" or Type == "double":
                                    ass = get_struct_assign().lvalue
                                    if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                        ass.name = rname
                                    else:
                                        ass.name.name = rname
                                    ass.field.name = subname
                                    ass.type = "->"
                                    assume = get_poiter_arr_assume()
                                    assume.cond.right.value = str(arr_size)
                                    if type(ass)==c_ast.StructRef or type(ass)==c_ast.ArrayRef:
                                        assume.stmt.block_items[0].args.exprs[0].left.expr.args.exprs[
                                            0].expr.name = ass
                                        assume.stmt.block_items[0].args.exprs[0].right.expr.args.exprs[
                                            0].expr.name = ass

                                    else:
                                        assume.stmt.block_items[0].args.exprs[0].left.expr.args.exprs[0].expr.name.name = ass
                                        assume.stmt.block_items[0].args.exprs[0].right.expr.args.exprs[0].expr.name.name =ass
                                    rast.body.block_items.insert(record, assume)
                                if Type == "float" or Type == "double":
                                    x = record + 1
                                else:
                                    x = record
                                arr=get_arr_related()
                                decl=arr[3]
                                decl.name=subnewname
                                decl.type.type.declname=subnewname
                                decl.type.type.type.names=ty1
                                decl.type.dim.value=str(arr_size)
                                rast.body.block_items.insert(x, decl)
                                x = x + 1
                                address_assign=arr[4]
                                address_assign.cond.right.value=str(arr_size)
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    address_assign.stmt.block_items[0].lvalue.name.name=newname
                                else:
                                    address_assign.stmt.block_items[0].lvalue.name.name.name=newname
                                address_assign.stmt.block_items[0].lvalue.name.field.name=subname
                                address_assign.stmt.block_items[0].lvalue.name.type = "->"
                                address_assign.stmt.block_items[0].rvalue.expr=name.name=subnewname
                                rast.body.block_items.insert(x, address_assign)
                                x = x + 1

                                arr1 = get_arr_related()
                                decl = arr1[3]
                                decl.name = subnewname+"2"
                                decl.type.type.declname = subnewname+"2"
                                decl.type.type.type.names = ty1
                                decl.type.dim.value = str(arr_size)
                                rast.body.block_items.insert(x, decl)
                                x = x + 1
                                address_assign = arr1[4]
                                address_assign.cond.right.value = str(arr_size)
                                if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                    address_assign.stmt.block_items[0].lvalue.name.name = rname
                                else:
                                    address_assign.stmt.block_items[0].lvalue.name.name.name = rname
                                address_assign.stmt.block_items[0].lvalue.name.field.name = subname
                                address_assign.stmt.block_items[0].lvalue.name.type = "->"
                                address_assign.stmt.block_items[0].rvalue.expr = name.name = subnewname+"2"
                                rast.body.block_items.insert(x, address_assign)
                                x = x + 1

                                if ii.getAttribute("level") == 'L':
                                    assign=arr[5]
                                    assign.cond.right.value=str(arr_size)
                                    assign.stmt.block_items[0].lvalue.name.name=subnewname
                                    if type(rname) == c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        assign.stmt.block_items[0].rvalue.expr.name.name=rname
                                    else:
                                        assign.stmt.block_items[0].rvalue.expr.name.name.name=rname
                                    assign.stmt.block_items[0].rvalue.expr.name.field.name=subname
                                    assign.stmt.block_items[0].rvalue.expr.name.type="->"
                                    rast.body.block_items.insert(x, assign)


                                    ass=arr[6]
                                    ass.cond.right.value = str(arr_size)
                                    if type(rname) == c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        ass.stmt.block_items[0].args.exprs[0].left.expr.name.name=rname
                                    else:
                                        ass.stmt.block_items[0].args.exprs[0].left.expr.name.name.name=rname
                                    ass.stmt.block_items[0].args.exprs[0].left.expr.name.field.name=subname
                                    ass.stmt.block_items[0].args.exprs[0].left.expr.name.type="->"
                                    if type(newname) == c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        ass.stmt.block_items[0].args.exprs[0].right.expr.name.name=newname
                                    else:
                                        ass.stmt.block_items[0].args.exprs[0].right.expr.name.name.name=newname
                                    ass.stmt.block_items[0].args.exprs[0].right.expr.name.field.name=subname
                                    ass.stmt.block_items[0].args.exprs[0].right.expr.name.type="->"

                                    if funtype != 'void':
                                        slen = len(mast.body.block_items)
                                        mast.body.block_items.insert(slen - 1, ass)
                                    else:
                                        mast.body.block_items.append(ass)

                            elif ii.hasAttribute("ptr"):
                                subname = ii.getAttribute("name")
                                subnewname=subname+"_"+str(ran)
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    name="self_"
                                    subnewname=name+"_"+subnewname
                                else:
                                    subnewname=rname+"_"+subnewname
                                Type=ii.getAttribute("type")
                                ty1=re.findall('(.*[a-zA-Z0-9_])', Type)


                                if Type == "float" or Type == "double":
                                    ass = get_struct_assign().lvalue
                                    if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                        ass.name = rname
                                    else:
                                        ass.name.name = rname
                                    ass.field.name = subname
                                    ass.type = "->"
                                    assume = get_assume_poiter()
                                    assume.args.exprs[0].left.expr.args.exprs[0].expr = ass
                                    assume.args.exprs[0].right.expr.args.exprs[0].expr = ass
                                    rast.body.block_items.insert(record, assume)
                                if Type == "float" or Type == "double":
                                    x = record + 1
                                else:
                                    x = record
                                decl1 = get_decl()    #float a;
                                decl=decl1[0]
                                decl.name = subnewname
                                decl.type.declname = subnewname
                                decl.type.type.names = ty1
                                rast.body.block_items.insert(x, decl)
                                x = x + 1

                                structref=get_ptr_struct_assign1()
                                address_assign=structref[4]
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    address_assign.lvalue.name=newname
                                else:
                                    address_assign.lvalue.name.name=newname
                                address_assign.lvalue.field.name=subname
                                address_assign.lvalue.type="->"
                                address_assign.rvalue.expr.name=subnewname
                                rast.body.block_items.insert(x,address_assign)
                                x=x+1

                                decl1 = get_decl()  # float a;
                                decl = decl1[0]
                                decl.name = subnewname+"2"
                                decl.type.declname = subnewname+"2"
                                decl.type.type.names = ty1
                                rast.body.block_items.insert(x, decl)
                                x = x + 1

                                structref = get_ptr_struct_assign1()
                                address_assign = structref[4]
                                if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                    address_assign.lvalue.name = rname
                                else:
                                    address_assign.lvalue.name.name = rname
                                address_assign.lvalue.field.name = subname
                                address_assign.lvalue.type = "->"
                                address_assign.rvalue.expr.name = subnewname+"2"
                                rast.body.block_items.insert(x, address_assign)
                                x = x + 1


                                if ii.getAttribute("level") == 'L':
                                    ss = get_structref_assign()
                                    struct_assign = ss[2]  #a=*(node.key);
                                    struct_assign.lvalue.name = subnewname
                                    if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        struct_assign.rvalue.expr.name = rname
                                    else:
                                        struct_assign.rvalue.expr.name.name = rname
                                    struct_assign.rvalue.expr.field.name = subname
                                    struct_assign.rvalue.expr.type = '->'
                                    rast.body.block_items.insert(x, struct_assign)

                                    #
                                    # INDEX += 1
                                    ss1 = ss[3]  # node1.key=&a;
                                    # ss1.lvalue.name.name = nname
                                    # ss1.lvalue.field.name = rawname
                                    # ss1.rvalue.type = '->'
                                    # ss1.rvalue.expr.name = newname1
                                    # rast.body.block_items.insert(x, ss1)
                                    ss1 = get_structref_assign()
                                    right = ss1[2].rvalue
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        right.expr.name = newname
                                    else:
                                        right.expr.name.name =newname
                                    right.expr.field.name = subname
                                    right.expr.type = '->'

                                    ass = get_assert()
                                    ass.args.exprs[0].left = struct_assign.rvalue
                                    ass.args.exprs[0].right = right
                                    if funtype != 'void':
                                        slen = len(mast.body.block_items)
                                        mast.body.block_items.insert(slen - 1, ass)
                                    else:
                                        mast.body.block_items.append(ass)
                            elif ii.hasAttribute("arr"):
                                arr_size=ii.getAttribute("arr")
                                subname=ii.getAttribute("name")
                                Type=ii.getAttribute("type")
                                if Type == "float" or Type == "double":
                                    ass = get_struct_assign().lvalue
                                    if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                        ass.name = rname
                                    else:
                                        ass.name.name = rname
                                    ass.field.name = subname
                                    ass.type = "->"
                                    assume = get_assume_arr()
                                    assume.cond.right.value = str(arr_size)
                                    if type(ass)==c_ast.StructRef or type(ass)==c_ast.ArrayRef:
                                        assume.stmt.block_items[0].args.exprs[0].left.expr.args.exprs[0].name= ass
                                        assume.stmt.block_items[0].args.exprs[0].right.expr.args.exprs[
                                            0].name= ass
                                    else:
                                        assume.stmt.block_items[0].args.exprs[0].left.expr.args.exprs[0].name.name = ass
                                        assume.stmt.block_items[0].args.exprs[0].right.expr.args.exprs[0].name.name= ass
                                    rast.body.block_items.insert(record, assume)
                                if Type == "float" or Type == "double":
                                    x = record + 1
                                else:
                                    x = record
                                if ii.getAttribute("level") == 'L':
                                    arr = get_arr_related()
                                    assign=arr[7]
                                    assign.cond.right.value=str(arr_size)
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        assign.stmt.block_items[0].lvalue.name.name=newname
                                    else:
                                        assign.stmt.block_items[0].lvalue.name.name.name=newname
                                    assign.stmt.block_items[0].lvalue.name.field.name=subname
                                    assign.stmt.block_items[0].lvalue.name.type = "->"
                                    if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        assign.stmt.block_items[0].rvalue.name.name=rname
                                    else:
                                        assign.stmt.block_items[0].rvalue.name.name.name=rname
                                    assign.stmt.block_items[0].rvalue.name.field.name=subname
                                    assign.stmt.block_items[0].rvalue.name.type = "->"
                                    rast.body.block_items.insert(x, assign)

                                    ass=arr[8]
                                    ass.cond.right.value = str(arr_size)
                                    if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        ass.stmt.block_items[0].args.exprs[0].left.name.name=rname
                                    else:
                                        ass.stmt.block_items[0].args.exprs[0].left.name.name.name=rname
                                    ass.stmt.block_items[0].args.exprs[0].left.name.field.name=subname
                                    ass.stmt.block_items[0].args.exprs[0].left.name.type = "->"
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        ass.stmt.block_items[0].args.exprs[0].right.name.name=newname
                                    else:
                                        ass.stmt.block_items[0].args.exprs[0].right.name.name.name=newname
                                    ass.stmt.block_items[0].args.exprs[0].right.name.field.name=subname
                                    ass.stmt.block_items[0].args.exprs[0].right.name.type = "->"
                                    if funtype != 'void':
                                        slen = len(mast.body.block_items)
                                        mast.body.block_items.insert(slen - 1, ass)
                                    else:
                                        mast.body.block_items.append(ass)

                                continue

                            else:  # no ptr
                                subname = ii.getAttribute("name")
                                Type=ii.getAttribute("type")
                                # subnewname = subname + "1"
                                if Type == "float" or Type == "double":
                                    ass=get_struct_assign().lvalue
                                    if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                        ass.name = rname
                                    else:
                                        ass.name.name = rname
                                    ass.field.name = subname
                                    ass.type = "->"
                                    assume = get_assume()
                                    if type(ass)==c_ast.ArrayRef or type(ass)==c_ast.StructRef:
                                        assume.args.exprs[0].left.expr.args.exprs[0]= ass
                                        assume.args.exprs[0].right.expr.args.exprs[0] = ass
                                    else:

                                        assume.args.exprs[0].left.expr.args.exprs[0].name =ass
                                        assume.args.exprs[0].right.expr.args.exprs[0].name = ass
                                    rast.body.block_items.insert(record, assume)
                                if Type == "float" or Type == "double":
                                    x = record + 1
                                else:
                                    x = record
                                if ii.getAttribute("level") == 'L':
                                    print("aaaaaaaa"+ii.getAttribute("level"))
                                    ass = get_struct_assign()
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        ass.lvalue.name = newname
                                    else:
                                        ass.lvalue.name.name = newname
                                    ass.lvalue.field.name = ii.getAttribute("name")
                                    ass.lvalue.type="->"
                                    if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        ass.rvalue.name = rname
                                    else:
                                        ass.rvalue.name.name = rname
                                    ass.rvalue.field.name = ii.getAttribute("name")
                                    ass.rvalue.type = '->'
                                    rast.body.block_items.insert(x, ass)

                                    lname=get_struct_assign()
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        lname.lvalue.name=newname
                                    else:
                                        lname.lvalue.name.name = newname
                                    lname.lvalue.field.name=ii.getAttribute("name")
                                    lname.lvalue.type="->"

                                    ass1 = get_assert()
                                    ass1.args.exprs[0].left = lname.lvalue
                                    ass1.args.exprs[0].right = ass.rvalue
                                    if funtype != 'void':
                                        slen = len(mast.body.block_items)
                                        mast.body.block_items.insert(slen - 1, ass1)
                                    else:
                                        mast.body.block_items.append(ass1)

                        else:  # isptr false
                            if ii.hasAttribute("ptr") and ii.hasAttribute("arr"):
                                # print("continue+recur+level+nisptr+ptr+arr")
                                continue
                            elif ii.hasAttribute("ptr"):
                                subname = ii.getAttribute("name")
                                subnewname=subname+"_"+str(ran)
                                if type(rname) == c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    name = "self_"
                                    subnewname = name + "_" + subnewname
                                else:
                                    subnewname = rname + "_" + subnewname
                                Type=ii.getAttribute("type")
                                ty1=re.findall('(.*[a-zA-Z0-9_])', Type)
                                if Type == "float" or Type == "double":
                                    ass = get_struct_assign().lvalue
                                    if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                        ass.name = rname
                                    else:
                                        ass.name.name = rname
                                    ass.field.name = subname
                                    ass.type = "."
                                    assume = get_assume_poiter()
                                    assume.args.exprs[0].left.expr.args.exprs[0].expr = ass
                                    assume.args.exprs[0].right.expr.args.exprs[0].expr = ass
                                    rast.body.block_items.insert(record, assume)
                                if Type == "float" or Type == "double":
                                    x = record + 1
                                else:
                                    x = record
                                decl1 = get_decl()
                                decl=decl1[0]
                                decl.name = subnewname
                                decl.type.declname = subnewname
                                decl.type.type.names = ty1
                                rast.body.block_items.insert(x, decl)
                                x = x + 1

                                structref = get_ptr_struct_assign1()
                                address_assign = structref[4]
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    address_assign.lvalue.name = newname
                                else:
                                    address_assign.lvalue.name.name = newname
                                address_assign.lvalue.field.name = subname
                                address_assign.lvalue.type="."
                                address_assign.rvalue.expr.name = subnewname
                                rast.body.block_items.insert(x, address_assign)
                                x = x + 1

                                decl1 = get_decl()
                                decl = decl1[0]
                                decl.name = subnewname+"2"
                                decl.type.declname = subnewname+"2"
                                decl.type.type.names = ty1
                                rast.body.block_items.insert(x, decl)
                                x = x + 1

                                structref = get_ptr_struct_assign1()
                                address_assign = structref[4]
                                if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                    address_assign.lvalue.name = rname
                                else:
                                    address_assign.lvalue.name.name = rname
                                address_assign.lvalue.field.name = subname
                                address_assign.lvalue.type = "."
                                address_assign.rvalue.expr.name = subnewname+"2"
                                rast.body.block_items.insert(x, address_assign)
                                x = x + 1

                                if ii.getAttribute("level") == 'L':
                                    ss = get_structref_assign()
                                    struct_assign = ss[2]
                                    struct_assign.lvalue.name = subnewname
                                    if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        struct_assign.rvalue.expr.name = rname
                                    else:
                                        struct_assign.rvalue.expr.name.name = rname
                                    struct_assign.rvalue.expr.field.name = subname
                                    struct_assign.rvalue.expr.type = '.'
                                    rast.body.block_items.insert(x, struct_assign)
                                    x = x + 1
                                    # ss1 = ss[3]
                                    # ss1.lvalue.name.name = nname
                                    # ss1.lvalue.field.name = rawname
                                    # ss1.lvalue.type = '.'
                                    # ss1.rvalue.expr.name = newname1
                                    # rast.body.block_items.insert(x, ss1)
                                    # x = record + 1

                                    ss1 = get_structref_assign()
                                    right = ss1[2].rvalue
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:

                                        right.expr.name = newname
                                    else:
                                        right.expr.name.name = newname
                                    right.expr.field.name = subname
                                    right.expr.type = '.'

                                    ass = get_assert()
                                    ass.args.exprs[0].left = struct_assign.rvalue
                                    ass.args.exprs[0].right = right
                                    if funtype != 'void':
                                        slen = len(mast.body.block_items)
                                        mast.body.block_items.insert(slen - 1, ass)
                                    else:
                                        mast.body.block_items.append(ass)
                            elif ii.hasAttribute("arr"):
                                # print("continue+recur+level+nisptr+arr")
                                continue

                            else:  # no ptr
                                subname=ii.getAttribute("name")
                                Type=ii.getAttribute("type")
                                if Type == "float" or Type == "double":
                                    ass=get_struct_assign().lvalue
                                    if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                        ass.name = rname
                                    else:
                                        ass.name.name = rname
                                    ass.field.name = subname
                                    ass.type = "."
                                    assume = get_assume()
                                    if type(ass)==c_ast.ArrayRef or type(ass)==c_ast.StructRef:
                                        assume.args.exprs[0].left.expr.args.exprs[0]= ass
                                        assume.args.exprs[0].right.expr.args.exprs[0] = ass
                                    else:
                                        assume.args.exprs[0].left.expr.args.exprs[0].name =ass
                                        assume.args.exprs[0].right.expr.args.exprs[0].name = ass
                                    rast.body.block_items.insert(record, assume)
                                if Type == "float" or Type == "double":
                                    x = record + 1
                                else:
                                    x = record
                                if ii.getAttribute("level") == 'L':
                                    ass = get_struct_assign()
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        ass.lvalue.name = newname
                                    else:
                                        ass.lvalue.name.name = newname
                                    ass.lvalue.field.name = ii.getAttribute("name")
                                    ass.lvalue.type = '.'
                                    if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        ass.rvalue.name = rname
                                    else:
                                        ass.rvalue.name.name= rname
                                    ass.rvalue.field.name = ii.getAttribute("name")
                                    ass.rvalue.type = '.'
                                    rast.body.block_items.insert(x, ass)
                                    ass1 = get_assert()
                                    ass1.args.exprs[0].left = ass.lvalue
                                    ass1.args.exprs[0].right = ass.rvalue
                                    if funtype != 'void':
                                        slen = len(mast.body.block_items)
                                        mast.body.block_items.insert(slen - 1, ass1)
                                    else:
                                        mast.body.block_items.append(ass1)

                    else:  # ref
                        rdepth=depth+1

                        if len(sys.argv) > 3:
                            if int(sys.argv[3]) == rdepth:
                                continue
                        elif rdepth == 3:
                            continue
                        if ii.getAttribute("ref")=="void":
                            # print("continue+recur+ref+void")
                            continue
                        if isptr:
                            if ii.hasAttribute("ptr") and ii.hasAttribute("arr"):
                                # print("continue+recur+ref+isptr+ptr+arr")
                                continue
                            elif ii.hasAttribute("ptr"):
                                n_isptr = True
                                """create object ref point to"""
                                subname = ii.getAttribute("name")  # nest object's name
                                subnewname = subname + "_"+str(ran)
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    name="self_"
                                    subnewname=name+"_"+subnewname
                                else:
                                    subnewname=rname+"_"+subnewname
                                Type = ii.getAttribute("type")
                                ty1 = re.findall('(.*[a-zA-Z0-9_])', Type)
                                #ty = ii.getAttribute("type")  # nest objec's type

                                structref = get_ptr_struct_assign2()
                                decl = structref[5] #B b;
                                decl.name = subnewname
                                decl.type.declname = subnewname
                                decl.type.type.names = ty1
                                rast.body.block_items.insert(record, decl)
                                x = record + 1
                                """ A a1;
                                    B b;
                                    b.c=(*(a.b)).c;
                                    a1.b=&b;
                                """

                                address_assign=structref[6]
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    address_assign.lvalue.name=newname
                                else:
                                    address_assign.lvalue.name.name = newname
                                address_assign.lvalue.type="->"

                                address_assign.lvalue.field.name=subname
                                address_assign.rvalue.expr.name=subnewname
                                rast.body.block_items.insert(x,address_assign)
                                x=x+1

                                structref = get_ptr_struct_assign2()
                                decl = structref[5]  # B b;
                                decl.name = subnewname+"2"
                                decl.type.declname = subnewname+"2"
                                decl.type.type.names = ty1
                                rast.body.block_items.insert(x, decl)
                                x = x + 1
                                address_assign = structref[6]
                                if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                    address_assign.lvalue.name = rname
                                else:
                                    address_assign.lvalue.name.name = rname
                                address_assign.lvalue.type = "->"
                                address_assign.lvalue.field.name = subname
                                address_assign.rvalue.expr.name = subnewname+"2"
                                rast.body.block_items.insert(x, address_assign)
                                x = x + 1

                                ass1 = structref[7] #b.c=(*(a.b)).c;

                                temprname = ass1.lvalue.expr
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    temprname.name = rname #*(a.b)
                                else:
                                    temprname.name.name = rname  # *(a.b)
                                temprname.field.name = subname
                                temprname.type = "->"
                                #a1
                                #a1.b

                                temnewname=ass1.rvalue.expr.expr.name
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    temnewname.name=newname
                                else:
                                    temnewname.name.name = newname
                                temnewname.field.name=subname
                                temnewname.type="->"


                                recur(structs, temprname, temnewname,subnewname, n_isptr, Type, rast, x, mast, funtype,rdepth)
                            elif ii.hasAttribute("arr"):
                                isptr1=False
                                subname = ii.getAttribute("name")  # nest object's name
                                Type = ii.getAttribute("type")
                                ty1 = re.findall('(.*[a-zA-Z0-9_])', Type)
                                arr_size=ii.getAttribute("arr")
                                arr=get_arr_related()
                                temprname=arr[1].lvalue.name.name
                                tempnewname=arr[1].rvalue.name.name
                                if type(rname) == c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    temprname.name = rname
                                else:
                                    temprname.name.name = rname
                                temprname.type="->"
                                temprname.field.name = subname

                                if type(newname) == c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    tempnewname.name=newname
                                else:
                                    tempnewname.name.name=newname
                                tempnewname.type="->"
                                tempnewname.field.name=subname


                                tempnewname1=arr[2].lvalue.name.name
                                if type(nname) == c_ast.StructRef or type(nname)==c_ast.ArrayRef:
                                    tempnewname1.name=nname
                                else:
                                    tempnewname1.name.name=nname
                                tempnewname1.field.name=subname

                                arr_recur(structs,temprname,tempnewname,tempnewname1,arr_size,isptr1,Type,rast,record,mast,funtype,rdepth)
                                continue
                            else:  # no ptr
                                if ii.hasAttribute("Enum"):
                                    ass = get_struct_assign()
                                    if type(newname) == c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        ass.lvalue.name = newname
                                    else:
                                        ass.lvalue.name.name = newname
                                    ass.lvalue.field.name = ii.getAttribute("name")
                                    ass.lvalue.type = "->"
                                    if type(rname) == c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        ass.rvalue.name = rname
                                    else:
                                        ass.rvalue.name.name = rname
                                    ass.rvalue.field.name = ii.getAttribute("name")
                                    ass.rvalue.type = '->'
                                    rast.body.block_items.insert(record, ass)

                                    lname = get_struct_assign()
                                    if type(newname) == c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        lname.lvalue.name = newname
                                    else:
                                        lname.lvalue.name.name = newname
                                    lname.lvalue.field.name = ii.getAttribute("name")
                                    lname.lvalue.type = "->"

                                    ass1 = get_assert()
                                    ass1.args.exprs[0].left = lname.lvalue
                                    ass1.args.exprs[0].right = ass.rvalue
                                    if funtype != 'void':
                                        slen = len(mast.body.block_items)
                                        mast.body.block_items.insert(slen - 1, ass1)
                                    else:
                                        mast.body.block_items.append(ass1)
                                    continue
                                n_isptr = False
                                """create object ref point to"""
                                subname = ii.getAttribute("name")  # nest object's name
                                subnewname = subname + "_"+str(ran)
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    name="self_"
                                    subnewname=name+"_"+subnewname
                                else:
                                    subnewname=rname+"_"+subnewname
                                Type = ii.getAttribute("type")
                                ty1 = re.findall('(.*[a-zA-Z0-9_])', Type)
                                #ty = ii.getAttribute("type")  # nest objec's type

                                structref = get_ptr_struct_assign2()
                                # decl = structref[1]
                                # decl.name = subnewname
                                # decl.type.declname = subnewname
                                # decl.type.type.names = ty
                                # rast.body.block_items.insert(record, decl)
                                # x = record + 1

                                ass1 = structref[3]
                                temprname = ass1.lvalue.name
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    temprname.name = rname
                                else:
                                    temprname.name.name = rname
                                temprname.field.name = subname
                                temprname.type = "->"

                                tempnewname=ass1.rvalue.name
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    tempnewname.name =newname
                                else:
                                    tempnewname.name.name = newname
                                tempnewname.field.name=subname
                                tempnewname.type="->"

                                ass2 = structref[4]
                                temname = ass2.args.exprs[0].left.name
                                if type(nname)==c_ast.StructRef or type(nname)==c_ast.ArrayRef:
                                    temname.name = nname
                                else:
                                    temname.name.name = nname

                                temname.field.name = subname
                                temname.type="."


                                recur(structs, temprname, tempnewname,temname,n_isptr, Type, rast, record, mast, funtype,rdepth)

                        else:  # isptr is false
                            if ii.hasAttribute("ptr") and ii.hasAttribute("arr"):
                                # print("continue+recur+ref+nisptr+ptr+arr")
                                continue
                            elif ii.hasAttribute("ptr"):
                                #ptra, ptra__1, ptrcopy
                                n_isptr = True
                                """create object ref point to"""
                                subname = ii.getAttribute("name")  # nest object's name
                                subnewname = subname + "_"+str(ran)
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    name="self_"
                                    subnewname=name+"_"+subnewname
                                else:
                                    subnewname=rname+"_"+subnewname
                                Type = ii.getAttribute("type")
                                ty1 = re.findall('(.*[a-zA-Z0-9_])', Type)  # nest objec's type

                                structref = get_ptr_struct_assign1()
                                decl = structref[3]
                                decl.name = subnewname
                                decl.type.declname = subnewname
                                decl.type.type.names = ty1
                                rast.body.block_items.insert(record, decl)
                                x = record + 1

                                address_assign=structref[4]
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    address_assign.lvalue.name=newname
                                else:
                                    address_assign.lvalue.name.name = newname
                                address_assign.lvalue.field.name=subname
                                address_assign.rvalue.expr.name=subnewname
                                rast.body.block_items.insert(x,address_assign)
                                x=x+1
                                structref = get_ptr_struct_assign1()
                                decl = structref[3]
                                decl.name = subnewname+"2"
                                decl.type.declname = subnewname+"2"
                                decl.type.type.names = ty1
                                rast.body.block_items.insert(x, decl)
                                x = x + 1

                                address_assign = structref[4]
                                if type(rname) == c_ast.StructRef or type(rname) == c_ast.ArrayRef:
                                    address_assign.lvalue.name = rname
                                else:
                                    address_assign.lvalue.name.name = rname
                                address_assign.lvalue.field.name = subname
                                address_assign.lvalue.type = "."
                                address_assign.rvalue.expr.name = subnewname+"2"
                                rast.body.block_items.insert(x, address_assign)
                                x = x + 1


                                ass1 = structref[5]

                                temprname = ass1.lvalue
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    temprname.name = rname
                                else:
                                    temprname.name.name = rname
                                temprname.field.name = subname


                                temnewname = ass1.rvalue.expr.name
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    temnewname.name = newname
                                else:
                                    temnewname.name.name = newname
                                temnewname.field.name = subname

                                recur(structs, temprname, temnewname, subnewname,n_isptr, Type, rast, x, mast, funtype,rdepth)
                            elif ii.hasAttribute("arr"):
                                # print("continue+recur+ref+nisptr+arr")
                                continue
                            else:  # no ptr
                                if ii.hasAttribute("Enum"):
                                    ass = get_struct_assign()
                                    if type(newname) == c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        ass.lvalue.name = newname
                                    else:
                                        ass.lvalue.name.name = newname
                                    ass.lvalue.field.name = ii.getAttribute("name")
                                    ass.lvalue.type = '.'
                                    if type(rname) == c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        ass.rvalue.name = rname
                                    else:
                                        ass.rvalue.name.name = rname
                                    ass.rvalue.field.name = ii.getAttribute("name")
                                    ass.rvalue.type = '.'
                                    rast.body.block_items.insert(record, ass)
                                    ass1 = get_assert()
                                    ass1.args.exprs[0].left = ass.lvalue
                                    ass1.args.exprs[0].right = ass.rvalue
                                    if funtype != 'void':
                                        slen = len(mast.body.block_items)
                                        mast.body.block_items.insert(slen - 1, ass1)
                                    else:
                                        mast.body.block_items.append(ass1)
                                    continue
                                n_isptr = False
                                """create object ref point to"""
                                subname = ii.getAttribute("name")  # nest object's name
                                subnewname = subname + "_"+str(ran)
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    name="self_"
                                    subnewname=name+"_"+subnewname
                                else:
                                    subnewname=rname+"_"+subnewname
                                Type = ii.getAttribute("type")
                                ty1 = re.findall('(.*[a-zA-Z0-9_])', Type)  # nest objec's type

                                structref = get_ptr_struct_assign1()
                                # decl = structref[1]
                                # decl.name = subnewname
                                # decl.type.declname = subnewname
                                # decl.type.type.names = ty
                                # rast.body.block_items.insert(record, decl)
                                # x = record + 1

                                ass1 = structref[1]
                                temprname = ass1.rvalue.name
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    temprname.name = rname
                                else:
                                    temprname.name.name = rname
                                temprname.field.name = subname


                                temnewname = ass1.lvalue.name
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:

                                    temnewname.name = newname
                                else:
                                    temnewname.name.name = newname
                                temnewname.field.name = subname


                                recur(structs, temprname, temnewname, temnewname,n_isptr, Type, rast, record, mast, funtype,rdepth)

            break

def find_ID(st,r_pa, n_pa):

    for i in st:
        if (i==None):
            break
        elif type(i)==c_ast.ID:
            if i.name in r_pa:
                index = r_pa.index(i.name)
                newname= n_pa[index]
                i.name=newname

            find_ID(i,r_pa,n_pa)
        else:
            find_ID(i,r_pa,n_pa)

def modify_label(st,r_pa,n_pa):
    for i in st:
        if (i == None):
            break
        elif type(i) == c_ast.Goto or type(i)==c_ast.Label:
            if i.name in r_pa:
                index = r_pa.index(i.name)
                newname = n_pa[index]
                i.name = newname

            modify_label(i, r_pa, n_pa)
        else:
            modify_label(i, r_pa, n_pa)


def modify_local_variable(rast,mast):
    l=[]
    l1=[]
    for i in rast.body.block_items:
        if type(i)==c_ast.Decl or type(i)==c_ast.Label:

            name=i.name
            name1=name+"1"
            l.append(i.name)
            l1.append(name1)
    for ii in mast.body.block_items:
        if type(ii)==c_ast.Decl:

            index=l.index(ii.name)
            name=l1[index]
            if type(ii.type)==c_ast.PtrDecl or type(ii.type)==c_ast.ArrayDecl:
                ii.type.type.declname=name
            else:
                ii.type.declname=name
            ii.name=name


    st=mast.body.block_items
    find_ID(st,l,l1)


def arr_recur(structs, rname, newname, newname1, arr_size, isptr, ty, r_ast, record, m_ast, funtype,depth):
    for s in structs:
        if s.getAttribute("name") == ty:
            var1 = s.getElementsByTagName("variable")
            if not var1:
                break
            else:
                for ii in var1:
                    subname = ii.getAttribute("name")
                    Type=ii.getAttribute("type")
                    ty1 = re.findall('(.*[a-zA-Z0-9_])', Type)
                    if ii.hasAttribute("level"):
                        if isptr:
                            if ii.hasAttribute("ptr") and ii.hasAttribute("arr"):
                                # print("arr_recur+continue+level+isptr+ptr+arr")
                                continue
                            elif ii.hasAttribute("ptr"):
                                # print("arr_recur+continue+level+isptr+ptr")
                                continue
                            elif ii.hasAttribute("arr"):
                                # print("arr_recur+continue+level+isptr+arr")
                                continue
                            else: #basic type
                                # print("arr_recur+continue+level+isptr+basic type")
                                continue

                        else: # isptr is false
                            if ii.hasAttribute("ptr") and ii.hasAttribute("arr"):
                                # print("arr_recur+continue+level+nisptr+ptr+arr")
                                continue
                            elif ii.hasAttribute("ptr"):
                                # print("arr_recur+continue+level+nisptr+ptr")
                                continue
                            elif ii.hasAttribute("arr"):
                                # print("arr_recur+continue+level+nisptr+arr")
                                continue
                            else: #basic type
                                if Type=="float" or Type=="double":
                                    # print("continue+ar_recur+basic type+float+double")
                                    continue
                                if ii.getAttribute("level") == 'L':
                                    arr=get_arr_recur()
                                    assign = arr[1]
                                    assign.cond.right.name = str(arr_size)
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        assign.stmt.block_items[0].lvalue.name.name = newname
                                    else:
                                        assign.stmt.block_items[0].lvalue.name.name.name = newname
                                    assign.stmt.block_items[0].lvalue.field.name = subname
                                    if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        assign.stmt.block_items[0].rvalue.name.name = rname
                                    else:
                                        assign.stmt.block_items[0].rvalue.name.name.name = rname
                                    assign.stmt.block_items[0].rvalue.field.name = subname
                                    r_ast.body.block_items.insert(record,assign)

                                    ass = arr[2]
                                    ass.cond.right.name = str(arr_size)
                                    if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                        ass.stmt.block_items[0].args.exprs[0].left.name.name = newname
                                    else:
                                        ass.stmt.block_items[0].args.exprs[0].left.name.name.name = newname
                                    ass.stmt.block_items[0].args.exprs[0].left.field.name = subname
                                    if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                        ass.stmt.block_items[0].args.exprs[0].right.name.name = rname
                                    else:
                                        ass.stmt.block_items[0].args.exprs[0].right.name.name.name  = rname
                                    ass.stmt.block_items[0].args.exprs[0].right.field.name = subname
                                    if funtype != 'void':
                                        slen = len(m_ast.body.block_items)
                                        m_ast.body.block_items.insert(slen - 1, ass)
                                    else:
                                        m_ast.body.block_items.append(ass)

                                continue
                    else: # ref
                        rdepth=depth+1
                        if len(sys.argv)>3 and rdepth==int(sys.argv[3]):
                            continue
                        elif rdepth==3:
                            continue

                        if isptr:
                            if ii.hasAttribute("ptr") and ii.hasAttribute("arr"):
                                # ("arr_recur+continue+ref+isptr+ptr+arr")
                                continue
                            elif ii.hasAttribute("ptr"):
                                # print("arr_recur+continue+ref+isptr+ptr")
                                continue
                            elif ii.hasAttribute("arr"):
                                # print("arr_recur+continue+ref+isptr+arr")
                                continue
                            else:  # basic type
                                # print("arr_recur+continue+ref+isptr+basic type")
                                continue

                        else:  # isptr is false
                            isptr1=False
                            if ii.hasAttribute("ptr") and ii.hasAttribute("arr"):
                                # print("arr_recur+continue+ref+nisptr+ptr+arr")
                                continue
                            elif ii.hasAttribute("ptr"):
                                # print("arr_recur+continue+ref+nisptr+ptr")
                                continue
                            elif ii.hasAttribute("arr"):
                                # print("arr_recur+continue+ref+nisptr+arr")
                                continue
                            else:  # basic type
                                arr=get_arr_recur()
                                a = arr[3]
                                temprname = a.lvalue
                                tempnewname = a.rvalue
                                if type(rname)==c_ast.StructRef or type(rname)==c_ast.ArrayRef:
                                    temprname.name.name = rname
                                else:
                                    temprname.name.name.name = rname
                                temprname.name.subscript.value = "i"
                                temprname.field.name = subname
                                if type(newname)==c_ast.StructRef or type(newname)==c_ast.ArrayRef:
                                    tempnewname.name.name = newname
                                else:
                                    tempnewname.name.name.name = newname
                                tempnewname.name.subscript.value = "i"
                                tempnewname.field.name = subname

                                arr_recur(structs,temprname,tempnewname,tempnewname,arr_size,isptr1,ty1,r_ast,record,m_ast,funtype,rdepth)
                                continue
            break




def before_recur(v,r_ast,funtype,m_ast,structs,record):
    print("3333333333333333")
    """"v is params,global or ret """
    if v.hasAttribute("level"):  # base type
        # if v.hasAttribute("quals"):
        #     pass
        if v.hasAttribute("ptr") and v.hasAttribute("arr"):
            # print("contiune+1111111111111")
        #array of pointer
            rname = v.getAttribute("name")
            Type = v.getAttribute("type")
            ty = re.findall('(.*[a-zA-Z0-9_])', Type)

            newname = rname + "1"
            arr_size = int(v.getAttribute("arr"))
            if Type == "float" or Type == "double":
                assume = get_assume_arr()
                assume.cond.right.value = str(arr_size)
                assume.stmt.block_items[0].args.exprs[0].left.expr.args.exprs[0].name = rname
                assume.stmt.block_items[0].args.exprs[0].right.expr.args.exprs[0].name = rname
                r_ast.body.block_items.insert(record, assume)
            if Type == "float" or Type == "double":
                x = record + 1
            else:
                x = record
            arr = get_basic_pointer_array()
            arr_base = arr[2]  # int *arr__1[n]
            arr_base.name = newname
            arr_base.type.type.type.declname = newname
            arr_base.type.type.type.type.names = ty
            arr_base.type.dim.value = str(arr_size)
            r_ast.body.block_items.insert(x, arr_base)
            x=x+1
            arr_base = arr[3]  # int arr__2[n]
            newname2 = rname + "2"
            arr_base.name = newname2
            arr_base.type.type.declname = newname2
            arr_base.type.type.type.names = ty
            arr_base.type.dim.value = str(arr_size)
            r_ast.body.block_items.insert(x, arr_base)
            x=x+1
            adress_assign=arr[4]
            adress_assign.cond.right.value=str(arr_size)
            adress_assign.stmt.block_items[0].lvalue.name.name=newname
            adress_assign.stmt.block_items[0].rvalue.expr.name.name=newname2
            r_ast.body.block_items.insert(x,adress_assign)
            x=x+1
            arr=get_basic_pointer_array()
            arr_base = arr[3]  # int arr__2[n]
            newname3 = rname + "3"
            arr_base.name = newname2
            arr_base.type.type.declname = newname3
            arr_base.type.type.type.names = ty
            arr_base.type.dim.value = str(arr_size)
            r_ast.body.block_items.insert(x, arr_base)
            x = x + 1
            adress_assign = arr[4]
            adress_assign.cond.right.value = str(arr_size)
            adress_assign.stmt.block_items[0].lvalue.name.name = rname
            adress_assign.stmt.block_items[0].rvalue.expr.name.name = newname3
            r_ast.body.block_items.insert(x, adress_assign)
            x = x + 1

            if v.getAttribute("level") == 'L':
                arr_base = arr[5]
                arr_base.cond.right.value = str(arr_size)
                arr_base.stmt.block_items[0].lvalue.name.name = newname2
                arr_base.stmt.block_items[0].rvalue.expr.name.name = rname
                r_ast.body.block_items.insert(x, arr_base)
                x=x+1
                arr_base = arr[4]
                arr_base.cond.right.value = str(arr_size)
                arr_base.stmt.block_items[0].lvalue.name.name = newname
                arr_base.stmt.block_items[0].rvalue.expr.name.name = newname2
                r_ast.body.block_items.insert(x, arr_base)

                m_ast_len=len(m_ast.body.block_items)
                arr_base = arr[6]
                arr_base.cond.right.value = str(arr_size)
                arr_base.stmt.block_items[0].args.exprs[0].left.expr.name.name = newname
                arr_base.stmt.block_items[0].args.exprs[0].right.expr.name.name = rname

                if funtype == 'void':
                    m_ast.body.block_items.append(arr_base)
                else:
                    m_ast.body.block_items.insert(m_ast_len - 1, arr_base)

        elif v.hasAttribute("ptr"):
            #baisc type pointer   need modify
            rname = v.getAttribute("name")
            newname = rname + "1"
            Type = v.getAttribute("type")
            ty = re.findall('(.*[a-zA-Z0-9_])', Type)
            if Type == "float" or Type == "double":
                assume = get_assume_poiter()
                assume.args.exprs[0].left.expr.args.exprs[0].expr.name= rname
                assume.args.exprs[0].right.expr.args.exprs[0].expr.name= rname
                r_ast.body.block_items.insert(record, assume)
            if Type == "float" or Type == "double":
                x = record + 1
            else:
                x = record
            pointer=get_basic_pointer()
            decl = pointer[1]
            decl.name = newname
            decl.type.type.declname = newname

            decl.type.type.type.names = ty
            r_ast.body.block_items.insert(x, decl)
            x=x+1
            if v.getAttribute("ref") == "void":
                pass
            else:
            # malloc = get_onestar_malloc()
            # malloc.lvalue.name = newname
            # malloc.rvalue.to_type.type.type.type.names = ty
            # malloc.rvalue.expr.args.exprs[0].expr.type.type.names = ty
            # r_ast.body.block_items.insert(1, malloc)

                newname1 = rname + "2"
                decl = pointer[2]  # float a;
                decl.name = newname1
                decl.type.declname = newname1
                decl.type.type.names = ty
                r_ast.body.block_items.insert(x, decl)
                x=x+1
                assign=pointer[3]
                assign.lvalue.name=newname
                assign.rvalue.expr.name=newname1
                r_ast.body.block_items.insert(x,assign)
                x=x+1
                pointer = get_basic_pointer()
                newname2 = rname + "3"
                decl = pointer[2]  # float a;
                decl.name = newname2
                decl.type.declname = newname2
                decl.type.type.names = ty
                r_ast.body.block_items.insert(x, decl)
                x = x + 1
                assign = pointer[3]
                assign.lvalue.name = rname
                assign.rvalue.expr.name = newname2
                r_ast.body.block_items.insert(x, assign)
                x = x + 1
                if v.getAttribute("level") == 'L':
                    assign = pointer[4]
                    assign.lvalue.name = newname1
                    assign.rvalue.expr.name = rname
                    r_ast.body.block_items.insert(x, assign)


                    ass = pointer[5]
                    ass.args.exprs[0].left.expr.name = rname
                    ass.args.exprs[0].right.expr.name = newname
                    if funtype != 'void':
                        slen = len(m_ast.body.block_items)
                        m_ast.body.block_items.insert(slen - 1, ass)
                    else:
                        m_ast.body.block_items.append(ass)

        elif v.hasAttribute("arr"):
            #basic type array
            rname = v.getAttribute("name")
            Type = v.getAttribute("type")
            ty = re.findall('(.*[a-zA-Z0-9_])', Type)
            newname = rname + "1"
            arr_size = int(v.getAttribute("arr"))
            if Type == "float" or Type == "double":
                assume = get_assume_arr()
                assume.cond.right.value = str(arr_size)
                assume.stmt.block_items[0].args.exprs[0].left.expr.args.exprs[0].name = rname
                assume.stmt.block_items[0].args.exprs[0].right.expr.args.exprs[0].name = rname
                r_ast.body.block_items.insert(record, assume)
            if Type == "float" or Type == "double":
                x = record + 1
            else:
                x = record
            arr = get_array()
            arr_base = arr[0]  # int arr__1[n];
            arr_base.name = newname
            arr_base.type.type.declname = newname
            arr_base.type.type.type.names = ty
            arr_base.type.dim.value = str(arr_size)
            r_ast.body.block_items.insert(x, arr_base)
            x=x+1
            if v.getAttribute("level") == "L":
                assign = arr[3]
                assign.cond.right.value = str(arr_size)
                assign.stmt.block_items[0].lvalue.name.name = newname
                assign.stmt.block_items[0].rvalue.name.name = rname
                r_ast.body.block_items.insert(x, assign)

                m_ast_len = len(m_ast.body.block_items)
                ass = arr[4]
                ass.cond.right.value = str(arr_size)
                ass.stmt.block_items[0].args.exprs[0].left.name.name = newname
                ass.stmt.block_items[0].args.exprs[0].right.name.name = rname

                if funtype == 'void':
                    m_ast.body.block_items.append(ass)
                else:
                    m_ast.body.block_items.insert(m_ast_len - 1, ass)

        else:  # no ptr and no arr
            # create a variable and rename
            if v.hasAttribute("Enum"):
                rname = v.getAttribute("name")
                Type = v.getAttribute("type")
                ty = re.findall('(.*[a-zA-Z0-9_])', Type)
                newname = rname + "1"

                decl = tese()
                decl.name = newname
                decl.type.declname = newname
                ty1=ty[0]
                decl.type.type.name = ty1
                r_ast.body.block_items.insert(record, decl)
                x = record + 1

                assign = get_assign()
                assign.lvalue.name = newname
                assign.rvalue.name = rname
                r_ast.body.block_items.insert(x, assign)

                m_ast_len = len(m_ast.body.block_items)
                ass = get_assert()
                ass.args.exprs[0].left.name = newname
                ass.args.exprs[0].right.name = rname

                if funtype == 'void':
                    m_ast.body.block_items.append(ass)
                else:
                    m_ast.body.block_items.insert(m_ast_len - 1, ass)
            else:
                rname = v.getAttribute("name")
                Type = v.getAttribute("type")
                ty = re.findall('(.*[a-zA-Z0-9_])', Type)
                if Type == "float" or Type == "double":
                    assume = get_assume()
                    assume.args.exprs[0].left.expr.args.exprs[0].name = rname
                    assume.args.exprs[0].right.expr.args.exprs[0].name = rname
                    r_ast.body.block_items.insert(record, assume)
                if Type == "float" or Type == "double":
                    x = record + 1
                else:
                    x = record
                newname = rname + "1"
                decl1 = get_decl()
                decl=decl1[0]
                decl.name = newname
                decl.type.declname = newname
                decl.type.type.names = ty
                r_ast.body.block_items.insert(x, decl)
                x=x+1
                if v.getAttribute("level") == "L":
                    assign = get_assign()
                    assign.lvalue.name = newname
                    assign.rvalue.name = rname
                    r_ast.body.block_items.insert(x, assign)

                    m_ast_len = len(m_ast.body.block_items)
                    ass = get_assert()
                    ass.args.exprs[0].left.name = newname
                    ass.args.exprs[0].right.name = rname

                    if funtype == 'void':
                        m_ast.body.block_items.append(ass)
                    else:
                        m_ast.body.block_items.insert(m_ast_len - 1, ass)

    else:  # compound type ref
        depth=1
        # if v.hasAttribute("quals"):
        #     pass
        if v.hasAttribute("ptr") and v.hasAttribute("arr"):
            print("\n")
            # print("befor_recur+continue+ref+ptr+arr")

            # rname = v.getAttribute("name")
            # Type = v.getAttribute("type")
            # ty = re.findall('(.*[a-zA-Z0-9])', Type)
            # newname = rname + "1"
            # arr_size = int(v.getAttribute("arr"))
            # arr = get_array()
            # arr_base = arr[1]  # A *arr[n]
            # arr_base.name = newname
            # arr_base.type.type.type.declname = newname
            # arr_base.type.type.type.type.names = ty
            # arr_base.type.dim.value = str(arr_size)
            # r_ast.body.block_items.insert(0, arr_base)
            #
            # array_malloc = arr[9]
            # array_malloc.cond.right.value = str(arr_size)
            # array_malloc.stmt.block_items[0].lvalue.name.name = newname
            # array_malloc.stmt.block_items[0].rvalue.to_type.type.type.type = ty
            # array_malloc.stmt.block_items[0].rvalue.expr.args.exprs[0].expr.type.type.names = ty
            # r_ast.body.block_items.insert(1, array_malloc)
            #
            # isptr = True
            # record = 2
            # for j in range(arr_size):
            #     c_arr = get_compound_array()
            #     rawname = c_arr.lvalue.name
            #     rawname.name.name = rname
            #     rawname.subscript.value = j
            #     newname1 = c_arr.rvalue.name
            #     newname1.name.name = newname
            #     newname1.subscript.value = j
            #     recur(structs, rawname, newname1, newname1, isptr, Type, r_ast, record, m_ast,
            #           funtype)

        elif v.hasAttribute("ptr"):
            rname = v.getAttribute("name")
            newname = rname + "1"
            copyname=rname+"2"
            decl = get_struct_onestar_decl()
            decl.name = newname
            decl.type.type.declname = newname
            Type = v.getAttribute("type")
            ty = re.findall('(.*[a-zA-Z0-9_])', Type)
            decl.type.type.type.names = ty
            r_ast.body.block_items.insert(record, decl)

            if v.getAttribute("ref") == "void":
                pass
            else:
                x=record+1
                isptr = True
                s=get_ptr_struct_assign2()
                copy=s[5]

                copy.name=copyname
                copy.type.declname=copyname
                copy.type.type.names = ty
                r_ast.body.block_items.insert(x, copy)
                x=x+1
                address_assign=s[2]
                address_assign.lvalue.name=newname
                address_assign.rvalue.expr.name=copyname
                r_ast.body.block_items.insert(x,address_assign)
                x=x+1
                s = get_ptr_struct_assign2()
                copy = s[5]
                copy.name = copyname+"3"
                copy.type.declname = copyname+"3"
                copy.type.type.names = ty
                r_ast.body.block_items.insert(x, copy)
                x = x + 1
                address_assign = s[2]
                address_assign.lvalue.name = rname
                address_assign.rvalue.expr.name = copyname+"3"
                r_ast.body.block_items.insert(x, address_assign)
                x = x + 1


                recur(structs, rname, newname, copyname, isptr, Type, r_ast, x, m_ast, funtype,depth)

        elif v.hasAttribute("arr"):
            rname = v.getAttribute("name")
            Type = v.getAttribute("type")
            ty = re.findall('(.*[a-zA-Z0-9_])', Type)
            newname = rname + "1"
            arr_size = v.getAttribute("arr")

            arr = get_array()  # A arr[n]
            arr_cpmpound = arr[0]
            arr_cpmpound.name = newname
            arr_cpmpound.type.type.declname = newname
            arr_cpmpound.type.type.type.names = ty
            arr_cpmpound.type.dim.value = str(arr_size)
            r_ast.body.block_items.insert(record, arr_cpmpound)
            x=record+1

            isptr = False
            arr_recur(structs,rname,newname,newname,arr_size,isptr,Type,r_ast,x,m_ast,funtype,depth)
            # for j in range(arr_size):
            #     c_arr = get_compound_array()
            #     rawname = c_arr.lvalue.name
            #     rawname.name.name = rname
            #     rawname.subscript.value = j
            #     newname1 = c_arr.rvalue.name
            #     newname1.name.name = newname
            #     newname1.subscript.value = j
            #     recur(structs, rawname, newname1, newname1, isptr, Type, r_ast, record, m_ast, funtype)

        else:  # no ptr and no arr
            if v.hasAttribute("Enum"):
                rname = v.getAttribute("name")
                Type = v.getAttribute("type")
                ty = re.findall('(.*[a-zA-Z0-9_])', Type)
                newname = rname + "1"

                decl = tese()
                decl.name = newname
                decl.type.declname = newname
                ty1=ty[0]
                decl.type.type.name = ty1
                r_ast.body.block_items.insert(record, decl)
                x = record + 1

                assign = get_assign()
                assign.lvalue.name = newname
                assign.rvalue.name = rname
                r_ast.body.block_items.insert(x, assign)

                m_ast_len = len(m_ast.body.block_items)
                ass = get_assert()
                ass.args.exprs[0].left.name = newname
                ass.args.exprs[0].right.name = rname

                if funtype == 'void':
                    m_ast.body.block_items.append(ass)
                else:
                    m_ast.body.block_items.insert(m_ast_len - 1, ass)
            else:
                rname = v.getAttribute("name")
                Type = v.getAttribute("type")
                ty = re.findall('(.*[a-zA-Z0-9_])', Type)
                newname = rname + "1"
                decl1 = get_decl()
                decl=decl1[0]
                decl.name = newname
                decl.type.declname = newname
                if type(decl.type.type) == c_ast.IdentifierType:
                    decl.type.type.names = ty
                else:
                    decl.type.type.name = ty
                r_ast.body.block_items.insert(record, decl)
                isptr = False
                x=record+1

                recur(structs, rname, newname, newname, isptr, Type, r_ast, x, m_ast, funtype,depth)

# Finish_list=["AP_ADSB_set_is_auto_mode","AP_AHRS_get_compass","AP_AHRS_NavEKF_getMagOffsets",
#              "AP_AHRS_set_correct_centrifugal","AP_BattMonitor_get_highest_failsafe_priority",
# "AP_BattMonitor_has_failsafed","AP_Camera_set_is_auto_mode","AP_DEVO_Telem_update_control_mode",
#              "AP_HAL_Util_set_soft_armed","AP_Mission_init_jump_tracking",
# "AP_Mission_reset","Compass_get_learn_type","Compass_get_primary","Compass_save_offsets","constrain_int16",
#              "Copter_init_disarm_motors","Copter_should_disarm_on_failsafe",
# "get16","get8","MIN","NavEKF2_core_getMagOffsets","NavEKF3_core_getMagOffsets","RC_Channel_get_control_in",
#              "RC_Channel_get_control_mid","RC_Channel_pwm_to_angle_dz_trim",
# "RC_Channel_rc_channel","RC_Channel_set_radio_in","Semaphore_give","ToyMode_enabled",
#              "ToyMode_get_throttle_mid","RCInput_read_self_com","RCInput_new_input_self_com","main_self_com","RC_Channel_read_self_com"]
def self_com(ast,ast1,f,structs,filename,content):
    print("confidentianl selfcom")
    fp = open("../../../path/project.txt")
    line = fp.readline().strip()
    path = '../../Project/'+line+'/pilot_src/Source/Src/'+filename+'.c'


    generator=c_generator.CGenerator()
    funname=f.getAttribute("name")
    funname1=funname+"_self_com"


    funtype=f.getAttribute("Returntype")
    raw_params = []  # parameter and global variable
    new_params = []
    var=f.getElementsByTagName("params")
    function_global=f.getElementsByTagName("global")
    function_ret=f.getElementsByTagName("return_value")
    for l in var:
        varname = l.getAttribute("name")
        # element=l.childNodes[0].data
        varname1 = varname + "1"
        raw_params.append(varname)
        new_params.append(varname1)
    for g in function_global:
        gname = g.getAttribute("name")
        gname1 = gname+"1"
        raw_params.append(gname)
        new_params.append(gname1)
    # raw_params.append("Second")
    # new_params.append("End")
    raw_params.append("ret_self_com")
    new_params.append("ret_self_com1")

    for i in range(0, len(ast.ext)):
        if (type(ast.ext[i]) == c_ast.FuncDef and ast.ext[i].decl.name == funname):
            if funname1 in content:
                break


            r_ast = ast.ext[i]
            #print(r_ast)

            r_ast.decl.name=funname1
            if type(r_ast.decl.type.type)==c_ast.PtrDecl:
                r_ast.decl.type.type.type.declname=funname1
            else:
                r_ast.decl.type.type.declname=funname1

            m_ast = ast1.ext[i]

            if funtype != 'void':
                deal_return(r_ast)
                r_ast.body.block_items.pop()
                deal_return1(m_ast)
            elif funtype=="void":
                deal_void_return(r_ast)
                deal_void_return(m_ast)


            st = m_ast.body.block_items
            if st is None:
                 break
            raw=['Second']
            new=['End']

            modify_label(st, raw, new)

            """modify local variable"""
            modify_local_variable(r_ast,m_ast)


            if raw_params is not None:
                st=m_ast.body.block_items
                if st is None:
                    break

                find_ID(st,raw_params,new_params)
            else:
                break

            for i in var:
                print("1111111111111")
                record=0
                before_recur(i,r_ast,funtype,m_ast,structs,record)
            for a in function_global:
                print("222222222222222")
                global_name=a.getAttribute("name")
                for g_var in structs:
                    g_var_name=g_var.getAttribute("name")
                    if global_name == g_var_name:
                        variable=g_var.getElementsByTagName('variable')
                        v=variable[0]
                        record=0
                        before_recur(v,r_ast,funtype,m_ast,structs,record)
                        break
            for i in function_ret:
                decl = get_decl()
                Type = i.getAttribute("type")
                ty=re.findall('(.*[a-zA-Z0-9_])', Type)
                if i.hasAttribute("ptr"):
                    ptr=decl[1]
                    ptr.name="ret_sef_com"
                    ptr.type.type.declname="ret_self_com"

                    ptr.type.type.type.names=ty
                    r_ast.body.block_items.insert(0, ptr)
                elif i.hasAttribute("Enum"):
                    decl=tese()
                    decl.name="ret_self_com"
                    decl.type.declname="ret_self_com"
                    ty1=ty[0]
                    decl.type.type.name=ty1
                    r_ast.body.block_items.insert(0, decl)

                else:
                    normal=decl[0]
                    normal.name="ret_self_com"
                    normal.type.declname="ret_self_com"
                    normal.type.type.names=ty
                    r_ast.body.block_items.insert(0, normal)
                record=1
                before_recur(i,r_ast,funtype,m_ast,structs,record)


            result=merge_ast(r_ast,m_ast)
            print(result)
            c_result=generator.visit(result)
            path1=os.path.abspath(path)
            delete_fun(path1,funname1)
            objectfile = open(path1, 'a+')
            objectfile.write("\n")
            objectfile.write(c_result)
            objectfile.close()

            break

def translate_to_cc(filename, structfile,content):
    """ Simply use the c_generator module to emit a parsed AST.
    """
    ast = parse_file(filename) 
    ast1 = parse_file(filename)
    doc=parse(structfile)
    root=doc.documentElement
    structs=root.getElementsByTagName('decl')
    function=root.getElementsByTagName('function')
    objectname = os.path.basename(filename)
    for f in function:

        # self_com(ast,ast1,f,structs,object_file_path)
        self_com(ast, ast1, f, structs, objectname,content)


   
