import h5py
import os

path = r"C:\Users\user\Desktop\Github\projects\output.hdf5"
print(f"Существует: {os.path.exists(path)}")

if os.path.exists(path):
    with h5py.File(path, 'r') as f:
        print(f"Ключи: {list(f.keys())}")
        print(f"Атрибуты: {dict(f.attrs)}")