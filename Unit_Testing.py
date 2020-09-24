import unittest
from unittest.mock import patch
import time
import config

from Functions import *

config.unitTesting = True


from Evaluation import *


class mainTests(unittest.TestCase):

    mainSimpleInputs = ['Westpac Bank', 'corporate', 'Nic', 'natural person', '1',
                      '1', 'ANZ', 'corporate', '1', '1', 'BobBankingCo', 'partnership', '0', '1', 'Commonwealth Bank',
                      'corporate', '1', '0',
                      '1', '1', '500', '27', '0', '11/10/2019', '0', '12/10/2019', '1', '12/02/2019', '1', '0', '1',
                      '1', '1', '1', '1', '1', '1', '0'
                     ]
    @patch('builtins.input', side_effect=mainSimpleInputs)
    def testMainSimple(self, mock_input):
        print("\n\n========\nTest 1\n========")
        testNo = 1
        results = main()
        Contraventions = results[0]
        Uncertainties = results[1]
        time.sleep(1) #Don't interrupt determination
        self.assertEqual(len(Uncertainties), 0)
        Results.Uncertainties = []



    mainLicenseUnknown = ['Westpac Bank', 'corporate', 'Nic', 'natural person', None,
                        '1', 'ANZ', 'corporate', '1', '1', 'BobBankingCo', 'partnership', '0', '1', 'Commonwealth Bank',
                        'corporate', '1', '0',
                        '1', '1', '500', '27', '0', '11/10/2019', '0', '12/10/2019', '1', '12/02/2019', '1', '0', '1',
                        '1', '1', '1', '1', '1', '1', '0'
                        ]
    @patch('builtins.input', side_effect=mainLicenseUnknown)
    def testMainLicenseUnknown(self, mock_input):
        print("\n\n========\nTest 2\n========")
        testNo = 2
        results = main()
        Contraventions = results[0]
        Uncertainties = results[1]
        time.sleep(1) #Don't interrupt determination
        self.assertEqual(len(Contraventions), 0)
        self.assertEqual(Uncertainties, ["\t\t\t --Whether Westpac Bank held a license."])
        Results.Uncertainties = []


    mainNoContract = ['Westpac Bank', 'corporate', 'Nic', 'natural person', '1',
                         '0', '0', '0', '0'
                         ]
    @patch('builtins.input', side_effect=mainNoContract)
    def testNoContract(self, mock_input):
        print("\n\n========\nTest 3\n========")
        testNo = 3
        results = main()
        Contraventions = results[0]
        Uncertainties = results[1]
        time.sleep(1)  # Don't interrupt determination
        print(Uncertainties)

        self.assertEqual(len(Contraventions), 0)
        self.assertEqual(len(Uncertainties), 0)
        Results.Uncertainties = []



    mainTrusteesNumberUnknown_CreditGuideProvidedUnknown = ['Westpac Bank', 'Trust', "Unknown", 'Nic', 'natural person', '1',
                        '0', '0', '1', '1', '6000', '232', '1', '1', '1',
                        '12/12/2019', 'Unknown', '20/12/2019', '1', '20/12/2018', '1', '1', '1',
                        '1', '1', '1', '1', '1'
                        ]
    @patch('builtins.input', side_effect=mainTrusteesNumberUnknown_CreditGuideProvidedUnknown)
    def testTrusteesNumberUnknown_CreditGuideProvidedUnknown(self, mock_input):
        print("\n\n========\nTest 4\n========")
        testNo = 4
        results = main()
        Contraventions = results[0]
        Uncertainties = results[1]
        time.sleep(1) #Don't interrupt determination
        #self.assertEqual(len(Contraventions), 0)
        #self.assertEqual(Uncertainties, ["\t\t\t --Whether Westpac Bank held a license."])
        Results.Uncertainties = []


