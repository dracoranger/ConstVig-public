import argparse
def main():
    parser = argparse.ArgumentParser(description='Tests both -ip and -p.')
    parser.add_argument('-ip', action='append')
    parser.add_argument('-p', action='append')

    args = parser.parse_args()
    print(args)
main()
