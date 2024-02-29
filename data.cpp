
#define _USE_MATH_DEFINES
#define lenght 10000001

#include <stdio.h>
#include <cmath>
#include <iostream>
#include <fstream>

const int rkd = 4;

const int a = 0;
const int A = 1;
const int b = 2;
const int B = 3;

const int st = 4;

const double tm = 1000;
const double dst = 0.0001;
const double A0 = 0;
const double a0 = 100;
const double b0 = 1000;
const double B0 = 0;
const double st0 = 0;

const double m = 10;
const double w = 10;
const double G = 6.672*pow(10,-11);
const double M = 5.97*pow(10,24);
const double x = 400000;
const double c = 0;
const double C = 0;

double* rkv;
double sumrkv;

double rkl[rkd+1][5];
double* rki;

double va[lenght][5];
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

double sum(double rkl[rkd+1][5], double* rkv,int i){
    double v = 0;
    for (int j = 0; j < rkd; j++){
        v += rkv[j] * rkl[j+1][i];
    }
    return v;
}

double fsumrkv(double* rkv){
    int v = 0;
    for (int i = 0; i < rkd; i++){
        v += rkv[i];
    }
    return v;
}

void save(int breaking)
{
    std::ofstream outfile ("/Users/juan_antonio/Documents/UDG/Relatividad/27124//try2.csv");

    outfile << "y',y,o,o',st" << std::endl;
    int i = 0;
    if (breaking == 0){
        i = lenght;
    }
    else{
        i = breaking;
    }
    for (int j = 0; j < i; j++){
        outfile << std::to_string(va[j][A]) <<  "," << std::to_string(va[j][a]) <<  "," << std::to_string(va[j][b]) << "," << std::to_string(va[j][B]) << "," << std::to_string(va[j][st]) <<   std::endl;
    }
    outfile.close();
}
int main(){

    double Ak;
    double ak;
    double bk;
    double Bk;
    double stk;
    rkv = frkv();
    sumrkv = fsumrkv(rkv);
    va[0][A] = A0;
    va[0][a] = a0;
    va[0][B] = B0;
    va[0][b] = b0;
    va[0][st] = st0;

 int breaking = 0;


    for (int i = 0; i < lenght; i++){
        Ak = va[i][A];
        ak = va[i][a];
        bk = va[i][b];
        Bk = va[i][B];
        stk = va[i][st];

        for (int n = 0; n < rkd; n++){
            for (int j = 0; j < 3; j++){
                rkl[n][j] = 0;
            }
        }

        for (int n = 0; n<rkd;n++){
            rki = rkl[n+1];
            rki[A] = ((-1.0*G*m*M*((bk + (rkl[n][b])/rkv[n])+(ak + (rkl[n][a])/rkv[n]))-m*pow(w,2)*(ak + (rkl[n][a])/rkv[n])*pow(pow(x,2)+pow((bk + (rkl[n][b])/rkv[n])+(ak + (rkl[n][a])/rkv[n]),2),1.5))/(m*pow(pow(x,2)+pow((bk + (rkl[n][b])/rkv[n])+(ak + (rkl[n][a])/rkv[n]),2),1.5))) * dst;
            rki[a] = ((Ak + (rkl[n][A])/rkv[n])) * dst;
            rki[st] = rkl[n][st] + dst;

            rki[B] = (((-1.0*G*m*M*((bk + (rkl[n][b])/rkv[n]))))/(m*pow(pow(x,2)+pow((bk + (rkl[n][b])/rkv[n]),2),1.5))) * dst;
            rki[b] = ((Bk + (rkl[n][B])/rkv[n])) * dst;

        }
        va[i+1][A] = Ak + sum(rkl,rkv,A)/sumrkv;
        va[i+1][a] = ak + sum(rkl,rkv,a)/sumrkv;
        va[i+1][B] = Bk + sum(rkl,rkv,B)/sumrkv;
        va[i+1][b] = bk + sum(rkl,rkv,b)/sumrkv;

        va[i+1][st] = va[i][st] + dst;
    }
    save(breaking);
}