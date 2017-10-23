import utilities

def main(cmd):
    if utilities.check_input((str), cmd):
        return cmd
    else:
        return "error"
