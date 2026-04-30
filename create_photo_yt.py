import h5py
import matplotlib.pyplot as plt
import numpy as np

file_path = r"C:\Users\user\Desktop\GitHub\projects\output.hdf5"

print("Reading HDF5 file...")

with h5py.File(file_path, 'r') as f:
    # Показываем структуру
    print("\nKeys in file:", list(f.keys()))


    # Ищем данные
    def find_data(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"\nFound dataset: {name}")
            print(f"Shape: {obj.shape}")
            print(f"Data type: {obj.dtype}")

            # Читаем данные
            data = obj[:]
            print(f"Min: {np.min(data)}, Max: {np.max(data)}")

            # Сохраняем как картинку если 2D или 3D
            if len(data.shape) == 2:
                plt.figure()
                plt.imshow(data, cmap='viridis')
                plt.colorbar()
                plt.savefig('output.png', dpi=300)
                plt.close()
                print("Saved 2D plot to output.png")

            elif len(data.shape) == 3:
                # Берем средний срез
                mid = data.shape[0] // 2
                plt.figure()
                plt.imshow(data[mid], cmap='viridis')
                plt.colorbar()
                plt.savefig('output.png', dpi=300)
                plt.close()
                print(f"Saved 3D slice (z={mid}) to output.png")


    f.visititems(find_data)

print("Done")