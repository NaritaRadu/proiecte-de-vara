from abc import ABC, abstractmethod
# aici importez metode abstracte

#__init__=constructor in JAVA
#self=this 
class Car:
    def __init__(self,model,year,color,for_sale):
        self.model=model
        self.year=year
        self.color=color
        self.for_sale=for_sale
    def drive(self):
        print(f"you drive the {self.model}")



class Student:
    class_year=2024
    num_students=0
    #astea is variabile de clasa,comune clasei,nu unui obiect
    
    def __init__(self,name,age):
        self.name=name
        self.age=age
        Student.num_students+=1
    
    #trebuie sa pun acest decorator ca sa stie ca e statica
    @staticmethod
    def is_valid_age(age):
        if age<17:
            print("not a valid age")
        else:
            print("valid age")
            
            
    def get_info(self):
        return f"{self.name} {self.age} "
    
    #asta se comporta exact ca si toString
    #acum,cand voi printa student,nu voi mai primi
    #adresa referintei obiectului,ci formatul de mai jos
    def __str__(self):
        return f"name:{self.name} age:{self.age}"
    
    #asta e un fel de equals,acum cand fac student1==student2
    #nu mai verific referinta,ci numele
    #self e primu,other e al doilea 
    #daca vreau sa verific mai multe atribute
    #fac and intre conditii 
    def __eq__(self, other):
        return self.name==other.name
    
    def __add__(self,other):
        return f"{self.age+other.age} varsta totala"
    
    #asta e o metoda specifica clasei
    #nu mai pun self,ci cls
    @classmethod
    def get_count(cls):
        return f"total # of students: {cls.num_students}"



class Animal:
    
    def __init__(self,name):
        self.name=name
        self.is_alive=True
        
    # asta sunt metode instanta,specifice obiectului    
    def eating(self):
        print(f"the animal {self.name} is eating")
    
    def sleep(self):
        print(f"{self.name} is sleeping")

#asa fac inheritance,pot avea mai multe ,spre deosebire
# de JAVA
class Dog(Animal):
    def speak(self):
        print("WOOF!")

class Cat(Animal):
    def speak(self):
        print("MEOW!")

class Mouse(Animal):
    def speak(self):
        print("CHITS!")
        
class Prey(Animal):
    def flee(self):
        print("this animal is fleeing")

class Predator(Animal):
    def hunt(self):
        print("this animal is hunting")

class Rabbit(Prey):
    pass

class Hawk(Predator):
    pass

class Fish(Prey,Predator):
    pass


#aici am facut polimorfism
class Shape:
    def __init__(self,color,is_filled):
        self.color=color
        self.is_filled=is_filled
        
        
    def describe(self):
        print(f" it is {self.color} and {'filled ' if self.is_filled else 'not filled'}")
   
    @abstractmethod
    def area(self):
        pass    

class Circle(Shape):
    #asa se foloseste super in python
    def __init__(self, color, is_filled,radius):
        super().__init__(color, is_filled)
        self._radius=radius
    #asta obliga sa fie o proprietate,si nu mai trebuie
    #sa pun circle.radius(),ci circle.radius
    #underscore ,adica e private
    @property
    def radius(self):
        return self._radius    
    
    @radius.setter
    def radius(self,new_radius):
        if new_radius>0:
            self._radius=new_radius
        else:
            print("radius must be greater than 0")
        
    def describe(self):
        super().describe()
        print(f"it is a circle with an area of {3.14*self._radius*self._radius}cm")
    
    #aici am facut override
    def area(self):
        return 3.14*self._radius**2

def main():
        
        
    print("MASINI")
    print()   
    car1=Car("BMW",2026,"red",False)
    car2=Car("Audi",2024,"white",True)

    car1.drive()
    car2.drive()
    
    print("STUDENTI")
    print()


    student1=Student("andrei",18)
    student2=Student("andrei",17)
    print(Student.num_students)
    Student.is_valid_age(17)
    print(Student.get_count())
    print(student1) # se comporta ca si toString
    print(student1==student2)#rezulta True,fara __eq__ era false
    print(student1+student2)
    print("ANIMALE")
    print()
    
    dog1=Dog("Scooby")
    cat1=Cat("Tom")
    mouse1=Mouse("Jerry")
    print(dog1.name)
    cat1.sleep()
    cat1.speak()
    
    
    rabbit=Rabbit("Buggs")
    hawk=Hawk("Hawk tuah")
    fish=Fish("Fesh")
    fish.flee()
    fish.hunt()
    fish.eating()
    
    
    print("FORME")
    print()
    
    circle=Circle("red",True,5)
    print(circle.color)
    circle.describe()
    print(circle.area())
    print(circle.radius)#aici am accesat getter
    circle.radius=6 # aici am accesat setter
    print(circle.radius) # aici iar getter
if __name__=='__main__':
    main()