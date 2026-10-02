class RootResult:
    def __init__(self, root, history, iterations, error, converged, message=None):
        self.root = root
        self.history = history
        self.iterations = iterations
        self.error = error
        self.converged = converged
        self.message = message

    def __str__(self):
        return(
            f"root={self.root}\n"
            f"iterations={self.iterations}\n"
            f"error={self.error}\n"
            f"converged={self.converged}\n"
            f"message={self.message}"
        )

def bisection (f, xl, xu, es, maxloop):
    ''' parameters (5):

    f= the function, defined externally 
    xl= initial lower bound guess
    xu= initial upper bound guess
    es= error tolerance
    maxloop = maximum number of iterations

    functionality: this function uses the bracketing method bisection in order to find roots of a funciton
    return: none'''
    loop = 1
    ea = es +1 
    history = [] 
    xr = 0 

    if f(xl)*f(xu) > 0:
        return RootResult(
                root=None,
                history=history,
                iterations=0,
                error=None,
                converged=False,
                message="no sign change in interval"
        )
    

    while ea > es and loop <= maxloop:
        oldxr = xr 
        fl = f(xl)
        xr = (xl+xu)/2
        fr = f(xr)
        if loop == 1: 
            ea = float("inf")
        else:
            ea = abs ((xr - oldxr)/xr ) * 100
        history.append({
            "iteration": loop, 
            "xr": xr, 
            "f(xr)": fr, 
            "approx_error": ea
        })
        if fl*fr < 0:
            xu = xr 
        elif fl*fr > 0:
            xl = xr
        elif abs(fr) < 1e-15:
            return RootResult(
                root=xr,
                history=history,
                iterations=loop,
                error=ea,
                converged=True,
                message="exact root found"
            )
        loop += 1
    
    return RootResult(
        root=xr, 
        history=history, 
        iterations=loop-1, 
        error=ea, 
        converged=(ea <= es)
        )

def false_position(f, xl, xu, es, maxloop):
    ''' parameters (4):
xl= initial lower bound guess
xu= initial upper bound guess
es= error tolerance
maxloop = maximum number of iterations
functionality: this function uses the bracketing method false position in order to find roots of a funciton
return: none'''
    loop = 1
    ea = es +1
    xr = 0
    history = []
    
    if f(xl)*f(xu) > 0:
        return RootResult(
                root=None,
                history=history,
                iterations=loop,
                error=None,
                converged=False,
                message="no sign change in interval"
        )
    
    while ea > es and loop <= maxloop:
        oldxr = xr
        fl = f(xl)
        fu = f(xu)
        if abs(fl - fu) < 1e-15:
            return RootResult(
                root=None,
                history=history,
                iterations=loop,
                error=None,
                converged=False,
                message="division by zero"
                )
        xr = xu - (fu*(xl-xu))/(fl - fu)
        fr = f(xr)

        if loop == 1:
            ea = float ("inf")
        else: 
            ea = abs ((xr - oldxr)/xr ) * 100
        history.append({
            "iteration": loop, 
            "xr": xr, 
            "f(xr)": fr, 
            "approx_error": ea
        })
        if fl*fr < 0:
            xu = xr 
        elif fl*fr > 0:
            xl = xr
        elif abs(fr) < 1e-15:
            return RootResult(
                root=xr,
                history=history,
                iterations=loop,
                error=ea,
                converged=True,
                message="exact root found"
            )
        
        loop += 1
    return RootResult(
        root=xr, 
        history=history, 
        iterations=loop-1, 
        error=ea, 
        converged=(ea <= es)
        )
        
