import sys
import os
from shutil import copyfile

def main():
    print('Welcome to text classifier main program!')
    print('developed by Lorenzo Adreani')

    print('args: ', str(sys.argv))
    needToBeSplitted = False
    datasetPath = ""

    for arg in sys.argv:
        if arg == '-s':
            needToBeSplitted = True
        if arg == '-d':
            datasetPath = sys.argv[sys.argv.index(arg) + 1]

    print('You selected the path', datasetPath)

def importData(datasetPath):
    os.mkdir("data")
    copyfile()



main()