import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as plt3d
import h5py
import sys


AE = 149597870700
N = 5000
M_SUN = 1.998e30
G = 6.67e-11
RHO_SUN = M_SUN / 1.40927e27
T_SUN = 5780
# R_SUN = 6957e5

box_size = 100 * AE


masses = np.full(N, 1e17)
densities = np.full(N, 3137)
id_parts = np.arange(0, N, 1)

phi = np.linspace(0, 2*np.pi, N)
r = (np.random.random(N) * 1.2 + 2.01) * AE

x = r * np.cos(phi)
y = r * np.sin(phi)
z = np.arange(N)
coords = np.zeros((N, 3))
coords[:, 0], coords[:, 1], coords[:, 2] = x, y, z

v = np.sqrt(G * M_SUN / r)
v_x = - v * np.sin(phi)
v_y = v * np.cos(phi)
v_z = np.arange(N)

vel = np.zeros((N, 3))
vel[:, 0], vel[:, 1], vel[:, 2] = v_x, v_y, v_z
    
# masses[4] = M_SUN
# coords[4] = [AE, -5*AE, 0]
# vel[4] = [30000, 0, 0]
    
# masses[3] = M_SUN
# coords[3] = [-AE, 5*AE, 0]
# vel[3] = [-30000, 0, 0]
temperatures[0] = T_SUN
densities[0] = RHO_SUN
masses[0] = M_SUN
coords[0] = [0, 0, 0]
vel[0] = [0, 0, 0]

# masses[2] = M_SUN
# coords[2] = [-5*AE, AE, 0]
# vel[2] = [0, -30000, 0]

 #Sun
# masses[1] = M_SUN
# coords[1] = [5*AE, -AE, 0]
# vel[1] = [0, 30000, 0]
coords = coords + box_size / 2
# print(coords)
# print(vel)
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# ax.plot(coords[:, 0], coords[:, 1], coords[:, 2] , 'o', color='#FF3838')
# ax.axis('equal')
# plt.savefig('Solor_sys.png', dpi=1000)
# plt.close()


# File

file = h5py.File('./IC.hdf5', "w")

# Header
grp = file.create_group("/Header")
grp.attrs["BoxSize"] = box_size
grp.attrs["NumPart_Total"] = [0, N, 0, 0, 0, 0]
grp.attrs["NumPart_Total_HighWord"] = [0, 0, 0, 0, 0, 0]
grp.attrs["NumPart_ThisFile"] = [0, N, 0, 0, 0, 0]
grp.attrs["Time"] = 0.0
grp.attrs["NumFilesPerSnapshot"] = 1
grp.attrs["MassTable"] = [0.0, N, 0.0, 0.0, 0.0, 0.0]
grp.attrs["Flag_Entropy_ICs"] = 0
grp.attrs["Dimension"] = 3

# Units
grp = file.create_group("/Units")
grp.attrs["Unit length in cgs (U_L)"] = 100
grp.attrs["Unit mass in cgs (U_M)"] = 1000
grp.attrs["Unit time in cgs (U_t)"] = 1.0
grp.attrs["Unit current in cgs (U_I)"] = 1.0
grp.attrs["Unit temperature in cgs (U_T)"] = 1.0


# Particle group
grp = file.create_group("/PartType1")

ds = grp.create_dataset("Velocities", (N, 3), "f", data=vel)
ds = grp.create_dataset("Masses", (N, 1), "f", data=masses)
ds = grp.create_dataset("ParticleIDs", (N, 1), "L", data = id_parts)
ds = grp.create_dataset("Coordinates", (N, 3), "d", data=coords)
ds = grp.create_dataset("Densities", (N, 1), "f", data=densities)

file.close()