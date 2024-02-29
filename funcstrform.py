from os.path import isfile, isdir, dirname, join,realpath
import os
import funclatexstr as fls
import pandas as pd
def vars2str(*vars):
    textvars = ''
    for var in vars:
        for v in var:
            textvars += f'{v},'
    return textvars[0:-1]


def initialize(L,vars,dotvars,ddvars,const,textvars):
    code = f'''
import funclatexstr as f
import funcstrform as f2
from sympy import *
from os.path import isfile, isdir, dirname, join,realpath
import os

{textvars} = symbols("{textvars}")

L = {L}
vars = {vars}
dotvars = {dotvars}
ddvars = {ddvars}
const = {const}
derv = []
equations = []
'''
    return code


def derv(v):
    return f'''
d{v} = simplify(diff(L,{v}))
derv.append(d{v})
'''


def const(L,dot,dotvars,pvars,pddvars):
    return f'''

    loc = sepvar(str(d{dot}),{dot})
    d{dot}list = f.sepfracs2(str(d{dot}),'{dot}')
    eqloc = f.solve(d{dot}list[1],'{dot}',const[-1])
    f2.simplify(eqloc,{dot},vars,dotvars[1],const)

    d = open(join(dirname(realpath(__file__)),f'simp{dot}.txt'),'r')
    equations.append(d.read())
    d.close()
'''

def const(L,dot,vars,dotvars):
    return f'''

    loc = f2.sepvar(str(d{dot}),'{dot}',{vars},{dotvars},const)

    d{dot}sep = f.sepfracs2(loc[1][0],'{dot}')[0]
    d{dot}tot = f.replaceminus(d{dot}sep + '+' + loc[1][1])

    d{dot}totlist = f.createbrackets(d{dot}tot)

    eqloc = f.solve(d{dot}totlist[1],'{dot}',const[-1])

    equations.append(f2.simpandsave(eqloc,'{dot}',vars,dotvars[1],const))


'''

def var(L,v,vars,dotvars,ddvars,const,pvars,pddvars):
    code = ''

    code += f'''
    textvars = f2.vars2str(vars,dotvars[1],ddvars,const)

    d = open(join(dirname(realpath(__file__)),f'der{v}.py'),'w')
    d.write(f2.der(L,{v},textvars))
    d.close()

    os.system(f"python3 {{join(dirname(realpath(__file__)),f'der{v}.py')}}")

    d = open(join(dirname(realpath(__file__)),f'der{v}.txt'),'r')
    der{v} = d.read()
    d.close()
'''
    #Derivar el resultado de f2.der respecto a todas las variables
    #si el valor a derivar coincide con v.upper() entonces no derivar pero cambiar v
    #en el código por v.upper()

    #En otros casos, agregar dotvars respectivas de cada derivada
    return code


def var(L,dot,vars,dotvars,ddvars,const,pvars,pddvars):
    code = f'''
    der = ''
    for v in vars:
        der += f2.simpandsave(dotvars[1][dotvars[0].index(v)]+ '*' +f2.derandsave(str(d{dot}),v,{vars},{dotvars},{ddvars},{const}),v,{vars},{dotvars},{ddvars},{const}) + '+'
    
    for v in dotvars[1]:
        der +=f2.simpandsave(v.upper()+ '*' +f2.derandsave(str(d{dot}),v,{vars},{dotvars},{ddvars},{const}),v,{vars},{dotvars},{ddvars},{const}) + '+'
        
    der += '-' + f2.derandsave(L,dotvars[0][dotvars[1].index('{dot}')],{vars},{dotvars},{ddvars},{const})
    loc = f2.sepvar(der,'{dot.upper()}',{vars},{dotvars},{ddvars},{const})

    d{dot.upper()}sep = f.sepfracs2(loc[1][0],'{dot.upper()}')[0]
    d{dot.upper()}tot = f.replaceminus(d{dot.upper()}sep + '+' + loc[1][1])

    d{dot.upper()}totlist = f.createbrackets(d{dot.upper()}tot)

    eqloc = f.solve(d{dot.upper()}totlist[1],'{dot.upper()}','0')

    equations.append(f2.simpandsave(eqloc,'{dot.upper()}',{vars},{dotvars},{ddvars},{const}))

'''
    return code



def derandsave(L,v,*vars):
    textvars = vars2str(*vars)
    der(L,v,textvars)
    
    d = open(join(dirname(realpath(__file__)),f'der{v}.txt'), 'r')
    eq = d.read()
    d.close()
    return eq

def der(L,v,textvars):
    code = f'''
import funclatexstr as f
import funcstrform as f2
from sympy import *
from os.path import isfile, isdir, dirname, join,realpath
import os

{textvars} = symbols("{textvars}")
L = {L}

der{v} = simplify(diff(L,{v}))

d = open(join(dirname(realpath(__file__)),f'der{v}.txt'), 'w')

d.write(str(der{v}))
d.close()
'''
    d = open(join(dirname(realpath(__file__)),f'der{v}.py'), 'w')
    d.write(code)
    d.close()

    os.system(f"python3 {join(dirname(realpath(__file__)),f'der{v}.py')}")

def simplify(eq,var,*vars):
    d = open(join(dirname(realpath(__file__)),f'simp{var}.py'), 'w')

    textvars = vars2str(*vars)

    code = f'''
from sympy import *
from os.path import isfile, isdir, dirname, join,realpath

{textvars} = symbols("{textvars}")
eq = {eq}

d = open(join(dirname(realpath(__file__)),f'simp{var}.txt'), 'w')
d.write(str(simplify(eq)).replace(" ", ""))
d.close()
'''
    d.write(code)
    d.close()

    os.system(f"python3 {join(dirname(realpath(__file__)),f'simp{var}.py')}")


def simpandsave(eq,var,*vars):
    simplify(eq,var,*vars)
    d = open(join(dirname(realpath(__file__)),f'simp{var}.txt'),'r')
    eq = d.read()
    d.close()
    return eq

def sepvar(L,var,*vars):
    Llist = fls.createbrackets(fls.replaceminus(L))[1]


    valv = ['0']
    nvalv = ['0']
    simpeq = '0+'
    simprest = '0+'
    for v in Llist:
        if var in v:
            valv.append(v)
            simpeq += v + '+'
        else:
            nvalv.append(v)
            simprest += v + '+'

    while '' in valv:
        if '' in valv:
            valv.pop(valv.index(''))
    while '' in nvalv:
        if '' in nvalv:
            nvalv.pop(nvalv.index(''))
    simpeq = simpeq[0:-1]
    simprest = simprest[0:-1]


    simpeq = simpandsave(simpeq,var,*vars)
    simprest = simpandsave(simprest,var,*vars)
    return (simpeq + '+' + simprest).replace('+-','-'),[simpeq,simprest],[valv, nvalv]
    

def savingequations(equations,constl,vars,dotvars,ddvars,const):
    datalist = []
    rnames = []
    for n,c in enumerate(constl):
        rnames.append(f'eq_{vars[n]}')
        if c:
            eq = f'{dotvars[1][n]}={equations[n]}'
        else:
            eq = f'{ddvars[n]}={equations[n]}'
        
        datalist.append([eq,vars[n],dotvars[1][n],ddvars[n]])
    datalist.append([const])
    rnames.append('const')

    df = pd.DataFrame(datalist, index = rnames, columns = ['equation','var','dotvar','ddvar'])
    df.to_csv(join(dirname(realpath(__file__)),f'data.csv'))




#print(sepvar('a+a-b+c','a',['a','b','c']))