import main
import random
import checking

def creating(blocks_amount=5, amount_0=3):
    alphabet = ['a', 'c', 'd', 'v', 'b', 'f', 'g', 't', 'h', 'r', 'd', 'f', 'a', 'g', 'h', 'r', 'g', 'j', 'o', 'r', 'f']
    amounts = [int(random.randint(0,10**10)) for i in range(20)]
    sanders = [alphabet[(random.randint(0,20))] + alphabet[(random.randint(0,20))] + alphabet[(random.randint(0,20))] for i in range(20)]
    receviers = [alphabet[(random.randint(0,20))] + alphabet[(random.randint(0,20))] + alphabet[(random.randint(0,20))] for i in range(20)]
    for i in range(blocks_amount):
        main.start(sanders[i], receviers[i], amounts[i], amount_0)



def start():
    action = int(input('Enter here 1 if you want to create some blocks or enter 2 if you only want to check the blockchain and see results of checking in "checking_results" folder '))
    if action == 2:
        zeroes = int(input('Enter here amount of 0 you entered before to be sure that program will work correctly '))
        checking.start_checking(amount_0=zeroes)
    else:
        block_amount = int(input('Enter here amount of blocks you want to create  '))
        amount_zeroes = int(input('Enter the amount of 0 you want the hashes to start with but be careful if you enter more tnah 5 the program will be work very slow '))
        creating(blocks_amount=block_amount, amount_0=amount_zeroes)

if __name__ == '__main__':
    start()
