import numpy as np
from scipy.signal import savgol_filter
import os, sys, json, datetime
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import extractor

#enable prnting of long numpy arrays
np.set_printoptions(threshold=np.inf)

mact = \
'0,1,472,652,1025;1,1,479,649,1021;2,1,487,643,1011;3,1,496,634,990;4,1,503,622,968;5,1,531,578,899;6,1,535,558,867;7,1,544,538,831;8,1,551,518,799;9,1,559,496,765;10,1,568,478,737;11,1,575,452,695;12,1,584,436,669;13,1,591,412,633;14,1,600,398,607;15,1,607,372,563;16,1,615,358,537;17,1,624,338,499;18,1,631,324,469;19,1,640,310,435;20,1,647,304,421;21,1,655,295,394;22,1,664,287,374;23,1,671,283,354;24,1,679,279,337;25,1,688,277,325;26,1,696,276,314;27,1,705,274,306;28,1,712,274,293;29,1,719,274,288;30,1,728,274,283;31,1,735,274,280;32,1,743,275,278;33,1,752,275,276;34,1,759,276,274;35,1,768,276,273;36,1,775,277,271;37,1,783,278,270;38,1,791,279,268;39,1,800,280,266;40,1,807,283,263;41,1,816,286,259;42,1,824,290,255;43,1,832,294,250;44,1,840,299,246;45,1,847,304,242;46,1,855,306,241;47,1,863,310,239;48,1,871,313,238;49,1,879,314,238;50,1,887,315,238;51,1,896,317,238;52,1,904,320,240;53,1,912,324,242;54,1,920,329,246;55,1,928,338,253;56,1,935,352,266;57,1,943,366,278;58,1,951,376,288;59,1,959,389,301;60,1,968,398,310;61,1,976,408,326;62,1,984,420,339;63,1,992,431,357;64,1,1001,447,381;65,1,1008,461,401;66,1,1016,473,417;67,1,1023,485,430;68,1,1032,489,436;69,1,1039,493,441;70,1,1048,495,444;71,1,1055,496,445;72,1,1064,497,446;73,1,1079,497,447;74,1,1087,498,448;75,1,1096,498,450;76,1,1103,499,452;77,1,1111,500,456;78,1,1119,502,462;79,1,1127,504,470;80,1,1135,507,481;81,1,1143,511,496;82,1,1152,516,515;83,1,1160,524,541;84,1,1168,530,565;85,1,1176,536,591;86,1,1184,540,607;87,1,1192,546,632;88,1,1200,552,668;89,1,1208,560,704;90,1,1216,564,730;91,1,1224,568,752;92,1,1232,570,772;93,1,1239,572,794;94,1,1248,574,816;95,1,1255,574,833;96,1,1264,574,847;97,1,1272,574,865;98,1,1280,574,884;99,1,1287,572,904;'
file = 'data.json'

coords, X,Y,T = extractor.extract_coords_from_mact(mact)

#print the value of X
print(X[:, 0])
print(Y[:, 0])

# Compute the Euclidean distance between consecutive points
distance = np.zeros(len(X) - 1)
TIME_DIFFERENCES = np.zeros(len(X) - 1) # vector of time differences
for i in range(len(X) - 1):
    dx = X[i+1] - X[i]
    dy = Y[i+1] - Y[i]
    dt = T[i+1] - T[i]

    TIME_DIFFERENCES[i] = dt
    distance[i] = np.sqrt(dx**2 + dy**2)


# Compute the velocity between consecutive points
velocities = distance / TIME_DIFFERENCES

# Smooth the velocities to make the plot better
velocities = savgol_filter(velocities, window_length=15, polyorder=2)

data = [{'velocity': velocity, 'time': time} for velocity, time in zip(velocities, TIME_DIFFERENCES[:-1])]

# Load existing data from the JSON file, if it exists
try:
    with open(file, 'r') as f:
        existing_data = json.load(f)
except FileNotFoundError:
    existing_data = []

# Separate the new data with a timestamp key and a list of dictionaries for the data
new_data = {'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'data': []}
for datum in data:
    if datum not in existing_data:
        new_data['data'].append(datum)

# Append the new data to the existing data
all_data = existing_data.copy()
if new_data['data']:
    all_data.append(new_data)

# Save the updated data to the JSON file
with open(file, 'w') as f:
    json.dump(all_data, f) 

# Plot the velocities
plt.plot(T[1:], velocities)
plt.show()