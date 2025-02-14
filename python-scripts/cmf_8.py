import sys
import json
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    data = json.loads(sys.stdin.read())
    response = {}
    
    try:
        a = float(data['a'])
        b = float(data['b'])
        n = int(data['n'])
        func_str = data['func']
        
        # Проверка безопасности функции
        if any(c in func_str for c in ['import', 'exec', 'eval']):
            raise ValueError("Недопустимые символы в функции")
            
        # Парсинг функции
        x = sp.symbols('x')
        f_expr = sp.sympify(func_str)
        f = sp.lambdify(x, f_expr, 'numpy')
        
        # Вычисление интеграла
        h = (b - a)/n
        x_vals = np.linspace(a, b, n+1)
        y_vals = f(x_vals)
        trap = (h/2)*(y_vals[0] + 2*np.sum(y_vals[1:-1]) + y_vals[-1])
        
        # Точное значение
        exact = float(sp.integrate(f_expr, (x, a, b)))
        error = abs(trap - exact)
        
        # Генерация графика
        plt.figure(figsize=(10,6))
        x_dense = np.linspace(a, b, 200)
        y_dense = f(x_dense)
        plt.plot(x_dense, y_dense, 'b-', label=f'f(x) = {sp.pretty(f_expr)}')
        
        for i in range(n):
            plt.fill_between(
                [x_vals[i], x_vals[i+1]],
                [0, 0],
                [y_vals[i], y_vals[i+1]],
                color='gray',
                alpha=0.3
            )
        
        plot_path = f'public/images/task8_{abs(hash(str(data)))}.png'
        plt.savefig(plot_path)
        plt.close()
        
        response = {
            'result': {
                'approximate': round(trap, 5),
                'exact': round(exact, 5),
                'error': round(error, 5)
            },
            'plot': plot_path.replace('public/', '')
        }
        
    except Exception as e:
        response['error'] = str(e)
        
    print(json.dumps(response))

if __name__ == "__main__":
    main()