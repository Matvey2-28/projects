import matplotlib.pyplot as plt
import numpy as np

def log_sp(b=0.5):
    
    f = np.arange(0, 8*np.pi, 0.01)
    r = np.exp(b * f)
    
    x = r * np.cos(f)
    y = r * np.sin(f)
    
    plt.plot(x, y)
    plt.savefig('log_sp.png')
    plt.close()
    
def arh_sp(k=0.5):
    
    f = np.arange(0, 8*np.pi, 0.01)
    r = k * f
    
    x = r * np.cos(f)
    y = r * np.sin(f)
    
    plt.plot(x, y)
    plt.savefig('arh_sp.png')
    plt.close()
    
def zhezl_sp(k=0.5):
    
    f = np.arange(0.01, 8*np.pi, 0.01)
    r = k / np.sqrt(f)
    
    x = r * np.cos(f)
    y = r * np.sin(f)
    
    plt.plot(x, y)
    plt.savefig('zhezl_sp.png')
    plt.close()
    
def rose(k=9):
    
    f = np.arange(0.01, 8*np.pi, 0.01)
    r = np.sin(k * f)
    
    x = r * np.cos(f)
    y = r * np.sin(f)
    
    plt.plot(x, y)
    plt.savefig('rose.png')
    plt.close()
    
if __name__ == '__main__':
    log_sp()
    arh_sp()
    zhezl_sp()
    rose()
    
    