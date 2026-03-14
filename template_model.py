import shapely.geometry as geom
import numpy as np
import random
import h5py
import yaml
import sys

AU = 1.49e11 # Астрономическая единица, м
G = 6.67e-11 # Гравитационная постоянная, м^3/(кг*с^2)
M_SUN = 1.998e+30 # Масса Солнца, кг
GAMMA = 5.0 / 3.0 # Постоянная адиобатты
m_H = 2 * 1.6735575e-27 # Масса молекулы водорода, кг
n_H = 2e+12  # Характерная концентрация газа, частиц/м^3
MU_H = 0.002  # Молярная масса водорода, кг/моль
R = 8.3144598  # Газовая постоянная, Дж/(моль*К)
N_a = 6.0221409e+23 # Число Авогадро 
k = 1.38064852e-23 # Больцманская постоянная
ETA = 1.2348 # Коэффициент среднего расстояния между частицами SPH


def vel_calc(r):
    return np.sqrt(G * M_SUN / r)


def create_random_dist_model(temperature, # Температура, К
                             radius_interior, # Внутренний радиус газового диска
                             radius_exterior, # Внешний радиус газового диска
                             thickness # Толщина газового диска
                             ):

    x_centre = box_size / 2
    y_centre = box_size / 2
    z_centre = box_size / 2

    ############## PartType0 (Gas) ##############
    T = np.full(num_part, temperature)
    rho = np.full(num_part, n_H * m_H) # Плотность водорода, кг/м^3
    P = R / MU_H * rho * T
    # u = P / rho / (gamma - 1)
    u = 3  * k * T / m_H / 2

    radius_interior = AU * radius_interior
    radius_exterior = AU * radius_exterior
    thickness = AU * thickness

    V_disk = np.pi * (radius_exterior**2 - radius_interior**2) * thickness
    smth_lnght = np.full(num_part, (V_disk / num_part)**(1 / 3))

    pos = np.zeros([num_part, 3])
    vel = np.zeros([num_part, 3])
    masses = V_disk / num_part * rho
    smth_lnght = ETA * (masses / rho)**(1 / 3) * 10

    for i in range(0, num_part):
        theta = random.uniform(0, 2*np.pi)
        radius = random.uniform(radius_interior, radius_exterior)

        pos[i, 0] = x_centre + radius * np.cos(theta)
        pos[i, 1] = y_centre + radius * np.sin(theta)
        pos[i, 2] = z_centre + random.uniform(-thickness, thickness)

        vel[i, 0] = - vel_calc(radius) * np.sin(theta)
        vel[i, 1] = vel_calc(radius) * np.cos(theta)
        vel[i, 2] = 0

    ############## PartType1 (Dark Matter) ##############
    pos_star = np.zeros([1, 3])
    pos_star[0, 0], pos_star[0, 1], pos_star[0, 2] = (
        x_centre, y_centre, z_centre)
    vel_star = np.zeros([1, 3])
    mass_star = np.array([M_SUN])

    return ((pos, vel, masses, u, P, T, rho, smth_lnght),
            (pos, vel, masses, pos_star, vel_star, mass_star))


def coords_generator(r, N):
    phi = np.linspace(0, 2*np.pi, N)
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return np.array(list(zip(x, y)))


def _vel_calc(x, y):
    alpha = np.atan2(y, x)
    r = np.sqrt(x**2 + y**2)
    v_x = np.sqrt(G * M_SUN / r) * np.cos(alpha)
    v_y = np.sqrt(G * M_SUN / r) * np.sin(alpha)
    return v_x, v_y


