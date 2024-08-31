# -*- coding: UTF-8 -*-

def printMsg(*args):
    msgCon=""
    if args:
        for msg in args:
            msgCon = msgCon + str(msg) + "\t"

        print("***********Test output:**********",msgCon)

def printInfo(msg):
    print("----->",msg)

def printWarning(msg):
    print("-***->",msg)

def printError(msg):
    print("*****->",msg)
