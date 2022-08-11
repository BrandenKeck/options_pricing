import numpy as np
import matplotlib.pyplot as plt

def wiener_process(n, m, x0=0, dt=0.01):
    X = np.zeros([n, m])
    X[:,0] = x0
    N = np.random.normal(0, np.sqrt(dt), [n, m])
    for ii in np.arange(1,m):
        X[:,ii] = np.sum(N[:,:ii], 1)
    return X

def geometric_brownian_motion(n, m, x0=100, dt=0.01, mu=0.1, sig=0.3):
    N = np.exp(
        (mu - sig**2 / 2)*dt
        + sig * np.random.normal(0, np.sqrt(dt), [n,m])
    )
    N.shape
    X = np.hstack([np.reshape(x0*np.ones(n),(-1,1)), N]).cumprod(axis=1)
    return X

xx = wiener_process(100, 1000)
[plt.plot(np.arange(len(x)), x) for x in xx]

xx = wiener_process(100, 100, dt=0.1)
[plt.plot(np.arange(len(x)), x) for x in xx]

xx = geometric_brownian_motion(100, 1000)
[plt.plot(np.arange(len(x)), x) for x in xx]
