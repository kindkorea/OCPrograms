# dataList = {
#     'a' : 123,
#     'b' : 456
#     }


# print(dataList['a'])

# dataList = [0,2,3]

# for i, e in enumerate(dataList[1::], start=1):
#     print(f'{i=} {e=}')
    
    
# for i in range(1,10,1)



def aaa(d,c):   
    try :
        if d > 0 and c > 0 :
            return d, c
    except TypeError:
        return False

print(aaa('',''))

# print(type(d))
# # print(d.isdigit())


# try :
#     e = int(d)
#     print(e)
# except ValueError :
#     print('it is not a int') 