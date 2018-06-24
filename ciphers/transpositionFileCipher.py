import time, os, transposition, sys
def main():
    fileName= input('Emter file name: ')
    if not os.path.exists(fileName):
        print('File not exist')
        sys.exit()
    outputFileName=fileName+'encrypted.txt'
    if os.path.exists(outputFileName):
        print('This will overwrite the file %s. (C)ontinue or (Q)uit?' % (outputFileName))
        e = input('> ')
        if e!='c':
            sys.exit()
    mode = ''
    while(mode!='e' and mode !='d'):
        mode = input('Please select mode, press e for (e)ncript, d for (d)ecrypt')
    startTime=time.time()
    fileObject=open(fileName)
    fileContent=fileObject.read()
    fileObject.close()
    if(mode=="e"):
        print('Encrypting file %s' %(fileName))
        translated=transposition.encryptMessage(10,fileContent)
    if(mode=='d'):
        print('Decrypting file %s' %(fileName))
        translated=transposition.descryptMessage(10,fileContent)
    outputFileObject=open(outputFileName,'w')
    outputFileObject.write(translated)
    outputFileObject.close()
    print('processing file success')
    totalTime = round(time.time() - startTime, 2)
    print('%secryption time: %s seconds' % (mode, totalTime))
if __name__=='__main__':
    main()

