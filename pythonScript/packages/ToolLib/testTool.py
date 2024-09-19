# -*- coding: UTF-8 -*-
import inspect

current_frame = inspect.currentframe()

def printMsg(*args):
    msgCon=""
    caller_frame = inspect.getframeinfo(current_frame.f_back)
    stack_lists = inspect.stack()
    if args:
        for msg in args:
            msgCon = msgCon + str(msg) + "\t"
        # print(f"***********Test output {current_frame.f_code.co_name}:**********",msgCon)
        print(f"***********MsgFunction functionName:{stack_lists[1].function}() lineNumber:{stack_lists[1].lineno}**********",msgCon)

def printInfo(*args):
    msgCon=""
    stack_lists = inspect.stack()
    if args:
        for msg in args:
            msgCon = msgCon + str(msg) + "\t"
        # print(f"***********Test output {current_frame.f_code.co_name}:**********",msgCon)
        print(f"----->functionName:{stack_lists[1].function}() lineNumber:{stack_lists[1].lineno}<-----",msgCon)

def printWarning(*args):
    msgCon=""
    stack_lists = inspect.stack()
    if args:
        for msg in args:
            msgCon = msgCon + str(msg) + "\t"
        # print(f"***********Test output {current_frame.f_code.co_name}:**********",msgCon)
        print(f"-***->functionName:{stack_lists[1].function}() lineNumber:{stack_lists[1].lineno}<-***-",msgCon)
def printError(*args):
    msgCon=""
    stack_lists = inspect.stack()
    if args:
        for msg in args:
            msgCon = msgCon + str(msg) + "\t"
        # print(f"***********Test output {current_frame.f_code.co_name}:**********",msgCon)
        print(f"*****->functionName:{stack_lists[1].function}() lineNumber:{stack_lists[1].lineno}<-*****",msgCon)
