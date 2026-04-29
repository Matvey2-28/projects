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
            
            
        
        
        
        
    def solve(self, output_path: str):
        
        
        
        AU = 1.49e11 # Астрономическая единица, м
        G = 6.67e-11 # Гравитационная постоянная, м^3/(кг*с^2)
        GAMMA = 5.0 / 3.0 # Постоянная адиобатты
        m_H = 2 * 1.6735575e-27 # Масса молекулы водорода, кг
        n_H = 2e+20  # Характерная концентрация газа, частиц/м^3
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
        
        temperature_disk = self.T_MIN_GAS
        temperature_sphere = self.T_MIN_SPHERE
        temperature_nebula = self.T_MIN_NEBULA
        
        
        
        
        
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
        
        
        def gas_disk(temperature_disk, 
                              radius_interior, 
                              radius_exterior, 
                              thickness, 
                              box_size):
            
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
        
            
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses))
        
        def gas_sphere(temperature_sphere,
                              radius_interior,
                              radius_exterior,
                              box_size):
            
            x0 = box_size / 2
            y0 = box_size / 2
            z0 = box_size / 2
            
            if func_sphere == 'bell':
                T = temperature_sphere * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2 - (2.5 * (pos[:, 1] - z0) / AU) ** 2)
                rho = n_H * m_H * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2)
            else:
                T = temperature_sphere * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2 + (pos[:, 2] - z0)**2) - (2.5 * (pos[:, 1] - z0) / AU) ** 2)
                rho = n_H * m_H * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2 + (pos[:, 2] - z0)**2))
                
            P = R / MU_H * rho * T
            u = 3  * k * T / m_H / 2
        
            V_sphere = 4 / 3 * np.pi * (radius_exterior**3 - radius_interior**3)
            smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
        
            masses = V_sphere / num_part * rho
        
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses))
        
        def gas_nebula(temperature_nebula, 
                              radius_interior, 
                              radius_exterior,  
                              box_size):
            
            x0 = box_size / 2
            y0 = box_size / 2
            z0 = box_size / 2
            
            if func_nebula == 'bell':
                T = temperature_sphere * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2 - (2.5 * (pos[:, 1] - z0) / AU) ** 2)
                rho = n_H * m_H * np.exp((-0.5 * (pos[:, 0] - x0) / AU) ** 2 - (1.5 * (pos[:, 1] - y0) / AU) ** 2)
            else:
                T = temperature_sphere * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2 + (pos[:, 2] - z0)**2) - (2.5 * (pos[:, 1] - z0) / AU) ** 2)
                rho = n_H * m_H * (AU / np.sqrt((pos[:, 0] - x0)**2 + (pos[:, 1] - y0)**2 + (pos[:, 2] - z0)**2))
                
            P = R / MU_H * rho * T
            u = 3  * k * T / m_H / 2
        
            V_nebula =  4 / 3 * np.pi * (radius_exterior**3 - radius_interior**3)
            smth_lnght = np.full(num_part, ((3 * V_disk) / (4 * np.pi * num_part))**(1 / 3))
        
            masses = V_nebula / num_part * rho
        
            
            return ((pos, vel, masses, u, P, T, rho, smth_lnght),
                    (pos, vel, masses))
        
        if gas_disk_set == None:
            None
        else:
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
            
            gas_data, material_parts_data = gas_disk(temperature_disk, radius_interior, radius_exterior, thickness, box_size)
            
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
                                
            sun_mass = np.array([M_SUN])
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
            
        if spheres_set == None:
            None
        else:
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
            
            gas_data, material_parts_data = gas_sphere(temperature_sphere, radius_interior, radius_exterior, box_size)
            
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
                                
            sun_mass = np.array([M_SUN])
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
            
            
            
        if nebulas_set == None:
            None
        else:
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
            
            gas_data, material_parts_data = gas_nebula(temperature_nebula, radius_interior, radius_exterior, box_size)
            
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
                                
            sun_mass = np.array([M_SUN])
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
                        
                    
            
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
        
        
        
        
        