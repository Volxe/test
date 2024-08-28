def fibonacci(n)
    if n <= 1
        return n
    else
        return fibonacci(n-1) + fibonacci(n-2)

def print_fibonacci_sequence(count)
    for i in range(count)
        print(fibonacci(i), end=" ")
    print()

try
    num = int(input("Введите количество чисел Фибоначчи: "))
    print_fibonacci_sequence(num)
except ValueError
    print("Ошибка: Введите целое число")
finally
    print("Программа завершена")