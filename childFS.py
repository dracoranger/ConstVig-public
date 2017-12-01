""" Controlls access to the file system

Classes: None
Exceptions:
Functions:
fsys --
main --
"""

import sys
import utilities

def fsys(filename, intent):
    """ TODO -- make one line Summary

    Summary of behavior:
    Arguments: name of file to be accessed, 'r' or 'w' for read & write respectively
    Return values:
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called:
    """
    if intent == 'r':
        pass
    elif intent == 'w':
        pass
    else: return -1
    return -1

def main():
    """ TODO -- fill out one-line summary

    Summary of behavior: For now, this function just checks the type and
     returns an error message in the event of a wrong type
    Arguments: None
    Return values:
    Side effects:
    Exceptions raised:
    Restrictions on when it can be called:
    """
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
