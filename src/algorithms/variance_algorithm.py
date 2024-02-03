import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import extractor

a = 0.955  # Smoothing factor used in the MACT

def calculate_var(y,a):

    """
    Reverse the EWMA formula to calculate the variance of the clusters
    @param y: the input signal
    @param a: the smoothing factor
    @return: the variance of the clusters
    """

    # Reverse the EWMA formula
    x_approx = np.zeros_like(y)
    for n in range(1, len(y)):
        x_approx[n] = (y[n] - a * y[n-1]) / (1 - a)

    # We assume that the cluster size is 12
    cluster_size = 12

    variances = []
    #measure the variance of each cluster in an
    for i in range(0, len(y), cluster_size):
        variances.append(np.var(x_approx[i:i+cluster_size]))

    return variances

def calculate_params(mact):

    coords, X,Y,T = extractor.extract_coords_from_mact(mact)

    if len(X) == 0 or len(Y) == 0:
        return None
    
    X_VAL = X[:,0]
    Y_VAL = Y[:,0]

    velocityX = np.diff(X_VAL)
    velocityY = np.diff(Y_VAL)

    #if velocityX or velocityY contains NaN values, return None
    if np.isnan(velocityX).any() or np.isnan(velocityY).any():
        return None

    smoothed_valueX = calculate_var(velocityX, a)
    smoothed_valueY = calculate_var(velocityY, a)

    #if smoothed_valueX or smoothed_valueY contains NaN values, return None
    if np.isnan(smoothed_valueX).any() or np.isnan(smoothed_valueY).any():
        return None

    if len(smoothed_valueX) != len(smoothed_valueY):
        print("Error: smoothed_vel and velocity_total are not the same length")
        return None
    
    #concatenate into a single array
    smoothed_vel = np.concatenate([smoothed_valueX, smoothed_valueY])

    return smoothed_vel


