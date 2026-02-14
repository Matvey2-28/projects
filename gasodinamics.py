import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as plt3d
import h5py
import sys
import shapely.geometry as geom

AE = 149597870700
M_SUN = 1.998e30
G = 6.67e-11
m_H = 2 * 1.67e-27
MU_H = 0.002
R = 8.31
k = 1.38e-23

def coords_generator(r, N):
    phi = np.linspace(0, 2*np.pi, N)
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return np.array(list(zip(x, y)))

def vel_cal(x, y):
    alpha = np.atan(y, x)
    r = np.sqrt(x**2 + y**2)
    v = np.sqrt(G * M_SUN / r)
    return v*np.cos(alpha), v*np.sin(alpha)

box_size = 100 * AE

masses = np.full(N, 1e17)
id_parts = np.arange(0, N, 1)

z = np.arange(N)
coords = np.zeros((N, 3))
coords[:, 0], coords[:, 1], coords[:, 2] = x, y, z

v = np.sqrt(G * M_SUN / r)
v_x = - v * np.sin(phi)
v_y = v * np.cos(phi)

vel = np.zeros((N, 3))
vel[:, 0], vel[:, 1] = v_x, v_y
    
# masses[4] = M_SUN
# coords[4] = [AE, -5*AE, 0]
# vel[4] = [30000, 0, 0]
    
# masses[3] = M_SUN
# coords[3] = [-AE, 5*AE, 0]
# vel[3] = [-30000, 0, 0]

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

# plt.plot(coords[:, 0], coords[:, 1] , 'o', color='#FF3838')
# plt.axis('equal')
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

file.close()