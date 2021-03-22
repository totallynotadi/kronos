from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import os
import sys
import timeit
import hashlib
import struct

file_name = sys.argv [1]

decrypted_file_name = file_name [ : -4]

password = str(input('enter the password to decrypt with'))
password = hashlib.sha256(password.encode()).digest()

len_file = os.path.getsize(file_name)

'''
with open(file_name, 'rb') as infile:
	iv = infile.read(16)
	print(f'iv from the decryptor is : {iv}')
	decipher = AES.new(password, AES.MODE_CBC, iv)
	with open(decrypted_file_name, 'wb') as outfile:
		print(infile.tell())
		while True:
			chunk = infile.read(24*1024)
			if len(chunk) == 0:
				break 
			outfile.write(decipher.decrypt(chunk))
			if infile.tell() == len_infile - 16:
				print(f'len of the infile : ')
				print(infile.tell())
				last_chunk = infile.read(16)
				print(last_chunk)
				chunk = decipher.decrypt(last_chunk)
				print(f'len of the chunk before unpadding : {len(chunk)}')
				chunk = unpad(chunk, 16)
				print(f'len of the chunk after unpadding : {len(chunk)}')
				outfile.write(chunk)
'''

with open(file_name, 'rb') as infile:
	origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
	iv = infile.read(16)
	decipher = AES.new(password, AES.MODE_CBC, iv)
	with open(decrypted_file_name, 'wb') as outfile:
		start = timeit.default_timer()
		while True:
			chunk = infile.read(64*1024)
			if len(chunk) == 0:
				break
			outfile.write(decipher.decrypt(chunk))
		stop = timeit.default_timer()
		print()
		outfile.truncate(origsize)

print(f'time taken to decrypt the file : {stop - start}')	
