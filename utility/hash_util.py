import hashlib as hl
import json


def hash_string_265(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    #new way of hashing
    return hl.sha256(json.dumps(hashable_block,sort_keys=True).encode()).hexdigest()
    #old way of hashing
    #return '-'.join([str(block[key]) for key in block])
    
