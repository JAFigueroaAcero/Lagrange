import numpy as np
from os.path import isfile, isdir, dirname, join,realpath
import os

vars = list('abcdefghijklmnopqrstuvwxyz')

VARS = list('abcdefghijklmnopqrstuvwxyz'.upper())

def createbrackets(L):
    Llist = []
    Lloc = ''
    lb = 0
    rb = 0
    i = 0
    zero = True
    for n,l in enumerate(L):
        if l == '+' and (lb != 0 or zero):
            zero = False
            if lb == rb:
                zero = True
                Lloc += "(" + L[i:n] + ")" + "+"
                Llist.append(L[i:n])
                i = n+1
                lb = 0
                rb = 0
                
        elif l == '(':
            zero = False
            lb += 1
        elif l == ')':
            zero = False
            rb += 1
    Lloc += "(" + L[i:n+1] + ")"
    Llist.append(L[i:n+1])
    return Lloc, Llist




def simplify(eq,var):
    d = open(join(dirname(realpath(__file__)),f'simp{var}.py'), 'w')

    lvars = []
    for l in eq:
        if l in vars or l in VARS:
            if not l in lvars:
                lvars.append(l)
    textvars = ''

    for v in lvars:
        textvars += f'{v},'
    code = f'''
from sympy import *
from os.path import isfile, isdir, dirname, join,realpath

{textvars[0:-1]}= symbols("{str(lvars)[1:-1].replace("'", "").replace(" ", "")}")
eq = {eq}

d = open(join(dirname(realpath(__file__)),f'simp{var}.txt'), 'w')
d.write(str(simplify(eq)).replace(" ", ""))
d.close()
'''
    d.write(code)
    d.close()

    os.system(f"python3 {join(dirname(realpath(__file__)),f'simp{var}.py')}")



def createbracketsmd(L):
    Llist = []
    oplist = []
    Lloc = ''
    lb = 0
    rb = 0
    i = 0
    zero = True
    for n,l in enumerate(L):
        if (l == '*' and (L[n-1] != '*' and L[n+1] != '*')) and (lb != 0 or zero):
            zero = False
            if lb == rb:
                zero = True
                if L[i] == '(':
                    Lloc += L[i:n] + "*"
                    Llist.append(L[i:n])
                else:
                    Lloc += "(" + L[i:n] + ")" + "*"
                    Llist.append("("+L[i:n]+")")
                oplist.append('*')
                i = n+1
                lb = 0
                rb = 0
        elif l == '/' and (lb != 0 or zero):
            zero = False
            if lb == rb:
                zero = True
                if L[i] == '(':
                    Lloc += L[i:n] + "/"
                    Llist.append(L[i:n])
                else:
                    Lloc += "(" + L[i:n] + ")" + "/"
                    Llist.append("("+L[i:n]+")")
                oplist.append('/')
                i = n+1
                lb = 0
                rb = 0
                
        elif l == '(':
            zero = False
            lb += 1
        elif l == ')':
            zero = False
            rb += 1
    
    if L[i] == '(':
        pass
        Lloc += L[i:n+1]
        Llist.append(L[i:n+1])
    else:
        pass
        Lloc += "(" + L[i:n+1] + ")"
        Llist.append("("+L[i:n+1]+")")
    return Lloc, Llist, oplist
    
def removespace(L):
    return L.replace(' ', '')

def removevar(L,var):
    return L.replace(f'{var}', '1')

def solve(Llist,var,const):
    
    varterms = []
    newLlist = []
    for term in Llist:
        if var in term:
            varterms.append(term)
        else:
            newLlist.append(term)
    div = ''
    for v in varterms:
        div += f'({v})+'
    div = removevar(div[0:-1],var)

    num = ''
    for v in newLlist:
        num += f'({v})+'
    if num == '':
        return f'({const})/{div}'
    else:
        return f'({const}-({num[0:-1]}))/{div}'


def sepfracs(term,ddvars):
    ##Dado un termino
#separar por parentesis y simbolos de */
    Lloc, Llist, oplist = createbracketsmd(term)
#Buscar los términos con derivadas mayusculas
    i = 0
    flag = False
    for n,t in enumerate(Llist):
        for var in ddvars:
            if var in t:
                i = n
                flag = True
                break
        if flag:
            break
#Ese término separarlo por sumas en parentesis
    _, Llist2 = createbrackets(Llist[i][1:-1])
    
#Unir esos terminos a los demás
    newterm = ''
    for term in Llist2:
        locterm = ''
        for n,term2 in enumerate(Llist):
            if n != i:
                if n == 0:
                   locterm += term2
                else:
                    locterm += f'{oplist[n-1]}{term2}'
        newterm += f'({locterm})*{term}+'
    return createbrackets(removespace(newterm[0:-1]))

def updatevars(pvars,pddvars,removevars):
    '''
    Actualización de variables eliminando removevars de la lista
    '''
    lpvars = []
    lpddvars = []
    for n,var in enumerate(pvars):
        if not (var in removevars):
            lpvars.append(var)
            lpddvars.append(pddvars[n])
    return lpvars, lpddvars


