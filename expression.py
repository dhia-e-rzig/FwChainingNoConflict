import ast
import re
class Expression:
    regex = re.compile(r'(^|,)(\w+)\(')
    reg = re.compile(r'([(,)])')
    def __init__(self,chain):
        if(isinstance(chain,list)):
            self.expression=chain
            return
        chain=chain.replace(" ", "")
        tmp = self.regex.sub(r'\1(#\2,', chain)
        while(tmp!=chain):
            chain=tmp
            tmp = self.regex.sub(r'\1(#\2,', chain)

        if (chain[0] != '('):
            chain = '(' + chain + ')'
        chain = self.reg.sub(r'"\1"', chain)
        chain=chain.replace('""','"').replace('(','[').replace(')',']').replace(']"',']').replace('"[','[')
        self.expression = ast.literal_eval(chain)

    def isAtom(self):
        return (len(self.expression)<=1)

    def isVariable(self):
        return len(self.expression)==1 and '?' in self.expression[0]

    def isFunction(self):
        a=self.expression[0]
        if(isinstance(a,str) and a[0]=='#'):
            return True
        return False

    def separate(self):
        if(isinstance(self.expression[0],list)):
            first = self.expression[0]
        else:
            first = [self.expression[0]]
        queue=self.expression[1:]
        if(len(queue)==1 and isinstance(queue[0],list)):
            queue=queue[0]
        return Expression(first),Expression(queue)

    def __contains__(self, expr):
        tmp = self.expression.__str__()
        return (expr.expression[0] in tmp)

    def __eq__(self, expr):
        return  len(self.expression) == 1 and len(expr.expression)==1 and self.expression[0]==expr.expression[0]


    def substitute(self,subs:list):
        tmp = self.expression.__str__()
        for sub in subs:
            v = "'" + sub[0] + "'"
            s="'"+sub[1]+"'"
            tmp=tmp.replace(v, s)
        tmp=tmp.replace('\'[','[').replace(']\'',']')
        self.expression = ast.literal_eval(tmp)
    def toString(self):
         tmp=self.expression[0][1:]+"("
         for i in self.expression[1:]:
            tmp+=i+","
         tmp=tmp[:len(tmp)-1]+")"
         return tmp


