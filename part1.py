from unification import *
from expression import *

class Display:

    def formatFunctionOutput(self, input):
        temp = str(input).split(',')
        toReturn=''
        # print(s)
        i = 0
        for c in temp:
            if '[' in c:
                toReturn+=c.split('[')[1].replace('\'', '')+'('
                i = i + 1
            elif ']' in c:
                toReturn+=c.split(']')[0].replace('\'', '')
                for i in range(0, i):
                    toReturn+=(')')
            else:
               toReturn+=c.replace('\'', '')+ ','
        return toReturn

    def unify(self, exp1, exp2):
        d = unifier(exp1, exp2)
        print(type(d))
        toReturn=''
        if d is None or len(d)==0:
           toReturn+=("Unification impossible")
           return toReturn
        for key, value in d:
            if ']' in str(value):
                toReturn+='('+str(key)+'/ '
                toReturn+= self.formatFunctionOutput(str(value))
                toReturn+=')'
            else:
                toReturn+='('+str(key)+'/'+str(value)+')'

        print('\n')
        return toReturn



fin=open("input.txt","r")
fout = open("traceUnification.log",'a')

x=input("choisir mode : 1 --> depuis fichier input txt , 2 -- > saisie \n")
if(int(x)==1):
    line=fin.readline()
    line=fin.readline()
    while line:
        expr1=line.split('--')[0].replace('\n', '')
        expr2=line.split('--')[1].replace('\n', '')
        e1=Expression(expr1)
        e2=Expression(expr2)
        result=Display().unify(e1,e2)
        print(result)
        fout.write("unifier("+expr1+","+expr2+") == "+str(result)+"\n")
        line=fin.readline()
else :
    expr1=input('Entrer la prémière expression :')
    expr2=input('Entrer la deuxiéme expression :')
    e1=Expression(expr1)
    e2=Expression(expr2)
    result=Display().unify(e1,e2)
    print(result)
    fout.write("unifier("+expr1+","+expr2+") == "+str(result)+"\n")
