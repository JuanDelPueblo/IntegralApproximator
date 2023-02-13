import sympy as sym

class IntegralApproximator:
    def __init__(self, expression, lower_bound, higher_bound, n):
        try:
            self.exp = sym.sympify(expression, evaluate=False)
        except:
            raise Exception("Invalid expression")
        self.low = lower_bound
        self.high = higher_bound
        self.n = n
        self.deltax = (self.high - self.low) / self.n

    def trapezoidal_approx(self):
        x = sym.symbols('x')
        sum = 0
        for i in range(0, self.n+1):
            xi = self.low + i*self.deltax
            if i == 0 or i == self.n:
                sum += self.exp.subs(x, xi)
            else:
                sum += 2*self.exp.subs(x, xi)
        return (self.deltax/2)*sum
    
    def trapezoidal_error(self):
        x = sym.symbols('x')
        snd_dev = sym.diff(self.exp, x, 2)
        k = sym.calculus.maximum(snd_dev, x, sym.Interval(self.low, self.high))
        return ((k*((self.high - self.low)**3))/(12*(self.n**2)))

    def midpoint_approx(self):
        x = sym.symbols('x')
        sum = 0
        for i in range(1, self.n+1):
            xi = 1/2*((self.low + (i-1)*self.deltax) + (self.low + i*self.deltax))
            sum += self.exp.subs(x, xi)
        return self.deltax*sum

    def midpoint_error(self):
        x = sym.symbols('x')
        snd_dev = sym.diff(self.exp, x, 2)
        k = sym.calculus.maximum(snd_dev, x, sym.Interval(self.low, self.high))
        return ((k*((self.high - self.low)**3))/(24*(self.n**2)))

    def simpsons_approx(self):
        x = sym.symbols('x')
        sum = 0
        if self.n % 2 != 0:
            return "N must be even"
        for i in range(0, self.n+1):
            xi = self.low + i*self.deltax
            if i == 0 or i == self.n:
                sum += self.exp.subs(x, xi)
            elif i % 2 == 0:
                sum += 2*self.exp.subs(x, xi)
            else:
                sum += 4*self.exp.subs(x, xi)
        return (self.deltax/3)*sum

    def simpsons_error(self):
        x = sym.symbols('x')
        fourth_dev = sym.diff(self.exp, x, 4)
        k = sym.calculus.maximum(fourth_dev, x, sym.Interval(self.low, self.high))
        return ((k*((self.high - self.low)**5))/(180*(self.n**4)))
    
    def definite_integral_calc(self):
        x = sym.symbols('x')
        return sym.integrate(self.exp, (x, self.low, self.high))

    def calc_all(self):
        return {"-DEFINITE-": self.definite_integral_calc(), "-TRAPEZOIDAL-": self.trapezoidal_approx(),
                "-MIDPOINT-": self.midpoint_approx(), "-SIMPSON-": self.simpsons_approx()}

    def calc_error(self):
        return {"-DEFINITE_ERROR-": "N/A", "-TRAPEZOIDAL_ERROR-": self.trapezoidal_error(),
                "-MIDPOINT_ERROR-": self.midpoint_error(), "-SIMPSON_ERROR-": self.simpsons_error()}


