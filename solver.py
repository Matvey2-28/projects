import matplotlib.pyplot as plt
import numpy as np

class Solver:
    
    def __init__(self, model_data):
        visual_settings = model_data.get_visual_settings()
        self.GRAPHIC_NAME = visual_settings[0]
        self.TYPE_OF_FILE = visual_settings[1]
        self.LINE_COLOR = visual_settings[2]
        self.PIC_QUALITY = visual_settings[3]
    
        math_settings = model_data.get_math_settings()
        self.X_MIN = math_settings[0]
        self.X_MAX = math_settings[1]
        self.X_COORDS = math_settings[2]
        self.MIN_ANGLE = math_settings[3]
        self.MAX_ANGLE = math_settings[4]
        self.MIN_RAD = math_settings[5]
        self.MAT_FUNC = math_settings[6]
        
    def solve(self, output_path: str):
        
        def line():
            x = np.linspace(self.X_MIN, self.X_MAX, self.X_COORDS)
            y = x
            
            plt.plot(x, y, color=self.LINE_COLOR, label=self.MAT_FUNC)
        
        def parabola():
            x = np.linspace(self.X_MIN, self.X_MAX, self.X_COORDS)
            y = x ** 2
            
            plt.plot(x, y, color=self.LINE_COLOR, label=self.MAT_FUNC)
        
        def hiperbola():
            x = np.linspace(self.X_MIN, self.X_MAX, self.X_COORDS)
            y = 1 / x + 1
            
            plt.plot(x, y, color=self.LINE_COLOR, label=self.MAT_FUNC)
        
        def circle():
            alpha = np.arange(self.MIN_ANGLE, self.MAX_ANGLE, 0.01)
            x = np.cos(alpha) * self.MIN_RAD
            y = np.sin(alpha) * self.MIN_RAD
            
            plt.plot(x, y, color=self.LINE_COLOR, label=self.MAT_FUNC)
        
        def log_sp():
            k = 0.5
            alpha = np.arange(self.MIN_ANGLE, self.MAX_ANGLE, 0.01)
            r = np.exp(k * alpha)
            
            x = r * np.cos(alpha)
            y = r * np.sin(alpha)
            
            plt.plot(x, y, color=self.LINE_COLOR, label=self.MAT_FUNC)
        
        def astroid():
            t = np.arange(-2 * (self.MIN_RAD / 4), 2 * self.MIN_RAD, 0.1)
            
            x = self.MIN_RAD * np.cos(t) ** 3
            y = self.MIN_RAD * np.sin(t) ** 3
            
            plt.plot(x, y, color=self.LINE_COLOR, label=self.MAT_FUNC)
        
        if self.MAT_FUNC == 'Line':
           line()
                   
        elif self.MAT_FUNC == 'Parabola':
            parabola()
            
        elif self.MAT_FUNC == 'Hiperbola':
            hiperbola()
            
        elif self.MAT_FUNC == 'Circle':
            circle()
            
        elif self.MAT_FUNC == 'Log spiral':
            log_sp()
            
        elif self.MAT_FUNC == 'Astroid':
            astroid()
            
        plt.axis('equal')
        plt.savefig(output_path + '/' + self.GRAPHIC_NAME + self.TYPE_OF_FILE, dpi = self.PIC_QUALITY)
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

