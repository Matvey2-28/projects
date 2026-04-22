import matplotlib.pyplot as plt
import numpy as np

class Solver:
    
    def __init__(self, model_data):
        visual_settings = model_data.get_visual_settings()
        self.GRAPHIC_NAME = visual_settings[0]
        self.TYPE_OF_FILE = visual_settings[1]
        self.MARKER_COLOR = visual_settings[2]
        self.LINE_COLOR = visual_settings[3]
        self.PIC_QUALITY = visual_settings[4]
    
        math_settings = model_data.get_math_settings()
        self.X_MIN = math_settings[0]
        self.X_MAX = math_settings[1]
        self.X_COORDS = math_settings[2]
        self.MIN_ANGLE = math_settings[3]
        self.MAX_ANGLE = math_settings[4]
        self.MIN_RAD = math_settings[5]
        self.MAT_FUNC = math_settings[6]
        
    def solve(self):
        
        def line(X_MIN, X_MAX, X_COORDS):
            x = np.lispace(self.X_MIN, self.X_MAX, self.X_COORDS)
            y = x
            
            return x, y
        
        def parabola(X_MIN, X_MAX, X_COORDS):
            x = np.lispace(self.X_MIN, self.X_MAX, self.X_COORDS)
            y = x ** 2
            
            return x, y
        
        def giperbola(X_MIN, X_MAX, X_COORDS):
            x = np.lispace(self.X_MIN, self.X_MAX, self.X_COORDS)
            y = 1 / x
            
            return x, y
        
        def circle(MIN_RAD, MIN_ANGLE, MAX_ANGLE):
            alpha = np.arange(self.MIN_ANGLE, self.MAX_ANGLE, 0.01)
            x = np.cos(alpha) * self.MIN_RAD
            y = np.sin(alpha) * self.MIN_RAD
            
            return x, y
        
        def log_sp(MIN_ANGLE, MAX_ANGLE):
            k = 0.5
            alpha = np.arange(self.MIN_ANGLE, self.MAX_ANGLE, 0.01)
            r = np.exp(k * alpha)
            
            x = r * np.cos(alpha)
            y = r * np.sin(alpha)
            
            return x, y
        
        def astroid(MIN_RAD):
            t = np.arange(-2 * (self.MIN_RAD / 4), 2 * self.MIN_RAD)
            
            x = R * np.cos(t) ** 3
            y = R * np.sin(t) ** 3
            
            return x, y
        
        if self.MAT_FUNC == 'line':
            plt.plot(line(), color=self.LINE_COLOR, markerfacecolor=self.MARKER_COLOR)
            plt.savefig(self.GRAPHIC_NAME+self.TYPE_OF_FILE, self.PIC_QUALITY)
            
        elif self.MAT_FUNC == 'parabola':
            plt.plot(line(), color=self.LINE_COLOR, markerfacecolor=self.MARKER_COLOR)

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

