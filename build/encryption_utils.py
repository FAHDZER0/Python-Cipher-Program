import numpy as np
import string
import math
import random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2



#====================================================================
#=====================shift_cipher_encrypt===========================
#====================================================================

def shift_cipher_encrypt(plaintext, shift):
    """
    Encrypts the plaintext using a Shift Cipher with the given shift.

    Parameters:
    plaintext (str): The plaintext message to be encrypted.
    shift (int): The number of positions to shift each character.

    Returns:
    str: The encrypted ciphertext.
    """
    ciphertext = ""
    for char in plaintext:
        # Encrypt uppercase letters
        if char.isupper():
            ciphertext += chr((ord(char) + shift - 65) % 26 + 65)
        # Encrypt lowercase letters
        elif char.islower():
            ciphertext += chr((ord(char) + shift - 97) % 26 + 97)
        # Keep other characters unchanged
        else:
            ciphertext += char
    return ciphertext

#====================================================================
#==========================Play_Fair_encrypt=========================
#====================================================================

# Function to convert the string to lowercase
def toLowerCase(text):
	return text.lower()

# Function to remove all spaces in a string
def removeSpaces(text):
	newText = ""
	for i in text:
		if i == " ":
			continue
		else:
			newText = newText + i
	return newText

# Function to group 2 elements of a string
# as a list element
def Diagraph(text):
	Diagraph = []
	group = 0
	for i in range(2, len(text), 2):
		Diagraph.append(text[group:i])

		group = i
	Diagraph.append(text[group:])
	return Diagraph

# Function to fill a letter in a string element
# If 2 letters in the same string matches
def FillerLetter(text):
	k = len(text)
	if k % 2 == 0:
		for i in range(0, k, 2):
			if text[i] == text[i+1]:
				new_word = text[0:i+1] + str('x') + text[i+1:]
				new_word = FillerLetter(new_word)
				break
			else:
				new_word = text
	else:
		for i in range(0, k-1, 2):
			if text[i] == text[i+1]:
				new_word = text[0:i+1] + str('x') + text[i+1:]
				new_word = FillerLetter(new_word)
				break
			else:
				new_word = text
	return new_word

list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
		'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Function to generate the 5x5 key square matrix
def generateKeyTable(word, list1):
	key_letters = []
	for i in word:
		if i not in key_letters:
			key_letters.append(i)

	compElements = []
	for i in key_letters:
		if i not in compElements:
			compElements.append(i)
	for i in list1:
		if i not in compElements:
			compElements.append(i)

	matrix = []
	while compElements != []:
		matrix.append(compElements[:5])
		compElements = compElements[5:]

	return matrix

def search(mat, element):
	for i in range(5):
		for j in range(5):
			if(mat[i][j] == element):
				return i, j

