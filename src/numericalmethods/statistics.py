import math 

class StatResult:
    def __init__(self, x_average = None, x_standard_deviation=None, y_average=None, y_standard_deviation=None, r=None, r_squared=None, 
                 standard_error=None, linear_model = None, nonlinear_model = None, message=None):
        self.x_average = x_average
        self.x_standard_deviation = x_standard_deviation
        self.y_average = y_average
        self.y_standard_deviation = y_standard_deviation
        self.r = r
        self.r_squared = r_squared
        self.standard_error = standard_error
        self.linear_model = linear_model
        self.nonlinear_model = nonlinear_model
        self.message = message
    def __str__(self):
        return(
            f"x average = {self.x_average}\n"
            f"x standard_deviation = {self.x_standard_deviation}\n"
            f"y average = {self.y_average}\n"
            f"y standard_deviation = {self.y_standard_deviation}\n"
            f"r = {self.r}\n"
            f"r_squared = {self.r_squared}\n"
            f"standard_error = {self.standard_error}\n"
            f"linear_model = {self.linear_model}\n"
            f"nonlinear_model = {self.nonlinear_model}\n"
            f"message = {self.message}"
        )


def check (x,y): 
    ''' Parameters (2):
        x: list of x values
        y: list of y values
        '''
    if len (x) != len(y): 
        return StatResult(
            message="x and y must have the same length"
            )
    if len(x) <= 2:
        return StatResult(
            message="x and y must have more than 2 points"
            )

def sumsquares(x,y, slope, intercept):
    ''' Parameters (4):
    x: list of x values
    y: list of y values
    slope: slope of the line
    intercept: y-intercept of the line
    functionality: calculates the sum of squares of the residuals for a linear regression line
    return: sum of squares of the residuals
    '''
    n = len(x)
    sums = [ ] 
    for i in range (n):
        sums.append((y[i] - (slope * x[i] + intercept))**2)
    ssr = sum(sums)
    return ssr

def stats (x,y): 
    ''' Parameters (2):
    x: list of x values
    y: list of y values
    functionality: calculates the average and standard deviation of a set of data points
    return: average and standard deviation of the data points
    '''
    check_result = check(x,y)
    if check_result is not None:
        return check_result
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    std_dev_x = (sum([(x[i]-mean_x)**2 for i in range(n)]) / n) ** 0.5
    std_dev_y = (sum([(y[i]-mean_y)**2 for i in range(n)]) / n) ** 0.5
    return StatResult(
        x_average = mean_x, 
        x_standard_deviation = std_dev_x,
        y_average = mean_y,
        y_standard_deviation= std_dev_y,
    )

def linear_regression(x,y):
    ''' Parameters (2):
    x: list of x values
    y: list of y values
    functionality: uses least squares method to find the best linear fit for the model y = mx + b for a set of data points
    return: StatResult object with slope, intercept, average, standard deviation, r, r_squared, and standard error
    '''
   
    check_result = check(x,y)
    if check_result is not None:
        return check_result
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum([x[i]*y[i] for i in range(n)])
    sum_x2 = sum([x[i]**2 for i in range(n)])

    slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
    intercept = (sum_y - slope*sum_x) / n
    r = (n*sum_xy - sum_x*sum_y) / ((n*sum_x2 - sum_x**2)**0.5 * (n*sum([y[i]**2 for i in range(n)]) - sum_y**2)**0.5)
    r_squared = r**2
    sumofsquares = sumsquares(x,y, slope, intercept)
    standard_error = (sumofsquares / (n-2)) ** 0.5
    return StatResult(
        r=r,
        r_squared=r_squared,
        linear_model=f" y = {slope}x + {intercept}",
        standard_error=standard_error
    )

