import numpy as np

# Implementação da cifra de Vigenère

def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key_len = len(key)
    key_pos = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_pos % key_len].lower()) - ord('a')
            if char.isupper():
                ciphertext += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                ciphertext += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            key_pos += 1
        else:
            ciphertext += char
    return ciphertext


# Implementação da cifra de Hill

def hill_encrypt(plaintext, key):
    n = key.shape[0]
    plaintext = plaintext.lower().replace(' ', '')
    plaintext_len = len(plaintext)
    if plaintext_len % n != 0:
        plaintext += 'x' * (n - plaintext_len % n)
        plaintext_len = len(plaintext)
    ciphertext = ""
    for i in range(0, plaintext_len, n):
        block = np.array([ord(char) - ord('a') for char in plaintext[i:i+n]])
        block = block.reshape((n, 1))
        result = key @ block
        result = result.flatten() % 26
        ciphertext += "".join([chr(char + ord('a')) for char in result])
    return ciphertext

def hill_decrypt(ciphertext, key):
    n = key.shape[0]
    det = int(np.round(np.linalg.det(key))) % 26
    inv_det = -1
    for i in range(26):
        if (det * i) % 26 == 1:
            inv_det = i
            break
    if inv_det == -1:
        return "Invalid key"
    inv_key = inv_det * np.round(np.linalg.inv(key) * det) % 26
    inv_key = inv_key.astype(int)
    plaintext = ""
    ciphertext_len = len(ciphertext)
    for i in range(0, ciphertext_len, n):
        block = np.array([ord(char) - ord('a') for char in ciphertext[i:i+n]])
        block = block.reshape((n, 1))
        result = inv_key @ block
        result = result.flatten() % 26
        plaintext += "".join([chr(char + ord('a')) for char in result])
    return plaintext.replace('x', '')

def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key_len = len(key)
    key_pos = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_pos % key_len].lower()) - ord('a')
            if char.isupper():
                plaintext += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                plaintext += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            key_pos += 1
        else:
            plaintext += char
    return plaintext



# Combinação das cifras

def vigenere_hill_encrypt(plaintext, vigenere_key, hill_key):
    ciphertext = vigenere_encrypt(plaintext, vigenere_key)
    ciphertext = hill_encrypt(ciphertext, hill_key)
    return ciphertext


def vigenere_hill_decrypt(ciphertext, vigenere_key, hill_key):
    plaintext = hill_decrypt(ciphertext, hill_key)
    plaintext = vigenere_decrypt(plaintext, vigenere_key)
    return plaintext