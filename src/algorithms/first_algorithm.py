import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import extractor
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_squared_error
from math import sqrt

a = 0.955

def calculate_smoothed_values(velocity, a):

    def smooth(step, prev, a):
        return (1-a)*step + a*prev

    smoothed_values = [0]

    # Reverse the EWMA formula
    x_approx = np.zeros_like(velocity)
    for n in range(1, len(velocity)):
        x_approx[n] = (velocity[n] - a * velocity[n-1]) / (1 - a)

    for i in range(0, len(velocity)):
        smoothed_values.append(smooth(x_approx[i], smoothed_values[i-1], a))
    
    return smoothed_values

def calculate_params(mact):

    _, X,Y,T = extractor.extract_coords_from_mact(mact)

    if len(X) == 0 or len(Y) == 0:
        return None
    
    X_VAL = X[:, 0]
    Y_VAL = Y[:, 0]
    
    velocityX = np.diff(X_VAL)
    velocityY = np.diff(Y_VAL)

    smoothed_valueX = calculate_smoothed_values(velocityX, a)
    smoothed_valueY = calculate_smoothed_values(velocityY, a)

    #apply pithagoras theorem
    smoothed_vel= np.sqrt(np.square(smoothed_valueX) + np.square(smoothed_valueY))
    velocity_total = np.sqrt(np.square(velocityX) + np.square(velocityY))

    if len(velocityX) != len(velocityY) or len(smoothed_vel) != len(velocity_total):
        print("Error: smoothed_vel and velocity_total are not the same length")
        return None

    #calculate pearson correlation between smoothed and total velocity
    pearson, _ = pearsonr(velocity_total, smoothed_vel)

    #calculate spearmans correlation between smoothed and total velocity
    corr, _ = spearmanr(velocity_total, smoothed_vel)

    #calculate cosine similarity between smoothed and total velocity
    cosine_similarity = cosine_similarity(velocity_total.reshape(1,-1), smoothed_vel.reshape(1,-1))

    # calculate rmse between smoothed and total velocity
    rmse = sqrt(mean_squared_error(velocity_total, smoothed_vel))
    
    return [pearson, corr, cosine_similarity[0][0], rmse]
