import sys
import numpy as np
import h5py
import sys
import template_model as cai

float_type = np.float64
int_type = np.int32

def part_filter(parts_type):
    parts_data = {}

    for key, value in cai.data.items():
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
                    

stars_parts = part_filter('star')

num_star_part = len(stars_parts['particle_mass'])

stars_parts_coords = np.array(tuple(zip(
                    stars_parts['particle_position_x'], 
                    stars_parts['particle_position_y'], 
                    stars_parts['particle_position_z'])))

stars_parts_vel = np.array(tuple(zip(
                stars_parts['particle_velocity_x'], 
                stars_parts['particle_velocity_y'], 
                stars_parts['particle_velocity_z'])))

sink_parts = part_filter('sinks')

IC = h5py.File('./IC.hdf5', 'w')
grp = IC.create_group("/Header")
grp.attrs["BoxSize"] = [cai.meta_data['box_size'], cai.meta_data['box_size'], 0]
grp.attrs["NumPart_Total"] = [len(gas_parts['particle_mass']), 2, 0, 0, 0, 0]
grp.attrs["NumPart_Total_HighWord"] = [0, 0, 0, 0, 0, 0]
grp.attrs["NumPart_ThisFile"] = [len(gas_parts['particle_mass']), 2, 0, 0, 0, 0]
grp.attrs["Time"] = 0.0
grp.attrs["NumFileOutputsPerSnapshot"] = 1
grp.attrs["MassTable"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
grp.attrs["Flag_Entropy_ICs"] = [0, 0, 0, 0, 0, 0]
grp.attrs["Dimension"] = 2

grp = IC.create_group("/Units")
grp.attrs["Unit length in cgs (U_L)"] = 1.0
grp.attrs["Unit mass in cgs (U_M)"] = 1.0
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
grp.create_dataset("Coordinates",  data=stars_parts_coords, dtype="f")
grp.create_dataset("Velocities", data=stars_parts_vel, dtype="f")
grp.create_dataset("Masses", data=stars_parts['particle_mass'], dtype="f")
grp.create_dataset("ParticleIDs", data=np.arange(len(gas_parts['particle_mass']), len(gas_parts['particle_mass'])+int(2)))


# IC = h5py.File('./IC.hdf5', 'w')

# ## create hdf5 groups
# header = IC.create_group("Header")
# part0 = IC.create_group("PartType0")
# part1 = IC.create_group("PartType1")

# ## header entries
# NumPart = np.array([len(gas_parts['particle_mass']), 2, 0, 0, 0, 0], dtype = int_type)
# header.attrs.create("NumPart_ThisFile", NumPart)
# header.attrs.create("NumPart_Total", NumPart)
# header.attrs.create("NumPart_Total_HighWord", np.zeros(6, dtype = int_type))
# header.attrs.create("MassTable", np.zeros(6, dtype = int_type))
# header.attrs.create("Time", 0.0)
# header.attrs.create("Redshift", 0.0)
# header.attrs.create("BoxSize", cai.meta_data['box_size'])
# header.attrs.create("NumFilesPerSnapshot", 1)
# header.attrs.create("Omega0", 0.0)
# header.attrs.create("OmegaB", 0.0)
# header.attrs.create("OmegaLambda", 0.0)
# header.attrs.create("HubbleParam", 1.0)
# header.attrs.create("Flag_Sfr", 0)
# header.attrs.create("Flag_Cooling", 0)
# header.attrs.create("Flag_StellarAge", 0)
# header.attrs.create("Flag_Metals", 0)
# header.attrs.create("Flag_Feedback", 0)
# header.attrs.create("Flag_DoublePrecision", 1)

# # part0
# part0.create_dataset("ParticleIDs", data=np.arange(0, len(gas_parts['particle_mass'])))
# part0.create_dataset("Coordinates", data=gas_parts_coords)
# part0.create_dataset("Velocities", data=gas_parts_vel)
# part0.create_dataset("Masses", data=gas_parts['particle_mass'])
# part0.create_dataset("SmoothingLength", data=gas_parts['smoothing_length'])
# part0.create_dataset("InternalEnergy", data=gas_parts['internal_energy'])


# # part1
# part1.create_dataset("ParticleIDs", data=np.arange(len(gas_parts['particle_mass']), len(gas_parts['particle_mass'])+2))
# part1.create_dataset("Coordinates", data=stars_parts_coords)              
# part1.create_dataset("Velocities", data=stars_parts_vel)                  
# part1.create_dataset("Masses",data=stars_parts['particle_mass'])

# ## close file
# IC.close()
# sys.exit(0)
