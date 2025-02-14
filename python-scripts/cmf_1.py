import sys
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

def main():
    data = json.loads(sys.stdin.read())
    a = float(data['a'])
    b = float(data['b'])
    c = float(data['c'])
    d = float(data['d'])
    approx_root = float(data['approx_root'])

    def f(x): return a*x**3 + b*x**2 + c*x + d
    
    x_vals = np.linspace(-5, 5, 400)
    y_vals = f(x_vals)
    exact_root = fsolve(f, approx_root)[0]
    absolute_error = abs(exact_root - approx_root)
    
    # Сохранение графика
    plt.figure(figsize=(8,5))
    plt.plot(x_vals, y_vals, label=f'$f(x) = {a}x^3 + {b}x^2 + {c}x + {d}$')
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(exact_root, color='red', linestyle='--', label=f'Exact Root: {exact_root:.5f}')
    plt.scatter([approx_root], [f(approx_root)], color='green', label=f'Approx Root: {approx_root}')
    plt.legend()
    plt.grid(True)
    plot_path = f'public/images/task1_{abs(hash(str(data)))}.png'
    plt.savefig(plot_path)
    plt.close()

    print(json.dumps({
        "equation": f"{a}x³ + {b}x² + {c}x + {d} = 0",
        "exact_root": round(exact_root, 5),
        "absolute_error": round(absolute_error, 5),
        "plot": plot_path.replace('public/', '')
    }))

if __name__ == "__main__":
    main()
