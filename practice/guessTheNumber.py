# Guess the numer
import random

secret_number = random.randint(1, 20)
print("Please guess the number from 1 to 20.")

for guesses_taken in range(1, 7):
    print("Input the number.")
    guess = int(input())

    if guess < secret_number:
        print("It's smaller")
    elif guess > secret_number:
        print("It's larger")
    else:
        break # Bingo!

if guess == secret_number:
    print("Bingo! It takes " + str(guesses_taken) + " times")
else:
    print("I'm sorry, the number is " + str(secret_number))

