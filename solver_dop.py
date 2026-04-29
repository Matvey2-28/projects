import numpy as np
import h5py
import yaml
from scipy.spatial import cKDTree
from typing import Union
import parser

float_type = np.float64
int_type = np.int32

class Solver:
    def __init__(self, model_data):
        self.GAS_DISKS = model_data.get_gas_disks()
        self.SPHERES = model_data.get_spheres()
        self.ARBITARY_CLUSTERS = model_data.get_arbitrary_clusters()
        self.MATERIAL_POINTS = model_data.get_material_points()
        
        # BOX_SIZE: [0] - это список из одного элемента, [0] - сам элемент (кортеж или число)
        bs_raw = model_data.get_box_size()[0]
        self.BOX_SIZE = bs_raw[0] * 1.49e11 if isinstance(bs_raw, tuple) and bs_raw[1] == 'ae' else bs_raw

        # TIME_PERIOD
        tp_raw = model_data.get_time_period()
        self.TIME_END = tp_raw[0][0] if isinstance(tp_raw[0], tuple) else tp_raw[0]
        self.DELTA_TIME = tp_raw[1][0] if isinstance(tp_raw[1], tuple) else tp_raw[1]

    def solve(self, output_path: str):
        # Параметры физики
        AU = 1.49e11
        G = 6.67e-11
        M_SUN = 1.998e+30
        GAMMA = 5.0 / 3.0
        m_H = 2 * 1.6735575e-27
        n_H = 2e+12
        MU_H = 0.002
        R = 8.3144598
        N_a = 6.0221409e+23
        k = 1.38064852e-23
        ETA = 1.2348

        def calculate_smoothing_lengths(
            coordinates: np.ndarray,
            boxsize=None,
            n_neighbors=32,
            kernel_gamma=1.4,
            dimension=3,
            use_periodic=False
        ) -> np.ndarray:
            coordinates = np.asarray(coordinates, dtype=np.float64)
            n_particles = len(coordinates)
            if n_particles == 0:
                return np.array([], dtype=np.float64)

            if use_periodic and boxsize is not None:
                if np.isscalar(boxsize):
                    box_arr = np.full(3, float(boxsize), dtype=np.float64)
                else:
                    box_arr = np.asarray(boxsize, dtype=np.float64).reshape(3)
                tree = cKDTree(coordinates, boxsize=box_arr)
            else:
                tree = cKDTree(coordinates)

            k_estimate = min(n_neighbors * 2, n_particles - 1)
            h_lengths = np.empty(n_particles, dtype=np.float64)
            kernel_volume_factor = (4.0 / 3.0) * np.pi * (kernel_gamma ** 3)
            block_size = 8192

            for start in range(0, n_particles, block_size):
                end = min(start + block_size, n_particles)
                distances, _ = tree.query(coordinates[start:end], k=k_estimate, workers=-1)
                r_k = distances[:, -1] if k_estimate > 1 else distances
                local_volume = (4.0 / 3.0) * np.pi * (r_k ** 3)
                local_density = k_estimate / np.maximum(local_volume, 1e-40)
                h_lengths[start:end] = np.power(
                    n_neighbors / (local_density * kernel_volume_factor + 1e-40),
                    1.0 / dimension
                )

            if boxsize is not None:
                b_val = boxsize if np.isscalar(boxsize) else np.min(boxsize)
                h_min = 1e-6 * b_val
                h_max = 0.1 * b_val
            else:
                coord_range = np.ptp(coordinates)
                h_min = max(1e-6, coord_range * 1e-4)
                h_max = coord_range * 0.1
            h_lengths = np.clip(h_lengths, h_min, h_max)
            return h_lengths

        def create_point_cube_3d(V_FIGURE, Lx, Ly, Lz):
            """
            Генерирует FCC-подобную упаковку в прямоугольный параллелепипед размером Lx × Ly × Lz.
            Возвращает x, y, z в локальной системе координат (центр = 0).
            """
            h_grid = (((V_FIGURE / 15000) * 3) / (4 * np.pi))**(1 / 3) / 1.5
            x, y, z = [], [], []

            x0, y0, z0 = -Lx/2, -Ly/2, -Lz/2
            x1, y1, z1 = Lx/2, Ly/2, Lz/2
            x_step = h_grid * 2
            y_step = h_grid * 2 * np.sqrt(3)
            z_step = h_grid * 4 * np.sqrt(2 / 3)

            # 4 слоя (FCC)
            for dz in [0, z_step/2]:
                for z_now in np.arange(z0 + dz, z1, z_step):
                    for dy in [0, y_step/2]:
                        for y_now in np.arange(y0 + dy, y1, y_step):
                            for x_now in np.arange(x0, x1, x_step):
                                x.append(x_now)
                                y.append(y_now)
                                z.append(z_now)

            return np.array(x), np.array(y), np.array(z)

        def vel_calc_clockwise(x, y):
            alpha = np.arctan2(y, x)
            r = np.sqrt(x**2 + y**2)
            v_x = -np.sqrt(G * M_SUN / r) * np.sin(alpha)
            v_y = np.sqrt(G * M_SUN / r) * np.cos(alpha)
            v_z = 0
            return v_x, v_y, v_z

        def vel_calc_counterclockwise(x, y):
            alpha = np.arctan2(y, x)
            r = np.sqrt(x**2 + y**2)
            v_x = np.sqrt(G * M_SUN / r) * np.sin(alpha)
            v_y = -np.sqrt(G * M_SUN / r) * np.cos(alpha)
            v_z = 0
            return v_x, v_y, v_z

        def create_gas_disk():
            pos, vel, masses, u, P, T, rho, smth_lnght = [], [], [], [], [], [], [], []
            for gd in self.GAS_DISKS:
                num_part = gd[2][0] if isinstance(gd[2], tuple) else gd[2]
                r_ext = (gd[3][0] if isinstance(gd[3], tuple) else gd[3]) * AU
                r_int = (gd[4][0] if isinstance(gd[4], tuple) else gd[4]) * AU
                thickness = (gd[5][0] if isinstance(gd[5], tuple) else gd[5]) * AU
                x0 = (gd[6][0] if isinstance(gd[6], tuple) else gd[6]) * AU
                y0 = (gd[7][0] if isinstance(gd[7], tuple) else gd[7]) * AU
                z0 = (gd[8][0] if isinstance(gd[8], tuple) else gd[8]) * AU
                phys_func = gd[9][0] if isinstance(gd[9], tuple) else gd[9]
                temp_min = gd[10][0] if isinstance(gd[10], tuple) else gd[10]
                direction = gd[11][0] if isinstance(gd[11], tuple) else gd[11]

                V_disk = np.pi * (r_ext**2 - r_int**2) * thickness
                x_loc, y_loc, z_loc = create_point_cube_3d(V_disk, 2*r_ext, 2*r_ext, thickness)

                # ФИЛЬТРАЦИЯ В ЛОКАЛЬНОЙ СИСТЕМЕ КООРДИНАТ ДИСКА (центр = 0)
                r_xy = np.sqrt(x_loc**2 + y_loc**2)
                mask = (r_xy <= r_ext) & (r_xy >= r_int)
                x_loc = x_loc[mask]
                y_loc = y_loc[mask]
                z_loc = z_loc[mask]

                # Смещение в глобальную систему: центр диска → (x0, y0, z0), а затем в коробку
                x_glob = x_loc + x0 + self.BOX_SIZE / 2
                y_glob = y_loc + y0 + self.BOX_SIZE / 2
                z_glob = z_loc + z0 + self.BOX_SIZE / 2

                cpos = np.column_stack([x_glob, y_glob, z_glob])

                # Скорости: относительно центра диска (x_loc, y_loc)
                cvel = np.zeros_like(cpos)
                for i in range(len(cpos)):
                    dx = x_loc[i]
                    dy = y_loc[i]
                    if direction == 'clockwise':
                        vx, vy, vz = vel_calc_clockwise(dx, dy)
                    else:
                        vx, vy, vz = vel_calc_counterclockwise(dx, dy)
                    cvel[i] = [vx, vy, vz]

                # Физика: T, rho — в локальных координатах (относительно центра диска)
                if phys_func == 'bell':
                    T_local = temp_min * np.exp((-0.5 * (x_loc / AU) ** 2 - (1.5 * (y_loc / AU) ** 2)))
                    rho_local = n_H * m_H * np.exp((-0.5 * (x_loc / AU) ** 2 - (1.5 * (y_loc / AU) ** 2)))
                else:
                    dist = np.sqrt(x_loc**2 + y_loc**2)
                    factor = AU / np.maximum(dist, 1e-9)
                    T_local = temp_min * factor
                    rho_local = n_H * m_H * factor

                P_local = R / MU_H * rho_local * T_local
                u_local = 3 * k * T_local / m_H / 2
                masses_local = (V_disk / num_part) * rho_local
                h_local = calculate_smoothing_lengths(cpos)

                pos.append(cpos)
                vel.append(cvel)
                masses.append(masses_local)
                u.append(u_local)
                P.append(P_local)
                T.append(T_local)
                rho.append(rho_local)
                smth_lnght.append(h_local)

            if not pos:
                return np.empty((0,3)), np.empty((0,3)), np.empty(0), np.empty(0), np.empty(0), np.empty(0), np.empty(0), np.empty(0)
            return (
                np.vstack(pos),
                np.vstack(vel),
                np.hstack(masses),
                np.hstack(u),
                np.hstack(P),
                np.hstack(T),
                np.hstack(rho),
                np.hstack(smth_lnght)
            )

        def create_sphere():
            pos, vel, masses, u, P, T, rho, smth_lnght = [], [], [], [], [], [], [], []
            for sp in self.SPHERES:
                num_part = sp[2][0] if isinstance(sp[2], tuple) else sp[2]
                r_ext = (sp[3][0] if isinstance(sp[3], tuple) else sp[3]) * AU
                x0 = (sp[4][0] if isinstance(sp[4], tuple) else sp[4]) * AU
                y0 = (sp[5][0] if isinstance(sp[5], tuple) else sp[5]) * AU
                z0 = (sp[6][0] if isinstance(sp[6], tuple) else sp[6]) * AU
                phys_func = sp[7][0] if isinstance(sp[7], tuple) else sp[7]
                temp_min = sp[8][0] if isinstance(sp[8], tuple) else sp[8]
                direction = sp[9][0] if isinstance(sp[9], tuple) else sp[9]

                V_sphere = (4/3) * np.pi * r_ext**3
                x_loc, y_loc, z_loc = create_point_cube_3d(V_sphere, 2*r_ext, 2*r_ext, 2*r_ext)

                # Фильтрация в локальной системе: внутри сферы
                r = np.sqrt(x_loc**2 + y_loc**2 + z_loc**2)
                mask = r <= r_ext
                x_loc = x_loc[mask]
                y_loc = y_loc[mask]
                z_loc = z_loc[mask]

                # Смещение в глобальную систему
                x_glob = x_loc + x0 + self.BOX_SIZE / 2
                y_glob = y_loc + y0 + self.BOX_SIZE / 2
                z_glob = z_loc + z0 + self.BOX_SIZE / 2
                cpos = np.column_stack([x_glob, y_glob, z_glob])

                # Скорости: относительно центра сферы (x_loc, y_loc)
                cvel = np.zeros_like(cpos)
                for i in range(len(cpos)):
                    dx = x_loc[i]
                    dy = y_loc[i]
                    if direction == 'clockwise':
                        vx, vy, vz = vel_calc_clockwise(dx, dy)
                    else:
                        vx, vy, vz = vel_calc_counterclockwise(dx, dy)
                    cvel[i] = [vx, vy, vz]

                # Физика — в локальных координатах
                if phys_func == 'bell':
                    T_local = temp_min * np.exp((-0.5 * (x_loc / AU) ** 2 - (1.5 * (y_loc / AU) ** 2) - (2.5 * (z_loc / AU) ** 2)))
                    rho_local = n_H * m_H * np.exp((-0.5 * (x_loc / AU) ** 2 - (1.5 * (y_loc / AU) ** 2)))
                else:
                    dist = np.sqrt(x_loc**2 + y_loc**2 + z_loc**2)
                    factor = AU / np.maximum(dist, 1e-9)
                    T_local = temp_min * factor
                    rho_local = n_H * m_H * factor

                P_local = R / MU_H * rho_local * T_local
                u_local = 3 * k * T_local / m_H / 2
                masses_local = (V_sphere / num_part) * rho_local
                h_local = calculate_smoothing_lengths(cpos)

                pos.append(cpos)
                vel.append(cvel)
                masses.append(masses_local)
                u.append(u_local)
                P.append(P_local)
                T.append(T_local)
                rho.append(rho_local)
                smth_lnght.append(h_local)

            if not pos:
                return np.empty((0,3)), np.empty((0,3)), np.empty(0), np.empty(0), np.empty(0), np.empty(0), np.empty(0), np.empty(0)
            return (
                np.vstack(pos),
                np.vstack(vel),
                np.hstack(masses),
                np.hstack(u),
                np.hstack(P),
                np.hstack(T),
                np.hstack(rho),
                np.hstack(smth_lnght)
            )

        def create_arbitrary_cluster():
            pos, vel, masses, u, P, T, rho, smth_lnght = [], [], [], [], [], [], [], []

            for ac in self.ARBITARY_CLUSTERS:
                # === 1. Извлечение параметров с учётом unit (через parser → _clean_json)
                num_part = ac[2][0] if isinstance(ac[2], tuple) else ac[2]
                r_ext = (ac[3][0] if isinstance(ac[3], tuple) else ac[3]) * AU
                math_func_str = ac[4][0] if isinstance(ac[4], tuple) else ac[4]
                z_lim = (ac[5][0] if isinstance(ac[5], tuple) else ac[5]) * AU
                x0 = (ac[6][0] if isinstance(ac[6], tuple) else ac[6]) * AU
                y0 = (ac[7][0] if isinstance(ac[7], tuple) else ac[7]) * AU
                z0 = (ac[8][0] if isinstance(ac[8], tuple) else ac[8]) * AU
                phys_func = ac[9][0] if isinstance(ac[9], tuple) else ac[9]
                temp_min = ac[10][0] if isinstance(ac[10], tuple) else ac[10]
                direction = ac[11][0] if isinstance(ac[11], tuple) else ac[11]

                # === 2. Генерация плотной кубической сетки в локальной системе (центр = 0)
                V_est = (4/3) * np.pi * r_ext**3
                x_loc, y_loc, z_loc = create_point_cube_3d(V_est, 2*r_ext, 2*r_ext, 2*z_lim)

                # === 3. ПРОСТАЯ ПРОВЕРКА УСЛОВИЯ ПО ФУНКЦИИ — КЛЮЧЕВОЙ БЛОК
                delta = 0.1 * r_ext  # толщина стенки = 10% от радиуса

                mask = np.ones(len(x_loc), dtype=bool)

                # Подстановка в функцию: вычисляем f(x) или f(y), сравниваем с y или x
                if math_func_str == "y=x**2":
                    f_vals = x_loc**2
                    mask &= np.abs(y_loc - f_vals) <= delta
                elif math_func_str == "y=-x**2":
                    f_vals = -x_loc**2
                    mask &= np.abs(y_loc - f_vals) <= delta
                elif math_func_str == "x=y**2":
                    f_vals = y_loc**2
                    mask &= np.abs(x_loc - f_vals) <= delta
                elif math_func_str == "x=-y**2":
                    f_vals = -y_loc**2
                    mask &= np.abs(x_loc - f_vals) <= delta
                else:
                    # Если не распознана — используем цилиндр как fallback
                    mask &= (x_loc**2 + y_loc**2) <= r_ext**2

                # Ограничение по Z и радиусу
                mask &= np.abs(z_loc) <= z_lim
                mask &= (x_loc**2 + y_loc**2) <= r_ext**2

                x_loc = x_loc[mask]
                y_loc = y_loc[mask]
                z_loc = z_loc[mask]

                # === 4. Смещение в глобальную систему координат
                x_glob = x_loc + x0 + self.BOX_SIZE / 2
                y_glob = y_loc + y0 + self.BOX_SIZE / 2
                z_glob = z_loc + z0 + self.BOX_SIZE / 2
                cpos = np.column_stack([x_glob, y_glob, z_glob])

                # === 5. Скорости — вращение вокруг оси Z (как у дисков)
                cvel = np.zeros_like(cpos)
                for i in range(len(cpos)):
                    dx, dy = x_loc[i], y_loc[i]  # относительно центра тела
                    if direction == 'clockwise':
                        vx, vy, vz = vel_calc_clockwise(dx, dy)
                    else:
                        vx, vy, vz = vel_calc_counterclockwise(dx, dy)
                    cvel[i] = [vx, vy, vz]

                # === 6. Физика (T, rho) — в локальных координатах
                if phys_func == 'bell':
                    T_local = temp_min * np.exp(
                        -0.5 * (x_loc / AU)**2
                        -1.5 * (y_loc / AU)**2
                        -2.5 * (z_loc / AU)**2
                    )
                    rho_local = n_H * m_H * np.exp(
                        -0.5 * (x_loc / AU)**2
                        -1.5 * (y_loc / AU)**2
                    )
                else:  # 'radius'
                    dist_xy = np.sqrt(x_loc**2 + y_loc**2)
                    factor = AU / np.maximum(dist_xy, 1e-9)
                    T_local = temp_min * factor
                    rho_local = n_H * m_H * factor

                P_local = R / MU_H * rho_local * T_local
                u_local = 3 * k * T_local / m_H / 2
                V_actual = (4/3) * np.pi * r_ext**3
                masses_local = (V_actual / num_part) * rho_local
                h_local = calculate_smoothing_lengths(cpos)

                pos.append(cpos)
                vel.append(cvel)
                masses.append(masses_local)
                u.append(u_local)
                P.append(P_local)
                T.append(T_local)
                rho.append(rho_local)
                smth_lnght.append(h_local)

            if not pos:
                return np.empty((0,3)), np.empty((0,3)), np.empty(0), np.empty(0), np.empty(0), np.empty(0), np.empty(0), np.empty(0)
            return (
                np.vstack(pos),
                np.vstack(vel),
                np.hstack(masses),
                np.hstack(u),
                np.hstack(P),
                np.hstack(T),
                np.hstack(rho),
                np.hstack(smth_lnght)
            )

        def create_material_points():
            pos, vel, masses = [], [], []
            for mp in self.MATERIAL_POINTS:
                mass = mp[2][0] if isinstance(mp[2], tuple) else mp[2]
                x0 = (mp[3][0] if isinstance(mp[3], tuple) else mp[3]) * AU
                y0 = (mp[4][0] if isinstance(mp[4], tuple) else mp[4]) * AU
                z0 = (mp[5][0] if isinstance(mp[5], tuple) else mp[5]) * AU  # ← исправлено: Z0 теперь тоже в метрах
                vx = mp[6][0] if isinstance(mp[6], tuple) else mp[6]
                vy = mp[7][0] if isinstance(mp[7], tuple) else mp[7]
                vz = mp[8][0] if isinstance(mp[8], tuple) else mp[8]

                pos.append([x0 + self.BOX_SIZE / 2, y0 + self.BOX_SIZE / 2, z0 + self.BOX_SIZE / 2])
                vel.append([vx, vy, vz])
                masses.append(mass)

            return np.array(pos), np.array(vel), np.array(masses)

        # --- Генерация всех компонент ---
        gas_pos, gas_vel, gas_masses, gas_u, gas_P, gas_T, gas_rho, gas_h = create_gas_disk()
        sph_pos, sph_vel, sph_masses, sph_u, sph_P, sph_T, sph_rho, sph_h = create_sphere()
        arb_pos, arb_vel, arb_masses, arb_u, arb_P, arb_T, arb_rho, arb_h = create_arbitrary_cluster()
        mat_pos, mat_vel, mat_masses = create_material_points()

        # --- Объединение всех данных ---
        all_gas_arrays = [arr for arr in [gas_pos, sph_pos, arb_pos] if arr.size > 0]
        all_gas_pos = np.vstack(all_gas_arrays) if all_gas_arrays else np.empty((0,3))
        all_gas_vel = np.vstack([arr for arr in [gas_vel, sph_vel, arb_vel] if arr.size > 0]) if any(arr.size > 0 for arr in [gas_vel, sph_vel, arb_vel]) else np.empty((0,3))
        all_gas_masses = np.hstack([arr for arr in [gas_masses, sph_masses, arb_masses] if arr.size > 0]) if any(arr.size > 0 for arr in [gas_masses, sph_masses, arb_masses]) else np.empty(0)
        all_gas_u = np.hstack([arr for arr in [gas_u, sph_u, arb_u] if arr.size > 0]) if any(arr.size > 0 for arr in [gas_u, sph_u, arb_u]) else np.empty(0)
        all_gas_P = np.hstack([arr for arr in [gas_P, sph_P, arb_P] if arr.size > 0]) if any(arr.size > 0 for arr in [gas_P, sph_P, arb_P]) else np.empty(0)
        all_gas_T = np.hstack([arr for arr in [gas_T, sph_T, arb_T] if arr.size > 0]) if any(arr.size > 0 for arr in [gas_T, sph_T, arb_T]) else np.empty(0)
        all_gas_rho = np.hstack([arr for arr in [gas_rho, sph_rho, arb_rho] if arr.size > 0]) if any(arr.size > 0 for arr in [gas_rho, sph_rho, arb_rho]) else np.empty(0)
        all_gas_h = np.hstack([arr for arr in [gas_h, sph_h, arb_h] if arr.size > 0]) if any(arr.size > 0 for arr in [gas_h, sph_h, arb_h]) else np.empty(0)

        # --- Запись в HDF5 ---
        IC = h5py.File(output_path, 'w')

        num_gas = len(all_gas_pos)
        num_mat = len(mat_pos)
        total_parts = [num_gas, num_mat, 0, 0, 0, 0] # PartType0, PartType1, ...

        grp = IC.create_group("/Header")
        grp.attrs["BoxSize"] = np.array([self.BOX_SIZE, self.BOX_SIZE, self.BOX_SIZE], dtype=np.float64)
        grp.attrs["NumPart_Total"] = np.array(total_parts, dtype=np.int32)
        grp.attrs["NumPart_Total_HighWord"] = np.array([0, 0, 0, 0, 0, 0], dtype=np.int32)
        grp.attrs["NumPart_ThisFile"] = np.array(total_parts, dtype=np.int32)
        grp.attrs["Time"] = 0.0
        grp.attrs["NumFileOutputsPerSnapshot"] = 1
        grp.attrs["MassTable"] = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64)
        grp.attrs["Flag_Entropy_ICs"] = np.array([0, 0, 0, 0, 0, 0], dtype=np.int32)
        grp.attrs["Dimension"] = 3

        grp = IC.create_group("/Units")
        grp.attrs["Unit length in cgs (U_L)"] = 100.0
        grp.attrs["Unit mass in cgs (U_M)"] = 1000.0
        grp.attrs["Unit time in cgs (U_t)"] = 1.0
        grp.attrs["Unit current in cgs (U_I)"] = 1.0
        grp.attrs["Unit temperature in cgs (U_T)"] = 1.0

        # PartType0 - Все газовые тела (диски, сферы, скопления)
        if num_gas > 0:
            grp = IC.create_group("/PartType0")
            grp.create_dataset("Coordinates", data=all_gas_pos.astype(np.float64))
            grp.create_dataset("Velocities", data=all_gas_vel.astype(np.float64))
            grp.create_dataset("Masses", data=all_gas_masses.astype(np.float64))
            grp.create_dataset("SmoothingLength", data=all_gas_h.astype(np.float64))
            grp.create_dataset("InternalEnergy", data=all_gas_u.astype(np.float64))
            grp.create_dataset("ParticleIDs", data=np.arange(0, num_gas, dtype=np.int64))
            grp.create_dataset("Density", data=all_gas_rho.astype(np.float64))

        # PartType1 - Материальные точки
        if num_mat > 0:
            grp = IC.create_group("/PartType1")
            grp.create_dataset("Coordinates", data=mat_pos.astype(np.float64))
            grp.create_dataset("Velocities", data=mat_vel.astype(np.float64))
            grp.create_dataset("Masses", data=mat_masses.astype(np.float64))
            grp.create_dataset("ParticleIDs", data=np.arange(num_gas, num_gas + num_mat, dtype=np.int64))

        IC.close()
        print(f"HDF5 файл '{output_path}' успешно создан.")