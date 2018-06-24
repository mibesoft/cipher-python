import math
def main():
    message=input('Enter message: ')
    encryptedMessage=descryptMessage(8,message)
    print(encryptedMessage)
def encryptMessage(key, message):
    ciphertext = [''] * key
    for i in range(key):
        pointer= i
        while pointer < len(message):
            ciphertext[i]+=message[pointer]
            pointer+=key
    return ''.join(ciphertext)
def descryptMessage(key, ciphertext):
    numOfColumns=math.ceil(len(ciphertext)/key)
    numOfRows=key
    numOfShadedBoxes=numOfRows*numOfColumns-len(ciphertext)
    plaintext = [''] * numOfColumns
    col = 0
    row = 0
    for symbol in ciphertext:
        plaintext[col] += symbol
        col += 1 # point to next column
        if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            col = 0
            row += 1
    return ''.join(plaintext)

    message=encryptMessage(numOfColumn,ciphertext)
    return message


if __name__=='__main__':
    main()