def create_regular_dist_model(temperature, # Температура, К
                              radius_interior, # Внутренний радиус газового диска
                              radius_exterior, # Внешний радиус газового диска
                              thickness # Толщина газового диска
                              ):

    inner_polygon = geom.Polygon(coords_generator(radius_interior, 1000))
    outer_polygon = geom.Polygon(coords_generator(radius_exterior, 1000))
    points_numper_per_side = 200

    x_pictures_limits = [-radius_exterior, radius_exterior]
    y_pictures_limits = [-radius_exterior, radius_exterior]

    pos_xy = []
    vel_xy = []

    for x in np.linspace(*x_pictures_limits, points_numper_per_side):
        for y in np.linspace(*y_pictures_limits, points_numper_per_side):
            p = geom.Point(x, y)
            if p.within(outer_polygon) and not p.within(inner_polygon):
                pos_xy.append([x + box_size / 2, y + box_size / 2, 0])
                v_x, v_y = _vel_calc(x, y)
                vel_xy.append([v_x, v_y, 0])
    
    num_part = len(pos_xy)
    pos = np.array(pos_xy)
    vel = np.array(vel_xy)

    T = np.full(num_part, temperature)
    rho = np.full(num_part, n_H * m_H)
    P = R / MU_H * rho * T
    u = 3  * k * T / m_H / 2

    V_disk = np.pi * (radius_exterior**2 - radius_interior**2) * thickness
    smth_lnght = np.full(num_part, (V_disk / num_part)**(1 / 3))

    masses = V_disk / num_part * rho

    pos_star = np.array([[box_size / 2, box_size / 2, 0]])
    vel_star = np.array([[0, 0, 0]])
    mass_star = np.array([M_SUN])

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


def output_material_parts_data(pos, vel, masses, pos_star, vel_star, mass_star):
    return {
            ("dm", "particle_position_x"): pos[:, 0],
            ("dm", "particle_position_y"): pos[:, 1],
            ("dm", "particle_position_z"): pos[:, 2],
            ("dm", "particle_velocity_x"): vel[:, 0],
            ("dm", "particle_velocity_y"): vel[:, 1],
            
            ("dm", "particle_mass"): masses,
            ("star", "particle_position_x"): pos_star[:, 0],
            ("star", "particle_position_y"): pos_star[:, 1],
            ("star", "particle_position_z"): pos_star[:, 2],
            ("star", "particle_velocity_x"): vel_star[:, 0],
            ("star", "particle_velocity_y"): vel_star[:, 1],
            ("star", "particle_velocity_z"): vel_star[:, 2],
            ("star", "particle_mass"): mass_star,
        }


def output_meta_data():
    return {
            "length_unit": AU,
            "mass_unit": float(M_SUN),
            "time_unit": AU / vel_calc(box_size / 2),
            'box_size': box_size
        }


if __name__ == "__main__":
    import yt

    num_part = 500000
    box_size = 20 * AU
    radius_interior = AU * 0.6
    radius_exterior = AU * 1.2
    thickness = AU * 0.2
    temperature = 100

    gas_data, material_parts_data = create_regular_dist_model(temperature, radius_interior, radius_exterior, thickness)
    
    gas_data = output_gas_data(*gas_data)
    material_parts_data = output_material_parts_data(*material_parts_data)

    bbox = [[0, box_size], [0, box_size], [0, box_size]]
    ds_gas = yt.load_particles(gas_data, unit_system='mks', bbox=bbox)

    gas_pic_z = yt.SlicePlot(ds_gas, "z", ("gas", "particle_mass"),
                             center=[box_size / 2, box_size / 2, box_size / 2])
    gas_pic_z.set_cmap(field=("gas", "particle_mass"), cmap="inferno")
    gas_pic_z.save("gas_pic_z.png")

    ds_material_parts = yt.load_particles(material_parts_data, unit_system='mks', bbox=bbox)

    partcls_disk = yt.ParticlePlot(ds_material_parts, 
        ("dm", "particle_position_x"), 
        ("dm", "particle_position_y"),
        ("dm", "particle_position_z"),
        ("dm", "particle_mass"))
    partcls_disk.save("partcls_disk.png")

    star = yt.ParticlePlot(ds_material_parts, 
        ("star", "particle_position_x"), 
        ("star", "particle_position_y"),
        ("star", "particle_position_z"),
        ("star", "particle_mass"))
    star.save("star.png")
