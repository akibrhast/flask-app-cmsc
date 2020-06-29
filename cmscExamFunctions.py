import os
import time
from math import log
from if_condition_generator import *
# number = '00100000,00000000,00000000,00000000'
def FloatAnalysisBitsToValue(originalBinaryValue):
    originalBinaryValueCommaStripped = originalBinaryValue.replace(",","")
    sign = originalBinaryValue[0]
    
    if(sign=="0"):
        signInterpretation = "+"
    elif(sign=="1"):
        signInterpretation = "-"

    biasedExponent = originalBinaryValue[1:originalBinaryValue.find(",")+2]
    biasedExponent = biasedExponent.replace(",","")
    biasedExponentDEC = int(biasedExponent,2)
    trueexponent = biasedExponentDEC - 127
    significand = originalBinaryValue[originalBinaryValue.find(",")+2:].replace(",","")
    actualValueinBinary = "1." + significand
    overallValue = signInterpretation,trueexponent,actualValueinBinary

    result = {"sign"                : sign,
              "signInterpretation"  : signInterpretation,
              "biasedExponent"      :biasedExponent,
              "biasedExponentDEC"   :biasedExponentDEC,
              "trueexponent"        :trueexponent,
              "significand"         :significand,
              "actualValueinBinary" :actualValueinBinary,
              "overallValue"        :overallValue}
    # print(mylist[0:2])
    # print(mylist[2:5])
    # print(mylist[5:7])
    # print(mylist[7])
    
    return result


#Usage: argument 1 is a string charecter, argument 2 is "odd" or "even"
def AsciiParity(param):
    charecter,parity = param.split("+")
    
    bitRepre = bin(int.from_bytes(charecter.encode(),"big")).replace("0b","")
    numberOfOnes = bitRepre.count("1")
    
    if parity == "odd" and numberOfOnes%2 == 0:
        parityBit = 1
    elif parity == "odd" and numberOfOnes%2 != 0:
        parityBit = 0
    elif parity == "even" and numberOfOnes%2 == 0:
        parityBit = 0
    elif parity == "even" and numberOfOnes%2 != 0:
        parityBit = 1

    BitRepresentation = '{:0>7}'.format(bitRepre)
    
    result = {"BitRepresentation"   :   BitRepresentation,
              "numberOfOnes"        :   numberOfOnes,
              "parityBit"           :   parityBit}

    return result
    # print( "Bit Reresentation: ",BitRepresentation," <----- ", len(bitRepre),"bit") 
    # print("Number Of 1s: " , numberOfOnes)
    # print("Parity Bit: " , parityBit)


#hexaWord = "FDC62D93" , endian = "be" or "le"
def ByteOrder(param):
    hexaWord,endian = param.split("+")
    byteValue = bin(int(hexaWord,16)).replace("0b","")
    if endian == "be":
        hexlist = [hexaWord[0:2],hexaWord[2:4],hexaWord[4:6],hexaWord[6:8]]
        binlist = ('{:0>8}'.format(bin(int(hexlist[0],16)).replace("0b","")),
            '{:0>8}'.format(bin(int(hexlist[1],16)).replace("0b","")),
            '{:0>8}'.format(bin(int(hexlist[2],16)).replace("0b","")),
            '{:0>8}'.format(bin(int(hexlist[3],16)).replace("0b",""))
            )


        # print(hexaWord[0:2], "-",hexaWord[2:4],"-",hexaWord[4:6],"-",hexaWord[6:8])
        # print('{:0>8}'.format(bin(int(hexlist[0],16)).replace("0b","")),
        #     '{:0>8}'.format(bin(int(hexlist[1],16)).replace("0b","")),
        #     '{:0>8}'.format(bin(int(hexlist[2],16)).replace("0b","")),
        #     '{:0>8}'.format(bin(int(hexlist[3],16)).replace("0b",""))
        #     )

    elif endian == "le":
        hexlist = [hexaWord[6:8],hexaWord[4:6],hexaWord[2:4],hexaWord[0:2]]
        binlist = ('{:0>8}'.format(bin(int(hexlist[0],16)).replace("0b","")),
            '{:0>8}'.format(bin(int(hexlist[1],16)).replace("0b","")),
            '{:0>8}'.format(bin(int(hexlist[2],16)).replace("0b","")),
            '{:0>8}'.format(bin(int(hexlist[3],16)).replace("0b",""))
            )        
        # print(hexlist)
        # print('{:0>8}'.format(bin(int(hexlist[0],16)).replace("0b","")),
        #     '{:0>8}'.format(bin(int(hexlist[1],16)).replace("0b","")),
        #     '{:0>8}'.format(bin(int(hexlist[2],16)).replace("0b","")),
        #     '{:0>8}'.format(bin(int(hexlist[3],16)).replace("0b",""))
        #     )

    result = {
        "ByteValue (hex)" : hexlist,
        "ByteValue (binary)" : binlist
    }


    return result

