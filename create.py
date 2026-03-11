import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as plt3d
import h5py
import sys
import shapely.geometry as geom
from scipy import interpolate

AE = 149597870700
N = 10000
M_SUN = 1.998e30
G = 6.67e-11

sun_coord = np.array([5 * AE, -AE, 0])
sun_vel = np.array([0, 0, 0])
sun_mass = np.array([M_SUN])

box_size = 100 * AE

phi = np.linspace(0, 2*np.pi, 40)
r = 0.5 + np.cos(phi)
x = r * np.cos(phi)
y = r * np.sin(phi)

################## PAVEL ########################################
spline_coords, figure_spline_part = interpolate.splprep([x, y], s=0)
spline_curve = interpolate.splev(figure_spline_part, spline_coords)

curve_coords = []
for i in range(len(spline_curve[0])):
    curve_coords.append([spline_curve[0][i], spline_curve[1][i]])

polygon = geom.Polygon(curve_coords)
points_numper_per_side = 500
x_pictures_limits = [-0.5, 2]
y_pictures_limits = [-1, 1]

points_coords = []

for x_point_coord in np.linspace(*x_pictures_limits, points_numper_per_side):
    for y_point_coord in np.linspace(*y_pictures_limits, points_numper_per_side):
        p = geom.Point(x_point_coord, y_point_coord)
        if p.within(polygon):
            points_coords.append(x_point_coord)
            points_coords.append(y_point_coord)

x_p = np.array(points_coords[0::2]) + box_size / 2
y_p = np.array(points_coords[1::2]) + box_size / 2

gas_part_num = len(x_p)
id_parts = np.arange(0, gas_part_num, 1)
gas_h = np.full(gas_part_num, 0.1)
################################################################

#################### MATVEI ####################################
m_H = 2*1.6735575e-24 # масса молекулы водорода в граммах
n_H = 2*10**5 # характерная концентрация частиц в частицах на куб. см
R = 8.314
mu = 2 * 10**(-3)
k = 1.38 * 10**(-23)

scale = 0.1

T = 100
rho = m_H * n_H * scale
p = rho * R / mu * T


area_disk = np.pi * (max(x_p)**2 + max(y_p)**2 
                  - min(x_p)**2 - min(y_p)**2)
m = rho * area_disk

gas_rho = np.full(gas_part_num, rho)
gas_T = np.full(gas_part_num, T)
gas_p = gas_rho * R / mu * gas_T
gas_energy = 3 / 2 * k * gas_T
gas_m = np.full(gas_part_num, m)
###############################################

gas_coords = np.zeros([gas_part_num, 3])
gas_vel = np.zeros([gas_part_num, 3])

for i in range(len(x_p)):
    gas_coords[i, 0] = x_p[i]
    gas_coords[i, 1] = y_p[i]

    gas_vel[i, 0] = 0.001
    gas_vel[i, 1] = 0.0



file = h5py.File('./IC.hdf5', "w")

# Header
grp = file.create_group("/Header")
grp.attrs["BoxSize"] = box_size
grp.attrs["NumPart_Total"] = [gas_part_num, 1, 0, 0, 0, 0]
grp.attrs["NumPart_Total_HighWord"] = [0, 0, 0, 0, 0, 0]
grp.attrs["NumPart_ThisFile"] = [gas_part_num, 1, 0, 0, 0, 0]
grp.attrs["Time"] = 0.0
grp.attrs["NumFilesPerSnapshot"] = 1
grp.attrs["MassTable"] = [gas_part_num, 1, 0.0, 0.0, 0.0, 0.0]
grp.attrs["Flag_Entropy_ICs"] = 0
grp.attrs["Dimension"] = 3

# Units
grp = file.create_group("/Units")
grp.attrs["Unit length in cgs (U_L)"] = 100
grp.attrs["Unit mass in cgs (U_M)"] = 1000
grp.attrs["Unit time in cgs (U_t)"] = 1.0
grp.attrs["Unit current in cgs (U_I)"] = 1.0
grp.attrs["Unit temperature in cgs (U_T)"] = 1.0

    
grp = file.create_group("/PartType0")
grp.create_dataset("Coordinates", data=gas_coords, dtype="f")
grp.create_dataset("Velocities", data=gas_vel, dtype="f")
grp.create_dataset("Masses", data=gas_m, dtype="f")
grp.create_dataset("SmoothingLength", data=gas_h, dtype="f")
grp.create_dataset("InternalEnergy", data=gas_energy, dtype="f")
grp.create_dataset("ParticleIDs", data=np.arange(0, gas_part_num))
grp.create_dataset("Density", data=gas_rho, dtype="f")


grp = file.create_group("/PartType1")
grp.create_dataset("Coordinates",  data=sun_coord, dtype="f")
grp.create_dataset("Velocities", data=sun_vel, dtype="f")
grp.create_dataset("Masses", data=sun_mass, dtype="f")
grp.create_dataset("ParticleIDs", data=np.arange(gas_part_num+1))



file.close()