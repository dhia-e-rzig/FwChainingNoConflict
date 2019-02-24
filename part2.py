from unification import *
from Classes import *
import os

fout=open("trace.txt","w")

base_faits=[]
base_regles=[]


def read_BF(fichier):
    bc = open(fichier, "r")
    str = bc.read()
    faits = str.rstrip().split(', ')
    for f in faits:
        fait = Fait(f.strip())
        base_faits.append(fait)

def read_BR(fichier):
    bc = open(fichier, "r")
    str = bc.read()
    regles = str.rstrip().split('\n')
    i = 0
    for r in regles:
        regle = Regle()
        regle.id=i
        regle.conclusion = r.split(" :- ")[0].strip()
        premisses = r.split(" :- ")[1].split("),")
        premisses_1 = []
        for pre in premisses:
            pre = pre.strip()
            if pre != '':
                pre+=')'
                premisses_1.append(pre)
        regle.premisses = premisses_1
        base_regles.append(regle)
        i+=1


def unifierPremisses(prems, i, unif, unifications):
    if i<len(prems):
        e1=Expression(prems[i])
        for u in unif:
            e1.substitute(u)
        for fact in base_faits:
            e2=Expression(fact.fait)
            for u in unif:
                e2.substitute(u)
            test=unifier(e1,e2)

            if test is not None:
                unifCopy=unif[:]
                unifCopy.append(test)
                unifierPremisses(prems, i + 1, unifCopy, unifications)
    else:
         unifications.append(unif)
    return unifications


def evalSiRegleDeclanchable(regles):
    prems=regles.premisses
    # nbprem=len(prems)
    # for i in prems:
    #     fait.append(0)
    unif=[]
    unifications=unifierPremisses(prems, 0, unif, [])
    if len(unifications)>0:
        return [True,unifications]
    else:
        return [False, unifications]

def unifierConclusion(unifications, regle):
    e1=Expression(regle.conclusion)
    for u in unifications:
        e1.substitute(u)
    return e1.toString()






def Chainage_Avant_Sans_Conflit(but):
    Bi=list()
    for i in base_faits:
        if "?" not in but:
            if but == i.fait:
                print(but+" est Trouve dans la base de faits")
                fout.write(str(but+" est Trouve dans la base de faits"))
                fout.write("\n")
                return
        elif(unifier(Expression(but),Expression(i.fait))):
            print("but trouvé dans la base de faits initiales "+i.fait)
            fout.write(str("but trouvé dans la base de faits initiales "+i.fait))
            fout.write("\n")
            Bi.append(i)
    notDone=True
    Traces = []
    brCopy = base_regles.copy()
    lastMatchIndex=0
    while notDone:
        notDone = False
        i = 0
        while i < len(brCopy):
            unifs = evalSiRegleDeclanchable(brCopy[i])
            if unifs[0]:
                regle = brCopy[i]
                del (brCopy[i])
                for u in unifs[1]:
                    c = unifierConclusion(u, regle)
                    if c[0] == '!':
                        nonC = c[1:]
                    else:
                        nonC = '!' + c
                    if nonC in base_faits:
                        return False
                    else:
                        base_faits.append(Fait(c))
                    Traces.append(regle)
                    Traces.append(u)
                    Traces.append(c)
                    if unifier(Expression(but),Expression(c)):# marquer dernier endroit ou match  trouvée
                        lastMatchIndex=i
                    if "?" not in but and "?" not in c: # arreter éxecution lorsque but trouvée
                        if(but == c):
                            notDone=False
                            lastMatchIndex=i
                        else:
                            notDone=True
                    else:
                        notDone = True
            else:
                i = i + 1

    nouveauTrouvee=False
    for i in base_faits:
        if unifier(Expression(but),Expression(i.fait)) and i not in Bi:
            print("nouveaux buts trouvé dans la base de faits finale "+i.fait)
            fout.write(str("nouveaux buts trouvé dans la base de faits finale "+i.fait))
            fout.write("\n")
            nouveauTrouvee=True
    if not nouveauTrouvee and len(Bi)==0:
        print("Aucun but trouvée dans la base de faits")
        fout.write(str("Aucun but trouvée dans la base de faits"))
        fout.write("\n")
    elif not nouveauTrouvee:
        print("Aucun nouveau but trouvée dans la base de faits")
        fout.write(str("Aucun nouveau but trouvée dans la base de faits"))
        fout.write("\n")
    print("Trace d'éxecution")
    fout.write("Trace d'éxecution")
    fout.write("\n")
    j=0
    end=len(Traces)- 2
    if(lastMatchIndex!=0):
        end = lastMatchIndex
    while j<end:
        print()
        print('\033[1m'+"Regle"+ str(Traces[j])+ '\033[0m')
        fout.write(str('\033[1m'+"Regle"+ str(Traces[j])+ '\033[0m'))
        fout.write("\n")
        print('\033[4m'+"Avec les unifications suivantes: "+'\033[0m')
        fout.write(str('\033[4m'+"Avec les unifications suivantes: "+'\033[0m'))
        fout.write("\n")
        for subs in Traces[j+1]:
            for sub in subs:
                print("(",sub[0],"/",sub[1],") ")
                fout.write(str("("+sub[0]+"/"+sub[1]+") "))
                fout.write("\n")
        print('\033[92m'+"Fait ajouté a la base de fait: " + '\033[0m'+'\033[92m'+Traces[j+2])
        fout.write('\033[92m'+"Fait ajouté a la base de fait: " + '\033[0m'+'\033[92m'+Traces[j+2])
        fout.write("\n")
        j+=3
        print()
        fout.write("\n")
    print('\033[94m'+"Base de fait finale: "+'\033[0m')
    fout.write('\033[94m'+"Base de fait finale: "+'\033[0m')
    fout.write("\n")
    for i in base_faits:
        print(i.fait)
        fout.write(i.fait)
        fout.write("\n")


fichierbf=input("entrer le nom de fichier BF(BF.txt est fournie par défaut)")
fichierbr=input("entrer le nom de fichier BR(BR1.txt et BR2.txt est fournie par défaut)")
read_BF(fichierbf)
read_BR(fichierbr)
but=input("entrer le but à atteindre")
Chainage_Avant_Sans_Conflit(but)
sauvegarder=input("Voulez vous sauveagarder la trace ? o=oui, n = non")
if(sauvegarder == "n"):
    os.remove("trace.txt")


