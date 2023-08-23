import checkJPEG
import zlib, sys, os
from PIL import Image

if len(sys.argv) != 2:
	print(f"USAGE: {sys.argv[0]} cropped.jpg")
	exit()

JPEG_SOI = b"\xFF\xD8" # start of image
JPEG_EOI = b"\xFF\xD9" # end of image
JPEG_APP0 = b"\xFF\xE0" # JFIF APP0
JPEG_SOS = b"\xFF\xDA" # start of scan
JFIF_identifier = b"\x4A\x46\x49\x46\x00" # "JFIF" in ASCII

n_times = 4

# multiply the density by n times
def den_multiply(den_l, n_times):
	# convert bytes to int
	den_l_int = int.from_bytes(den_l, byteorder='big')
	den_l_int = den_l_int * n_times
	return den_l_int.to_bytes(2, byteorder='big')

def parse_jpeg(f):
	# move file pointer to beginning 
	f.seek(0, 0)
	# check JPEG format, if not, exit
	# first 2 bytes should be SOI
	assert(f.read(2) == JPEG_SOI)
	# next 2 bytes should be APPO marker
	assert(f.read(2) == JPEG_APP0)
	# next 2 bytes, length of segment excluding APPO marker
	length = int.from_bytes(f.read(2), "big")
	# minus the size of JFIF version, 2 bytes
	APP0_content = f.read(length - 2) 


	f.seek(0, 0)	
	file = f.read()

	# search pos
	SOS_pos = file.index(JPEG_SOS)
	EOI_pos = file.index(JPEG_EOI)

	assert(SOS_pos)
	assert(EOI_pos)

	# beginning to EOI + EOI size (2 bytes)
	cropped = file[:EOI_pos + 2]
	# the rest of image, image - cropped
	rest = file[EOI_pos + 2:]

	# last 2 bytes are EOI marker
	if rest and rest[-2:] == JPEG_EOI:
		print(str(sys.argv[1]) + " is cropped and affected by aCropalypse.")
		is_vuln = True

	# restore
	if is_vuln:
		sanitized_name = str(sys.argv[1]).rstrip(".jpg") + "_sanitized.jpg"
		restored_name = str(sys.argv[1]).rstrip(".jpg") + "_restored.jpg"
		"""
		print("Sanitized jpg: ", sanitized_name)
		with open(sanitized_name, "wb") as f_s:
			f_s.write(cropped)
		"""
		print("Restored jpg: ", restored_name)
		new_len = min(len(file[EOI_pos + 2:]), 65535) 

		"""
		den_l = file[14:16]
		den_w = file[16:18]
		den_l_new = den_multiply(den_l, n_times)
		den_w_new = den_multiply(den_w, n_times)
		print("rest len: ", len(rest))
		"""
		if len(rest) % 3 == 0:
			#print(len(rest)/3)
			pass
		else:
			print("Not 3's times")
			exit(1)
		
		SOS_len = int.from_bytes(file[SOS_pos + 2: SOS_pos + 4], byteorder='big')
		#print("SOS len: ", SOS_len)
		#print(file[SOS_pos: SOS_pos + SOS_len + 2])
		
		# replace EOI marker to be  0, 0
		#restored_content = file[:14] + den_l_new + den_w_new + file[18: EOI_pos] + b"\x00\x00" + rest
		restored_content = file[: SOS_pos] + file[SOS_pos: SOS_pos + SOS_len + 2] + b"\x00\x00" + rest
		with open(restored_name, "wb") as f_r:
			f_r.write(restored_content)

def main():
	f = open(sys.argv[1], "rb")
	checkJPEG.jpg_info(f)
	parse_jpeg(f)

if __name__ == '__main__':
	main()