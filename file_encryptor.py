from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import shutil
import os
import sys
import timeit
import hashlib
import struct


file_name = sys.argv[1]

print(f'size of the original file : {os.path.getsize(file_name)}')

if os.path.isfile(file_name):
	encrypted_file_name = file_name + '.enc'

elif os.path.isdir(file_name):
	root_dir, file = os.path.split(file_name)
	shutil.make_archive(file_name, 'zip', file_name)
	file_name = file_name + '.zip'
	encrypted_file_name = file_name + '.enc'

password = str(input('enter the password to encrypt with'))
password = hashlib.sha256(password.encode()).digest()
iv = os.urandom(16)
print(f'the iv is : {iv}')

cipher = AES.new(password, AES.MODE_CBC, iv)

'''
with open(file_name, 'rb') as infile:
	with open(encrypted_file_name, 'wb') as outfile:
		start = timeit.default_timer()
		outfile.write(iv)
		while True:
			chunk = infile.read(64*1024)
			if len(chunk) == 0:
				break
			elif len(chunk) % 16 != 0:
				print(f'length of this chunk : {len(chunk)}')
				print('this chunk needs padding')
				print(chunk)
				print('padding the chunk...')
				chunk = pad(chunk, 16)
				print('chunk padded')
				print(f'the same chunk after padding : {chunk}')
				print(f'length of the chunk after padding : {len(chunk)}')
			outfile.write(cipher.encrypt(chunk))
		stop = timeit.default_timer()
'''

with open(file_name, 'rb') as infile:
	with open(encrypted_file_name, 'wb') as outfile:
		outfile.write(struct.pack('<Q', os.path.getsize(file_name)))
		outfile.write(iv)

		start = timeit.default_timer()
		while True:
			chunk = infile.read(64*1024)
			if len(chunk) == 0:
				break
			elif len(chunk) % 16 != 0:
				chunk = pad(chunk, 16)
			outfile.write(cipher.encrypt(chunk))
		stop = timeit.default_timer()
		outfile.close()
	infile.close()
		

print(f'time taken to encrypt the file : {stop - start} seconds')

with open(encrypted_file_name, 'rb') as file:
	print(f'the first 16 bytes written to the encryptes file : {file.read(16)}')
	file.close()

