import json

class Product():
    
    def __init__(self,name,price:float,quantity:float,identifier,brand):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.identifier = identifier
        self.brand = brand
    def to_json(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
#subclass
class Clothing(Product): 
    def __init__(self,name,price,quantity,identifier,brand,size,material):
        super().__init__(name,price,quantity,identifier,brand)
        self.size = size
        self.material = material
    
class Food(Product):
     def __init__(self,name,price,quantity,identifier,brand,expiry_date,gluten_free,suiteable_for_vegans):
        super().__init__(name,price,quantity,identifier,brand)
        self.expiry_date = expiry_date
        self.gluten_free = gluten_free
        self.suiteable_for_vegans = suiteable_for_vegans

#Container        
class ShoppingCart():
   
    def __init__(self):
        self.cart = {}
    def addProduct(self,p):
        cartTemp = {}
        added = False

        for item in self.cart.values():
            if(item.name < p.name or added == True):
                cartTemp[item.identifier] = item
            else: #append item to the appropriate position
                cartTemp[p.identifier] = p
                cartTemp[item.identifier] = item
                added = True
        if added == False:
            cartTemp[p.identifier] = p
        
        self.cart = cartTemp
        #self.cart[p.identifier] = p
        
    def removeProduct(self,identifier):
        del self.cart[identifier]
    
    def getContents(self):
        pass
    def changeProductQuantity(self,p,q):
        p.quantity = q
    def getCapacity(self):
        return len(self.cart)
    def findProduct(self,identifier):
        return self.cart[identifier]
    def isExistIdentifierInCart(self,identifier):
        return identifier in self.cart
    def showCartByExpenses(self):
        index = 0
        total = 0
        for item in self.cart.values():
            index = index + 1

            out_str = str(index) + " - " 
            if item.quantity == 1 : 
                out_str += item.name + " = "
            else:
                out_str += str(item.quantity) + " * " + item.name + " = "
            prices = float(item.quantity) * float(item.price)
            total += prices
            out_str += "£" + str(prices)
            
            print(out_str)
            print ("Total = £" + str(total))
    def showCartByJSON(self):

        json_array = []
        for item in self.cart.values():
            json_array.append(item.__dict__)
        print(json.dumps(json_array))

print('The program has started.')
my_cart = ShoppingCart()
print('Insert your net command (H for help):')

terminated = False
while not terminated:
    c= input("Type your next command:")
    c = c.upper()
    
    if c == "A":
        print("Adding a new product:")
        typeModel = input("Insert its type:").lower()
        if (typeModel == "clothing"):
            name = input("Insert its name:")

            price = input("Insert its price(£):")
            try:
                while price.isalpha() or float(price) < 0:
                    price = input("Wrong Price! Please Insert a Positive Number(£):")
            except ValueError:
                price = input("Wrong Price! Please Insert a Positive Number(£):")

            price = float(price)

            quantity = input("Insert its quantity:")
            while not quantity.isdigit():
                quantity = input("Wrong Quantity! Please Insert a Positive Number:")
            quantity = int(quantity)

            brand = input("Insert its brand:")
            identifier = input("Insert its EAN code:")

            #check this ideitifer exist in cart
            if my_cart.isExistIdentifierInCart(identifier):
                print("This identifer already exists in shopping cart.")
                continue

            size = input("Insert its size:")
            material = input("Insert its material:")
            clothing = Clothing(name, price, quantity, identifier, brand, size, material)
            my_cart.addProduct(clothing)
            print("The product " + name + " has been added to the cart.")
            print("The cart contains " + str(my_cart.getCapacity()) + " Products.")
        elif (typeModel == "food"):
            name = input("Insert its name:")
            
            price = input("Insert its price(£):")
            try:
                while price.isalpha() or float(price) < 0:
                    price = input("Wrong Price! Please Insert a Positive Number(£):")
            except ValueError:
                price = input("Wrong Price! Please Insert a Positive Number(£):")

            price = float(price)

            quantity = input("Insert its quantity:")
            while not quantity.isdigit():
                quantity = input("Wrong Quantity! Please Insert a Positive Number:")
            quantity = int(quantity)
            
            brand = input("Insert its brand:")
            identifier = input("Insert its EAN code:")

            #check this ideitifer exist in cart
            if my_cart.isExistIdentifierInCart(identifier):
                print("This identifer already exists in shopping cart.")
                continue
            expiry_date = input("Insert its expiry_date:")
            gluten_free = input("Insert its gluten_free:")
            suiteable_for_vegans = input("Insert its suiteable_for_vegans:")
            food = Food(name, price, quantity, identifier, brand,expiry_date,gluten_free,suiteable_for_vegans)
            my_cart.addProduct(food)
            print("The product " + name + " has been added to the cart.")
            print("The cart contains " + str(my_cart.getCapacity()) + " Products")
        else:
            print('sorry, we cannot find matching product')

    elif c == "R":
        identifier = input("Type product EAN code to remove:")
        if not my_cart.isExistIdentifierInCart(identifier):
            print("This product doesnot exist in shopping cart.")
            continue
        my_cart.removeProduct(identifier)     
        print("This product is removed in shopping cart succesfully.")

    elif c == "S":
        print("This is the total of the expenses:")
        my_cart.showCartByExpenses()
        
    elif c == "Q":        
        identifier = input("Type product EAN code:")
        quantity = input("Input quantity:")
        product = my_cart.findProduct(identifier)
        my_cart.changeProductQuantity(product, quantity)

    elif c == "E":
        my_cart.showCartByJSON()
        
    elif c == "T":        
        terminated = True
    elif c == "H":
        pass
    else:
        print('Command not recognised.Please try again.')
print('Goodbye.')
