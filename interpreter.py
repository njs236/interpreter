import cmd
import re
import io
import abc
import csv


#The interfaces for Controller are to make it easier for me to follow the use cases and what they do

class FileReader(metaclass=abc.ABCMeta):
    def openFile(self):
        print("")

class DataChecker(metaclass=abc.ABCMeta):
    def makeCheckers(self):
        print("")
    def check(self):
        print("")

class TestFramework(metaclass=abc.ABCMeta):
    def findInputChecker(self, desc):
        print("")



class Controller(FileReader, DataChecker):
# instancing the model and views in this way is a design decision, the views should be initialised when the program is started

    def __init__(self, myModel, myViews):
        self.Gender = {"0": "Male", "1": "Female"}
        self.BMI = {"0": "Normal", "1": "Overweight", "2": "Obesity", "3": "Underweight"}
        self.DataColumns = {"0": "ID","1": "Gender","2": "Age", "3": "Sales", "4" :"BMI","5" :"Income"}
        self.myModel = myModel
        self.myViews = myViews

    """
    def controllerLoop(self):


    """
    def openFile(self):
        #testcase, if data is loaded it will print the data in lines. Success
        csvfile = open('data.csv', newline='')
        self.bmireader = csv.reader(csvfile, delimiter = ' ', quotechar= '|')
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

        self.myModel.countIC()
        for item in range (0,6):
            print(self.myModel.findInputChecker(typeCheckerList[item][0]).__str__())



    def check(self):
        #needs bmireader data.
        #sets up a count of how many wrong lines there are
        #uses input checkers to determine the right data set
        #
        wrongLines = 0

        for row in self.bmireader:
            for k,v in self.DataColumns:
                #check for input checker based on description
                if (self.myModel.findInputChecker(v) != None):
                    IC = self.myModel.findInputChecker(v)
                    if (IC.isValid(row[k])):
                        pass
                    else:
                        wrongLines += 1
                        break
        #case of wronglines of code
        if (wrongLines > 0):
            print("We found" + wrongLines + " of wrong data")











class IView(metaclass=abc.ABCMeta):

    def ReadLine(self, string):
        return string
    def display(self):
        return

class View():
    def display(self):
        return


class Model(TestFramework):

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

    def countIC(self):
        print(len(self.allMyInputCheckers))

    def getAllMyCheckers(self):
        return self.allMyInputCheckers






    def addData(self, ID, Gender, Age, Sales, BMI, Income):
        newData = Data(ID, Gender, Age, Sales, BMI, Income)
        self.AllMyData += newData

class Data(object):
    def __init__(self, ID, Gender, Age, Sales, BMI, Income):
        self.id = ID
        self.gender = Gender
        self.age = Age
        self.sales = Sales
        self.BMI = BMI
        self.income = Income

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
        return

class Enum(InputChecker):
    Gender = {"0": "Male", "1": "Female"}
    BMI = {"0": "Normal", "1": "Overweight", "2": "Obesity", "3": "Underweight"}
    def isValid(self, data):
        return

if (__name__ == '__main__'):
    model = Model()
    views = View()
    controller = Controller(model, views)
    controller.openFile()
    controller.makeCheckers()