def encrypt_RowRule(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	if e1c == 4:
		char1 = matr[e1r][0]
	else:
		char1 = matr[e1r][e1c+1]

	char2 = ''
	if e2c == 4:
		char2 = matr[e2r][0]
	else:
		char2 = matr[e2r][e2c+1]

	return char1, char2

def encrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	if e1r == 4:
		char1 = matr[0][e1c]
	else:
		char1 = matr[e1r+1][e1c]

	char2 = ''
	if e2r == 4:
		char2 = matr[0][e2c]
	else:
		char2 = matr[e2r+1][e2c]

	return char1, char2

def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	char1 = matr[e1r][e2c]

	char2 = ''
	char2 = matr[e2r][e1c]

	return char1, char2

def encryptByPlayfairCipher(Matrix, plainList):
	CipherText = []
	for i in range(0, len(plainList)):
		c1 = 0
		c2 = 0
		ele1_x, ele1_y = search(Matrix, plainList[i][0])
		ele2_x, ele2_y = search(Matrix, plainList[i][1])

		if ele1_x == ele2_x:
			c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
			# Get 2 letter cipherText
		elif ele1_y == ele2_y:
			c1, c2 = encrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
		else:
			c1, c2 = encrypt_RectangleRule(
				Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

		cipher = c1 + c2
		CipherText.append(cipher)
	return CipherText

def Play_Fair_Encryption(text_Plain, key):
    text_Plain = removeSpaces(toLowerCase(text_Plain))
    PlainTextList = Diagraph(FillerLetter(text_Plain))
    if len(PlainTextList[-1]) != 2:
        PlainTextList[-1] = PlainTextList[-1]+'z'

    print("Key text:", key)
    key = toLowerCase(key)
    Matrix = generateKeyTable(key, list1)

    print("Plain Text:", text_Plain)
    CipherList = encryptByPlayfairCipher(Matrix, PlainTextList)

    CipherText = ""
    for i in CipherList:
        CipherText += i
    print("CipherText:", CipherText)
    return CipherText

#====================================================================
#=======================row_column_encrypt===========================
#====================================================================

def row_column_encrypt(plaintext, key):
    cipher = ""
    k_indx = 0				    # ---------------------------to track key indix
	
    msg_len = float(len(plaintext))	# ---------------------------to get message length 
    msg_lst = list(plaintext)			# ---------------------------to get list of the message 
    key_lst = sorted(list(key))	# ---------------------------to get list of the key 
    col = len(key)   		 	# ---------------------------calculate column of the matrix
    
    row = int(math.ceil(msg_len / col)) # -------------------calculate maximum row of the matrix
	
    fill_null = int((row * col) - msg_len) # ----------------the empty cell of the matix 
    msg_lst.extend('_' * fill_null) # -----------------------add the padding character '_' in empty
	
    # -------------------------------------------------------create Matrix and insert message and padding characters row-wise 
    matrix = []
    for i in range(0, len(msg_lst), col):
        row = msg_lst[i: i + col]
        matrix.append(row)
	
    # -------------------------------------------------------read matrix column-wise using key
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
        cipher += ''.join([row[curr_idx] 
                        for row in matrix])
        k_indx += 1
	
    return cipher

#====================================================================
#=======================rail_fence_encrypt===========================
#====================================================================

def rail_fence_encrypt(plaintext, rails):   
    # plaintext = plaintext.replace(" ", "")
    fence = [[] for _ in range(rails)]  # Create a list of empty lists to represent the fence
    rail = 0
    direction = 1  # Direction of movement along the rails (down or up)
    
    # Fill the fence with characters from the plaintext
    for char in plaintext:
        fence[rail].append(char)
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1  # Change direction when reaching the top or bottom rail
    
    # Flatten the fence and concatenate the characters
    encrypted_text = ''.join(char for rail in fence for char in rail)
    return encrypted_text

#====================================================================
#===========================AES_encrypt==============================
#====================================================================

def AES_Encryption(message, password):
    print ("AES_Encryption")
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)  # Generate a 256-bit key using PBKDF2
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    encrypted_message = f"salt = {salt}\nnonce = {cipher.nonce}\nciphertext = {ciphertext}\ntag = {tag}\n"
    return encrypted_message
    # return salt + cipher.nonce + ciphertext + tag

#====================================================================
#===========================Vigenere_encrypt=========================
#====================================================================

def vigenere_encrypt(plaintext, key):
    """
    Encrypts the plaintext using the Vigenère Cipher with the given key.

    Parameters:
    plaintext (str): The plaintext message to be encrypted.
    key (str): The key to use for encryption.

    Returns:
    str: The encrypted ciphertext.
    """
    ciphertext = ""
    key_index = 0  # Keep track of the current position in the key
    for char in plaintext:
        if char.isalpha():  # Encrypt only alphabetical characters
            # Convert the character to uppercase for consistency
            char = char.upper()
            # Calculate the shift value based on the current letter of the key
            shift = ord(key[key_index % len(key)].upper()) - ord('A')
            # Encrypt the character using the Vigenère cipher formula
            encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            ciphertext += encrypted_char
            # Move to the next letter of the key
            key_index += 1
        else:
            # Keep non-alphabetical characters unchanged
            ciphertext += char
    return ciphertext

#====================================================================
#===========================affine_encrypt===========================
#====================================================================

def mod_inverse(a, m):
    """
    Computes the modular multiplicative inverse of a modulo m.

    Parameters:
    a (int): The number to find the inverse of.
    m (int): The modulus.

    Returns:
    int: The modular multiplicative inverse of a modulo m, or None if it doesn't exist.
    """
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def affine_encrypt(plaintext, a, b):
    """
    Encrypts the plaintext using the Affine Cipher with the given keys (a, b).

    Parameters:
    plaintext (str): The plaintext message to be encrypted.
    a (int): The first key of the cipher (must be coprime with m, where m is the size of the alphabet).
    b (int): The second key of the cipher.

    Returns:
    str: The encrypted ciphertext.
    """
    # Define the alphabet
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Ensure that a is coprime with the size of the alphabet (26)
    if mod_inverse(a, len(alphabet)) is None:
        raise ValueError("The first key (a) must be coprime with the size of the alphabet.")

    ciphertext = ''
    for char in plaintext:
        if char.isalpha():  # Encrypt only alphabetical characters
            char_index = alphabet.index(char.upper())
            encrypted_index = (a * char_index + b) % len(alphabet)
            encrypted_char = alphabet[encrypted_index]
            # Preserve the case of the original character
            if char.islower():
                encrypted_char = encrypted_char.lower()
            ciphertext += encrypted_char
        else:
            # Keep non-alphabetical characters unchanged
            ciphertext += char
    return ciphertext

#====================================================================
#============================DES_encrypt=============================
#====================================================================

# Hexadecimal to binary conversion
def Hex_To_Bin(hex_string):
	mapping = {'0': "0000", '1': "0001", '2': "0010", '3': "0011",
		'4': "0100", '5': "0101", '6': "0110", '7': "0111",
		'8': "1000", '9': "1001", 'A': "1010", 'B': "1011",
		'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"}
	binary = ""
	for char in range(len(hex_string)):
		binary = binary + mapping[hex_string[char]]
	return binary

# Binary to hexadecimal conversion
def Bin_To_Hex(binary_string):
	mapping = {"0000": '0', "0001": '1', "0010": '2', "0011": '3',
		"0100": '4', "0101": '5', "0110": '6', "0111": '7',
		"1000": '8', "1001": '9', "1010": 'A', "1011": 'B',
		"1100": 'C', "1101": 'D', "1110": 'E', "1111": 'F'}
	hexadecimal = ""
	for i in range(0, len(binary_string), 4):
		chunk = ""
		chunk = chunk + binary_string[i]
		chunk = chunk + binary_string[i + 1]
		chunk = chunk + binary_string[i + 2]
		chunk = chunk + binary_string[i + 3]
		hexadecimal = hexadecimal + mapping[chunk]

	return hexadecimal

# Binary to decimal conversion
def Bin_To_Dec(binary):
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

# Decimal to binary conversion
def Dec_To_Bin(num):
	result = bin(num).replace("0b", "")
	if(len(result) % 4 != 0):
		div = len(result) / 4
		div = int(div)
		counter = (4 * (div + 1)) - len(result)
		for i in range(0, counter):
			result = '0' + result
	return result

# Permute function to rearrange the bits
def permute(data, table, size):
	permutation = ""
	for i in range(0, size):
		permutation = permutation + data[table[i] - 1]
	return permutation

# shifting the bits towards left by nth shifts
def shift_left(data, nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1, len(data)):
			s = s + data[j]
		s = s + data[0]
		data = s
		s = ""
	return data

# calculating xow of two strings of binary number a and b
def xor(a, b):
	result = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			result = result + "0"
		else:
			result = result + "1"
	return result

# Table of Position of 64 bits at initial level: Initial Permutation Table
initial_permutation = [58, 50, 42, 34, 26, 18, 10, 2,
                    60, 52, 44, 36, 28, 20, 12, 4,
                    62, 54, 46, 38, 30, 22, 14, 6,
                    64, 56, 48, 40, 32, 24, 16, 8,
                    57, 49, 41, 33, 25, 17, 9, 1,
                    59, 51, 43, 35, 27, 19, 11, 3,
                    61, 53, 45, 37, 29, 21, 13, 5,
                    63, 55, 47, 39, 31, 23, 15, 7]

# Expansion D-box Table
expansion_d = [32, 1, 2, 3, 4, 5, 4, 5,
            6, 7, 8, 9, 8, 9, 10, 11,
            12, 13, 12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21, 20, 21,
            22, 23, 24, 25, 24, 25, 26, 27,
            28, 29, 28, 29, 30, 31, 32, 1]

# Straight Permutation Table
permutation_table = [16, 7, 20, 21,
                29, 12, 28, 17,
                1, 15, 23, 26,
                5, 18, 31, 10,
                2, 8, 24, 14,
                32, 27, 3, 9,
                19, 13, 30, 6,
                22, 11, 4, 25]

# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

		[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

		[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

		[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

		[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

		[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

		[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Final Permutation Table
final_permutation = [40, 8, 48, 16, 56, 24, 64, 32,
                    39, 7, 47, 15, 55, 23, 63, 31,
                    38, 6, 46, 14, 54, 22, 62, 30,
                    37, 5, 45, 13, 53, 21, 61, 29,
                    36, 4, 44, 12, 52, 20, 60, 28,
                    35, 3, 43, 11, 51, 19, 59, 27,
                    34, 2, 42, 10, 50, 18, 58, 26,
                    33, 1, 41, 9, 49, 17, 57, 25]

def des_encrypt(plainText, roundedKeyBinary, roundedKey):
	plainText = Hex_To_Bin(plainText)

	# Initial Permutation
	plainText = permute(plainText, initial_permutation, 64)
	print("After initial permutation", Bin_To_Hex(plainText))

	# Splitting
	left = plainText[0:32]
	right = plainText[32:64]
	for i in range(0, 16):
		# Expansion D-box: Expanding the 32 bits data into 48 bits
		right_expanded = permute(right, expansion_d, 48)

		# XOR RoundKey[i] and right_expanded
		xor_x = xor(right_expanded, roundedKeyBinary[i])

		# S-boxex: substituting the value from s-box table by calculating row and column
		sbox_str = ""
		for j in range(0, 8):
			row = Bin_To_Dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
			col = Bin_To_Dec(
				int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
			val = sbox[j][row][col]
			sbox_str = sbox_str + Dec_To_Bin(val)

		# Straight D-box: After substituting rearranging the bits
		sbox_str = permute(sbox_str, permutation_table, 32)

		# XOR left and sbox_str
		result = xor(left, sbox_str)
		left = result

		# Swapper
		if(i != 15):
			left, right = right, left
		print("Round ", i + 1, " ", Bin_To_Hex(left),
			" ", Bin_To_Hex(right), " ", roundedKey[i])

	# Combination
	combine = left + right

	# Final permutation: final rearranging of bits to get cipher text
	cipher_text = permute(combine, final_permutation, 64)
	return cipher_text

def Des_Encryption(PlainText, key):
    # PlainText = "123456ABCD132536"
    # key = "AABB09182736CCDD"

    # Key generation
    # --hex to binary
    key = Hex_To_Bin(key)

    # --parity bit drop table
    keyp = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]

    # getting 56 bit key from 64 bit using the parity bits
    key = permute(key, keyp, 56)

    # Number of bit shifts
    shift_table = [1, 1, 2, 2,
                2, 2, 2, 2,
                1, 2, 2, 2,
                2, 2, 2, 1]

    # Key- Compression Table : Compression of key from 56 bits to 48 bits
    key_comp = [14, 17, 11, 24, 1, 5,
                3, 28, 15, 6, 21, 10,
                23, 19, 12, 4, 26, 8,
                16, 7, 27, 20, 13, 2,
                41, 52, 31, 37, 47, 55,
                30, 40, 51, 45, 33, 48,
                44, 49, 39, 56, 34, 53,
                46, 42, 50, 36, 29, 32]

    # Splitting
    left = key[0:28] # rkb for RoundKeys in binary
    right = key[28:56] # rk for RoundKeys in hexadecimal

    Rounded_Key_Binary = []
    Rounded_Key = []
    for i in range(0, 16):
        # Shifting the bits by nth shifts by checking from shift table
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])

        # Combination of left and right string
        combine_str = left + right

        # Compression of key from 56 to 48 bits
        round_key = permute(combine_str, key_comp, 48)

        Rounded_Key_Binary.append(round_key)
        Rounded_Key.append(Bin_To_Hex(round_key))

    print("Encryption")
    cipher_text = Bin_To_Hex(des_encrypt(PlainText, Rounded_Key_Binary, Rounded_Key))
    print("Cipher Text : ", cipher_text)

    # print("Decryption")
    # rkb_rev = Rounded_Key_Binary[::-1]
    # rk_rev = Rounded_Key[::-1]
    # text = Bin_To_Hex(des_encrypt(cipher_text, rkb_rev, rk_rev))
    # print("Plain Text : ", text)
    return cipher_text

#====================================================================
#=============================RSA_encrypt============================
#====================================================================

def enc_rsa_algo( msg: str , p: int,q: int):
    # n = pq
    n = p * q
    # z = (p-1)(q-1)
    z = (p-1)*(q-1)

    # e -> gcd(e,z)==1      ; 1 < e < z
    # d -> ed = 1(mod z)        ; 1 < d < z
    e = find_e(z)
    d = find_d(e, z)

    # Convert Plain Text -> Cypher Text
    cypher_text = ''
    # C = (P ^ e) % n
    for ch in msg:
        # convert the Character to ascii (ord)
        ch = ord(ch)
        # encrypt the char and add to cypher text
        # convert the calculated value to Characters(chr)
        cypher_text += chr((ch ** e) % n)
    print("Encrypted (Cypher text) : ", cypher_text)

    return cypher_text

def find_e(z: int):
    # e -> gcd(e,z)==1      ; 1 < e < z
    e = 2
    while e < z:
        # check if this is the required `e` value
        if gcd(e, z)==1:
            return e
        # else : increment and continue
        e += 1

def find_d(e: int, z: int):
    # d -> ed = 1(mod z)        ; 1 < d < z
    d = 2
    while d < z:
        # check if this is the required `d` value
        if ((d*e) % z)==1:
            return d
        # else : increment and continue
        d += 1

def gcd(x: int, y: int):
    # GCD by Euclidean method
    small,large = (x,y) if x<y else (y,x)

    while small != 0:
        temp = large % small
        large = small
        small = temp

    return large

#====================================================================
#=============================Hill_encrypt============================
#====================================================================

def Hill_Cipher_encrypt(message, key):
    # Define the key matrix
    key_matrix = [[0] * 3 for _ in range(3)]
    
    # Generate vector for the message
    message_vector = [[0] for _ in range(3)]
    
    # Generate vector for the cipher
    cipher_matrix = [[0] for _ in range(3)]
    
    # Generate the key matrix from the key string
    k = 0
    for i in range(3):
        for j in range(3):
            key_matrix[i][j] = ord(key[k]) % 65
            k += 1
    
    # Generate vector for the message
    for i in range(3):
        message_vector[i][0] = ord(message[i]) % 65
    
    # Encryption process
    for i in range(3):
        for j in range(1):
            cipher_matrix[i][j] = 0
            for x in range(3):
                cipher_matrix[i][j] += (key_matrix[i][x] * message_vector[x][j])
            cipher_matrix[i][j] = cipher_matrix[i][j] % 26
    
    # Generate the encrypted text from the encrypted vector
    cipher_text = []
    for i in range(3):
        cipher_text.append(chr(cipher_matrix[i][0] + 65))
    
    # Return the ciphertext
    return "".join(cipher_text)


#====================================================================
#=======================Substitution_encrypt=========================
#====================================================================

def create_substitution_dict(key):
    alphabet = string.ascii_lowercase
    substitution_dict = {}
    for i in range(len(alphabet)):
        substitution_dict[alphabet[i]] = key[i % len(key)]
    return substitution_dict

def Substitution_encrypt(message, key):
    substitution_dict = create_substitution_dict(key)
    cipher_text = []
    for char in message:
        if char.lower() in substitution_dict:
            temp = substitution_dict[char.lower()]
            if char.isupper():
                temp = temp.upper()
            cipher_text.append(temp)
        else:
            cipher_text.append(char)
    return "".join(cipher_text)

