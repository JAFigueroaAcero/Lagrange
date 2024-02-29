import funcstrform as f
import latexstr as l
from os.path import isfile, isdir, dirname, join,realpath

def main(L,v,pdv):
    vars = v[0]
    dotvars = v[1]
    ddvars = v[2]
    const = v[3]
    pvars = pdv[0]
    pddvars = pdv[1]
    #Separa variables en str por ,
    textvars = f.vars2str(vars,dotvars[1],ddvars,const)

    #Inicializa el código
    code = f.initialize(L,vars,dotvars,ddvars,const,textvars)

    #Deriva respecto a vars
    for v in vars:
        code += f.derv(v)
    
    #Si son 0 entonces agregar al caso constantes de mov
    code +='''
constl= []
for eq in derv:
    constl.append(eq == 0)

'''
    for n,dot in enumerate(dotvars[1]):
        const.append(pvars.pop(0))
        const.append(pddvars.pop(0))
        #Separar en caso constante y variable
        code += f'''
d{dot} = simplify(diff(L,{dot}))
const.append('{const[-2]}')
const.append('{const[-1]}')
if constl[{n}]:
'''
        #agregamos caso constante
        code += f.const(L,dot,vars,dotvars[1])

        code += f'''
else:
'''
        #agregamos caso variable
        code += f.var(L,dot,vars,dotvars[1],ddvars,const,pvars,pddvars)

    code +='''
f2.savingequations(equations,constl,vars,dotvars,ddvars,const)
'''

    d = open(join(dirname(realpath(__file__)),'eq.py'), 'w')
    d.write(code)
    d.close()



if __name__ == "__main__":
    #d = l.main(r'\left(1-\frac{1}{r}\right)\dot{t}^{2} - \left(1-\frac{1}{r}\right)^{-1} \dot{r}^{2} - \left(r^{2}\right) \dot{p}^{2}',['r','t','p'])
    #d = l.main(r'\frac{m\dot{r}^{2}}{2} - \frac{mw^{2} r^{2}}{2}',['r'])
    #d = l.main(r'm\frac{\dot{x}^{2}+\dot{y}^{2}}{2} - mgx - \frac{mw^{2} x^{2}}{2}', ['x','y'])
    #d = l.main(r'm\frac{\dot{x}^{2}+x\dot{y}^{2} + x^{2} \dot{z}^{2}}{2} - \frac{mw^{2} x^{2}}{2}', ['x','y','z'])
    d = l.main(r'm\frac{\dot{y}^{2}}{2}- \frac{mw^{2}y^{2}}{2} + \frac{GM}{(x^{2}+(y+b)^{2})^{\frac{1}{2}}}',['y'])
    main(d[0][0],d[1],d[2])


