import cmd
import re
import io
import abc
import csv
import sys
import cmd



#The interfaces for Controller are to make it easier for me to follow the use cases and what they do

class FileReader(metaclass=abc.ABCMeta):
    def openFile(self):
        pass

class MyError(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return self.line

class DataChecker(metaclass=abc.ABCMeta):
    def makeCheckers(self):
        print("")
    def check(self):
        print("")

class Console(cmd.Cmd):
    def __init__(self):
        """

        :return: None
        """
        cmd.Cmd.__init__(self)
        self.prompt = "=>> "
        self.intro  = "Welcome to console!"  ## defaults to None
    def do_exit(self, line):
        """
        to Exit from the console
        :param line: a message
        :return: to Exit from console
        """
        return -1

    def do_q(self,line):
        """
        To exit from the console
        :param line: a message
        :return: to call Exit method
        """
        return self.do_exit(line)
    def do_help(self, args):
        """
        Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        :param args: a message
        :return: None
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

class Controller(FileReader, DataChecker):
# instancing the model and views in this way is a design decision, the views should be initialised when the program is started

    def __init__(self, myModel, myViews):
        self.Gender = {"0": "Male", "1": "Female"}
        self.BMI = {"0": "Normal", "1": "Overweight", "2": "Obesity", "3": "Underweight"}
        self.DataColumns = {"0": "ID","1": "Gender","2": "Age", "3": "Sales", "4" :"BMI","5" :"Income"}
        self.myModel = myModel
        self.myViews = myViews
        self.bmireader = ""
        self.csvfile = ""

    """
    def controllerLoop(self):


    """
    def openFile(self):
        #testcase, if data is loaded it will print the data in lines. Success
        filename = sys.argv[1]
        csvfile = open(filename, newline='')
        bmireader = csv.reader(self.csvfile, delimiter = ' ', quotechar= '|')
        for row in self.bmireader:
            print(', '.join(row))
        #testcase, see if multiple rows load. Success


    def makeCheckers(self):
        """
        I have to make a design decision whether the data belongs in controller or made solely in Model
        Is there a reason that controller would determine the checkers that are made
        i have 6 inputs i want to check.
         ID, RegExp
         Gender, Gender
         Age, RegExp
         Sales, RegExp
         BMI, BMI
         Income, RegExp

        """
        typeCheckerList = [[self.DataColumns['0'], "RegExp", "[A-Z][0-9]{3}"],
                           [self.DataColumns['1'], "Gender"],
                           [self.DataColumns['2'], "RegExp", "[0-9]{2}"],
                           [self.DataColumns['3'], "RegExp", "[0-9]{3}"],
                           [self.DataColumns['4'], "BMI"],
                           [self.DataColumns['5'], "RegExp", "[0-9]{2,3}"]]

        for i in range (0, 6):
            if (typeCheckerList[i][1] == "RegExp"):
                self.myModel.addRegExp(i, typeCheckerList[i][2], typeCheckerList[i][0])
            else:
                self.myModel.addEnum(i, typeCheckerList[i][1], typeCheckerList[i][0])

        """
        self.myModel.countIC()
        for item in range (0,6):
            print(self.myModel.findInputChecker(typeCheckerList[item][0]).__str__())
        """


    def check(self):
        """
        >>> print(self.myModel.findData('A001'))
        A001, Male, 36, 455, Normal, 889
        :param id:
        :return:
        """
        #needs bmireader data.
        #sets up a count of how many wrong lines there are
        #uses input checkers to determine the right data set
        #
        wrongLines = 0

        filename = sys.argv[1]
        csvfile = open(filename, newline='')
        bmireader = csv.reader(csvfile, delimiter = ' ', quotechar= '|')

        try:
            for row in bmireader:
                wrong = self.readLine(row)
                if(wrong==False):
                    self.myModel.addData(ID=row[0], Gender=row[1], Age=row[2], Sales=row[3], BMI=row[4], Income=row[5])

                elif (wrong==True):
                    wrongLines += 1
            #case of wronglines of code
            if (wrongLines > 0):
                print("We found " + str(wrongLines) + " row of wrong data")
            csvfile.close()
        except MyError:
            print("Incorrect Input Length")
            """
        for item in self.myModel.allMyData:
            print(item)
            """


    def readLine(self,line):
        if (line[5] == None):
            raise(MyError("here is my error"))
        headings = [self.DataColumns['0'],
                    self.DataColumns['1'],
                    self.DataColumns['2'],
                    self.DataColumns['3'],
                    self.DataColumns['4'],
                    self.DataColumns['5'],
                    ]
        for item in range(0,5):
            if self.myModel.findInputChecker(headings[item]):
                IC = self.myModel.findInputChecker(headings[item])
                if (IC.isValid(line[item])):
                    pass
                else:
                    return True
        return False









class IView(metaclass=abc.ABCMeta):

    def ReadLine(self, string):
        return string
    def display(self):
        return

class View():
    def display(self):
        return



class Model(object):

    def __init__(self):
        self.allMyData = []
        self.allMyInputCheckers = []

    def addRegExp(self, id, constraint, description):
        newIC = RegExp(id, constraint, description)
        self.allMyInputCheckers.append(newIC)

    def addEnum(self, id, constraint, description):
        newIC = Enum(id, constraint, description)
        self.allMyInputCheckers.append(newIC)

    def findInputChecker(self, desc):
        for i in self.allMyInputCheckers:
            if (i.description == desc):
                return i
        return None

    def findData(self, id):
        for i in self.allMyData:
            if (i.id == id):
                return i
        return None

    def countIC(self):
        print(len(self.allMyInputCheckers))

    def countData(self):
        print(len(self.allMyData))

    def getAllMyCheckers(self):
        return self.allMyInputCheckers

    def addData(self, ID, Gender, Age, Sales, BMI, Income):
        newData = Data(ID, Gender, Age, Sales, BMI, Income)
        self.allMyData.append(newData)

class Data(object):
    def __init__(self, ID, Gender, Age, Sales, BMI, Income):
        self.id = ID
        self.gender = Gender
        self.age = Age
        self.sales = Sales
        self.BMI = BMI
        self.income = Income

    def __str__(self):
        return self.id + ", " + self.gender + ", " +  self.age + ", " + self.sales + ", " + self.BMI + ", " + self.income

class InputChecker(object):

    def __init__(self, id, constraint, description):
        self.id = id
        self.constraint = constraint
        self.description = description

    def isValid(self, data):
        return True

    def __str__(self):
        return str(self.id) + " is a " + self.description + " with a " + self.constraint + " constraint"

class RegExp(InputChecker):

    def isValid(self, data):
        return re.match(self.constraint, data)

class Enum(InputChecker):
    __Gender = {"0": "Male", "1": "Female"}
    __BMI = {"0": "Normal", "1": "Overweight", "2": "Obesity", "3": "Underweight"}
    def isValid(self, data):
        if (self.constraint == "BMI"):
            for key in self._Enum__BMI:
                if (data==self._Enum__BMI[key]):
                    return True
            return False

        elif (self.constraint == "Gender"):
            for key in self._Enum__Gender:
                if (data==self._Enum__Gender[key]):
                    return True
            return False

if (__name__ == '__main__'):
    import doctest
    model = Model()
    views = View()
    controller = Controller(model, views)
    controller.openFile()
    controller.makeCheckers()
    controller.check()
    doctest.testmod()
    console = Console()
    console.cmdloop()
