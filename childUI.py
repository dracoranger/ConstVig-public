'''
TODO fill in docstring for module
'''

import utilities

def main(cmd):
    '''
    For now, this just asserts what child is being used and checks for the type
    '''
    print('UI')
    if utilities.check_input((str), cmd):
        return cmd
    return "error"
