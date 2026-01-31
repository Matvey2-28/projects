import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys

AE = 149597870700
N = 10000
M_SUN = 1.998e30
G = 6.67e-11

masses = np.full(N+1, 1e17)
id_parts = np.arange(0, N, 1)

phi = np.random.random(N) * 2.01 * np.pi
R = np.random.random(N) + 2.01 * AE

x = R * np.cos(phi)
y = R * np.sin(phi)

coords = np.zeros((N, 3))
coords[:, 0], coords[:, 1] = x, y

v = np.sqrt(G * M_SUN / R)
vx = v * np.cos(phi)
vy = v * np.sin(phi)

vel = np.zeros((N, 3))
vel[:, 0], vel[:, 1] = vx, vy

masses[0] = M_SUN
coords[0] = [0, 0, 0]
vel[0] = [0, 0, 0]

plt.plot(coords[:, 0], coords[:, 1], 'o')
plt.axis('equal')
plt.savefig('sun_system.png', dpi=1000)


# File
file = h5py.File('IC7.hdf5', "w")

# Header
grp = file.create_group("/Header")
grp.attrs["BoxSize"] = 4 * AE
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
grp.attrs["Unit length in cgs (U_L)"] = 1.0
grp.attrs["Unit mass in cgs (U_M)"] = 1.0
grp.attrs["Unit time in cgs (U_t)"] = 1.0
grp.attrs["Unit current in cgs (U_I)"] = 1.0
grp.attrs["Unit temperature in cgs (U_T)"] = 1.0


# Particle group
grp = file.create_group("/PartType1")
ds = grp.create_dataset("Velocities", (N, 3), "f", data=vel)
ds = grp.create_dataset("Masses", (N, 1), "f", data=masses)
ds = grp.create_dataset("ParticleIDs", (N, 1), "L", data=id_parts)
ds = grp.create_dataset("Coordinates", (N, 3), "d", data=coords)

file.close()