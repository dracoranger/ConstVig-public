""" handles the user interface

Classes: None
Exceptions:
Functions:
main --
"""

import utilities
import sys

def main():
    """
    For now, this just asserts what child is being used and checks for the type
    """
    keep_going = True
    while keep_going:
        #commented out print() and changed input()
        #print('UI')
        able = sys.stdin.readline(5)
        if utilities.check_input((str), able):
            print(able)

main()
