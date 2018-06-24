UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'
def loadDictionary():
    dictionaryFile = open('dictionary.txt')
    englishWords={}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word]=None
    dictionaryFile.close()
    return englishWords
ENGLISH_WORDS=loadDictionary()
def getEnglishCount(message):
    #print(message)
    message=removeNoneLetters(message)
    #print(message)
    message=message.upper()
    possibleWords = message.split()
    #print(possibleWords)
    matched=0
    for word in possibleWords:

        if(word in ENGLISH_WORDS):
            matched+=1
    #print(matched)
    return float(matched) / len(possibleWords)
def removeNoneLetters(message):
    letters=[]
    for symbol in message:
        if(symbol in LETTERS_AND_SPACE):
            letters.append(symbol)
    return ''.join(letters)
def isEnglish(message, wordPercentage=20, letterPercentage=85):
    wordsMatch = getEnglishCount(message) * 100 >= wordPercentage
    #print(getEnglishCount(message))
    
    numLetters = len(removeNoneLetters(message))
    messageLettersPercentage = float(numLetters) / len(message) * 100
    #print(messageLettersPercentage)
    lettersMatch = messageLettersPercentage >= letterPercentage
    return wordsMatch and lettersMatch

