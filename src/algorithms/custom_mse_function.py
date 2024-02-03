import numpy as np
def custom_asymmetric_train(y_true, y_pred):
    try:
        residual = (y_true - y_pred).astype("float")
        # gradient of the MSE (y_true - y_pred)^2, https://www.geeksforgeeks.org/ml-gradient-boosting/ explain the negative sign
        grad = np.where(residual<0, -2*100.0*residual, -2*residual)
        hess = np.where(residual<0, 2*100.0, 2.0)
    except:
        residual = (y_true - y_pred.label).astype("float")
        grad = np.where(residual<0, -2*100.0*residual, -2*residual)
        hess = np.where(residual<0, 2*100.0, 2.0)
    return grad, hess
