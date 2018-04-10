import argparse
def main():
    parser = argparse.ArgumentParser(description='Tests -p.')
    parser.add_argument('-p', action='append')

    args = parser.parse_args()
    print(args)
main()
