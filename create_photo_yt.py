import h5py
import matplotlib.pyplot as plt
import numpy as np
import os

file_path = r"C:\Users\user\Desktop\GitHub\projects\output.hdf5"
output_image = "result_plot.png"

print("File check started")
print(f"File exists: {os.path.exists(file_path)}")

with h5py.File(file_path, 'r') as f:
    print("\n=== FILE STRUCTURE ===")


    def print_structure(name, obj):
        print(name, type(obj))
        if isinstance(obj, h5py.Dataset):
            print(f"  Shape: {obj.shape}")
            print(f"  Dtype: {obj.dtype}")


    f.visititems(print_structure)

    print("\n=== TOP LEVEL KEYS ===")
    print(list(f.keys()))

    # Пробуем каждый датасет
    datasets = []


    def collect_datasets(name, obj):
        if isinstance(obj, h5py.Dataset):
            datasets.append(name)


    f.visititems(collect_datasets)

    print(f"\nFound {len(datasets)} datasets: {datasets}")

    if datasets:
        for ds_name in datasets:
            print(f"\n=== CHECKING: {ds_name} ===")
            data = f[ds_name][:]
            print(f"Shape: {data.shape}")
            print(f"Dtype: {data.dtype}")
            print(f"Min: {np.min(data)}")
            print(f"Max: {np.max(data)}")
            print(f"Mean: {np.mean(data)}")
            print(f"Has NaN: {np.any(np.isnan(data))}")
            print(f"Sample data (first 5): {data.flat[:5] if data.size > 0 else 'empty'}")

            # Сохраняем
            if len(data.shape) >= 2 and data.shape[-1] > 1 and data.shape[-2] > 1:
                plt.figure(figsize=(10, 8))

                if len(data.shape) == 2:
                    plot_data = data
                elif len(data.shape) == 3:
                    plot_data = data[data.shape[0] // 2]
                else:
                    continue

                print(f"Plotting data range: {np.min(plot_data)} to {np.max(plot_data)}")

                if np.max(plot_data) - np.min(plot_data) == 0:
                    print("WARNING: All values are the same!")

                plt.imshow(plot_data, cmap='viridis', origin='lower')
                plt.colorbar()
                plt.title(
                    f"{ds_name}\nShape: {plot_data.shape}\nRange: [{np.min(plot_data):.4f}, {np.max(plot_data):.4f}]")
                plt.savefig(output_image, dpi=300, bbox_inches='tight')
                plt.close()
                print(f"Saved to {output_image}")
                break
            else:
                print("Skipping - not 2D/3D data")