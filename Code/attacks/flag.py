import argparse
def main():
    parser = argparse.ArgumentParser(description='Tests -f')
    parser.add_argument('-f', action='append')

    args = parser.parse_args()
    print(args)
main()
