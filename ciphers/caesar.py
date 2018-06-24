message = input("Enter message: ")
letter ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
mode = "encrypt"
key =13
message=message.upper()
translated=''
for c in message :
    if(c in letter):
        num = letter.find(c)
        if(mode=="encrypt"):
            num=num+key
        elif(mode=="decrypt"):
            num=num-key
        if(num>=len(letter)):
            num=num-len(letter)
        if num <0:
            num = num +len(letter)
        translated=translated + letter[num]
    else:
        translated=translated+c
print(translated)

