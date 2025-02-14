import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    data = json.loads(sys.stdin.read())
    response = {}
    
    try:
        points = [tuple(map(float, p.split(','))) for p in data['points']]
        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])
        
        if len(points) < 2:
            raise ValueError("Нужно минимум 2 точки")
            
        # Вычисление коэффициентов
        n = len(points)
        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_x2 = np.sum(x**2)
        sum_xy = np.sum(x * y)
        
        denominator = n * sum_x2 - sum_x**2
        if denominator == 0:
            raise ValueError("Деление на ноль: невозможно вычислить коэффициенты")
            
        a = (sum_y * sum_x2 - sum_x * sum_xy) / denominator
        b = (n * sum_xy - sum_x * sum_y) / denominator

        # Генерация графика
        plt.figure(figsize=(8,5))
        plt.scatter(x, y, color='red', label='Data points')
        x_line = np.linspace(min(x)-1, max(x)+1, 100)
        plt.plot(x_line, a + b*x_line, 'b-', label=f'y = {a:.2f} + {b:.2f}x')
        plt.grid(True)
        plt.legend()
        
        plot_path = f'public/images/task5_{abs(hash(str(data)))}.png'
        plt.savefig(plot_path)
        plt.close()
        
        response = {
            'equation': f"y = {round(a, 4)} + {round(b, 4)}x",
            'coefficients': {'a': a, 'b': b},
            'plot': plot_path.replace('public/', '')
        }
        
    except Exception as e:
        response['error'] = str(e)
    
    print(json.dumps(response))

if __name__ == "__main__":
    main()