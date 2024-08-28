def factorial(n):
    if n == 0 or n == 1:
        return 1
        else:
            return n * factorial(n - 1)

            number = int(input("Введите число для вычисления факториала: "))
            result = factorial(number)
            print(f"Факториал числа {number} равен {result}")