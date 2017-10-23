import utilities

def main(cmd):
    print('UI')
    if utilities.check_input((str), cmd):
        return cmd
    else:
        return "error"
