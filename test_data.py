import os


path = 'c:/Users/kindk/.vscode/test/'
f = 'c:/Users/kindk/.vscode/test/FAX__20231208_092455.jpg'

# name = os.path.basename(f)
# name = os.path.splitext(f)	
# name = os.path.splitext(f)

ext = os.path.splitext(f)[1]

filename = 'hellow'

full = path + filename + ext

print(full)