import funclatexstr as f
import funcstrform as f2
import pandas as pd
from os.path import isfile, isdir, dirname, join,realpath


letters = 'abcdefghijklmnopqrstuvwxyz'

def get():
    df = pd.read_csv(join(dirname(realpath(__file__)),f'data.csv'), index_col = 0)
    indexes = df.index.tolist()
    equationsI = indexes[0:-1]
    eq = [df.equation[e] for e in equationsI]
    const = list(df.equation['const'][2:-2].replace('\'','').replace(',','').replace(' ',''))
    vars = df.loc[equationsI,'var'].tolist()
    dotvars = df.loc[equationsI,'dotvar'].tolist()
    ddvars = df.loc[equationsI,'ddvar'].tolist()
    return eq,vars,dotvars,ddvars,const


def getc(eq,dotvars):
    ceq = []
    nceq = []
    vc = []
    nvc = []
    for e in eq:
        if e[0] in dotvars:
            ceq.append(e[2::])
            vc.append(e[0])
        else:
            nceq.append(e[2::])
            nvc.append(e[0])
    return [ceq,vc], [nceq,nvc]


def pow(eq):
    while '**' in eq:
        i = eq.index('**')
        lb = 0
        rb = 0

        eqp = eq[0:i][::-1]

        eqp2 = eq[i+2::]
        powing = ''
        l = 0
        #print(eq)

        print('eqp2',eqp2)
        for n,v in enumerate(eqp2):
            if v == '(':
                lb += 1
            elif v == ')':
                rb += 1
            
            if lb == rb:
                if lb != 0:
                    powing = eqp2[1:n]
                    l = len(powing)
                    
                else:
                    input(f'hereing, {eqp2[0:n+1]}')
                    for n,v2 in enumerate(eqp2):
                        if not v2.isnumeric() and v2 != '.':
                            powing = eqp2[0:n]
                            break
                    l = len(powing)-1

                print(f'powing, {powing}')
                break
        print('broke')
        lb = 0
        rb = 0
        for n,v in enumerate(eqp):
            #print(eqp[0:n+1])
            if v == '(':
                lb += 1
            elif v == ')':
                rb += 1
            
            if lb == rb:
                if lb != 0:
                    v = eqp[1:n][::-1]
                    eq = eq[0:i-n-1] + f"pow({v},{powing})" + eq[i+3+l::]
                    #input(f'case1 {eq[0:i-n]}')
                    
                else:
                    v = eqp[0:1][::-1]
                    eq = eq[0:i-1] + f"pow({v},{powing})" + eq[i+3+l::]
                    #input(f'case2 {eq[0:i-1]}')
                break
        input(f'eq,{eq}')

    return eq




def initialize(ceq,nceq,vars,dotvars,ddvars,const,t,rkd,dt,tvar,i0,Cv):
    code =f'''
#define _USE_MATH_DEFINES
#define lenght {int((t + dt)/dt)}

#include <stdio.h>
#include <cmath>
#include <iostream>
#include <fstream>

const int rkd = {rkd};

'''
    i = 0
    disvars = []
    for v in ceq[1]:
        code += f'''const int {v} = {i};
'''
        i += 1
        disvars.append(v)
    for v in nceq[1]:
        code += f'''const int {v.lower()} = {i};
const int {v} = {i+1};
'''
        i += 2
        disvars.append(v)
        disvars.append(v.lower())
    code += f'''
const int s{tvar} = {i};

const double {tvar}m = {t};
const double ds{tvar} = {dt};
'''
    disvars.append(f's{tvar}')
    i += 1
    for n,v in enumerate(disvars):
        code += f'''const double {v}0 = {i0[0][i0[1].index(v)]};
'''
    code += '\n'
    for n,c in enumerate(const):
        code += f'''const double {c} = {Cv[0][Cv[1].index(c)]};
'''
    code += '\ndouble* rkv;\ndouble sumrkv;'

    code += f'\n\ndouble rkl[rkd+1][{i}];\ndouble* rki;'

    code += f'\n\ndouble va[lenght][{i}];'
    return code, i, disvars

