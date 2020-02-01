import hashlib
import os
import json

def check_JSON_errors(files_lst):
    files_with_JSON_errors = []
    for file in files_lst:
        f = open('./Blocks/'+str(file), 'r')
        try:
            json.loads(f.read())
        except json.decoder.JSONDecodeError:
            files_with_JSON_errors.append(file)
    return files_with_JSON_errors

def check_files_names(files_lst):
    bad_files_names = [file for file in files_lst if not file.endswith('.json')]
    return bad_files_names

def get_right_files_order(files_lst):
    right_order = []
    for i in range(1, len(files_lst) + 1):
        for file in files_lst:
            f = open('./Blocks/' + str(file), 'r')
            data = json.loads(f.read())
            f.close()
            numb = data.get('block_number')
            if type(numb) is str and numb == str(i):
                right_order.append(file)
    return right_order

def get_hash(file_name):
    with open('./Blocks/' + str(file_name), 'r') as file:
        data = json.loads(file.read())
    try:
        str_lst = [
'prev_hash', 'sender', 'amount',
'recevier', 'block_number', 'hash',
'nonce', str(data['prev_hash']), str(data['sender']),
str(data['amount']), str(data['recevier']),
str(data['block_number']), str(data['nonce'])
]
    except:
        return 'Error'
    else:
        string = str(' '.join(str_lst))
        hash = hashlib.sha256(string.encode())
        return hash

def checking_block_hashes(files_lst, amount_0):
    files_with_bad_hash = []
    for file in files_lst:
        with open('./Blocks/'+str(file), 'r') as f:
            data = json.loads(f.read())
        hash = get_hash(file)
        if type(hash) is str:
            files_with_bad_hash.append(file)
            continue
        hash = hash.hexdigest()
        if str(hash[:amount_0]) != '0'*amount_0 or str(hash) != str(data['hash']):
            files_with_bad_hash.append(file)
    return files_with_bad_hash

def checking_prev_hashes(right_order, amount_0):
    bad_prev_hash = []
    for i in range(1, len(right_order)):
        file = str(right_order[i])
        f = open('./Blocks/'+file, 'r')
        data = json.loads(f.read())
        f.close()
        prev_hash = data.get('prev_hash')
        if prev_hash == None:
            bad_prev_hash.append(file)
            continue
        real_prev_hash = get_hash(right_order[i-1])
        if str(type(real_prev_hash)) == "<class '_hashlib.HASH'>" and str(real_prev_hash.hexdigest()) == str(prev_hash) and str(prev_hash).startswith('0'*amount_0) :
            continue
        else:
            bad_prev_hash.append(file)
    return bad_prev_hash

def cheking_if_JSON_errors(files_lst, JSON_errors, amount_0):
    files_with_bad_hash = []
    files_with_bad_hash.extend(JSON_errors)
    for file in JSON_errors:
        files_lst.remove(file)
    checked_files_hashes = checking_block_hashes(files_lst, amount_0)
    if len(checked_files_hashes) > 0:
        files_with_bad_hash.extend(checked_files_hashes)
    write_results_JSON(
    bad_hash_in = files_with_bad_hash,
    JSON_errors_in = JSON_errors,
    )

def cheking_if_not_JSON_errors(right_order, files_lst, amount_0):
    files_with_bad_hash = checking_block_hashes(files_lst, amount_0)
    files_wit_bad_prev_hash = checking_prev_hashes(right_order, amount_0)
    write_results_JSON(bad_hash_in = files_with_bad_hash, bad_prev_hash_in = files_wit_bad_prev_hash)

def start_checking(amount_0):
    files_lst = os.listdir('./Blocks')
    files_wiht_bad_names = check_files_names(files_lst)
    if len(files_wiht_bad_names) > 0 :
        for file in files_wiht_bad_names:
            files_lst.remove(file)
    JSON_errors = check_JSON_errors(files_lst)
    if len(JSON_errors) > 0:
        cheking_if_JSON_errors(files_lst, JSON_errors, amount_0)
    else:
        right_order = get_right_files_order(files_lst)
        cheking_if_not_JSON_errors(right_order, files_lst, amount_0)

def write_results_JSON(*args, **kwargs):
     data = {str(key):kwargs[key] for key in kwargs}
     with open('./checking_results/results.json', 'w') as f:
         json.dump(data, f, indent=3)

if __name__ == "__main__":
    start_checking()
