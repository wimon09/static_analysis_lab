def check_number(x):
    if x <= 0:
        print("Invalid")
        return

    if x >= 100:
        print("Too large")
        return

    if x % 2 == 0:
        print("Valid even number")
    else:
        print("Odd number")