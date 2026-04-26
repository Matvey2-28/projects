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
        self.T_MIN = phys_settings[0]
        self.RAD_EX = phys_settings[1]
        self.RAD_IN = phys_settings[2]
        self.MASS = phys_settings[3]
        self.DEC_STEP = phys_settings[4]
        
        
        
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

        num_part = 50000
        box_size = 20 * AU
        thickness = AU * 0.2
        radius_exterior = self.RAD_EX * AU
        radius_interior = self.RAD_IN * AU
        temperature = self.T_MIN
        M = self.MASS * 10 ** self.DEC_STEP
        
        
        
        def params_returner():
            
            def coords_generator(r, N):
                phi = np.linspace(0, 2*np.pi, N)
                x = r * np.cos(phi)
                y = r * np.sin(phi)
                z = np.zeros(N)
                return np.array(list(zip(x, y, z)))
            
            
            def _vel_calc(x, y):
                alpha = np.atan2(y, x)
                r = np.sqrt(x**2 + y**2)
                v_x = -np.sqrt(G * M_SUN / r) * np.sin(alpha)
                v_y = np.sqrt(G * M_SUN / r) * np.cos(alpha)
                return v_x, v_y
            
            
            def create_regular_dist_model(temperature, # Температура, К
                                          radius_interior, # Внутренний радиус газового диска
                                          radius_exterior, # Внешний радиус газового диска
                                          thickness, # Толщина газового диска
                                          box_size
                                          ):
                
                inner_polygon = geom.Polygon(coords_generator(radius_interior, 1000))
                outer_polygon = geom.Polygon(coords_generator(radius_exterior, 1000))
                points_numper_per_side = 200
            
                x_pictures_limits = [-radius_exterior, radius_exterior]
                y_pictures_limits = [-radius_exterior, radius_exterior]
            
                pos_xyz = []
                vel_xyz = []
            
                for x in np.linspace(*x_pictures_limits, points_numper_per_side):
                    for y in np.linspace(*y_pictures_limits, points_numper_per_side):
                        p = geom.Point(x, y)
                        if p.within(outer_polygon) and not p.within(inner_polygon):
                            pos_xyz.append([x + box_size / 2, y + box_size / 2, 0])
                            v_x, v_y = _vel_calc(x, y)
                            vel_xyz.append([v_x, v_y, 0])
                            
                num_part = len(pos_xyz)
                pos_1 = np.array(pos_xyz)
                vel_1 = np.array(vel_xyz)
                pos_xyz.append(([pos_1[:, 0], pos_1[:, 1], 2])
                pos_xyz.append(([pos_1[:, 0], pos_1[:, 1], 4]))
                
                vel_xyz.append(([vel_1[:, 0], [vel_1[:, 1], 0]))
                vel_xyz.append(([vel_1[:, 0], [vel_1[:, 1], 0]))
                
                pos = np.array(pos_xyz)
                vel = np.array(vel_xyz)
                
                x0 = box_size / 2
                y0 = box_size / 2
                
                T = temperature * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2))
                rho = np.full(num_part, n_H * m_H)
                P = R / MU_H * rho * T
                u = 3  * k * T / m_H / 2
            
                V_disk = np.pi * (radius_exterior ** 2 - radius_interior ** 2) * thickness
                smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
            
                masses = V_disk / num_part * rho
            
                pos_star = np.array([[box_size / 2, box_size / 2, 0]])
                vel_star = np.array([[0, 0, 0]])
                mass_star = np.array([M])
                
                print(pos)
                return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                        (pos, vel, masses, pos_star, vel_star, mass_star))
            
            def output_gas_data(pos, vel, masses, u, P, T, rho, smth_lnght):
                return {
                        ("gas", "particle_position_x"): pos[:, 0],
                        ("gas", "particle_position_y"): pos[:, 1],
                        ("gas", "particle_position_z"): pos[:, 2],
                        ("gas", "particle_velocity_x"): vel[:, 0],
                        ("gas", "particle_velocity_y"): vel[:, 1],
                        ("gas", "particle_velocity_z"): vel[:, 2],
                        ("gas", "particle_mass"): masses,
                        ("gas", "internal_energy"): u,
                        ("gas", "pressure"): P,
                        ("gas", "temperature"): T,
                        ("gas", "smoothing_length"): smth_lnght,
                        ("gas", "density"): rho
                    }
            
            gas_data, material_parts_data = create_regular_dist_model(temperature, radius_interior, radius_exterior, thickness, box_size)
            
            data = output_gas_data(*gas_data)
            
            def part_filter(parts_type):
                parts_data = {}
            
                for key, value in data.items():
                    if parts_type in key:
                        parts_data[key[1]] = value
                
                return parts_data
            
            gas_parts = part_filter('gas')
            num_gas_part = len(gas_parts['density'])
            gas_parts_coords = np.array(tuple(zip(
                                gas_parts['particle_position_x'], 
                                gas_parts['particle_position_y'], 
                                gas_parts['particle_position_z'])))
            gas_parts_vel = np.array(tuple(zip(
                            gas_parts['particle_velocity_x'], 
                            gas_parts['particle_velocity_y'], 
                            gas_parts['particle_velocity_z'])))
                                
            sun_mass = np.array([M])
            sun_coords = np.array([box_size/2, box_size/2, 0])
            sun_vel = np.array([0, 0, 0])
            
            IC = h5py.File('./IC.hdf5', 'w')
            grp = IC.create_group("/Header")
            grp.attrs["BoxSize"] = [box_size, box_size, 0]
            grp.attrs["NumPart_Total"] = [len(gas_parts['particle_mass']), 1, 0, 0, 0, 0]
            grp.attrs["NumPart_Total_HighWord"] = [0, 0, 0, 0, 0, 0]
            grp.attrs["NumPart_ThisFile"] = [len(gas_parts['particle_mass']), 1, 0, 0, 0, 0]
            grp.attrs["Time"] = 0.0
            grp.attrs["NumFileOutputsPerSnapshot"] = 1
            grp.attrs["MassTable"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            grp.attrs["Flag_Entropy_ICs"] = [0, 0, 0, 0, 0, 0]
            grp.attrs["Dimension"] = 2
            
            grp = IC.create_group("/Units")
            grp.attrs["Unit length in cgs (U_L)"] = 100
            grp.attrs["Unit mass in cgs (U_M)"] = 1000
            grp.attrs["Unit time in cgs (U_t)"] = 1.0
            grp.attrs["Unit current in cgs (U_I)"] = 1.0
            grp.attrs["Unit temperature in cgs (U_T)"] = 1.0
            
            grp = IC.create_group("/PartType0")
            grp.create_dataset("Coordinates", data=gas_parts_coords, dtype="f")
            grp.create_dataset("Velocities", data=gas_parts_vel, dtype="f")
            grp.create_dataset("Masses", data=gas_parts['particle_mass'], dtype="f")
            grp.create_dataset("SmoothingLength", data=gas_parts['smoothing_length'], dtype="f")
            grp.create_dataset("InternalEnergy", data=gas_parts['internal_energy'], dtype="f")
            grp.create_dataset("ParticleIDs", data=np.arange(0, len(gas_parts['particle_mass'])))
            grp.create_dataset("Density", data=gas_parts['density'], dtype="f")
            
            
            grp = IC.create_group("/PartType1")
            grp.create_dataset("Coordinates",  data=sun_coords, dtype="f")
            grp.create_dataset("Velocities", data=sun_vel, dtype="f")
            grp.create_dataset("Masses", data=sun_mass, dtype="f")
            grp.create_dataset("ParticleIDs", data=np.arange(len(gas_parts['particle_mass']), len(gas_parts['particle_mass'])+int(1)))
            
            
            
            
            IC.close()

            


            
        
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

