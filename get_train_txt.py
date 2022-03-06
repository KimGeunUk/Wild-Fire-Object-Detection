import os

path_dir = '/home/oem/opencv/opencv-4.4.0/build/darknet/custom/fireV1V2V3V4/'

file_list = os.listdir(path_dir + 'obj')

f = open(path_dir + 'train.txt', 'w')

for i in file_list:
    if i[-4:] != '.txt':
        f.write('custom/fireV1V2V3V4/obj/' + i + '\n')

f.close()