def adddotvars(vars,pvars,pddvars,L):
    '''
    Dado un lagrangiano crear sus derivadas en función de \\dot{} 
    '''
    dotvars = [vars,[]]
    ddvars = []
    for v in vars:
        dotvars[1].append(pvars.pop(0))
        ddvars.append(pddvars.pop(0))
    while True:
        try:
            i = L.index("\\dot")
            Lp = L[i::]
            i0 = Lp.index('{')
            j0 = Lp.index('}')
            v = Lp[i0+1:j0]
            L = L[0:i] + f"({dotvars[1][dotvars[0].index(v)]})" + L[i+j0+1::]
        except:
            break
    return pvars,pddvars,L,dotvars,ddvars



def creatediv(L):
    '''
    Dado un lagrangiano remplazar \\frac por /
    '''
    while True:
        try:
            i = L.index("\\frac")
            Lp = L[i::]

            i0 = Lp.index('{')
            j0 = Lp.index('}')

            Lpp = Lp[j0+1::]

            i1 = Lpp.index('{')
            j1 = Lpp.index('}')
            L = L[0:i] + f"(({Lp[i0+1:j0]})/({Lpp[i1+1:j1]}))" + L[i+j0+j1+2::]
        except:
            break
    return L

def creatediv(L):
    '''
    Dado un lagrangiano remplazar \\frac por /
    '''
    while "\\frac" in L:
        i = L.index("\\frac")+5
        Lp = L[i::]
        input(f'Lp {Lp}')
        lc = 0
        rc = 0
        for n,v in enumerate(Lp):
            if v == '{':
                lc += 1
            elif v == '}':
                rc += 1
            if lc == rc and lc != 0:
                break
        
        num = Lp[1:n]
        print('num',num)
        
        lc = 0
        rc = 0
        print(Lp[n+1::])
        for m,v in enumerate(Lp[n+1::]):
            if v == '{':
                lc += 1
            elif v == '}':
                rc += 1
            if lc == rc and lc != 0:
                break

        den = Lp[n+2: m+n+1]
        print('den',den)

        L = L[0:i-5] + f"(({num})/({den}))" + L[i+m+n+2::]
        print('newL', L)
    return L
def createpow(L):
    '''
    Dado un lagrangiano, remplazar ^{} por **
    '''
    while '^{' in L:
        i = L.index("^")+1
        Lp = L[i::]
        
        lc = 0
        rc = 0
        for n,v in enumerate(Lp):
            if v == '{':
                lc += 1
            elif v == '}':
                rc += 1
            if lc == rc and lc != 0:
                break
        pow = Lp[1:n]
        input(f'pow , {pow}')
        
        L = L[0:i-1] + f"**({pow})" + L[i+n+1::]
        print(L)
    return L

def sepmult(L):
    newL = ''
    i = 0
    for n,l in enumerate(L[0:-1]):
        
        if (l in vars or l in VARS) and (L[n-1] != '(' or L[n+1] != ')'):
            
            newL += L[i:n] + '(' + L[n] + ')'
            input(f'locking {i},{n},{l}, {newL}, {L[i:n]}, {L[n]}, {L[n+1::]}')
            i = n+1
    if L[-1] in vars or L[-1] in VARS:
        return newL + '(' + L[i::] + ')'
    else: 
        return newL + L[i::]

def addmult(L):
    return L.replace(")(", ")*(")


def replaceminus(eq):
    eq = removespace(eq)
    if eq[0:2] == '--':
        eq = eq[2::]
    while '--' in eq or '++' in eq or '+-' in eq or '-+' in eq:
        input(f'??{eq}')
        eq = eq.replace('--','+').replace('++','+').replace('+-', '-').replace('-+','-')
    input(f'eqminus,{eq}')

    eq = '(-1)*' + eq[1::] if eq[0] == '-' else eq
    neweq = ''
    i=-1
    print('eq',eq)
    for n,v in enumerate(eq):
        
        if v == '-' and (eq[n-1:n+4] != '(-1)*'):
            print(n,v,eq[n-1:n+4])
            neweq += eq[i+1:n] + '+(-1)*'
            print(neweq)
            i = n
    print('?', eq[i+1::])
    neweq += eq[i+1::]
    print('end', neweq)

    return neweq

def sepfracs2(L,var):
    L = replaceminus(L)
    

    print('lag', L)
    Lloc, Llist, oplist = createbracketsmd(L)

    print('mult',Lloc,Llist, oplist)
    
    for n,v in enumerate(Llist):
        if var in v:
            break
    num = createbrackets(removespace(v)[1:-1])[1]

    L = ''
    for v in num:
        loc = ''
        j = 1
        for m,w in enumerate(Llist):
            #input(f'{oplist},{m},{w}')
            
            if n != m:
                if m == 0:
                   loc += w
                else:
                    loc += f'{oplist[m-1]}{w}'
            else:
                
                j += 1
                loc = '*' + loc
                if m == 0:
                    oplist[0] = ''
                else:
                    oplist[m-1] = ''

        L += v + loc + '+'
    
    print('broke',L)
    return createbrackets(removespace(L[0:-1]))
    

#print(sepfracs2('a*(r - 1)/2 + r','r')) # bug

#print(createbracketsmd('1*2*(ax+by)/(abcd)')) #bug


#print(createbracketsmd('a*(a+b*r+2)/2'))
#print(sepfracs2('a*(a+b*r+2)/2','r'))


'''

from sympy import *

['*','/']
r,A,a,x = symbols('r,A,a,x')



t = ((4+r)*(2 - 2/r)*(A+1))#+(((4+r)*a/r**2)*(a))



print(sepfracs2(str(simplify(t)),'A'))
'''
