
ESP = 1e-6
def koren(x, y):
    return x**(1/y)

def task1():
    data = False
    while data == False:
        x = int(input("x ="))
        y = int(input("y ="))
        z = int(input("z ="))
        if (koren(x, 5)+koren(y, 6)+ log(4, 2)) != 0 and y>ESP:
            data = True
        else:
            print("введите другие данные")

    a = (tan(koren(x-1,2))-koren(abs(y), 45))/(koren(x, 5)+koren(y, 6)+ log(4, 2))
    b = koren(x, 3)+sin(z)+cosh(x)-log(y, 10)
    print(f"a = {a}, b = {b}")

def task2(x):
    x = int(x)
    a = 1
    b = 4
    f = koren(x+a, 2)+(x**2+b)/x
    print(f"f = {f}")
    return f

def task3(x):
    x = int(x)
    f = log(x**2+1, 3)-3.25*x
    print(f"f = {f}")

def task4():
    r = int(input("r ="))
    R = int(input("R ="))
    h = int(input("h ="))
    l = koren(((R-r)/2)**2+h**2, 2)
    print(f"l = {l}")
    #считает не верное значение

def task5():
    m = int(input("m ="))
    v = int(input("v ="))
    data = False
    while data == False:
        k = int(input())
        if k!=0:
            data = True
        else:
            print("разделение на ноль!, введите другие данные")

    l = m*v/k
    print(f"l = {l}")

#def task6():
    #sp = int(input("l ="))
    #r = sp*4/pi

#def task7():
