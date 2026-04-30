import yt
import os

file_path = r"C:\Users\user\Desktop\GitHub\projects\output.hdf5"
output_file = "plot.png"

print("Starting conversion...")

try:
    # Пробуем разные типы данных
    ds = yt.load(file_path)

    # Или с явным указанием типа (раскомментируйте нужный):
    # ds = yt.load(file_path, data_format="Enzo")
    # ds = yt.load(file_path, data_format="FLASH")
    # ds = yt.load(file_path, data_format="Gadget")

    field = ds.field_list[0] if ds.field_list else ("gas", "density")

    plot = yt.SlicePlot(ds, "z", field)
    plot.save(output_file)

    print(f"Done: {output_file}")

except Exception as e:
    print(f"yt failed: {e}")
    print("Your HDF5 file might not be from a supported simulation code")