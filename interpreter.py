import cmd
import re
import io
import abc
import csv
import sys
import unittest
import tkinter

"""
The interfaces for Controller are to make it easier for me to follow the
use cases and what they do
"""



class FileReader(metaclass=abc.ABCMeta):
    def openFile(self, filename):
        pass


class MyError(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return self.line


class DataChecker(metaclass=abc.ABCMeta):
    def makeCheckers(self):
        pass

    def check(self, filename):
        pass


class Console(cmd.Cmd):
    def __init__(self, view):
        """

        :return: None
        """
        cmd.Cmd.__init__(self)
        self.myView = view
        self.prompt = "=>> "
        self.intro = "Welcome to console!"  # defaults to None

    def do_exit(self, line):
        """
        to Exit from the console
        :param line: a message
        :return: to Exit from console
        """
        return -1

    def do_q(self, line):
        """
        To exit from the console
        :param line: a message
        :return: to call Exit method
        """
        return self.do_exit(line)

    def do_help(self, args):
        """
        Get help on commands
           'help' or '?' with no arguments prints a list of
           commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        :param args: a message
        :return: None
        """
        # The only reason to define this method is for the help
        # text in the doc string
        cmd.Cmd.do_help(self, args)

    def do_age(self, args):
        """
        Present Age Data as bar chart
        :param args: message
        :return: None
        """
        self.myView.getController().displayAgeGraph()

    def do_bmi(self, args):
        """
        Present BMI information as pie chart
        :param args: message
        :return: None
        """
        self.myView.getController().displayBMIGraph()

    def do_gender(self, args):
        """
        Present Gender information as pie chart
        :param args: message
        :return: None
        """
        self.myView.getController().displayGenderGraph()

    def do_sales(self, args):
        """
        Present Sales information as bar chart
        :param args: message
        :return: None
        """
        self.myView.getController().displaySalesGraph()

    def do_income(self, args):
        """
        Present Income information as bar chart
        :param args: message
        :return: None
        """
        self.myView.getController().displayIncomeGraph()

    def do_bmisales(self, args):
        """
        Present a scatter graph of BMI and Sales data
        :param args: message
        :return: None
        """
        self.myView.getController().displayBMISalesGraph()

    def do_loadfile(self, args):
        """
        Load File and check contents
        :param args:
        :return:
        """
        try:
            self.myView.getController().check(args[0])
        except IndexError:
            self.myView.getController().check()


class Controller(FileReader, DataChecker):
    """
    instancing the model and views in this way is a design decision, the views
    should be initialised when the program is started.


    """

    def __init__(self, myModel, myViews):
        self.myModel = myModel
        self.myViews = myViews
        self.bmireader = ""
        self.csvfile = ""
        self.linkViewsToController()

    """
    def controllerLoop(self):


    """

    def getModel(self):
        return self.myModel

    def displayAgeGraph(self):
        data = self.myModel.getAgeData()
        plotly = self.findViewById('Chart')
        plotly.printLine("age")
        plotly.display(data)
        return data

    def displayBMIGraph(self):
        plotly = self.findViewById('Plotly')
        plotly.printLine("stub")

    def displayGenderGraph(self):
        plotly = self.findViewById('Plotly')
        plotly.printLine("stub")

    def displaySalesGraph(self):
        plotly = self.findViewById('Plotly')
        plotly.printLine("stub")

    def displayIncomeGraph(self):
        plotly = self.findViewById('Plotly')
        plotly.printLine("stub")

    def displayBMISalesGraph(self):
        plotly = self.findViewById('Plotly')
        plotly.printLine("stub")

    def linkViewsToController(self):
        for item in self.myViews:
            item.setController(self)

    def findViewById(self, id):
        for item in self.myViews:
            if item.getID() == id:
                return item
        return None

    def makeCheckers(self):
        return self.myModel.makeCheckers()

    def shelveObjects(self):
        return self.myModel.shelveObjects()

    def openFile(self, filename=None):
        if filename is None:
            filename = self.myViews[0].readLine("Enter a valid filename:")
        #clause for invalid filename in input
        bmireader = self.myModel.openFile(filename)
        if bmireader is None :
            self.myViews[0].printLine("Invalid Filename")
            self.openFile()
        return bmireader

    def check(self, filename=None):
        # needs bmireader data.
        # sets up a count of how many wrong lines there are
        # uses input checkers to determine the right data set
        #
        wrongLines = self.myModel.check(self.openFile(filename))
        # case of wronglines of code
        if (wrongLines > 0):
            print("We found " + str(wrongLines) + " row of wrong data")


class IView(metaclass=abc.ABCMeta):
    def getID(self):
        pass

    def readLine(self, string):
        pass

    def setController(self, controller):
        pass

    def getController(self):
        pass

    def printLine(self):
        pass


class PieView(IView):
    def __init__(self, id):
        self.id = id

    def getID(self):
        return self.id

    def readLine(self, string):
        return input(string)

    def setController(self, controller):
        self.myController = controller

    def getController(self):
        return self.myController

    def printLine(self, line):
        print(line)

    def display(self, args):
        import plotly

        fig = {'data': [{'labels': args['labels'],
                         'values': args['values'],
                         'type': args['pie']}],
               'layout': {'title': args['title']}
               }

        plotly.offline.plot(fig)

        return args


class ChartView(IView):
    def __init__(self, id):
        self.id = id

    def getID(self):
        return self.id

    def readLine(self, string):
        return input(string)

    def setController(self, controller):
        self.myController = controller

    def getController(self):
        return self.myController

    def printLine(self, line):
        print(line)

    def display(self, args):
        import plotly as py
        import plotly.graph_objs as go

        data = [go.Bar(y=args['y'],
                       x=args['x'])]
        layout = go.Layout(title=args['title'])
        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig)
        return args