def modified_false_position(f, xl,xu,es,maxloop):
    ''' parameters (4):
    xl= initial lower bound guess
    xu= initial upper bound guess
    es= error tolerance
    maxloop = maximum number of iterations
    functionality: this function uses the bracketing method false position in order to find roots of a funciton
    return: none'''
    loop = 1
    ea = es +1 
    iu = il = xr = 0
    history = []
    
    if f(xl)*f(xu) >0 :
        return RootResult(
                root=None,
                history=history,
                iterations=loop,
                error=None,
                converged=False,
                message="no sign change in interval"
        )
    fl = f(xl)
    fu = f(xu)
    while ea > es and loop <= maxloop:
        oldxr = xr
        if abs(fl - fu) < 1e-15:
            return RootResult(
                root=None,
                history=history,
                iterations=loop,
                error=None,
                converged=False,
                message="division by zero"
                )
        xr = xu - (fu*(xl- xu))/(fl - fu)
        fr = f(xr)
        if loop == 1:
            ea = float ("inf")
        else: 
            ea = abs ((xr - oldxr)/xr ) * 100
        history.append({
            "iteration": loop, 
            "xr": xr, 
            "f(xr)": fr, 
            "approx_error": ea
        })
        if fl*fr < 0:
            xu = xr
            fu = f(xu)
            iu = 0
            il += 1
            if il >= 2:
                fl /= 2
                il = 0 
        elif fl*fr > 0:
            xl = xr
            fl = f(xl)
            il = 0
            iu += 1
            if iu >= 2:
                fu /= 2
                iu = 0
        elif abs(fr) < 1e-15:
            return RootResult(
                root=xr,
                history=history,
                iterations=loop,
                error=ea,
                converged=True,
                message="exact root found"
            )

        loop += 1
        
    return RootResult(
        root=xr, 
        history=history, 
        iterations=loop-1, 
        error=ea, 
        converged=(ea <= es)
        )

# open methods 
def secant (f, x0, x, es, maxloop):
    ''' parameters (4):
    f = the function, defined externally
    x0= initial x i-1 guess
    x= initial xi guess
    es= error tolerance
    maxloop = maximum number of iterations
    functionality: this function uses the open method secant in order to find roots of a funciton
    return: none'''
    loop = 1
    ea = es +1
    history = []
    while ea > es and loop <= maxloop:
        f0 = f(x0)
        fx = f(x)
        if abs(f0 - fx) < 1e-15:
            return RootResult(
                root=None,
                history=history,
                iterations=loop,
                error=None,
                converged=False,
                message="division by zero"
            )
        x1 = x - (fx*(x0-x))/(f0-fx)
        f1 = f(x1)
        if abs(x1) > 1e-15:
            ea = abs((x1 - x)/x1) *100
        else:
            ea = 0
        history.append ({
            "iteration": loop,
            "x": x,
            "f(x)": fx,
            "x1": x1,
            "f(x1)": f1,
            "approx_error": ea})
        x0 = x
        x = x1 
        loop+=1
    return RootResult(
            root=x1,
            history=history,
            iterations=loop-1,
            error=ea,
            converged= (ea <= es)
        )

def fixed_point(g, x, es, maxloop):
    ''' parameters (4):
x= initial xi guess
es= error tolerance
maxloop = maximum number of iterations
functionality: this function uses the open method fixed point in order to find roots of a funciton
return: none'''
    ea = es + 1
    loop = 1
    history = []
    while ea > es and loop <= maxloop:
        x1 = g(x)
        if abs(x1) > 1e-15: 
            ea = abs((x1 - x)/x1) *100
        else:
            ea = 0
        history.append ({
            "iteration": loop,
            "x": x,
            "x1": x1,
            "g(x1)": g(x1),
            "approx_error": ea})
        x=x1
        loop+=1
    return RootResult(
            root=x1,
            history=history,
            iterations=loop-1,
            error=ea,
            converged= (ea <= es)
        )

def newton_raphson(f, df, x, es, maxloop):
    ''' parameters (4):
x= initial xi guess
es= error tolerance
maxloop = maximum number of iterations
functionality: this function uses the open method newton raphson in order to find roots of a funciton
return: rootresult'''
    loop = 1
    ea = es +1
    history = []
    while ea > es and loop <= maxloop:
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < 1e-15:
            return RootResult(
                root = None,
                history = history,
                iterations = loop,
                error = None,
                converged = False,
                message = "division by zero"
                )
        x1 = x - fx/dfx
        fx1 = f(x1)
        if abs(x1) > 1e-15: 
            ea = abs((x1 - x)/x1) *100
        else:
            ea = 0
        history.append ({
            "iteration": loop,
            "x": x,
            "f(x)": fx,
            "x1": x1,
            "f(x1)": fx1,
            "approx_error": ea})
        x = x1
        loop+=1
    return RootResult(
            root=x1,
            history=history,
            iterations=loop-1,
            error=ea,
            converged= (ea <= es)
        )