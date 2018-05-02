import argparse
def main():
    parser = argparse.ArgumentParser(description='Tests -ip.')
    parser.add_argument('-ip', action='append')

    args = parser.parse_args()
    print(args)
main()
