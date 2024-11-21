import os

needed = [2,46,70,74,139,169,202,230,276,369]

data_dir = '/home/muhammad-ali/github/AMAP/images'

for i in range(len(needed)):
    needed[i] = str(needed[i]) + '.jpg'
for j in os.listdir(data_dir):
    if j not in needed:
        os.remove(os.path.join(data_dir, j))

print(os.listdir(data_dir))