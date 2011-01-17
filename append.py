import sys

def append(file, arr):
    str = ' '.join(arr)
    with open(file, mode='a+') as theFile:
        theFile.write(str + '\n')

def main():
    append(sys.argv[1], sys.argv[2:])

if __name__ == '__main__':
    main()