class ConsoleView(IView):
    def __init__(self, id):
        self.id = id

    def getID(self):
        return self.id

    def readLine(self, string):
        return input(string)

    def printLine(self, line):
        print(line)

    def setController(self, controller):
        self.myController = controller

    def getController(self):
        return self.myController


class Model(object):
    def __init__(self):
        self.Gender = {"0": "Male", "1": "Female"}
        self.BMI = {"0": "Normal", "1": "Overweight",
                    "2": "Obesity", "3": "Underweight"}
        self.DataColumns = {"0": "ID", "1": "Gender", "2": "Age",
                            "3": "Sales", "4": "BMI", "5": "Income"}
        self.allMyData = []
        self.allMyInputCheckers = []

    def check(self, reader):
        wrongLines = 0
        try:
            for row in reader:
                wrong = self.readLine(row)
                if (not wrong):
                    self.addData(ID=row[0], Gender=row[1],
                            Age=row[2], Sales=row[3],
                            BMI=row[4], Income=row[5])

                elif (wrong):
                    wrongLines += 1
        except IndexError:
            print("Incorrect Input Length")
        return wrongLines

    def emptyData(self):
        self.allMyData = []

    def openFile(self, filename):
        self.emptyData()
        try:
            """
            testcase, if data is loaded it will print the
            data in lines. Success
            """
            csvfile = open(filename, newline='')
            return csv.reader(csvfile, delimiter=' ', quotechar='|')
        except OSError:
            return None
            # testcase, see if multiple rows load. Success

    def readLine(self, line):
        headings = [self.DataColumns['0'],
                    self.DataColumns['1'],
                    self.DataColumns['2'],
                    self.DataColumns['3'],
                    self.DataColumns['4'],
                    self.DataColumns['5'],
                    ]
        for item in range(0, 5):
            if self.findInputChecker(headings[item]):
                IC = self.findInputChecker(headings[item])
                if (IC.isValid(line[item])):
                    pass
                else:
                    return True
        return False

    def shelveObjects(self):
        """
        shelving Objects has a nice pattern to it as from
        doing previous ones, identification
        of objects by their ID
        """
        import shelve
        db = shelve.open('db.shelf')
        for item in self.allMyData:
            db[(item.getID())] = item
        db.close()
        return self.allMyData[0]

    def makeCheckers(self):
        """
        I have to make a design decision whether the data belongs
        in controller or made solely in Model
        Is there a reason that controller would determine the
        checkers that are made
        i have 6 inputs i want to check.
         ID, RegExp
         Gender, Gender
         Age, RegExp
         Sales, RegExp
         BMI, BMI
         Income, RegExp

        """
        typeCheckerList = [[self.DataColumns['0'], "RegExp", "[A-Z][0-9]{3}"],
                           [self.DataColumns['1'], self.Gender],
                           [self.DataColumns['2'], "RegExp", "[0-9]{2}"],
                           [self.DataColumns['3'], "RegExp", "[0-9]{3}"],
                           [self.DataColumns['4'], self.BMI],
                           [self.DataColumns['5'], "RegExp", "[0-9]{2,3}"]]

        for i in range(0, 6):
            #condition: checker already exists
            if self.findInputChecker(typeCheckerList[i][0]):
                pass

            if (typeCheckerList[i][1] == "RegExp"):
                self.addRegExp(i, typeCheckerList[i][2],
                                       typeCheckerList[i][0])
            else:
                self.addEnum(i, typeCheckerList[i][1],
                                     typeCheckerList[i][0])

        return self.findInputChecker("ID").__str__()


    def getAgeData(self):
        """

         Age Graph is a bar chart that displays age by range
         0-10,
         11-20,
         21-30,
         31-40,
         41-50,
         50+

        :return:
        """
        list = [0, 0, 0, 0, 0, 0]
        for item in self.allMyData:
            if item.getAge() <= 10:
                list[0] += 1
            elif item.getAge() <= 20:
                list[1] += 1
            elif item.getAge() <= 30:
                list[2] += 1
            elif item.getAge() <= 40:
                list[3] += 1
            elif item.getAge() <= 50:
                list[4] += 1
            else:
                list[5] += 1
        data = {'x': ['0-10', '11-20', '21-30', '31-40', '41-50', '50+'],
                'y': list,
                'title': 'BMI Age by bracket'}

        return data


    def addRegExp(self, id, constraint, description):
        newIC = RegExp(id, constraint, description)
        self.allMyInputCheckers.append(newIC)
        return newIC

    def addEnum(self, id, constraint, description):
        newIC = Enum(id, constraint, description)
        self.allMyInputCheckers.append(newIC)
        return newIC

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
        return len(self.allMyInputCheckers)

    def countData(self):
        return len(self.allMyData)

    def getAllMyCheckers(self):
        return self.allMyInputCheckers

    def getAllMyData(self):
        return self.allMyData

    def addData(self, ID, Gender, Age, Sales, BMI, Income):
        newData = Data(ID, Gender, Age, Sales, BMI, Income)
        self.allMyData.append(newData)
        return newData


