import os 
import sys
import numpy as np
import scipy.ndimage as spimg
import png
import math

if len(sys.argv) != 4:
	print('[frame folder] [blend (add/max)] [color (#_#_#)] [color (#_#_#)]')
	exit()

print("loading frames")

frame_folder = sys.argv[1]
frame_files = os.listdir(frame_folder)
blend_style = sys.argv[2]
if blend_style not in ["add", "max"]:
	print("[blend (add/max)]")
	exit()
color0 = np.zeros((3))
for i in range(3):
	color0[i] = float(sys.argv[3].split('_')[i])
color1 = np.zeros((3))
for i in range(3):
	color1[i] = float(sys.argv[4].split('_')[i])


frames = []
for frame_file in frame_files:
	frame = spimg.imread(frame_folder + "/" + frame_file)
	frames.append(frame)

print("blending frames")

pix_arr = np.zeros(frames[0].shape)

for i in range(len(frames)):
	fraction = i / (len(frames) - 1)
	blended_color = color0 * fraction + color1 * (1 - fraction)
	blended_frame = frames[i] * blended_color
	if blend_style == "add":
		pix_arr += blended_frame
	else if blend_style == "max":
		pix_arr = np.maximum(pix_arr, blended_frame)

print("saving")

z = (65535*((pix_arr - pix_arr.min())/pix_arr.ptp())).astype(np.uint16)
with open('time_gradient.png', 'wb') as f:
	writer = png.Writer(width=z.shape[1], height=z.shape[0], bitdepth=16)
	z2list = z.reshape(-1, z.shape[1]*z.shape[2]).tolist()
	writer.write(f, z2list)

