import os 
import sys
import numpy as np
import scipy.ndimage as spimg
import png
import colorsys

if len(sys.argv) != 3:
	print('[frame folder] [blend (add/max)]')
	exit()

print("loading frames")

frame_folder = sys.argv[1]
frame_files = os.listdir(frame_folder)
blend_style = sys.argv[2]
if blend_style not in ["add", "max"]:
	print("[blend (add/max)]")
	exit()

frames = []
for frame_file in frame_files:
	frame = spimg.imread(frame_folder + "/" + frame_file)
	frames.append(frame)

print("blending frames")

pix_arr = np.zeros(frames[0].shape)

for i in range(len(frames)):
	fraction = i / (len(frames) - 1)
	blended_color = np.array(colorsys.hsv_to_rgb(fraction, 1, 1))
	blended_frame = frames[i] * blended_color
	if blend_style == "add":
		pix_arr += blended_frame
	elif blend_style == "max":
		pix_arr = np.maximum(pix_arr, blended_frame)

print("saving")

z = (65535*((pix_arr - pix_arr.min())/pix_arr.ptp())).astype(np.uint16)
with open('time_gradient.png', 'wb') as f:
	writer = png.Writer(width=z.shape[1], height=z.shape[0], bitdepth=16)
	z2list = z.reshape(-1, z.shape[1]*z.shape[2]).tolist()
	writer.write(f, z2list)

