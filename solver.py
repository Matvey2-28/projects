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
        self.T_MIN_DISK = phys_settings[2]
        self.MASS_DISK = phys_settings[3]
        self.DEC_STEP_M_DISK = phys_settings[4]
        
        self.VEL_3D_SPHERE = phys_settings[5]
        self.T_MIN_SPHERE = phys_settings[6]
        self.MASS_SPHERE = phys_settings[7]
        self.DEC_STEP_M_SPHERE = phys_settings[8]
        
        self.VEL_3D_NEBULA = phys_settings[9]
        self.T_MIN_NEBULA = phys_settings[10]
        self.MASS_NEBULA = phys_settings[11]
        self.DEC_STEP_M_NEBULA = phys_settings[12]
        
        
        
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

        
        func = self.PHYS_FUNC
        
        direction_disk = self.VEL
        direction_sphere = self.VEL_3D_SPHERE
        direction_nebula = self.VEL_3D_NEBULA
        
        temperature_disk = self.T_MIN_DISK
        M_DISK = self.MASS_DISK * 10 ** self.DEC_STEP_M_DISK
        
        temperature_sphere = self.T_MIN_SPHERE
        M_SPHERE = self.MASS_SPHERE * 10 ** self.DEC_STEP_M_SPHERE
        
        temperature_nebula = self.T_MIN_NEBULA
        M_NEBULA = self.MASS_NEBULA * 10 ** self.DEC_STEP_M_NEBULA
        
        
        
        
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
        
        def vel_calc_circle(x, y, z):
            alpha = np.atan2(y, x)
            r = np.sqrt(x**2 + y**2 + z**2)
            teta = np.atan2(z, x)
            v_x = np.sqrt(G * M / r) * np.sin(teta) * np.cos(alpha)
            v_y = 0
            v_z = np.sqrt(G * M / r) * np.cos(teta)
            return v_x, v_y, v_z
        
        def phys_params():
            
            x0 = box_size / 2
            y0 = box_size / 2
            
            if func == 'bell':
                T = temperature * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2)
                rho = n_H * m_H * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2)
            else:
                T = temperature * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2))
                rho = n_H * m_H * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2))
                
            P = R / MU_H * rho * T
            u = 3  * k * T / m_H / 2
        
            V_disk = np.pi * (radius_exterior**2 - radius_interior**2) * thickness
            smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
        
            masses = V_disk / num_part * rho
        
            pos_star = np.array([[box_size / 2, box_size / 2, 0]])
            vel_star = np.array([[0, 0, 0]])
            mass_star = np.array([M_])
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses, pos_star, vel_star, mass_star))
            
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        