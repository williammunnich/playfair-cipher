#Verbose version below
#1 Create the digram diagram/grid by taking the key word 
#       and puting it from left to right into the grid. If there are repeated letters switch out with replacement letter. 
#       After key word is placed in, fill in remaining alpbhabet letters in alphabetical order
#       
#2 take the plaintext and split into pairs of letters. Repeated letters in a pair get a replacement letter then shifted to the right
#       stand alone letters get a replacement letter as its pair
#
#3 For encryption, using the cipher grid, if pair are in the same column, replace the letter with its neigbor to the bottom, or wrap around
#
#4 For encryption, using the cipher grid, if pair are in the same row, replace the letter with its neigbor to the right, or wrap around
#
#5 For encryption, using the cipher grid, if pair are not in same row or grid, make a box, swap with the letter in the same row inside the box

#take input for plain text
text_Plain = input("Enter what will be plaintext: ")
#take input for the encryption key
key = input("Enter what will be the key: ")


#sanitizing functions
def toLowerCase(text):
    	return text.lower()
def removeSpaces(text):
	newText = ""
	for i in text:
		if i == " ":
			continue
		else:
			newText = newText + i
	return newText

#group 2 elements of a string as a list
def Diagraph(text):
	Diagraph = []
	group = 0
	for i in range(2, len(text), 2):
		Diagraph.append(text[group:i])

		group = i
	Diagraph.append(text[group:])
	return Diagraph

#fill a letter if two letter match
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


#generate 5x5 square key
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

#search for repeated/match
def search(mat, element):
	for i in range(5):
		for j in range(5):
			if(mat[i][j] == element):
				return i, j

#rule #4, row rule
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

#rule #3, column rule
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

#rule #5, rectangle rule
def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
	char1 = ''
	char1 = matr[e1r][e2c]

	char2 = ''
	char2 = matr[e2r][e1c]

	return char1, char2


def encryptByPlayfairCipher(Matrix, plainList):
	CipherText = []
    
    #breaks into chunks of 2
	for i in range(0, len(plainList)):
		c1 = 0
		c2 = 0
		ele1_x, ele1_y = search(Matrix, plainList[i][0])
		ele2_x, ele2_y = search(Matrix, plainList[i][1])

        #handle cases for rule #4, #3, #5 respectivley
		if ele1_x == ele2_x:
			c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
			# Get 2 letter cipherText
		elif ele1_y == ele2_y:
			c1, c2 = encrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
		else:
			c1, c2 = encrypt_RectangleRule(
				Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        #reunite two letters in chunk
		cipher = c1 + c2
		CipherText.append(cipher)
	return CipherText

#santitize
text_Plain = removeSpaces(toLowerCase(text_Plain))
#sanitize
PlainTextList = Diagraph(FillerLetter(text_Plain))

#if groupings of plaintext are same insert filler 'z'
if len(PlainTextList[-1]) != 2:
	PlainTextList[-1] = PlainTextList[-1]+'z'


#sanitize
key = toLowerCase(key)

#generate a matrix for encryption and print the outcome
Matrix = generateKeyTable(key, list1)
print("\n\nPlayfair cipher grid: ")
for row in Matrix:
    print(row)
   
#print key and plaintext(sanitized)    
print("Key text:", key)
print("Plain Text:", text_Plain)

#create a list of encrypted letter pairs
CipherList = encryptByPlayfairCipher(Matrix, PlainTextList)

#append list of encrypted to cyphertext string then print/show
CipherText = ""
for i in CipherList:
	CipherText += i
print("CipherText:", CipherText)
