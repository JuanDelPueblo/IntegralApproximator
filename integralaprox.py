import sympy as sym
from sympy.parsing.sympy_parser import T


class IntegralApproximator:
    def __init__(self, expression, lower_bound, higher_bound, n):
        # Check if expression is valid, otherwise raise exception
        try:
            self.exp = sym.parse_expr(expression, transformations='all')
            self.low = sym.parse_expr(lower_bound)
            self.high = sym.parse_expr(higher_bound)
        except:
            raise Exception("Invalid expression")
        self.n = n
        self.deltax = (self.high - self.low) / self.n

    def trapezoidal_approx(self):
        x = sym.symbols('x')
        sum = 0
        # Calculate sum of function values at each interval end point
        for i in range(0, self.n+1):
            xi = self.low + i*self.deltax
            if i == 0 or i == self.n:
                sum += self.exp.subs(x, xi)
            else:
                sum += 2*self.exp.subs(x, xi)
        return sym.N((self.deltax/2)*sum)

    def trapezoidal_error(self):
        x = sym.symbols('x')
        try:
            snd_dev = sym.diff(self.exp, x, 2)
            k = sym.calculus.maximum(snd_dev, x, sym.Interval(self.low, self.high))
            return sym.N((k*((self.high - self.low)**3))/(12*(self.n**2)))
        except:
            return None

    def midpoint_approx(self):
        x = sym.symbols('x')
        sum = 0
        # Calculate sum of function values at each interval midpoint
        for i in range(1, self.n+1):
            xi = 1/2*((self.low + (i-1)*self.deltax) +
                      (self.low + i*self.deltax))
            sum += self.exp.subs(x, xi)
        return sym.N(self.deltax*sum)

    def midpoint_error(self):
        x = sym.symbols('x')
        try:
            snd_dev = sym.diff(self.exp, x, 2)
            k = sym.calculus.maximum(snd_dev, x, sym.Interval(self.low, self.high))
            return sym.N((k*((self.high - self.low)**3))/(24*(self.n**2)))
        except:
            return None

    def simpsons_approx(self):
        x = sym.symbols('x')
        sum = 0
        if self.n % 2 != 0:
            return None
        # Calculate sum of function values at each interval end point and midpoint
        for i in range(0, self.n+1):
            xi = self.low + i*self.deltax
            if i == 0 or i == self.n:
                sum += self.exp.subs(x, xi)
            elif i % 2 == 0:
                sum += 2*self.exp.subs(x, xi)
            else:
                sum += 4*self.exp.subs(x, xi)
        return sym.N((self.deltax/3)*sum)

    def simpsons_error(self):
        x = sym.symbols('x')
        if self.n % 2 != 0:
            return None
        try:
            fourth_dev = sym.diff(self.exp, x, 4)
            k = sym.calculus.maximum(
                fourth_dev, x, sym.Interval(self.low, self.high))
            return sym.N((k*((self.high - self.low)**5))/(180*(self.n**4)))
        except:
            return None

    def definite_integral_calc(self):
        x = sym.symbols('x')
        try:
            return sym.N(sym.integrate(self.exp, (x, self.low, self.high)))
        except:
            return None

    def calc_all(self):
        return {"-DEFINITE-": self.definite_integral_calc(), "-TRAPEZOIDAL-": self.trapezoidal_approx(),
                "-MIDPOINT-": self.midpoint_approx(), "-SIMPSON-": self.simpsons_approx()}

    def calc_error(self):
        return {"-DEFINITE_ERROR-": 0, "-TRAPEZOIDAL_ERROR-": self.trapezoidal_error(),
                "-MIDPOINT_ERROR-": self.midpoint_error(), "-SIMPSON_ERROR-": self.simpsons_error()}
