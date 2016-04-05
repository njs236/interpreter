import unittest
from interpreter import *

class MainTest(unittest.TestCase):
    def setUp(self):
        model = Model()
        views = [ConsoleView("Console"), PieView("Pie"), ChartView("Chart")]
        self.myController = Controller(model, views)
        self.myController.makeCheckers()

    def tearDown(self):
        pass

    """

    FUNCTIONAL TESTING


    """

    def test01(self):
        # There should be 6 checkers
        actual = self.myController.myModel.countIC()
        expected = 6

        # the assert
        self.assertEqual(actual, expected, "There are 6 Input Checkers")
        pass

    def test02(self):
        # Check to find an input checker and its constraint
        firstchecker = self.myController.myModel.findInputChecker('ID')
        expectedconstraint = "[A-Z][0-9]{3}"

        # assert
        self.assertTrue(firstchecker.getConstraint() == expectedconstraint,
                        "The id checker should have constraint [A-Z][0-9]{3}")
    """
    def test03(self):
        # check filename Input and console input
        filename = 'E:\PycharmProjects\interpreter\data.csv'
        actual = self.myController.check(filename)
        expected = self.myController.getModel().findData('A001')

        # assert

        self.assertIsNotNone(expected, "handles filename input")

    def test04(self):
        # give some invalid input expected a message
        filename = "E:\PycharmProjects\interpreter\data2.csv"
        actual = self.myController.check(filename)
        pass
    """
    def testAgeFunction(self):
        """
        expects to return a set of data for viewing in plotly
        :return:
        """
        age = self.myController.getModel().getAgeData()
        actual = self.myController.displayAgeGraph()
        expected = {'x': ['0-10', '11-20', '21-30', '31-40', '41-50', '50+'],
                'y': age,
                'title': 'BMI Age by bracket'}
        #assert
        self.assertEqual(actual, expected, "Functional Testing: Testing Age Function")


    def testFindViewByIdFunction(self):
        """

        Expects to return a view

        :return:
        """
        actual = self.myController.findViewById("Chart")
        expected = type(actual) is ChartView

        #assert
        self.assertTrue(expected, "Functional Testing: returns a proper type of View")

    def testmakeCheckersFunction(self):

        """
        Expects to return a checker after the make Checkers is run.

        i come up with a valid exception to the main flow, which is that make checkers would add a set of new checkers if ran twice,
        this would make it have 12 checkers and each have 2 duplicate names. To change this, you could set up a check based on the ID of a
        checker. As it is, this would make the whole thing fail
        :return:
        """
        pass

    def testshelveObjectsFunction(self):
        """

        Expects to return a Data object
        :return:
        """

        self.myController.check('H:\PycharmProjects\interpreter\data.csv')
        actual = self.myController.shelveObjects()
        expected = type(actual) is Data

        #assert

        self.assertTrue(expected, "Functional Testing: returns a Data object")

    def testLineCheckFunction(self):
        """


        Expects to pass test
        :return:
        """

        actual = self.myController.readLine(['A001','Male','36','455','Normal','889'])

        #assert

        self.assertFalse(actual, "Functional Testing: Line Check")

    def testPieViewDisplayFunction(self):
        """


        Expects to return success of drawing Pie with Plotly

        :return:
        """

        args = {'labels': ['Male', 'Female'],
                         'values': [33, 45],
                         'pie': 'pie',
               'title': 'Gender Pie Graph'}

        view = self.myController.findViewById('Pie')
        actual = view.display(args)

        #assert

        self.assertEqual(actual, args, "Functional Testing: Pie Display Function")

    def testChartViewDisplayFunction(self):
        """


        Expects to return success of drawing Chart with plotly
        :return:
        """

        args = {'x': ['0-10', '11-20', '21-30', '31-40', '41-50', '51+'],
                         'y': [0, 0, 2, 2, 0, 0],
               'title': 'Age Chart Graph'}

        view = self.myController.findViewById('Chart')
        actual = view.display(args)

        #assert

        self.assertEqual(actual, args, "Functional Testing: Chart Display Function")

    def testGetAgeDataFunction(self):
        """


        Expects to get a list of Age data.
        :return:
        """
        list = [0,0,0,0,0,0]
        actual =  self.myController.getModel().getAgeData()

        #assert

        self.assertEqual(list, actual, "Functional Testing: getAgeData")

    def testAddRegExpFunction(self):
        """


        Expects to add a RegExp function to Model
        :return:
        """
        myModel = self.myController.getModel()


        actual = myModel.addRegExp(0, '[0-9]{3}', "TaxCode")
        allIC = myModel.getAllMyCheckers()
        expected = allIC[6]

        #assert

        self.assertEqual(actual, expected, "Functional Testing: Add RegExp")


    def testAddEnumFunction(self):
        """


        Expects to add a Enum function to Model
        :return:
        """
        myModel = self.myController.getModel()


        actual = myModel.addEnum(0, {'0': 'IT', '1': 'Economics', '2': 'Accounting','3': 'Teaching','4': 'Cleaning'}, "JobDescription")
        allIC = myModel.getAllMyCheckers()
        expected = allIC[6]

        #assert

        self.assertEqual(actual, expected, "Functional Testing: Add Enum")

    def testAddDataFunction(self):
        """


        Expects to add Data function to Model
        :return:
        """
        myModel = self.myController.getModel()

        actual = myModel.addData('A001', 'Male', 355, 455, 'Normal', 677)
        allData = myModel.getAllMyData()
        expected = allData[0]

        #assert

        self.assertEqual(actual, expected, "Functional Testing: Add Data")

    def testFindICFunction(self):
        """


        Expects to add a Enum function to Model
        :return:
        """
        myModel = self.myController.getModel()


        myModel.addEnum(0, {'0': 'IT', '1': 'Economics', '2': 'Accountant','3': 'Teacher','4': 'Cleaner'}, "JobDescription")
        actual = myModel.findInputChecker('JobDescription')
        allIC = myModel.getAllMyCheckers()
        expected = allIC[6]

        #assert

        self.assertEqual(actual, expected, "Functional Testing: Find Input Checker")

    def testFindDataFunction(self):
        """


        Expects to find a created set of Data
        :return:
        """
        myModel = self.myController.getModel()
        allData = myModel.getAllMyData()

        myModel.addData('A001', 'Male', 355, 455, 'Normal', 677)
        actual = myModel.findData('A001')
        expected = allData[0]

        #assert

        self.assertEqual(actual, expected, "Functional Testing: Find Data")



