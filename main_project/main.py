
import hashlib
import json
import random
import os

def create_nonce(string, amount_0):
    while True:
        nonce = random.randint(0,10**10)
        hash = hashlib.sha256(str(str(string) + ' ' + str(nonce)).encode())
        if str(hash.hexdigest()[:amount_0]) == '0'*amount_0:
            break
        else:
            continue
    return str(nonce)

def create_the_first_block(amount_0):
    string = ' '.join([
'prev_hash', 'sender', 'amount',
'recevier', 'block_number', 'hash',
'nonce', 'None', 'Nobody',
'Nothing', 'Nobody', '1'
])
    nonce = create_nonce(string, amount_0)
    string += ' ' + nonce
    hash = create_hash(string)
    block_data = {
'prev_hash':'None',
'sender':'Nobody',
'amount':'Nothing',
'recevier':'Nobody',
'block_number':'1',
'hash':hash,
'nonce':nonce
    }
    with open('./Blocks/block1.json','w') as f:
        json.dump(block_data, f, indent=3)
    return None

def get_prev_hash(block_number):
    prev_numb = int(block_number) - 1
    file = open('./Blocks/'+'block' + str(prev_numb) + '.json', 'r')
    data = json.loads(file.read())
    prev_hash = data['hash']
    file.close()
    return str(prev_hash)

def create_hash(string):
    hash = hashlib.sha256(string.encode())
    return str(hash.hexdigest())

def create_new_block(data, amount_0):
    block_number = str(len(os.listdir(path="./Blocks")) + 1)
    prev_hash = get_prev_hash(block_number)
    string_lst = [
'prev_hash', 'sender', 'amount',
'recevier', 'block_number', 'hash',
'nonce', prev_hash, data['sender'],
data['amount'], data['recevier'], block_number
    ]
    string = ' '.join(string_lst)
    nonce = create_nonce(string, amount_0)
    string += ' ' + nonce
    hash = create_hash(string)
    create_new_json_block(block_number,prev_hash,nonce,hash,data)
    return None

def create_new_json_block(block_number, prev_hash, nonce, hash, data):
    block_data = {
    'prev_hash':prev_hash,
    'sender':data['sender'],
    'amount':data['amount'],
    'recevier':data['recevier'],
    'block_number':block_number,
    'hash':hash,
    'nonce':nonce
    }
    with open('./Blocks/'+'block' + str(block_number) + '.json','w') as f:
        json.dump(block_data, f, indent=3)
    return None

def start(sender, recevier, amount, amount_0=5):
    if  'block1.json' not in os.listdir(path="./Blocks"):
        create_the_first_block(amount_0)
    sender = str(sender)
    recevier = str(recevier)
    amount = str(amount)
    data = {
    'sender':sender,
    'amount':amount,
    'recevier':recevier
     }
    create_new_block(data, amount_0)
    return None
if __name__=='__main__':
    start()
