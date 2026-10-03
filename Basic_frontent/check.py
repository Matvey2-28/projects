import sys
print("Python:", sys.executable)
print("Версия:", sys.version)

try:
    import torch
    print("torch найден:", torch.__file__)
    print("torch версия:", torch.__version__)
    print("CUDA доступен:", torch.cuda.is_available())
except ImportError:
    print(" torch НЕ найден в этом окружении!")
    print("sys.path:", sys.path)