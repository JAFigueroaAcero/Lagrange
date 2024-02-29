import funclatexstr as f
import funcstrform as f2
import funcdisc as f3
from os.path import isfile, isdir, dirname, join,realpath


def main():

    eq,vars,dotvars,ddvars,const = f3.get()

    ceq,nceq = f3.getc(eq,dotvars)

    for n,e in enumerate(nceq[0]):
        for m,v in enumerate(ceq[1]):
            e = e.replace(f'{v}',f'({ceq[0][m]})')
            nceq[0][n] = e
    print(nceq)
    print(ceq)

    loc = []

    for eq in nceq[0]:
        loc.append(f3.pow(eq))
    nceq[0] = loc
    loc = []
    for eq in ceq[0]:
        loc.append(f3.pow(eq))
    ceq[0] = loc

    code,i,disvars = f3.initialize(ceq,nceq,vars,dotvars,ddvars,const,10,8,0.01,'t',[[0,0,0],['A','a','st']],[[0 for v in const],const])

    code += f3.frkv()
    code += f3.sum(i)
    code += f3.fsumrkv()
    code += f3.save(disvars,vars,dotvars,ddvars,dirname(realpath(__file__)),'try')

    code += f3.setmain(disvars)


    input(f'here{ceq},{nceq}')
    ceq,nceq = f3.discretize2(ceq,nceq,disvars,vars,dotvars)

    input(f'{ceq},{nceq}')
    code += f3.mainfor(disvars,i,ceq,nceq)
    code += f3.end()
    d = open(join(dirname(realpath(__file__)),'data.cpp'),'w')
    d.write(code)
    d.close()

if __name__ == "__main__":
    main()

#Compile with clang++ data.cpp -o data
    

#To do: Agregar un estimado de tiempo de simulación dependiendo de t y dt