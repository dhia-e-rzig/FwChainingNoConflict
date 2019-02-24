from expression import Expression

def unifier_atom(expr1:Expression,expr2:Expression):
    if(expr2.isAtom()):
        expr1,expr2=expr2,expr1

    if(expr1==expr2):
        return {}

    if(expr2.isVariable()):
        expr1,expr2 = expr2,expr1

    if(expr1.isVariable()):#1 seul element + contains "?"
        if(expr1 in expr2):
            return None
        if (expr2.isAtom()):
           return [[expr1.expression[0],expr2.expression[0]]]
        if(expr2.isFunction()):
            return [[expr1.expression[0],expr2.expression.__str__()]]

    return None

def unifier(terms1:Expression,terms2:Expression):
    if(terms1.isAtom() or terms2.isAtom()):
        return unifier_atom(terms1,terms2)

    F1,T1=terms1.separate()
    F2,T2=terms2.separate()


    Z1=unifier(F1,F2)
    if(Z1==None):
        return None

    T1.substitute(Z1)
    T2.substitute(Z1)


    Z2=unifier(T1,T2)

    if(Z2==None):
        return None
    Z2=list(Z2)
    Z2+=Z1
    return Z2
