from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import base64
import sys
import os
import getpass
import timeit
import argparse
import csv

def create_usr():
			usr_name = str(input('enter the username'))
			print(hashit(usr_name))
			if os.path.exists(kronos_usr_dir_path + '\\' + hashit(usr_name) + '.csv'):
				print('user already exists!')
				return
			pswrd = str(getpass.getpass('enter the password for the user'))
			pswrd_agen = str(getpass.getpass('enter the password again for confirmation'))
			while pswrd != pswrd_agen:
				print("the passwords don't match! enter correctly")
				pswrd = str(getpass.getpass('enter the password for the user'))
				pswrd_agen = str(getpass.getpass('enter the password again for confirmation'))

			with open('C:\\users\\' + usr_dir + '\\kronos\\users\\' + hashit(usr_name) + '.csv', 'a') as le_csv_file:
				writer = csv.writer(le_csv_file, delimiter = '|')
				writer.writerow([hashit(usr_name + pswrd)])
				writer.writerow(['website', 'url', 'email', 'password'])

			print('user created!')

def print_menu():	
		print('choose what you want to do \n')
		print('1. retreive a password')
		print('2. create a new user')
		print('3. add a website')
		print('Q. quit the program \n')

def de_slash(le_string):
	le_string = list(le_string)
	for char in le_string:
		if char == '/' or char == '\\':
			le_string.remove(char)
	le_string = ''.join(le_string)
	return le_string

def hashit(le_string):
	the_hash = base64.b64encode(hashlib.sha1(le_string.encode()).digest()).decode('utf-8')
	return de_slash(the_hash [ : -1])


def authenticate():

	global usr_name
	usr_name = str(input('enter your username'))

	tries = 0
	while str(hashit(usr_name) + '.csv') not in os.listdir(kronos_usr_dir_path):
		if tries == 3:
			print('too many attempts... quitting')
			exit()
		print('incorrect username!')
		usr_name = str(input('enter your username'))
		tries += 1

	global pswrd
	global le_bool
	tries = 0
	le_bool = False
	while not le_bool:
		if tries == 3:
			print('too many attempts!')
			exit()
		pswrd = str(getpass.getpass('enter your password : '))
		with open('C:\\users\\' + usr_dir + '\\kronos\\users\\' + hashit(usr_name) + '.csv', 'r') as le_csv_file:
			reader = csv.reader(le_csv_file, delimiter = '|')
			lol = 0
			row1 = []
			for row in reader:
				if len(row) != 0 and lol == 0:
					row1 = row
				lol += 1
			if row1 [0] == hashit(usr_name + pswrd):
				print("you're in!")
				le_bool = True
			else:
				print('wrong password!')
		tries += 1
	if le_bool == False:
		print("bad luck, you couldn't login.")
		exit()

usr_dir = getpass.getuser()
kronos_path = 'C:\\users\\' + usr_dir + '\\kronos'
kronos_usr_dir_path = 'C:\\users\\' + usr_dir + '\\kronos\\users'

if not os.path.exists(kronos_path):
	os.mkdir(kronos_path)
	os.mkdir(kronos_usr_dir_path)

line = '~' * 100
print(line, '\n' * 3)
print('WELCOME TO KRONOS PASSWORD MANAGER...!', '\n' * 3)
print(line ,'\n')

if len(os.listdir(kronos_usr_dir_path)) == 0:
	print('''
	create a user profile to store your passwords
	''')
	create_usr()
else:
	print('''
	1. create new user
	2. login as a existing user
	Q. quit the program
	''')
	le_option = str(input('choose your option : '))
	if le_option == '1':
		create_usr()
	elif le_option == '2':
		authenticate()

		while True:

			print_menu()

			le_choice = input('enter your choice - ')

			if le_choice == 'Q':
				exit()

			if le_choice == '2':
				
				create_usr()

			elif le_choice == '1':

				if le_bool:
					to_find = str(input('enter the website to find the password of'))

					with open('C:\\users\\' + usr_dir + '\\kronos\\users\\' + hashit(usr_name) + '.csv', 'r') as le_csv_file:
						reader = csv.reader(le_csv_file, delimiter = '|')
						rows = [rows for rows in reader if len(rows) != 0]
						print(rows)
						pass_usr_hash = rows[0]
						for row in rows:
							if to_find == row [0]:
								print(f'this is the row you need : {row}')
								the_row = row
					print(f'the row from outside the block : {the_row}')
					the_password = the_row [3]
					the_email = the_row [2]
					the_url = the_row [1]
					print(f'the password for the website {to_find} is {the_password} with the e-mail id {the_email}, at the url {the_url}')

			if le_choice == '3':
			
				if le_bool:
					website = str(input('enter the name of the website'))
					url = str(input('enter the url of the website'))
					email = str(input('enter the email to use for the website'))
					pswrd = getpass.getpass('set the password for the website')
					write_list = [website, url, email, pswrd]
					print(write_list)
					with open('C:\\users\\' + usr_dir + '\\kronos\\users\\' + hashit(usr_name) + '.csv', 'a') as file:
						writer = csv.writer(file, delimiter = '|')
						writer.writerow(write_list)
					print(f'fields written to the file!')
						