def IntegerRepresentation(decimalValue):
    decimalValue = int(decimalValue)
    PositiveBinaryValue32bit = '{:0>32}'.format(bin(decimalValue).replace("0b",""))
    NegativeBinaryValue32Bit = bin((1<<31)+decimalValue ).replace("0b","")
    OnesComplementNegative = ''.join('1' if x == '0' else '0' for x in PositiveBinaryValue32bit)

    SignMagnitudePositiveOut = [(PositiveBinaryValue32bit[i:i+8]) for i in range(0, len(PositiveBinaryValue32bit), 8)]
    SignMagnitudeNegativeOut = [(NegativeBinaryValue32Bit[i:i+8]) for i in range(0, len(NegativeBinaryValue32Bit), 8)]
    
    OnesComplementPositiveOut = SignMagnitudePositiveOut
    OnesComplementNegativeOut = [(OnesComplementNegative[i:i+8]) for i in range(0, len(OnesComplementNegative), 8)]
    
    TwosComplementPositiveOut = SignMagnitudePositiveOut
    TwosComplementNegative = bin(int(OnesComplementNegative,2) + int("0b1",2)).replace("0b","")
    TwosComplementNegativeOut = [(TwosComplementNegative[i:i+8]) for i in range(0, len(TwosComplementNegative), 8)]

    result = {"SignMagnitudePositiveOut"  : SignMagnitudePositiveOut,
              "SignMagnitudeNegativeOut"  : SignMagnitudeNegativeOut,
              "OnesComplementPositiveOut" : OnesComplementPositiveOut,
              "OnesComplementNegativeOut" : OnesComplementNegativeOut,
              "TwosComplementPositiveOut" : TwosComplementPositiveOut,
              "TwosComplementNegativeOut" : TwosComplementNegativeOut}

    # print("SignMagnitudePositiveOut:  " , SignMagnitudePositiveOut)
    # print("SignMagnitudeNegativeOut:  " , SignMagnitudeNegativeOut)
    # print("="*75)
    # print("OnesComplementPositiveOut: " , OnesComplementPositiveOut)
    # print("OnesComplementNegativeOut: " , OnesComplementNegativeOut)
    # print("="*75)
    # print("TwosComplementPositiveOut: " , TwosComplementPositiveOut)
    # print("TwosComplementNegativeOut: " , TwosComplementNegativeOut)
    return result

  
def IntegerAnalysisBitsToValue(hexValue):
    #Sorted positions of the 1 bits delimited by commas (,) without space:	
    binaryValue = bin(int(hexValue,16)).replace("0b","")
    bitThatDeterminesSign = int(hexValue.replace("0x","")[0],16)
    reversedBinaryValue = ''.join(reversed(binaryValue))
    PositionOfOnesList = []


    for index in reversed(range(0, len(reversedBinaryValue))):
        if reversedBinaryValue[index] == '1':
            PositionOfOnesList.append(index)
    
    

    #Sorted numeric expression without space:
    PositionOfOnesListString = [ str(x) for x in PositionOfOnesList]
    SortedNumericExpression = ["2^" + x for x in PositionOfOnesListString]
    if bitThatDeterminesSign >= int("8",16):
        outSortedNumericExpression = "-" + '+'.join([x for x in SortedNumericExpression])
    elif bitThatDeterminesSign < int("8",16):
        outSortedNumericExpression = '+'.join([x for x in SortedNumericExpression])
    
    #Overall Interger Value
    overAllInterValue = eval(outSortedNumericExpression.replace("^","**"))

    result = {"PositionOfOnesList"         : PositionOfOnesList,
              "outSortedNumericExpression" : outSortedNumericExpression,
              "overAllInterValue"          : overAllInterValue}

    return result
    # print(PositionOfOnesList)
    # print(outSortedNumericExpression)
    # print(overAllInterValue)


def CodeIfElseTest(ifloop):
    result = parser.parse(ifloop)
    return result
    # print(result)




# CodeIfElseTest('''
# if ( X0 == 11 ) {
# X10 = X0 ;
# }
# else {
# X10 = 11 ;
# }
# ''')
#IntegerAnalysisBitsToValue("0xC0209400")
#IntegerRepresentation("500")
#ByteOrder("83903990","le")
#AsciiParity("c","odd")
#FloatAnalysisBitsToValue( "00100000,00000000,00000000,00000000" )

























#incomplete
# def RamDesign(BoardSize,ChipSize):
#     BoardSize = BoardSize * 10000
#     ChipSize = ChipSize * 10000

#     numberofAdressLinesToBoard = round(log(BoardSize)/log(2))
#     numberofAdressLinesToChip = round(log(ChipSize)/log(2))

#     numberofChips = BoardSize/ChipSize
#     sizeOfDecoderOnBoard = log(numberofChips)/log(2)
#     #sizeOfDecoderOnChip =   