def exponential_regression(x,y):
    ''' Parameters (2):
        x: list of x values
        y: list of y values
        functionality: uses least squares method find the best fit of the model y = ae^(bx) for a set of data points. 
        model requires linearization to become ln(y) = ln(a) + bx, 
        where y axis is transformed to ln(y) and then linear regression is applied to find the slope and intercept.
        b = slope and a = e^(intercept) 
        return: StatResult object with r, r_squared, standard error, linear model, nonlinear model, and message 
        '''
       
    check_result = check(x,y)
    if check_result is not None:
        return check_result
    n = len(x)
    ynew = [math.log(y[i]) for i in range(n)]
    sum_x = sum(x)
    sum_y = sum(ynew)
    sum_xy = sum([x[i]*ynew[i] for i in range(n)])
    sum_x2 = sum([x[i]**2 for i in range(n)])

    slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
    intercept = (sum_y - slope*sum_x) / n
    r = (n*sum_xy - sum_x*sum_y) / (math.sqrt(n*sum_x2 - sum_x**2) * math.sqrt(n*sum([ynew[i]**2 for i in range(n)]) - sum_y**2))
    r_squared = r**2
    sumofsquares = sumsquares(x,ynew, slope, intercept)
    standard_error = (sumofsquares / (n-2)) ** 0.5
    alpha = math.exp(intercept)
    beta = slope 
    return StatResult(
        r=r,
        r_squared=r_squared,
        linear_model = f" y= {intercept} + {slope}x",
        nonlinear_model = f" y= {alpha} * e^({beta}x)",
        standard_error = standard_error,
        message= "y axis is transformed to ln(y)"
    )


def power_regression (x,y):
    ''' Parameters (2):
        x: list of x values
        y: list of y values
        functionality: uses least squares method to find the best linear fit of the model y = ax^b for a set of data points.
        model requires linearization to become log(y) = log(a) + b*log(x)
        x and y axis are transformed to log(x) and log(y) 
        b = slope and a = 10^(intercept) 
        return: StatResult object with r, r_squared, standard error, linear model, nonlinear model, and message
        '''
       
    check_result = check(x,y)
    if check_result is not None:
        return check_result
    n = len(x)
    xnew = [math.log10(x[i]) for i in range(n)]
    ynew = [math.log10(y[i]) for i in range(n)]
    sum_x = sum(xnew)
    sum_y = sum(ynew)
    sum_xy = sum([xnew[i]*ynew[i] for i in range(n)])
    sum_x2 = sum([xnew[i]**2 for i in range(n)])

    slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
    intercept = (sum_y - slope*sum_x) / n
    r = (n*sum_xy - sum_x*sum_y) / (math.sqrt(n*sum_x2 - sum_x**2) * math.sqrt(n*sum([ynew[i]**2 for i in range(n)]) - sum_y**2))
    r_squared = r**2
    sumofsquares = sumsquares(xnew,ynew, slope, intercept)
    standard_error = (sumofsquares / (n-2)) ** 0.5
    beta = slope 
    alpha = 10**intercept
    return StatResult(
        r=r,
        r_squared=r_squared,
        standard_error=standard_error, 
        linear_model = f" y= {intercept} + {slope}x", 
        nonlinear_model = f" y= {alpha} * x^{beta}",
        message= "x and y axis are transformed to log(x) and log(y)"
    )

def growth_regression(x,y):
    ''' Parameters (2):
        x: list of x values
        y: list of y values
        functionality: uses least squares method to find the best linear fit of the model y = (ax)/(b+x) for a set of data points. 
        model requires linearization to become 1/y = (b/a)(1/x) + (1/a)
        x and y axis are transformed to 1/x and 1/y
        b = slope*a and a = 1/intercept
        return: StatResult object with slope, intercept, average, standard deviation, r, r_squared, and standard error
        '''
       
    check_result = check(x,y)
    if check_result is not None:
        return check_result
    n = len(x)
    xnew = [1/x[i] for i in range(n)]
    ynew = [1/y[i] for i in range(n)]
    sum_x = sum(xnew)
    sum_y = sum(ynew)
    sum_xy = sum([xnew[i]*ynew[i] for i in range(n)])
    sum_x2 = sum([xnew[i]**2 for i in range(n)])

    slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
    intercept = (sum_y - slope*sum_x) / n
    r = (n*sum_xy - sum_x*sum_y) / (math.sqrt(n*sum_x2 - sum_x**2) * math.sqrt(n*sum([ynew[i]**2 for i in range(n)]) - sum_y**2))
    r_squared = r**2
    sumofsquares = sumsquares(xnew,ynew, slope, intercept)
    standard_error = (sumofsquares / (n-2)) ** 0.5
    a = 1 / intercept
    b = slope * a
    return StatResult(
        r=r,
        r_squared=r_squared,
        standard_error=standard_error,
        linear_model = f" y= {intercept} + {slope}x", 
        nonlinear_model = f" y= ({a}x)/({b}+x)",
        message= "x and y axis are transformed to 1/x and 1/y"
    )