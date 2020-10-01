import unittest
from unittest.mock import patch
import time
import config

from Functions import *

config.unitTesting = True


from Evaluation import *


class mainTests(unittest.TestCase):

    Uncertainties = Results.Uncertainties

    mainSimpleInputs = ['1',
        #Init
        'Westpac Bank', 'corporate', 'Nic1', 'natural person', '1',
        # Other Providers
                      '1', 'ANZ', 'corporate', '1', '1', 'BobBankingCo', 'partnership', '0', '1', 'Commonwealth Bank',
                      'corporate', '1', '0',
        # Define Contract
                      '1', '1', '500', '27', '0', '0', '1', '1', '1',
        # s126
                        '11/10/2019', '0',
        #s128
        '12/10/2019', '1', '12/02/2019', '1', '0', '1',
                      '1', '1', '1', '0', '1', '1', '1', '0',
                        '1', '1', '0', '0', '1', '0', '0', '0', '0', '0',
                        '1', '1', '1', '1', '1', '0', '1', '1', '0'
                     ]
    @patch('builtins.input', side_effect=mainSimpleInputs)
    def testMainSimple(self, mock_input):
        print("\n\n========\nTest 1\n========")
        testNo = 1
        Results.Uncertainties = []
        results = main()
        Contraventions = results[0]
        Uncertainties = results[1]
        time.sleep(1) #Don't interrupt determination
        self.assertEqual(len(Uncertainties), 0)



    mainLicenseUnknown = ['1',
        'Westpac Bank', None, 'Nic2', 'natural person', None,
                        '1', 'ANZ', 'corporate', '1', '1', 'BobBankingCo', None, '0', '1', 'Commonwealth Bank',
                        'corporate', '1', '0',
                        '1', '1', '500', '27', '0', None, '1', '1', None,
                          '11/10/2019', '0', '12/10/2019', '1', '12/02/2019', '1', '0', '1',
                        '1', '1', '1', None, '1', '1', '1', '0',
                          '1', '1', '0', '0', '1', '0', '0', '0', '1', '1', '0',
                          '0', '0', '0', '1', '0'
                        ]
    @patch('builtins.input', side_effect=mainLicenseUnknown)
    def testMainLicenseUnknown(self, mock_input):
        print("\n\n========\nTest 2\n========")
        testNo = 2
        Results.Uncertainties = []
        results = main()
        Contraventions = results[0]
        Uncertainties = results[1]
        time.sleep(1) #Don't interrupt determination
        #self.assertEqual(len(Contraventions), 0)
        self.assertEqual(Uncertainties, [
            "\t\t\t --What type of entity Westpac Bank is. For the purposes of this determination, it has "
            "been assumed that they are a 'person' under the Act.",
            "\t\t\t --Whether Westpac Bank held a license. For the purposes of this "
                                         "determination, this is assumed to be true.",
            "\t\t\t --Whether the amount of credit available under the contract "
                                          "ordinarily increases as the amount of credit is reduced.",
            "\t\t\t --Whether the credit was to be used in securing a reverse mortgage over a dwelling or land. "
            "This is relevant for determining whether r28HA of the National Consumer Credit Protection Regulations "
            "2010 applies.",
            "\t\t\t --Whether Westpac Bank made reasonable inquiries about the maximum credit limit "
            "required by Nic2. This is prescribed by r28JA of the National Consumer Credit "
            "Protection Regulations 2010 and its absence constitutes a breach of s130(d) of "
            "the Act. "
                                         ])


    mainNoContract = ['1',
                      'Westpac Bank', 'corporate', 'Nic3', 'natural person', '1',
                         '0', '0', '0', '0', '0', '0'
                         ]
    @patch('builtins.input', side_effect=mainNoContract)
    def testNoContract(self, mock_input):
        print("\n\n========\nTest 3\n========")
        testNo = 3
        Results.Uncertainties = []
        results = main()
        Contraventions = results[0]
        Uncertainties = results[0]
        time.sleep(1)  # Don't interrupt determination

        self.assertEqual(len(Contraventions), 0)
        self.assertEqual(len(Uncertainties), 0)



    mainTrusteesNumberUnknown_CreditGuideProvidedUnknown = ['1',
                                                            'Westpac Bank', 'Trust', "Unknown", 'Nic4', 'natural person', '1',
                        '0', '0', '1', '1', '6000', '232', '1', '1', '1', '0', '0',
                        '12/12/2019', 'Unknown', '20/12/2019', '1', '20/12/2018', '1', '1', '1',
                        '1', '1', '1', '1' '1', '1', '1',
                         '1', '1', '0', '0', '1', '0', '0', '0', '1', '1','0',
                         '1', '1', '0', '0', '1', '0', '0', '0', '1', '1'
                        ]
    @patch('builtins.input', side_effect=mainTrusteesNumberUnknown_CreditGuideProvidedUnknown)
    def testTrusteesNumberUnknown_CreditGuideProvidedUnknown(self, mock_input):
        print("\n\n========\nTest 4\n========")
        testNo = 4
        Results.Uncertainties = []
        results = main()
        Contraventions = results[0]
        Uncertainties = results[1]
        time.sleep(1) #Don't interrupt determination
        #self.assertEqual(len(Contraventions), 0)
        #self.assertEqual(Uncertainties, ["\t\t\t --Whether Westpac Bank held a license."])


