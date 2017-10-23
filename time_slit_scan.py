import os 
import sys
import numpy as np
import scipy.ndimage as spimg
import png

if len(sys.argv) != 3:
	print('[frame folder] [direction (x+,x-,y+,y-)]')
	exit()

print("loading frames")

frame_folder = sys.argv[1]
frame_files = os.listdir(frame_folder)
direction = sys.argv[2]

frames = []
for frame_file in frame_files:
	frame = spimg.imread(frame_folder + "/" + frame_file)
	frames.append(frame)

print("scanning frames")

pix_arr = np.zeros(frames[0].shape)

for i in range(len(frames)):
	fraction = i / (len(frames) - 1)
	next_fraction = (i + 1) / (len(frames) - 1)
	if direction == "x+":
		xs = int(fraction * pix_arr.shape[1])
		xe = int(next_fraction * pix_arr.shape[1])
		pix_arr[0:pix_arr.shape[0]-1,xs:xe] = frames[i][0:pix_arr.shape[0]-1,xs:xe]
	elif direction == "x-":
		xs = int((1 - fraction) * pix_arr.shape[1])
		xe = int((1 - next_fraction) * pix_arr.shape[1])
		pix_arr[0:pix_arr.shape[0]-1,xe:xs] = frames[i][0:pix_arr.shape[0]-1,xe:xs]
	elif direction == "y+":
		ys = int(fraction * pix_arr.shape[0])
		ye = int(next_fraction * pix_arr.shape[0])
		pix_arr[ys:ye,0:pix_arr.shape[1]-1] = frames[i][ys:ye,0:pix_arr.shape[1]-1]
	elif direction == "y-":
		ys = int((1 - fraction) * pix_arr.shape[0])
		ye = int((1 - next_fraction) * pix_arr.shape[0])
		pix_arr[ye:ys,0:pix_arr.shape[1]-1] = frames[i][ye:ys,0:pix_arr.shape[1]-1]

print("saving")

z = (65535*((pix_arr - pix_arr.min())/pix_arr.ptp())).astype(np.uint16)
with open('time_slit_scan.png', 'wb') as f:
	writer = png.Writer(width=z.shape[1], height=z.shape[0], bitdepth=16)
	z2list = z.reshape(-1, z.shape[1]*z.shape[2]).tolist()
	writer.write(f, z2list)

