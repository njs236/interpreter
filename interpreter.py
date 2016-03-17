import cmd
import re
import io
import abc
import csv
import sys
import cmd
import unittest


#The interfaces for Controller are to make it easier for me to follow the use cases and what they do

class MainTest(unittest.TestCase):

    def setUp(self):
        model = Model()
        views = [ConsoleView("Console"), PieView("Pie"), ChartView("Chart")]
        self.myController = Controller(model, views)
        self.myController.makeCheckers()

    def tearDown(self):
        pass

    def test01(self):
        #There should be 6 checkers
        actual = self.myController.myModel.countIC()
        expected = 6

        #the assert
        self.assertEqual(actual,expected, "There are 6 Input Checkers")
        pass

    def test02(self):
        #Check to find an input checker and its constraint
        firstchecker = self.myController.myModel.findInputChecker('ID')
        expectedconstraint ="[A-Z][0-9]{3}"

        #assert
        self.assertTrue(firstchecker.getConstraint() == expectedconstraint, "The id checker should have constraint [A-Z][0-9]{3}")


    def test03(self):
        #check filename Input and console input
        filename = 'E:\PycharmProjects\interpreter\data.csv'
        actual = self.myController.check(filename)
        expected = self.myController.myModel.findData('A001')

        #assert

        self.assertIsNotNone(expected, "handles filename input")

    def test04(self):
        #give some invalid input expected a message
        filename = "E:\PycharmProjects\interpreter\data2.csv"
        actual = self.myController.check(filename)


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
        print("")
    def check(self):
        print("")

class Console(cmd.Cmd):
    def __init__(self, view):
        """

        :return: None
        """
        cmd.Cmd.__init__(self)
        self.myView = view
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
    def do_age(self, args):
        self.myView.getController().displayAgeGraph()

    def do_bmi(self, args):
        self.myView.getController().displayBMIGraph()

    def do_gender(self, args):
        self.myView.getController().displayGenderGraph()

    def do_sales(self, args):
        self.myView.getController().displaySalesGraph()

    def do_income(self, args):
        self.myView.getController().displayIncomeGraph()

    def do_bmisales(self, args):
        self.myView.getController().displayBMISalesGraph()

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
        self.linkViewsToController()

    """
    def controllerLoop(self):


    """
    def displayAgeGraph(self):
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
        age = self.myModel.getAgeData()
        data = {'x': ['0-10', '11-20', '21-30', '31-40', '41-50', '50+'],
                'y': age,
                'title': 'BMI Age by bracket'}

        plotly = self.findViewById('Chart');
        plotly.printLine("age")
        plotly.display(data)
    def displayBMIGraph(self):
        plotly = self.findViewById('Plotly');
        plotly.printLine("stub")
    def displayGenderGraph(self):
        plotly = self.findViewById('Plotly');
        plotly.printLine("stub")
    def displaySalesGraph(self):
        plotly = self.findViewById('Plotly');
        plotly.printLine("stub")
    def displayIncomeGraph(self):
        plotly = self.findViewById('Plotly');
        plotly.printLine("stub")
    def displayBMISalesGraph(self):
        plotly = self.findViewById('Plotly');
        plotly.printLine("stub")

    def linkViewsToController(self):
        for item in self.myViews:
            item.setController(self)

    def findViewById(self, id):
        for item in self.myViews:
            if item.getID() == id:
                return item
        return None

    def openFile(self, filename):
        try:

        #testcase, if data is loaded it will print the data in lines. Success
            csvfile = open(filename, newline='')
            return csv.reader(csvfile, delimiter = ' ', quotechar= '|')
        except OSError:
            print("Invalid Filename")
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
    def shelveObjects(self):
        self.myModel.shelveObjects()


    def check(self, filename):
        #needs bmireader data.
        #sets up a count of how many wrong lines there are
        #uses input checkers to determine the right data set
        #
        wrongLines = 0
        if filename == None:
            filename = self.myViews[0].readLine("Enter a valid filename:")

        bmireader = self.openFile(filename)

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
        except IndexError:
            print("Incorrect Input Length")



    def readLine(self,line):
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
    def getID(self):
        pass
    def readLine(self, string):
        pass
    def setController(self, controller):
        pass
    def getController(self):
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

        data = [go.Bar(y= args['y'],
                         x= args['x'])]
        layout = go.Layout(title= args['title'])
        fig = go.Figure(data = data, layout=layout)
        py.offline.plot(fig)


class ConsoleView(IView):
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


class Model(object):

    def __init__(self):
        self.allMyData = []
        self.allMyInputCheckers = []

    def shelveObjects(self):
        # shelving Objects has a nice pattern to it as from doing previous ones, identification
        # of objects by their ID
        import shelve
        db = shelve.open('db.shelf', 'c')
        for item in self.allMyData:
            db[item.getID()] = item
        db.close()

    def getAgeData(self):
        """
        I need all data on age
        :return: age in brackets
        """
        list= [0, 0, 0,  0, 0,  0]
        for item in self.allMyData:
            if item.getAge() <= 10:
                list[0] += 1
            elif item.getAge() <=20:
                list[1] += 1
            elif item.getAge() <= 30:
                list[2] += 1
            elif item.getAge() <=40:
                list[3] += 1
            elif item.getAge() <=50:
                list[4] += 1
            else:
                list[5] += 1

        return list



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
        return len(self.allMyInputCheckers)

    def countData(self):
        return len(self.allMyData)

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

    def __str__(self):
        return self.id + ", " + self.gender + ", " +  self.age + ", " + self.sales + ", " + self.BMI + ", " + self.income

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
    model = Model()
    views = [ConsoleView("Console"), PieView("Pie"), ChartView("Chart")]
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = None
    controller = Controller(model, views)
    controller.makeCheckers()
    controller.check(filename)
    #unittest.main(verbosity=2)
    controller.shelveObjects()
    console = Console(views[0])
    console.cmdloop()
