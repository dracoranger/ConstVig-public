import urllib.request

def main():
    page = urllib.request.urlopen('http://kbroman.org/simple_site/')
    print(len(page.read()))


main()
