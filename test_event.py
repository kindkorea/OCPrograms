# class test:
#     # c = 8
#     @classmethod 
#     def __mySum(cls, a,b):
#         return a+b+cls.c
    
    


# print(test.__mySum(3,5))


class Singer:
    def __init__(self, name):
        self.name = name
    def introduce(self) : 
        print("안녕하세요! 가수 %s입니다." % self.name)
    
    def __str__(self):
        return 'I love Kpop.'
        
        
class KPopGroup(Singer):
    
    def __init__(self, name, cnt):
        super().__init__(name)
        self.nt = cnt
    
    def introduce(self):
        super().introduce()
        print('우린 Kpop 그룹으로 %d명 입니다.' % self.nt)
        
        

a = KPopGroup('김현민',10)

# a.introduce()
print(a)