class Data(object):
    def __init__(self, ID, Gender, Age, Sales, BMI, Income):
        self.id = ID
        self.gender = Gender
        self.age = Age
        self.sales = Sales
        self.BMI = BMI
        self.income = Income
        self.__pickleObject()

    def __pickleObject(self):
        import pickle
        with open('data2', 'ab') as f:
            pickle.dump(self, f)

    def getID(self):
        return self.id

    def getAge(self):
        return int(self.age)

    def getSales(self):
        return self.sales

    def getBMI(self):
        return self.BMI

    def getGender(self):
        return self.gender

    def getIncome(self):
        return self.income

    def getKey(self):
        return "'" + self.id + "'"


    def __str__(self):
        return self.id + ", " + self.gender + ", " \
               + self.age + ", " + self.sales \
               + ", " + self.BMI + ", " + self.income


class InputChecker(object):
    def __init__(self, id, constraint, description):
        self.id = id
        self.constraint = constraint
        self.description = description

    def isValid(self, data):
        return True

    def getConstraint(self):
        return self.constraint

    def __str__(self):
        return str(self.id) + " is a " + self.description \
               + " with a " + self.constraint + " constraint"


class RegExp(InputChecker):
    def isValid(self, data):
        return re.match(self.constraint, data)


class Enum(InputChecker):
    def isValid(self, data):
            for key in self.constraint:
                if (data == self.constraint[key]):
                    return True
            return False

if (__name__ == '__main__'):
    model = Model()
    views = [ConsoleView("Console"), PieView("Pie"),
             ChartView("Chart")]
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = None
    controller = Controller(model, views)
    controller.makeCheckers()
    controller.check(filename)
    # unittest.main(verbosity=2)
    controller.shelveObjects()
    console = Console(views[0])
    console.cmdloop()
