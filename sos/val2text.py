# -*- coding: utf-8 -*-
import math

class val2text:
    """Translate numeric value into text"""
    i = {}
    i[1] = "jeden"
    i[2] = "dwa"
    i[3] = "trzy"
    i[4] = "cztery"
    i[5] = "pięć"
    i[6] = "sześć"
    i[7] = "siedem"
    i[8] = "osiem"
    i[9] = "dziewięc"
    i[10] = "dziesięć"
    i[11] = "jedenaście"
    i[12] = "dwanaście"
    i[13] = "trzynaście"
    i[14] = "czternaście"
    i[15] = "pietnaście"
    i[16] = "szesnaście"
    i[17] = "siedemaście"
    i[18] = "osiemnaście"
    i[19] = "dziewietnaście"
    i[20] = "dwadzieścia"
    i[30] = "trzydzieści"
    i[40] = "czterdzieści"
    i[50] = "pięćdziesiąt"
    i[60] = "sześćdziesiąt"
    i[70] = "siedemdziesiąt"
    i[80] = "osiemdziesiąt"
    i[90] = "dziewięćdziesiąt"
    i[100] = "sto"
    i[200] = "dwieście"
    i[300] = "trzysta"
    i[400] = "czterysta"
    i[500] = "pięćset"
    i[600] = "sześćset"
    i[700] = "siedemset"
    i[800] = "osiemset"
    i[900] = "dziewięćset"
    i[1000] = "tysiąc"

    t = {}
    t['t3a'] = 'tysiące'
    t['t3b'] = 'tysięcy'

    def len1(self, inNumber):
        return self.i[inNumber]

    def len2(self, inNumber):
        n = divmod(inNumber,10)
        m = inNumber
        num1 = self.i[n[0]*10]
        if n[0] >1 and n[1] > 0:
            n2 = n[1]
            num2 = self.i[n2]
        elif n[0] == 1 and n[1] > 0:
            num1 = self.i[m]
            num2 = ''
        else:
            num2 = ''
        return num1 +' '+ num2

    def len3(self, inNumber):
        n = divmod(inNumber,100)
        num1 = self.i[n[0]*100]
        if n[1] > 0:
            num2 = self.len2(n[1])
        else:
            num2 = ''
        return num1 + ' ' + num2

    def len4(self, inNumber):
        n = divmod(inNumber,1000)
        if n[0] == 1:
            num1 = self.i[n[0]*1000]
        if n[0] > 1:
            num1 = self.i[n[0]] + t['t3a']
        num2 = self.len3(n[1])
        return num1 + ' ' + num2

    def len5(self, inNumber):
        n = divmod(inNumber,1000)
        if n[0] == 1:
            num1 = self.i[n[0]*1000]
        if n[0] > 1:
            num1 = self.len2(n[0]) + t['t3b']
        num2 = self.len3(n[1])
        return num1 + ' ' + num2

    def translate(self, inNumber):
        c = len(str(inNumber))
        if c == 1:
            num = self.len1(inNumber)
        if c == 2:
            num = self.len2(inNumber)
        if c == 3:
            num = self.len3(inNumber)
        if c == 4:
            num = self.len4(inNumber)
        if c == 5:
            num = self.len5(inNumber)
        return num
