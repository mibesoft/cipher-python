import random, sys, transposition
def main():
    num=40
    for i in range(num):
        message = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' * random.randint(4, 40)
        message = list(message)
        random.shuffle(message)
        message = ''.join(message) # convert list to string
        print('Test #%s: "%s..."' % (i+1, message[:50]))
        for key in range(len(message)):
            encrypttext=transposition.encryptMessage(key+1,message)
            if(transposition.descryptMessage(key+1, encrypttext)!=message):
                print("failed")
                print(key)
                print(message)
                print(encrypttext)
                print(transposition.descryptMessage(key+1, encrypttext))
                sys.exit()
    print("transposition passed")
if __name__=='__main__':
    main()
