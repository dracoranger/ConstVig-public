'''
TODO fill in docstring for module
'''

import utilities

def main():
    '''
    For now, this just asserts what child is being used and checks for the type
    '''

    print('UI')
    able = input()
    if utilities.check_input((str), able):
        print(able)

main()
