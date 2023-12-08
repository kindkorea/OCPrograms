import glob, os
 
files = glob.glob('../../test/*.jpg')

# print(files)
files.sort(key=os.path.getmtime)
# print(os.path.basename(files[0]))


checked_list = []
unchecked_list = [] 


for f in files:
    if os.path.basename(f)[0] == 'v':
        # print(f)
        checked_list.append(f)
    else :
        unchecked_list.append(f)


print(checked_list)
print(unchecked_list)
# checked_list.sort(key=os.path.getmtime)
# for f in checked_list:
#     print(f)
    
# # unchecked_list.sort(key=os.path.getmtime)
# for f in unchecked_list:
#     print(f)


 
# files = glob.glob('*.jpg')
# files.sort(key=os.path.getmtime)
# for f in files:
#     print(f)
 