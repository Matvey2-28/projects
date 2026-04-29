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
    
        gas_disk_set = model_data.get_gas_disks()
        spheres_set = model_data.get_spheres()
        nebulas_set = model_data.get_arbitrary_clusters()
        material_points_set = model_data.get_material_points()
        
        if gas_disk_set == None:
            None
        else:
            self.PHYS_FUNC_GAS = gas_disk_set[9]
            self.T_MIN_GAS = gas_disk_set[10]
            self.DIRECTION_GAS = gas_disk_set[11]
            
        if spheres_set == None:
            None
        else:
            self.PHYS_FUNC_SPHERE = spheres_set[7]
            self.T_MIN_SPHERE = spheres_set[8]
            self.DIRECTION_SPHERE = spheres_set[9]
            
        if nebulas_set == None:
            None
        else:
            self.PHYS_FUNC_NEBULA = nebulas_set[9]
            self.T_MIN_NEBULA = nebulas_set[10]
            self.DIRECTION_NEBULA = nebulas_set[11]
            
        if material_points_set == None:
            None
        else:
            self.MASS = material_points_set[2]
            self.VX = material_points_set[9]
            self.VY = material_points_set[10]
            self.VZ = material_points_set[11]
            
        
        
        
        
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

        
        func_disk = self.PHYS_FUNC_GAS
        func_sphere = self.PHYS_FUNC_SPHERE
        func_nebula = self.PHYS_FUNC_NEBULA
        
        direction_disk = self.DIRECTION_GAS
        direction_sphere = self.DIRECTION_SPHERE
        direction_nebula = self.DIRECTION_NEBULA
        
        temperature_disk = self.T_MIN_DISK
        temperature_sphere = self.T_MIN_SPHERE
        temperature_nebula = self.T_MIN_NEBULA
        
        M_POINT = self.MASS
        
        vel_point_x = self.VX
        vel_point_y = self.VY
        vel_point_z = self.VZ
        
        
        
        
        
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
        
        def gas_disk():
            
            x0 = box_size / 2
            y0 = box_size / 2
            
            if func_disk == 'bell':
                T = temperature_disk * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2)
                rho = n_H * m_H * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2)
            else:
                T = temperature_disk * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2))
                rho = n_H * m_H * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2))
                
            P = R / MU_H * rho * T
            u = 3  * k * T / m_H / 2
        
            V_disk = np.pi * (radius_exterior**2 - radius_interior**2) * thickness
            smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
        
            masses = V_disk / num_part * rho
        
            pos_star = np.array([[box_size / 2, box_size / 2, 0]])
            vel_star = np.array([[vel_point_x, vel_point_y, vel_point_z]])
            mass_point = np.array([M_POINT])
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses, pos_star, vel_star, mass_point))
        
        def gas_sphere():
            
            x0 = box_size / 2
            y0 = box_size / 2
            z0 = box_size / 2
            
            if func_disk == 'bell':
                T = temperature_sphere * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2 - (2.5 * (pos[:, 1] - z0) / AU) ** 2)
                rho = n_H * m_H * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2)
            else:
                T = temperature_sphere * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2) + (pos[:, 2] - z0)**2) - (2.5 * (pos[:, 1] - z0) / AU) ** 2)
                rho = n_H * m_H * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2 + (pos[:, 2] - z0)**2)
                
            P = R / MU_H * rho * T
            u = 3  * k * T / m_H / 2
        
            V_disk = np.pi * (radius_exterior**2 - radius_interior**2) * thickness
            smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
        
            masses = V_disk / num_part * rho
        
            pos_star = np.array([[box_size / 2, box_size / 2, 0]])
            vel_star = np.array([[vel_point_x, vel_point_y, vel_point_z]])
            mass_point = np.array([M_POINT])
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses, pos_star, vel_star, mass_point))
        
        def gas_nebula():
            
            x0 = box_size / 2
            y0 = box_size / 2
            
            if func_disk == 'bell':
                T = temperature_sphere * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2 - (2.5 * (pos[:, 1] - z0) / AU) ** 2)
                rho = n_H * m_H * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2)
            else:
                T = temperature_sphere * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2) + (pos[:, 2] - z0)**2) - (2.5 * (pos[:, 1] - z0) / AU) ** 2)
                rho = n_H * m_H * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2) + (pos[:, 2] - z0)**2)
                
            P = R / MU_H * rho * T
            u = 3  * k * T / m_H / 2
        
            V_disk = np.pi * (radius_exterior**2 - radius_interior**2) * thickness
            smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
        
            masses = V_disk / num_part * rho
        
            pos_star = np.array([[box_size / 2, box_size / 2, 0]])
            vel_star = np.array([[vel_point_x, vel_point_y, vel_point_z]])
            mass_point = np.array([M_POINT])
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses, pos_star, vel_star, mass_point))
            
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        