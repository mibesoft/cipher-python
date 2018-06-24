message = input("enter your encrypted message: ")
message=message.upper()
letter ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(len(letter)):
    translated=''
    for c in message:
        if c in letter:
            num=letter.find(c)
            num=num-i
            if num > len(letter):
                num = num- len(letter)
            if num <0:
                num = num + len(letter)
            translated= translated+letter[num]
        else:
            translated= translated+c
    print(translated)



