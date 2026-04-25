import matplotlib.pyplot as plt
import numpy as np

class Solver:
    
    def __init__(self, model_data):
    
        phys_settings = model_data.get_physical_settings()
        self.DIMENSION = math_settings[0]
        self.T_MIN = math_settings[1]
        self.RAD_EX = math_settings[2]
        self.RAD_IN = math_settings[3]
        self.MASS = math_settings[4]
        self.DEC_STEP = math_settings[5]
        
        
        
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

        
        r_exterior = self.RAD_EX * AU
        r_interior = self.RAD_IN * AU
        temperature = self.T_MIN
        M = self.MASS * 10 ** self.DEC_STEP
        
        
        
        def 3D_graph():
            
            num_part = len(pos_xy)
            pos = np.array(pos_xy)
            vel = np.array(vel_xy)
        
            T = np.full(num_part, temperature)
            rho = np.full(num_part, n_H * m_H)
            P = R / MU_H * rho * T
            u = 3  * k * T / m_H / 2
        
            V_disk = np.pi * (r_exterior ** 2 - r_interior ** 2) * thickness
            smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
        
            masses = V_disk / num_part * rho
        
            pos_star = np.array([[box_size / 2, box_size / 2, 0]])
            vel_star = np.array([[0, 0, 0]])
            mass_star = np.array([M])
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses, pos_star, vel_star, mass_star))

            
            
           
        def 2D_graph():
            
            num_part = len(pos_xy)
            pos = np.array(pos_xy)
            vel = np.array(vel_xy)
        
            T = np.full(num_part, temperature)
            rho = np.full(num_part, n_H * m_H)
            P = R / MU_H * rho * T
            u = 3  * k * T / m_H / 2
        
            V_disk = np.pi * (r_exterior ** 2 - r_interior ** 2) * thickness
            smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
        
            masses = V_disk / num_part * rho
        
            pos_star = np.array([[box_size / 2, box_size / 2, 0]])
            vel_star = np.array([[0, 0, 0]])
            mass_star = np.array([M])
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses, pos_star, vel_star, mass_star))

            
            
        DIM = self.DIMENSION
            
        if DIM == '3D':
            3D_graph()
        
        else:
            2D_graph()
        
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

