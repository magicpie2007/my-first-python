# Collatz

def collatz(number):
    if number % 2 == 0:
        return number / 2
    else:
        return 3 * number + 1

def main(arg):
    try:
        num = int(arg)
        while num != 1:
            num = collatz(num)
            print(int(num))
    except ValueError:
        print("Please input integer")


if __name__ == '__main__':
    import sys
    main(sys.argv[1])




