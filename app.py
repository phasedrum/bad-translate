import os
import time
import platform
from random import choice as rndchoice
from googletrans import Translator
from googletrans import LANGUAGES


# setup
translator = Translator()

# set app dir to working dir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# check os
is_windows = platform.system() == 'Windows'


# function
def funny_translate(text: str, ammount: int = 1, language: str = 'auto'):
	if ammount < 1:
		ammount = 1
	if language == 'auto':
		language = translator.detect(text).lang

	# translate
	for i in range(ammount):
		print(f'\nTranslating... ({i+1}/{ammount})', end='')
		try:
			text = translator.translate(text, dest=rndchoice(list(LANGUAGES.keys()))).text
		except:
			print(' [ERROR]', end='')
	
	# translate back to source language; if fail, try again
	fails = 0
	not_done = True
	print("\nTranslating... (Source)", end='')
	while not_done:
		if fails >= 3:
			print(' [ERROR]')
			print('Could not translate the text, please try again later...', end='')
			break
		try:
			text = translator.translate(text, dest=language).text
			not_done = False
		except:
			not_done = True
			fails += 1
	
	print("\n")
	return text


# app start
print("Welcome to Goofy Translate!")

# check translate ammount
print("How many times do you want to translate?")
translate_ammount = int(input('[A translation can take about 1-5 seconds; Integers >= 1]: '))

# create file if it doesn't exist
try:
	with open("input.txt", "x") as f:
		pass
except:
	pass

# open in notepad if platform is windows
if is_windows:
	print("Starting Notepad... You can enter/change the text that will be translated here. (UTF-8)\nSave (CTRL + S) and close (ALT + F4) Notepad to proceed... ")
	os.system('notepad.exe input.txt')
else:
	input('Open input.txt to enter/change the text that will be translated (UTF-8)... [PRESS ENTER TO CONTINUE]')

# read file
f = open('input.txt', encoding='UTF-8')
file_content = f.read()
f.close()

# translate contents
translated_text = funny_translate(file_content, translate_ammount)
file_path = f'results/translated_{time.strftime("%Y-%m-%d_at_%H-%M-%S")}.txt'

# write to file
print("Writing to file...")
try:
	with open(file_path, 'w', encoding='UTF-8') as f:
		f.write(translated_text)
except:
	os.mkdir('results')
finally:
	with open(file_path, 'w', encoding='UTF-8') as f:
		f.write(translated_text)

print("Finished!")

# open file if platform is windows
if is_windows:
	os.system(f'START notepad.exe {file_path}')
else:
	print(f'The result can be found at \"{file_path}\"')
	time.sleep(2)

time.sleep(5)
exit()


