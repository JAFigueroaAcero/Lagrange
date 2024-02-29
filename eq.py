
import funclatexstr as f
import funcstrform as f2
from sympy import *
from os.path import isfile, isdir, dirname, join,realpath
import os

y,a,A,m,w,G,M,x,b = symbols("y,a,A,m,w,G,M,x,b")

L = ((m)*(((a)**(2))/(2)))+((-1)*(((m)*(w)**(2)*(y)**(2))/(2)))+((((G)*(M))/(((x)**(2)+((y)+(b))**(2))**(((1)/(2))))))
vars = ['y']
dotvars = [['y'], ['a']]
ddvars = ['A']
const = ['m', 'w', 'G', 'M', 'x', 'b']
derv = []
equations = []

dy = simplify(diff(L,y))
derv.append(dy)

constl= []
for eq in derv:
    constl.append(eq == 0)


da = simplify(diff(L,a))
const.append('c')
const.append('C')
if constl[0]:


    loc = f2.sepvar(str(da),'a',['y'],['a'],const)

    dasep = f.sepfracs2(loc[1][0],'a')[0]
    datot = f.replaceminus(dasep + '+' + loc[1][1])

    datotlist = f.createbrackets(datot)

    eqloc = f.solve(datotlist[1],'a',const[-1])

    equations.append(f2.simpandsave(eqloc,'a',vars,dotvars[1],const))



else:

    der = ''
    for v in vars:
        der += f2.simpandsave(dotvars[1][dotvars[0].index(v)]+ '*' +f2.derandsave(str(da),v,['y'],['a'],['A'],['m', 'w', 'G', 'M', 'x', 'b', 'c', 'C']),v,['y'],['a'],['A'],['m', 'w', 'G', 'M', 'x', 'b', 'c', 'C']) + '+'
    
    for v in dotvars[1]:
        der +=f2.simpandsave(v.upper()+ '*' +f2.derandsave(str(da),v,['y'],['a'],['A'],['m', 'w', 'G', 'M', 'x', 'b', 'c', 'C']),v,['y'],['a'],['A'],['m', 'w', 'G', 'M', 'x', 'b', 'c', 'C']) + '+'
        
    der += '-' + f2.derandsave(L,dotvars[0][dotvars[1].index('a')],['y'],['a'],['A'],['m', 'w', 'G', 'M', 'x', 'b', 'c', 'C'])
    loc = f2.sepvar(der,'A',['y'],['a'],['A'],['m', 'w', 'G', 'M', 'x', 'b', 'c', 'C'])

    dAsep = f.sepfracs2(loc[1][0],'A')[0]
    dAtot = f.replaceminus(dAsep + '+' + loc[1][1])

    dAtotlist = f.createbrackets(dAtot)

    eqloc = f.solve(dAtotlist[1],'A','0')

    equations.append(f2.simpandsave(eqloc,'A',['y'],['a'],['A'],['m', 'w', 'G', 'M', 'x', 'b', 'c', 'C']))


f2.savingequations(equations,constl,vars,dotvars,ddvars,const)
