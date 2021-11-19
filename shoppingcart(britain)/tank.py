#Parent
class Fish():
    def __init__(self,color,size):
        self.color = color
        self.size = size
#Sub
class Swordtails(Fish):
    def __init__(self,color,size,origin):
        super().__init__(color,size)
        self.origin = origin
        
class Guppies(Fish):
    def __init__(self,color,size,age):
        super().__init__(color,size)
        self.age = age

#Container        
class MyFishTank():
   
    def __init__(self):
        self.MyFishTankList = []
        
    def fish_in(self,fish):
            
        self.MyFishTankList.append(fish)

    
    def fish_out(self,color):
        self.MyFishTankList.pop()
    def getContents(self):# get the length of fish list
        print("Fish Count:" , len(self.MyFishTankList))


tank = MyFishTank()



fish_type = input("Chose Swordtails  ")
 
if fish_type == "Swordtails":         
    color = input("color: ")               
    size = input("size: ")
    origin = input("origin: ")
    #fish_in(Swordtails(color,size,origin))
    tank.fish_in(Swordtails(color,size,origin))

else:        
    color = input("color: ")               
    size = input("size: ")
    age = input("age: ")
    
    tank.fish_in(Guppies(color,size,age))

tank.getContents()
tank.fish_out()
tank.getContents()
