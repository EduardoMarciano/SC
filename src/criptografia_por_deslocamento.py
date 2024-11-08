import math
import random
import itertools
import unicodedata
import numpy as np
import pandas as pd
from data.letras import frequencia_letras

def alphabet_mapping():
    alphabet_map = {}
    for i in range(ord('a'), ord('z') + 1):
        alphabet_map[chr(i)] = i - ord('a')
    return alphabet_map

def generate_key():
    return random.randint(1, 25)

def read_plain_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        plain_text = file.read()
    
    plain_text = plain_text.replace(" ", "")
    
    plain_text = unicodedata.normalize('NFD', plain_text)
    plain_text = ''.join(char for char in plain_text if unicodedata.category(char) != 'Mn')
    
    plain_text = plain_text.lower().replace("ç", "")
    plain_text = plain_text.replace(".", "")
    plain_text = plain_text.replace(",", "")
    plain_text = plain_text.replace("-", "")
    plain_text = plain_text.replace(":", "")
    plain_text = plain_text.replace(";", "")
    plain_text = plain_text.replace(")", "")
    plain_text = plain_text.replace("(", "")
    plain_text = plain_text.replace("{", "")
    plain_text = plain_text.replace("}", "")
    plain_text = plain_text.replace("\n", "")
    
    return plain_text


def encrypt(alphabet_map, plain_text, key):
    encrypted_text = []
    for char in plain_text:
        if char in alphabet_map:
            new_index = (alphabet_map[char] + key) % len(alphabet_map)
            encrypted_text.append(list(alphabet_map.keys())[new_index])

    return ''.join(encrypted_text)

def decrypt(alphabet_map, cypher_text, key):
    decrypted_text = []
    for char in cypher_text:
        if char in alphabet_map:
            new_index = (alphabet_map[char] - key) % len(alphabet_map)
            decrypted_text.append(list(alphabet_map.keys())[new_index])
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

import numpy as np

def break_shift_cipher(alphabet_map, cypher_text):
    alphabet = list(alphabet_map.keys())
    cypher_frequencies = {letter: 0 for letter in alphabet}
    
    for char in cypher_text:
        if char in cypher_frequencies:
            cypher_frequencies[char] += 1
    
    total_letters = sum(cypher_frequencies.values())
    cypher_frequencies = {k: (v / total_letters) * 100 for k, v in cypher_frequencies.items()}
    
    best_key = None
    best_correlation = float('-inf')
    
    for key in range(len(alphabet)):
        shifted_frequencies = [0] * len(alphabet)
        
        for i, letter in enumerate(alphabet):
            shifted_index = (i - key) % len(alphabet)
            shifted_frequencies[shifted_index] = cypher_frequencies.get(letter, 0)
        
        correlation = 0
        for i in range(len(alphabet)):
            correlation += shifted_frequencies[i] * frequencia_letras[i]
        
        if correlation > best_correlation:
            best_correlation = correlation
            best_key = key
    
    decrypted_text = decrypt(alphabet_map, cypher_text, best_key)
    
    return decrypted_text


alphabet_map = alphabet_mapping()

plain_text = plain_text = read_plain_text("../src/data/revo_bichos.txt")
print(f"Texto original: {plain_text}")

key = generate_key()
print(f"Chave de encriptação gerada: {key}")

cypher_text = encrypt(alphabet_map, plain_text, key)
print(f"Texto cifrado gerado:\n {cypher_text}")

decrypted_text_with_key = decrypt(alphabet_map, cypher_text, key)
print(f"Texto resultante da desencriptação com a chave:\n {decrypted_text_with_key}")

decrypted_text_without_key = break_shift_cipher(alphabet_map, cypher_text)
print(f"Texto originado da desencriptação sem a chave: {decrypted_text_without_key}")

if decrypted_text_with_key == plain_text:
    print("Criptografia gerada e revertida com sucesso!!")

if decrypted_text_without_key == plain_text:
    print("Criptografia quebrada com sucesso!!")
