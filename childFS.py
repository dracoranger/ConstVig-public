'''
TODO make module docstring
'''

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
        print('FS')
        able = input('file name: ')
        rorw = input('Read (r) or write (w)? ')
        if utilities.check_input((str), able):
            print(able)
        fsys(able, rorw)

main()
