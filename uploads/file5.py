class Person
    def __init__(self name, age):
        self.name = name
        self.age = age
    
    def greet(self)
        print(f"Привет, меня зовут {self.name} и мне {self.age} лет")

    def is_adult(self)
        return self.age >= 18

person1 = Person("Иван", 25)
person1.greet()
if person1.is_adult()
    print(f"{person1.name} совершеннолетний")
else
    print(f"{person1.name} несовершеннолетний")