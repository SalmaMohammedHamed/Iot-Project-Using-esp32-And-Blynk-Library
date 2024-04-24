#used packages
import random
import math
import matplotlib.pyplot as plt


NumOfSymbols = 1000
#number of bit represents every modulation type
BPSK = 1
PSK8 = 3
QPSK = 2
QAM16 = 4

#initialize the Data Stream lists
BPSK_DataStream = [0] * NumOfSymbols
QPSK_DataStream = [0] * NumOfSymbols * QPSK
PSK8_DataStream = [0] * NumOfSymbols * PSK8
QAM16_DataStream = [0] * NumOfSymbols * QAM16

#initialize the mapped Sympols lists
BPSK_Mapped = [0] * NumOfSymbols
QPSK_Mapped = [0] * NumOfSymbols
PSK8_Mapped = [0] * NumOfSymbols
QAM16_Mapped = [0] * NumOfSymbols

#the symbols position on the sample space for every modulation type
QPSK_Positions = [(-1,-1) , (-1,1) , (1,-1) , (1,1)]
QAM16_Positions = [(-3,-3) , (-3,-1) , (-3,3) , (-3,1) , (-1,-3) , (-1,-1) , (-1,3) , (-1,1) ,(3,-3) , (3,-1) , (3,3) , (3,1) , (1,-3) , (1,-1) , (1,3) , (1,1)]
#PSK8_Positions are calculated from cos((i-1)*pi/4) + i*sin((i-1)*pi/4) relation 
PSK8_Positions = []
tolerance = 1e-15 
for i in range(1, 9):  # Range from 1 to 8 inclusive
    angle = (i - 1) * math.pi / 4
    cos_value = math.cos(angle)
    sin_value = math.sin(angle)
    # Check if the cosine value is close to zero due to the due to the unaccuracy
    if abs(cos_value) < tolerance:
        cos_value = 0
    # Check if the sine value is close to zero due to the unaccuracy
    if abs(sin_value) < tolerance:
        sin_value = 0
    position = (cos_value, sin_value)
    PSK8_Positions.append(position)

#initialize the Demapped lists
BPSK_DeMapped = [0]*NumOfSymbols
QPSK_DeMapped = []
PSK8_DeMapped = []
QAM16_DeMapped = []


#Data Creation Function
def DataCreation(ModulationType):
    global BPSK_DataStream, QPSK_DataStream, PSK8_DataStream, QAM16_DataStream #to be able to edit global variables
    #generating NumOfSymbols * ModulationType random uniformly distributed binar bits
    random_numbers = [random.randint(0, 1) for _ in range(NumOfSymbols * ModulationType)] 
    #butting the result in the corresponding list
    if ModulationType == BPSK:
        BPSK_DataStream = random_numbers
    elif ModulationType == QPSK:
        QPSK_DataStream = random_numbers
    elif ModulationType == PSK8:
        PSK8_DataStream = random_numbers
    elif ModulationType == QAM16:
        QAM16_DataStream = random_numbers
    else:
        print('Wrong Modulation Type')



#Mapper function (to map the bit stream to sympols)
def Mapper(ModulationType):
    global BPSK_Mapped, QPSK_Mapped, PSK8_Mapped, QAM16_Mapped #to be able to edit global variables
    if ModulationType == BPSK:
        for index, item in enumerate(BPSK_DataStream):
            BPSK_Mapped[index] = 2*item-1   #1->1 & 0->-1

    elif ModulationType == QPSK:
        for i in range(0, len(QPSK_DataStream), QPSK):
            symbol = QPSK_DataStream[i:i+QPSK]  #every 2 bit is a symbol
            decimal_value = int(''.join(map(str, symbol)), 2) #getting the decimal value of the symbol
            QPSK_Mapped[i//QPSK] = QPSK_Positions[decimal_value] #map to the coresponding symbol

    elif ModulationType == PSK8:
        for i in range(0, len(PSK8_DataStream), PSK8):
            symbol = PSK8_DataStream[i:i+PSK8]  #every 3 bit is a symbol
            decimal_value = int(''.join(map(str, symbol)), 2)#getting the decimal value of the symbol
            PSK8_Mapped[i//PSK8] = PSK8_Positions[decimal_value]#map to the coresponding symbol

    elif ModulationType == QAM16:
        for i in range(0, len(QAM16_DataStream), QAM16):
            symbol = QAM16_DataStream[i:i+QAM16]#every 4 bit is a symbol
            decimal_value = int(''.join(map(str, symbol)), 2)#getting the decimal value of the symbol
            QAM16_Mapped[i//QAM16] = QAM16_Positions[decimal_value]#map to the coresponding symbol
        
    else:
        print('Wrong Modulation Type')

#the demapper function (get the data Stream from the recieved symbols)
""""
NOTE:
after creating the channel replace every mapped data by the mapped data after the channel
"""
def DeMapper(ModulationType):
    global BPSK_DeMapped, QPSK_DeMapped, PSK8_DeMapped, QAM16_DeMapped
    if ModulationType == BPSK:
        for i in range(0,len(BPSK_DataStream)):
                BPSK_DeMapped[i] =int(BPSK_Mapped[i]/2 + 0.5) #-1->0 & 1->1
    elif ModulationType == QPSK:
        for i in range(NumOfSymbols):
            TempList = format(QPSK_Positions.index(QPSK_Mapped[i]), '02b') #represent the symbol decimal value in 2 binary bits
            QPSK_DeMapped.extend(map(int, TempList))#append the bits to the demapped version as int

    elif ModulationType == PSK8:
        for i in range(NumOfSymbols):
            TempList = format(PSK8_Positions.index(PSK8_Mapped[i]), '03b')#represent the symbol decimal value in 3 binary bits
            PSK8_DeMapped.extend(map(int, TempList))#append the bits to the demapped version as int
            

    elif ModulationType == QAM16:
        for i in range(NumOfSymbols):
            TempList = format(QAM16_Positions.index(QAM16_Mapped[i]), '04b')#represent the symbol decimal value in 4 binary bits
            QAM16_DeMapped.extend(map(int, TempList))#append the bits to the demapped version as int
            

    else:
        print('Wrong Modulation Type')



DataCreation(BPSK)
Mapper(BPSK)
DeMapper(BPSK)
print(BPSK_DataStream==BPSK_DeMapped)


DataCreation(QPSK)
Mapper(QPSK)
DeMapper(QPSK)
print(QPSK_DataStream==QPSK_DeMapped)

DataCreation(PSK8)
Mapper(PSK8)
DeMapper(PSK8)
print(PSK8_DataStream==PSK8_DeMapped)

DataCreation(QAM16)
Mapper(QAM16)
DeMapper(QAM16)
print(QAM16_DataStream==QAM16_DeMapped)
