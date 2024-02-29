import funclatexstr as f

def main(L,vars):
    '''
    Dado un lagrangiano lo convierte a str y retorna sus datos

    [Lloc,Llist],[vars,dotvars,ddvars,const],[pvars,pddvars]

    Lloc: Términos separados parentesis
    Llist: Terminos separados por lista
    vars: Variables usadas
    dotvars: Variables derivadas
    ddvars: Variables derivadas 2
    const: Constantes usadas
    pvars: Posibles variables
    pddvars: Posibles variables derivadas 2

    '''
    L = f.replaceminus(L.replace("\\left", '').replace("\\right", '').replace(' ',''))

    pvars = list('abcdefghijklmnopqrstuvwxyz')
    pddvars = list('abcdefghijklmnopqrstuvwxyz'.upper())

    const = []

    #actualizar variables con vars
    pvars, pddvars = f.updatevars(pvars,pddvars,vars)


    #agregar constantes
    Lp = L.replace('\\dot', '').replace('\\frac','')

    print('Lp',Lp)
    for t in Lp:
        if t in pvars or t in pddvars:
            if not t in const:
                const.append(t)
    print(const)
    #actualizar variables con const
    pvars, pddvars = f.updatevars(pvars,pddvars,const)

    #Crear dot y dd vars
    pvars, pddvars,L,dotvars,ddvars = f.adddotvars(vars,pvars,pddvars,L)

    #eliminar \\frac{a}{b} y crear (a)/(b)
    L = f.creatediv(L)
    print('div',L)

    #eliminar b^{a} y agrega (b)**(a)
    L = f.createpow(L)

    #separa multiplicaciones de variables
    L = f.sepmult(L)

    #remplaza )( por )*(
    L = f.addmult(L)
    print(L)
    return list(f.createbrackets(L)),[vars,dotvars,ddvars,const],[pvars,pddvars]

if __name__ == "__main__":
    print(main(r'\left(1-\frac{1}{r}\right)\dot{t}^{2} - \left(1-\frac{1}{r}\right)^{-1} \dot{r}^{2} - \left(r^{2}\right) \dot{p}^{2}',['r','t','p']))

