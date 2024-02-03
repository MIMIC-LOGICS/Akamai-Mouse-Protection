import numpy as np


def extract_coords_from_mact(mact):
    """
    Extracts the coordinates from a mact string
    :param mact: mact string
    :return: coordinates, x, y, t
    """

    #remove " character from the string
    mact = mact.replace('"', '')
    
    mact_parsed = str(mact).split(";")
    X = []
    Y = []
    T = []
    coords = []
    
    for i in range(0, np.size(mact_parsed) - 1):
        value = mact_parsed[i].split(",")

        # remove clicks
        if len(value) == 6:
            continue #remove click

        x = int(value[3])
        y = int(value[4])
        t = int(value[2])

        T.append(t)
        X.append([x])
        Y.append([y])
        coords.append([x,y])

    coords = np.asarray(coords)
    X = np.asarray(X)
    Y = np.asarray(Y)
    T = np.asarray(T)
    return coords, X, Y, T