def frkv():
    return '''
double* frkv(){
    static double rkv[rkd];
    *rkv = 1;
    *(rkv+(rkd-1)) = 1;
    for (int i = 1; i < rkd-1; i++){
        *(rkv+i) = 2;
    }
    for (int i = 0; i < rkd; i++){
        printf("%lf,",rkv[i]);
    }
    return rkv;
}
'''

def sum(i):
    return f'''
double sum(double rkl[rkd+1][{i}], double* rkv,int i){{
    double v = 0;
    for (int j = 0; j < rkd; j++){{
        v += rkv[j] * rkl[j+1][i];
    }}
    return v;
}}
'''

def fsumrkv():
    return '''
double fsumrkv(double* rkv){
    int v = 0;
    for (int i = 0; i < rkd; i++){
        v += rkv[i];
    }
    return v;
}
'''

def save(disvars,vars,dotvars,ddvars,path,name):
    code = f'''
void save(int breaking)
{{
    std::ofstream outfile ("{path}//{name}.csv");
'''
    lvars = []
    for v in disvars:
        if v in ddvars:
            i = ddvars.index(v)
            lvars.append(dotvars[i])
        elif v in dotvars:
            i = dotvars.index(v)
            lvars.append(vars[i])
        else:
            lvars.append(v)
    t = ''
    t2 = ''
    #input(f'lvars, {lvars}')
    for n,v in enumerate(lvars):
        if v in dotvars:
            loc = vars[dotvars.index(v)] + "'"
        else:
            loc = v
        t += f'{loc},'
        t2 += f'<< std::to_string(va[j][{disvars[n]}]) <<  "," '
    t = t[0:-1]
    t2 = t2[0:-4]
    #input(f'{t},{t2}')
    code += f'''
    outfile << \"{t}\" << std::endl;
    int i = 0;
    if (breaking == 0){{
        i = lenght;
    }}
    else{{
        i = breaking;
    }}
    for (int j = 0; j < i; j++){{
        outfile {t2} std::endl;
    }}
    outfile.close();
}}
'''
    return code


def breakingcond():
    return ''

def setmain(disvars):
    code = 'int main(){\n'

    for v in disvars:
        code += f'''
    double {v}k;'''
    code += '''
    rkv = frkv();
    sumrkv = fsumrkv(rkv);
'''

    for v in disvars:
        code += f'''    va[0][{v}] = {v}0;\n'''
    
    code += '\n int breaking = 0;\n\n'

    return code

def mainfor(disvars,i,ceq,nceq):
    code = '''
    for (int i = 0; i < lenght; i++){
'''
    code += breakingcond()

    for v in disvars:
        code +=f'''        {v}k = va[i][{v}];\n'''

    code += f'''
        for (int n = 0; n < rkd; n++){{
            for (int j = 0; j < {i}; j++){{
                rkl[n][j] = 0;
            }}
        }}
'''
    code += '''
        for (int n = 0; n<rkd;n++){
            rki = rkl[n+1];
'''
    for v in disvars:
        if v in ceq[1]:
            code += f'''            rki[{v}] = ({ceq[0][ceq[1].index(v)]}) * d{disvars[-1]};\n'''
        elif v in nceq[1]:
            code += f'''            rki[{v}] = ({nceq[0][nceq[1].index(v)]}) * d{disvars[-1]};\n'''
        else:
            code += f'''            rki[{v}] = rkl[n][{disvars[-1]}] + d{disvars[-1]};\n'''
    code += '        }\n'
    
    for v in disvars[0:-1]:
        code += f'''        va[i+1][{v}] = {v}k + sum(rkl,rkv,{v})/sumrkv;\n'''
    code += f'        va[i+1][{disvars[-1]}] = va[i][{disvars[-1]}] + d{disvars[-1]};\n    }}\n'
    return code

def end():
    return '    save(breaking);\n}'

