import transposition, englishdetect
myMessage = """Cb b rssti aieih rooaopbrtnsceee er es no npfgcwu  plri ch nitaalr eiuengiteehb(e1  hilincegeoamn fubehgtarndcstudmd nM eu eacBoltaeteeoinebcdkyremdteghn.aa2r81a condari fmps" tad   l t oisn sit u1rnd stara nvhn fsedbh ee,n  e necrg6  8nmisv l nc muiftegiitm tutmg cm shSs9fcie ebintcaets h  aihda cctrhe ele 1O7 aaoem waoaatdahretnhechaopnooeapece9etfncdbgsoeb uuteitgna.rteoh add e,D7c1Etnpneehtn beete" evecoal lsfmcrl iu1cifgo ai. sl1rchdnheev sh meBd ies e9t)nh,htcnoecplrrh ,ide hmtlme. pheaLem,toeinfgn t e9yce da' eN eMp a ffn Fc1o ge eohg dere.eec s nfap yox hla yon. lnrnsreaBoa t,e eitsw il ulpbdofgBRe bwlmprraio po  droB wtinue r Pieno nc ayieeto'lulcih sfnc  ownaSserbereiaSm-eaiah, nnrttgcC  maciiritvledastinideI  nn rms iehn tsigaBmuoetcetias rn"""

def main():
    hackedMessage=hackTransposition(myMessage)
    if(hackedMessage==None):
        print('Decrypt message fail!!!!!')
    else:
        print("Translated message:")
        print(hackedMessage)
def hackTransposition(message):
    print("Hacking transposition....")
    print("Press C to stop encrypt")
    for i in range(1,len(message)) :
        translated=transposition.descryptMessage(i,message)
        #print(translated)
        #print(i)
        if(englishdetect.isEnglish(translated)):
            #print(translated)
            #response=input('> ')
            #if(response.upper()=='C'):
            #print(translated)
            return translated
    return None
if(__name__=='__main__'):
    main()

