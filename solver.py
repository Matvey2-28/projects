import shapely.geometry as geom
import numpy as np
import random
import h5py
import yaml
import sys

float_type = np.float64
int_type = np.int32

class Solver:
    
    def __init__(self, model_data):
    
        phys_settings = model_data.get_physical_settings()
        self.PHYS_FUNC = phys_settings[0]
        self.VEL = phys_settings[1]
        self.T_MIN = phys_settings[2]
        self.RHO_MIN = phys_settings[3]
        self.MASS = phys_settings[4]
        self.DEC_STEP_M = phys_settings[5]
        self.VEL_3D_SPHERE = phys_settings[6]
        self.VEL_3D_NEBULA = phys_settings[7]
        
        
        
    def solve(self, output_path: str):
        
        
        
        AU = 1.49e11 # Астрономическая единица, м
        G = 6.67e-11 # Гравитационная постоянная, м^3/(кг*с^2)
        GAMMA = 5.0 / 3.0 # Постоянная адиобатты
        m_H = 2 * 1.6735575e-27 # Масса молекулы водорода, кг
        n_H = 2e+12  # Характерная концентрация газа, частиц/м^3
        MU_H = 0.002  # Молярная масса водорода, кг/моль
        R = 8.3144598  # Газовая постоянная, Дж/(моль*К)
        N_a = 6.0221409e+23 # Число Авогадро 
        k = 1.38064852e-23 # Больцманская постоянная
        ETA = 1.2348 # Коэффициент среднего расстояния между частицами SPH

        
        
        temperature = self.T_MIN
        M = self.MASS * 10 ** self.DEC_STEP
        
        def vel_calc_clockwise(x, y):
            alpha = np.atan2(y, x)
            r = np.sqrt(x**2 + y**2)
            v_x = -np.sqrt(G * M / r) * np.sin(alpha)
            v_y = np.sqrt(G * M / r) * np.cos(alpha)
            return v_x, v_y
        
        def vel_calc_counterclockwise(x, y):
            alpha = np.atan2(y, x)
            r = np.sqrt(x**2 + y**2)
            v_x = np.sqrt(G * M / r) * np.sin(alpha)
            v_y = -np.sqrt(G * M / r) * np.cos(alpha)
            return v_x, v_y
        
        def vel_calc_up_circle(x, y, z):
            alpha = np.atan2(y, x)
            r = np.sqrt(x**2 + y**2 + z**2)
            teta = np.atan2(z, x)
            v_x = np.sqrt(G * M / r) * np.sin(teta) * np.cos(alpha)
            v_y = 0
            v_z = np.sqrt(G * M / r) * np.cos(teta)
            return v_x, v_y, v_z
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        