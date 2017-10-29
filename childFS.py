'''
TODO make module docstring
'''

import sys
import utilities

def fsys(filename, intent):
    '''
    TODO make function docstring
    intent is either read or write
    '''
    if intent == 'r':
        pass
    elif intent == 'w':
        pass
    else: return -1
    return -1

def main():
    '''
    For now, this function just checks the type and returns an error message
     in the event of a wrong type
    '''
    keep_going = True
    while keep_going:
        #commented out print() and changed input()
        #print('FS')
        print('file name: ')
        able = input()#sys.stdin.readline(5)
        print('Read (r) or write (w)? ')
        rorw = sys.stdin.readline()
        if utilities.check_input((str), able):
            print(able)
        fsys(able, rorw)

main()
