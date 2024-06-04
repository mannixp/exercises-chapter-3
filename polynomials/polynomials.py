from numbers import Number
import numpy as np

def derivative(f):

    if isinstance(f,Polynomial):
        return f.dx() 
    else:
        return NotImplemented

class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other


    def __sub__(self, other):

        if isinstance(other, Polynomial):
            # Work out how many coefficients they have in common
            common = min(self.degree(), other.degree()) + 1
            
            # subtract the common coefficients
            coefs  = tuple(a - b for a, b in zip(self.coefficients,other.coefficients))
            
            # append the higher degree coefficients
            coefs += self.coefficients[common:] + tuple(-b for b in other.coefficients[common:])
            
            return Polynomial(coefs)
            
        elif isinstance(other, Number):
            # subtract the number from the lowest cofficient + append other coefficients
            print(Polynomial((self.coefficients[0] - other,) + self.coefficients[1:]))
            return Polynomial((self.coefficients[0] - other,) + self.coefficients[1:])
            
        else:
            return NotImplemented

    def __rsub__(self, other):
        
        if isinstance(other, Polynomial):
            # Work out how many coefficients they have in common
            common = min(self.degree(), other.degree()) + 1
            
            # subtract the common coefficients
            coefs  = tuple(-a + b for a, b in zip(self.coefficients,other.coefficients))
            
            # append the higher degree coefficients
            coefs += tuple(-a for a in self.coefficients[common:]) + self.coefficients[common:]
            
            return Polynomial(coefs)
            
        elif isinstance(other, Number):
            
            # subtract the number from the lowest cofficient + append other coefficients
            return Polynomial((other - self.coefficients[0],) + tuple(-a for a in self.coefficients[1:]) )
            
        else:
            return NotImplemented
    
    def __mul__(self,other):

        if isinstance(other, Polynomial):

            coefs = np.zeros(self.degree() + other.degree() + 1)
            for i,a in enumerate(self.coefficients):    
                for j,b in enumerate(other.coefficients):
                    coefs[i+j] += a*b

            return Polynomial(tuple(coefs))

        elif isinstance(other, Number):

            coefs = tuple(other*a for a in self.coefficients)
            return Polynomial(coefs)

        else:
            return NotImplemented

    def __rmul__(self,other):
        return self * other        

    def __pow__(self,other):

        if   other == 0:
            return Polynomial(tuple(1))
        
        else:
            fp = Polynomial(self.coefficients)
            for i in range(other-1):
                fp = self * fp
        return fp
    
    def __call__(self,x):

        f = 0.
        for i,a in enumerate(self.coefficients):
            f+= a * x**i
        
        return f

    def dx(self):

        if self.degree() == 0:
            return Polynomial((0,))
        else:
            coefs = np.zeros(self.degree())
            for i,a in enumerate(self.coefficients):
                
                if i==1:
                    coefs[0] = a
                elif (i>1) and (i != 0):
                    coefs[i-1] = a*i
            
            return Polynomial(tuple(coefs))