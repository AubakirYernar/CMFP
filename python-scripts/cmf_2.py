import sys
import json

def f(x, a, b, c):
    return a * x**2 + b * x + c

def bisection_method(a, b, c, A, B, tol=1e-6):
    iter_count = 0
    try:
        while (B - A)/2 > tol:
            iter_count += 1
            mid = (A + B)/2
            if f(mid, a, b, c) == 0:
                return mid, iter_count
            elif f(A, a, b, c)*f(mid, a, b, c) < 0:
                B = mid
            else:
                A = mid
        return (A + B)/2, iter_count
    except:
        return None, 0

def secant_method(a, b, c, x0, x1, tol=1e-6):
    iter_count = 0
    try:
        while abs(x1 - x0) > tol:
            iter_count += 1
            f_x0 = f(x0, a, b, c)
            f_x1 = f(x1, a, b, c)
            if f_x1 - f_x0 == 0:
                break
            x_temp = x1 - f_x1*(x1 - x0)/(f_x1 - f_x0)
            x0, x1 = x1, x_temp
        return x1, iter_count
    except:
        return None, 0

if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    a = float(data['a'])
    b_coef = float(data['b'])
    c = float(data['c'])
    A = float(data['interval_start'])
    B = float(data['interval_end'])
    method = data['method']

    result = {}
    if method == 'bisection':
        root, iters = bisection_method(a, b_coef, c, A, B)
    elif method == 'secant':
        root, iters = secant_method(a, b_coef, c, A, B)
    
    result = {
        'root': round(root, 6) if root else None,
        'iterations': iters,
        'error': None if root else "Method failed to converge"
    }
    
    print(json.dumps(result))