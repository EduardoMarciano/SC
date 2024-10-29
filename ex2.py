import math
import random
import itertools
import numpy as np
import pandas as pd
from digrafos import frequencia_digrafos

def alphabet_mapping():
    alphabet_map = {}
    for i in range(ord('a'), ord('z') + 1):
        alphabet_map[chr(i)] = i - ord('a')
    return alphabet_map

def generate_key(alphabet_map, characters_length = 10):

    if characters_length < 1 or characters_length > 26:
        characters_length = 26

    shuffled_map = list(alphabet_map.items()).copy()
    random.shuffle(shuffled_map)
    
    key = []
    for i in range(characters_length):
        key.append(shuffled_map[i][0])

    return key

def encrypt_transposition(alphabet_map, plain_text, key):
    key_length = len(key)
    sorted_key = sorted(key)
    
    num_rows = len(plain_text) // key_length
    if (len(plain_text) % key_length) != 0:
        num_rows = num_rows+1

    matrix = []
    for _ in range(num_rows):
        matrix.append([''] * key_length)

    index = 0
    for row in range(len(matrix)):
        for c in range(len(matrix[row])):
            if(index < len(plain_text)):
                matrix[row][c] = plain_text[index]
            else:
                adjusted_index = (index - len(plain_text)) % len(alphabet_map)
                matrix[row][c] = chr(adjusted_index+ord('a'))
            index += 1

    cypher_text = ''

    for i in range(len(key)):
        col = key.index(sorted_key[i])
        for row in matrix:
            cypher_text = cypher_text + row[col]

    return cypher_text
    

def decrypt_transposition(alphabet_map, cypher_text, key):
    key_length = len(key)
    sorted_key = sorted(key)

    num_rows = len(cypher_text) // key_length
    if (len(cypher_text) % key_length) != 0:
        num_rows += 1

    matrix = []
    for _ in range(num_rows):
        matrix.append([''] * key_length)

    col = 0
    for i in range(len(key)):
        index = key.index(sorted_key[i])
        for row in range(num_rows):
            matrix[row][index] = cypher_text[col]
            col += 1

    plain_text = ''
    for row in matrix:
        plain_text += ''.join(row)
        
    return plain_text

def calculate_score(df, column_sequence, cypher_text, key_length):
    num_rows = len(cypher_text) // key_length
    if len(cypher_text) % key_length != 0:
        num_rows += 1
    
    matrix = [[''] * key_length for _ in range(num_rows)]
    col = 0
    for i in range(len(column_sequence)):
        index = column_sequence[i]
        for row in range(num_rows):
            if col < len(cypher_text):
                matrix[row][index] = cypher_text[col]
                col += 1

    # Calcula o score baseado na frequência dos dígrafos
    score = 0
    for row in matrix:
        for i in range(len(row) - 1):
            if row[i] and row[i + 1]:
                digraph = row[i] + row[i + 1]
                if digraph[0] in df.index and digraph[1] in df.columns:
                    score += df.at[digraph[0], digraph[1]]
    
    return score

import itertools

def break_transposition_cipher(df, alphabet_map, cypher_text):
    key_length = 4
    best_sequence = None
    best_score = -1
    
    # Gerar todas as combinações possíveis de colunas
    for perm in itertools.permutations(range(key_length)):
        score = calculate_score(df, perm, cypher_text, key_length)
        
        if score > best_score:
            best_score = score
            best_sequence = perm
    
    # Decifrar o texto com a melhor sequência encontrada
    plain_text = decrypt_transposition(alphabet_map, cypher_text, best_sequence)
    return plain_text

alphabet_map = alphabet_mapping()

plain_text = "aexploracaodemartecomecoucomasprimeirasmissoesnasdecadaspassadascomosondasmarinerosondaespectrometrogasasdeaguaparaentenderocomopodemoscampanharasatividadesnaexploracaoumadasmissõesfuturasincluemroverparacolonizacaoencontrarprovasdevidaexistenaarquiteturasustentavelnasuperficieasdescobertasemrevolucionaramoconhecimentoalienigenaesistemadevigilanciaespacialavancadaestamoscadavezmaisproximosdenovasdescobertasqueseramfundamentaisparanossacompreensaoesperoquesimulationsdevidaextraterrestreajudemanoceanodeconhecimentoemexploracaomarteenossoplaneta"
print(f"Texto original: {plain_text}")

key = generate_key(alphabet_map, 4)
print(f"Chave de encriptação gerada: {key}")

cypher_text = encrypt_transposition(alphabet_map, plain_text, key)
print(f"Texto cifrado gerado: {cypher_text}")

decrypted_text_with_key = decrypt_transposition(alphabet_map, cypher_text, key)
print(f"Texto resultante da desencriptação com a chave: {decrypted_text_with_key}")

#Preparando os dados para o Pandas
tamanho_grupo = 26
data= [frequencia_digrafos[i:i + tamanho_grupo] for i in range(0, len(frequencia_digrafos), tamanho_grupo)]
#Criando um DataFrame com Pandas
df = pd.DataFrame(data)
# Ajusta o índice e colunas conforme necessário
df.index = [chr(i) for i in range(ord('a'), ord('z') + 1)]
df.columns = [chr(i) for i in range(ord('a'), ord('z') + 1)]

decrypted_text_without_key = break_transposition_cipher(df, alphabet_map, cypher_text)
print(f"Texto originado da desencriptação sem a chave: {decrypted_text_without_key}")
