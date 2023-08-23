import zlib, sys, os
from PIL import Image
import jpeglib as jlib

def jpg_info(f):
	image = Image.open(f)
	print("------Info-----")
	print("Format:", image.format)
	print("Size:", image.size)
	print("Mode:", image.mode)
	print("Info:", image.info)
	print("---------------")

def get_markers(f):
	#the pixel data (such as RGB) in so called spatial domain are compressed
	try:
		j_spatial = jlib.read_spatial(f)
		print(j_spatial.spatial)
	except IOError:
		print("IO Error")
		pass

	# dequantize DCT coefficients
	try:
		j_DCT = jlib.read_dct(f)
		j_DCT = jlib.to_jpegio(j_DCT)
		print(j_DCT.coef_arrays)
		print(j_DCT.quant_tables)
	except IOError:
		print("IO Error")
		pass