def discretize(ceq,nceq,disvars,vars,dotvars):
    for v in disvars:
        if v in nceq[1]:
            ceq[0].append(v.lower())
            ceq[1].append(v.lower())
    input(f'ceq,{ceq}')
    for n,v in enumerate(ceq[0]):
        loc = v
        for var in disvars:
            if var in ceq[1]:
                input(f'{var} {ceq[1]}')
                change = vars[dotvars.index(var)]
                loc = loc.replace(f'{change}',f'({var}k + (rkl[n][{var}])/rkv[n])')
                input(f'v{var}, {loc}')
            elif var in nceq[1]:
                loc = loc.replace(f'{var.lower()}',f'({var}k + (rkl[n][{var}])/rkv[n])')
                input(f'v{var}, {loc}')

        
        ceq[0][n] = loc
    for n,v in enumerate(nceq[0]):
        loc = v
        for var in disvars:
            if var in ceq[1]:
                change = vars[dotvars.index(var)]
                loc = loc.replace(f'{change}',f'({var}k + (rkl[n][{var}])/rkv[n])')
            else:
                loc = loc.replace(f'{var.lower()}',f'({var}k + (rkl[n][{var}])/rkv[n])')
        nceq[0][n] = loc
    return ceq,nceq


def discretize2(ceq,nceq,disvars,vars,dotvars):
    for v in disvars:
        if v in nceq[1]:
            ceq[0].append(v.lower())
            ceq[1].append(v.lower())
    input(f'ceq,{ceq}')

    print(f'disvars, {disvars}')
    for n,v in enumerate(ceq[0]):
        loc = v
        input(f'locking, {loc}')
        
        for var in disvars+vars:
            j = -1
            print(f'var2,{var}')
            while True:
                j+=1
                if j >= len(loc):
                    print('byebye')
                    break
                elif loc[j] == var:
                    input(f'varing, {j}, {loc}, {loc[j]}, {len(loc)}')
                    if j != 0:
                        if loc[j-1] in 'rkl[n]':
                            continue
                    if j < len(loc)-1:
                        print('upi')
                        if loc[j+1] in 'rkl[n]':
                            print('yup')
                            continue
                        print('notworking')
                    if var == 'k':
                        if j != 0:
                            if loc[j-1] in letters:
                                continue
                    print('here')
                    if var in ceq[1]:
                        print('here2')
                        loc = loc[0:j] + f'({var.upper()}k + (rkl[n][{var.upper()}])/rkv[n])' + loc[j+1::]
                        print(loc)
                        j += len(f'({var.upper()}k + (rkl[n][{var.upper()}])/rkv[n])')

                        print('try',loc[0:j])
                    elif var in vars:
                        print('here3')
                        change = dotvars[vars.index(var)]
                        loc = loc[0:j] + f'({change}k + (rkl[n][{change}])/rkv[n])' + loc[j+1::]
                        j += len(f'({var.upper()}k + (rkl[n][{var.upper()}])/rkv[n])')

        ceq[0][n] = loc

    for n,v in enumerate(nceq[0]):
        loc = v
        input(f'locking, {loc}')
        
        for var in disvars+vars:
            j = -1
            print(f'var2,{var}')
            while True:
                j+=1
                if j >= len(loc):
                    print('byebye')
                    break
                elif loc[j] == var:
                    input(f'varing, {j}, {loc}, {loc[j]}, {len(loc)}')
                    if j != 0:
                        if loc[j-1] in 'rkl[n]':
                            continue
                    if j < len(loc)-1:
                        print('upi')
                        if loc[j+1] in 'rkl[n]':
                            print('yup')
                            continue
                        print('notworking')
                    if var == 'k':
                        if j != 0:
                            if loc[j-1] in letters:
                                continue
                    print('here')
                    if var in ceq[1]:
                        print('here2')
                        loc = loc[0:j] + f'({var.upper()}k + (rkl[n][{var.upper()}])/rkv[n])' + loc[j+1::]
                        print(loc)
                        j += len(f'({var.upper()}k + (rkl[n][{var.upper()}])/rkv[n])')

                        print('try',loc[0:j])
                    elif var in vars:
                        print('here3')
                        change = dotvars[vars.index(var)]
                        loc = loc[0:j] + f'({change}k + (rkl[n][{change}])/rkv[n])' + loc[j+1::]
                        j += len(f'({var.upper()}k + (rkl[n][{var.upper()}])/rkv[n])')

        nceq[0][n] = loc
    return ceq,nceq