import sys
from png_interface import png_maker

def main():
    printTitle()
    inputLoop()

def inputLoop():
    input_var = input("")
    parseInput(input_var)

def parseInput(input_var):
    if input_var   == "ls":
        lsOptions()
        inputLoop()
    elif input_var == "1":
        startOperations(1)
    elif input_var == "2":
        startOperations(2)
    elif input_var == "3":
        startOperations(3)
    elif input_var == "exit":
        sys.exit()
    else:
        print("Sorry, that is not a valid option. Enter \'ls\' for a list of options")
        inputLoop()

def startOperations(options):
    png_setup = png_maker(options)
    if png_setup.validFile==True or png_setup.validPath==True:
        if options == 3:
            png_setup.multipng()
        else:
            png_setup.createpng(False)
        print("File Created. Back to Main Menu")
    else:
        print("Select your option again, or press 'ls' for other options")
    inputLoop()

def lsOptions():
    print("""\n*********************************************************
* To add dots to an input png image, type \t\'1\'\t*
* To make a dotted png image, type \t\t\'2\'\t*
* To make a varied dotted palette, type \t\'3\'\t*
* To exit Dot maker, type \t\t\t\'exit\'\t*
*********************************************************\n""")

def printTitle():
    print("""\n*********************************************************
*\t\t Welcome to Dot Maker\t\t\t*
*\t\t\t\t\t\t\t*
*\t\tMade by Kevin Mendoza\t\t\t*
*********************************************************
*\t type \'ls\' for a list of commands\t\t*
*********************************************************\n""")

main()
