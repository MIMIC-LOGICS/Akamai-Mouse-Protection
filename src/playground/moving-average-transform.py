import matplotlib.pyplot as plt
import numpy as np

# Parameters
a = 0.955  # Smoothing factor
N1, N2 = 50, 75  # Step change points
u1, u2, u3 = 2, 5, 3  # Step values

# Generate the input signal
x = np.ones(300) * u1
x[200:212] = 5
x[212:225] = 8
x[225:237] = 2
x[237:250] = 2
x[250:262] = 5
x[262:275] = 7
x[275:282] = 10
x[282:300] = 1

# Apply the filter
y = np.zeros_like(x)
for n in range(1, len(x)):
    y[n] = a * y[n-1] + (1 - a) * x[n]

# Plot
plt.plot(x, label='Input')
plt.plot(y, label='Filtered Output')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.legend()
plt.title('Response of EWMA Filter to Step Inputs')
plt.show()
