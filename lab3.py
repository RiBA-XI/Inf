from math import *

def task1(x):
    x = int(x)
    def prime_number(x):
        for i in range(2, (x/2)+1):
            if x%i==0:
                return print("число x не является простым")
        else:
            return print("число x простое")
    def positive_number(x):
        if x>0:
            return print("число x положительное")
        elif x==0:
            return print("число x равно 0")
        else:
            return print("число x не является положительным")

def task2(x):
     x = int(x)
     if x >=0:
         return e**x+x
     else:
         return sin(x)+1

def task3(number):
    number = int(number)
    def number_in_binary_numeral_system(number):
        return print(bin(number)[2:])
    def number_in_new_numeral_system(number, base=2):
        k = number
        new_numeral_system = ""
        while k>0:
            new_numeral_system = str(k % base) + str(new_numeral_system)
            k = k // base
        return print(new_numeral_system)
    number_in_new_numeral_system(number)

# def task4():
#     def is_point_in_figure1(x, y):

def task5(a, b, c):
    l = list()
    l.append(a)
    l.append(b)
    l.append(c)
    print("наименьшее значение", l.min())

task5(input(), input(), input())
