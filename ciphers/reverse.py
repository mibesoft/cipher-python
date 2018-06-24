message = input('Enter message: ')
i = len(message)
translated=''
while(i>0):
    translated=translated + message[i-1]
    i=i-1
print(translated)

