import os 
import sys
import numpy as np
import scipy.ndimage as spimg
import png

if len(sys.argv) != 2:
	print('[frame folder]')
	exit()

print("loading frames")

frame_folder = sys.argv[1]
frame_files = os.listdir(frame_folder)

frames = []
for frame_file in frame_files:
	frame = spimg.imread(frame_folder + "/" + frame_file)
	frames.append(frame)

print("blending frames")

pix_arr = np.zeros(frames[0].shape)

for i in range(len(frames)):
	fraction = i / (len(frames) - 1)
	blended_frame = frames[i]
	pix_arr += blended_frame
	
print("saving")

z = (65535*((pix_arr - pix_arr.min())/pix_arr.ptp())).astype(np.uint16)
with open('time_blend.png', 'wb') as f:
	writer = png.Writer(width=z.shape[1], height=z.shape[0], bitdepth=16)
	z2list = z.reshape(-1, z.shape[1]*z.shape[2]).tolist()
	writer.write(f, z2list)

