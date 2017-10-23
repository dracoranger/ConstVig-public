'''
TODO make module docstring
'''

import utilities

def fsys(typ, file):
    '''
    TODO make function docstring
    '''
    return -1
def main(cmd):
    '''
    For now, this function just checks the type and returns an error message
     in the event of a wrong type
    '''
    print('FS')
    if utilities.check_input((str), cmd):
        return cmd
    return "error"
