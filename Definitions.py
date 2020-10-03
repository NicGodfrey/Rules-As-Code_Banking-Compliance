# ABBREVIATIONS
# NCCPA = National Consumer Credit Protection Act 2009 (Cth)
# AIA = Acts Interpretation Act 1901 (Cth)
# NCC = 'National Credit Code', Schedule 1 of the NCCPA
import Results
import config
from Functions import *

# Init Variables
smallCreditLimit = 2000
smallTermLimit = config.daysInYear

class Contract:
    def __init__(self, exists):
        self.exists = exists
        self.party1 = None
        self.party2 = None
        self.credit = None
        self.continuingCredit = None
        self.assigned = False
        self.represented = False
        self.creditLimit = 0
        self.term = 0
        self.smallAmountCredit = False
        self.creditDay = None
        self.likelySubstantialHardship = None
        self.deemedUnsuitable = None
        self.isUnsuitable = None
        self.notMeetRequirements = None
        self.otherwiseUnsuitable = None
        self.contemplatesMultipleCredit = None
        self.paymentOwed = None
        self.forResidentialProperty = None
        self.securedByMortgageOverPurchasedProperty = None
        self.s128_period = 90
        self.isStandardForm = None
        self.isStandardHomeLoan = None
        self.isToRefinanceCreditProvidedToPurchaseResidentialProperty = None


class document:
    def __init__(self, exists):
        self.exists = exists
        self.dateProvided = False
        # CREDIT GUIDE -- NCCPA s126(2)
        self.writing = True
        self.regulationForm = True
        self.licenseeDetails = True
        self.creditLicense = True
        self.licenseeProcedures = True
        self.internalDisResProc = True
        self.theAFCAScheme = True
        self.licenseeObligations = True
        self.otherRegulations = True
        self.regulationManner = True

        self.specifiesPeriod = True
        self.assesses = True
        self.coversCreditDay = True



class Entity:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.person = False  # Initialise as false
        self.licensee = False
        self.creditProvider = False
        self.consumer = False
        self.ADI = False
        self.holdsWithADI = False
        self.debtorInDefaultOfOtherSmallAmount = None
        self.debtorUnder2SmallAmountIn90 = None


class Trust:
    def __init__(self, name, numTrustees, exists):
        self.name = name
        self.numTrustees = numTrustees
        self.exists = exists


def holdsWithADI(consumer, provider):
    otherProviders = []
    ADIProviders = []
    otherProvidersExist = bool_input("Does %s hold (alone or jointly with another) an account with a provider other than %s into which "
                  "income payable to them is credited? " %(consumer.name, provider.name))
    if otherProvidersExist:
        moreProviders = True
        i = 0
        while moreProviders:
            providerName = input("Provider Name: ")
            providerType = input("Provider Type: ")
            otherProviders.append(Entity(providerName, providerType))
            isAuthorisedDepositTakingInstitution(otherProviders[i])
            if otherProviders[i].ADI:
                ADIProviders.append(otherProviders[i])
                consumer.holdsWithADI = True
            moreProviders = bool_input("Are there more providers to list? ")
            i += 1

    elif otherProvidersExist == None:
        Results.Uncertainties.append("\t\t\t --Whether %s holds accounts with any other providers into which income "
                                     "payable to them is credited." %consumer.name)
    return ADIProviders


def isAuthorisedDepositTakingInstitution(provider):
    provider.ADI = bool_input("Is %s a body corporate authorised by the Australian Prudential Regulation Authority to carry on "
                  "banking business in Australia? " %provider.name)
    if provider.ADI == None:
        Results.Uncertainties.append("\t\t\t --Whether %s is a body corporate authorised by the Australian Prudential "
                                     "Regulation Authority to carry on banking business in Australia." % provider.name)
    return provider.ADI

def isContinuingCreditContract(contract):
    contract.contemplatesMultipleCredit = bool_input("Does the contract contemplate multiple advances of credit? ")
    contract.creditAvailableOrdinarilyIncreases = bool_input("Does the amount of credit available under the contract "
                                                             "ordinarily increase as the amount of credit is reduced? ")
    if contract.contemplatesMultipleCredit == None:
        Results.Uncertainties.append("\t\t\t --Whether the contract contemplates multiple advances of credit.")
    if contract.creditAvailableOrdinarilyIncreases == None:
        Results.Uncertainties.append("\t\t\t --Whether the amount of credit available under the contract "
                                                             "ordinarily increases as the amount of credit is reduced.")
    if (contract.credit and contract.contemplatesMultipleCredit and contract.creditAvailableOrdinarilyIncreases):
        contract.continuingCredit = True
        return True


def contractExists(provider, debtor):
    if ((provider.person and debtor.person)):
        contract = Contract((bool_input("Did a contract exist between %s and %s? " % (debtor.name, provider.name))))
        if contract.exists == True:
            contract.party1 = provider.name
            contract.party2 = debtor.name
        elif contract.exists == False:
            contract = Contract(bool_input("Did a contract exist between %s and a third party from whom %s has been assigned "
                               "the rights of a credit provider? " % (debtor.name, provider.name)))
            contract.party1 = provider.name
            contract.party2 = debtor.name
            contract.assigned = True

            if contract.exists == None:
                Results.Uncertainties.append("\t\t\t --Whether a contract existed between %s and a third party from "
                                             "whom %s has been assigned the rights of a credit provider. "
                                         "For the purposes of this determination, it is that this is true."
                                         % (debtor.name, provider.name))

        elif contract.exists == None:
            Results.Uncertainties.append("\t\t\t --Whether a contract existed between %s and %s or a third party. "
                                             "For the purposes of this determination, it is assumed that a contract "
                                             "existed between %s and %s"
                                             % (debtor.name, provider.name, debtor.name, provider.name))


    else:
        contract = Contract(False)
    return contract


def creditProvided(provider, debtor, contract):
    # NCCPA s5, NCC s3(1)
    #contract.paymentOwed
    if (provider.person and debtor.person):

        paymentOwed = bool_input("Under the contract, was payment owed by %s to %s? " % (debtor.name, provider.name))
        if not paymentOwed:
            debtIncurred = bool_input("Under the contract, did %s incur a debt to %s? " % (debtor.name, provider.name))
        else: debtIncurred = paymentOwed

        if (paymentOwed or debtIncurred):
            provider.creditProvider = True
            contract.credit = True
            contract.creditLimit = int(input("What is the credit limit, in dollars, of the contract? "))
            contract.term = int(input("What is the term, in days, of the contract? "))

        elif ((paymentOwed == None) or (debtIncurred == None)):
            Results.Uncertainties.append("\t\t\t --Whether, under the contract, payment was owed or a debt incurred "
                                         "by %s to %s. For the purposes of this determination, this is assumed to have "
                                         "been true."
                                         % (debtor.name, provider.name))
            provider.creditProvider = True
            contract.credit = True
            contract.creditLimit = int(input("What is the credit limit, in dollars, of the contract? "))
            contract.term = int(input("What is the term, in days, of the contract? "))

        else:
            provider.creditProvider = False
            contract.credit = False


def isBodyPolitic(entity):
    # AIA s2C(1)
    if entity.type:
        if str.casefold(entity.type) == "body politic":
            return True #TODO
    else:
        return False


def isConsumer(entity):
    if entity.type:
        if ((str.casefold(entity.type) == "natural person") or isStrataCorporation(entity)):
            entity.consumer = True


def isCorporate(entity):
    # AIA s2C(1)
    if entity.type:
        if str.casefold(entity.type) == "corporate":
            return True #TODO


def isCreditProvider(entity):
    if bool_input("Did %s provide or expect to provide credit? " %entity.name):
        entity.creditProvider = True
        return True


def isLicensee(entity):
    if (entity.person):
        entity.licensee = bool_input("Did %s hold a license? " % entity.name)
    return entity.licensee


def isPerson(entity, trust):  # For the purposes of NCCPA (other than the National Credit Code)
    try:
        localEnt = str.casefold(entity.type)
    except TypeError:
        localEnt = None
    #  NCCPA ss14-15
    if (localEnt == "natural person" or localEnt == "partnership" or
            (localEnt == "trust" and (trust.numTrustees >= 2 or (trust.numTrustees == 1 and s15_1_b(entity))))
            or (isBodyPolitic(entity)) or (isCorporate(entity))):
        entity.person = True
        return True
    elif ((localEnt == None) or (localEnt == "")):
        Results.Uncertainties.append("\t\t\t --What type of entity %s is. For the purposes of this determination, it has "
                                     "been assumed that they are a 'person' under the Act."
                                     % (entity.name))
        entity.person = True
        return True

    else:
        return False


def isSmallAmountCreditContract(contract, provider):
    if not (isContinuingCreditContract(contract) and (not isAuthorisedDepositTakingInstitution(provider))
            and (contract.creditLimit <= smallCreditLimit ) and (contract.termLimit >= 16)
            and (contract.termLimit <= smallTermLimit) and smallAmountCreditContractRegulations(contract)):
        contract.smallAmountCredit = True
        return True
        #TODO conditional upon regulations too
        #TODO SOMETHING


def isStandardHomeLoan(contract):
    contract.isStandardForm = bool_input("Is the credit contract of a standard form? ")
    if contract.isStandardForm:
        if contract.forResidentialProperty:
            contract.isStandardHomeLoan = True
        else:
            contract.isToRefinanceCreditProvidedToPurchaseResidentialProperty = bool_input("Was the credit provided to "
                                                                                           "refinance credit that has "
                                                                                           "been provided wholly or "
                                                                                           "predominantly to purchase "
                                                                                           "residential property?")
            if contract.isToRefinanceCreditProvidedToPurchaseResidentialProperty:
                contract.isStandardHomeLoan = True



def isStrataCorporation(entity):
    if entity.type:
        if str.casefold(entity.type) == "strata corporation":
            return True #TODO
    else:
        return False


def smallAmountCreditContractRegulations(contract):
    #TODO include regulation conditions
    return True


def reverseMortgageCredit(contract):
    contract.isForReverseMortgage = bool_input("Was the credit to be used to secure a reverse mortgage over a dwelling "
                                               "or land?")
    if contract.isForReverseMortgage == None:
        Results.Uncertainties.append(
            "\t\t\t --Whether the credit was to be used in securing a reverse mortgage over a dwelling or land. "
            "This is relevant for determining whether r28HA of the National Consumer Credit Protection Regulations "
            "2010 applies.")


def standardHomeLoanKeyFactsSheet():
    pass #TODO

def s15_1_b(entity):
    trusteeAtTimeWith2 = bool_input("Was the current sole trustee of %s a trustee at a time when it had two or "
                  "more trustees? " %entity.name)
    if trusteeAtTimeWith2:
        return True
    elif ((trusteeAtTimeWith2 == None) or (trusteeAtTimeWith2 == "")):
        Results.Uncertainties.append(
            "\t\t\t --Whether the sole trustee of %s was a trustee at a time when it had two or more trustees. "
            "This is relevant for determining whether %s is a 'person' under the Act, and has been assumed to be true "
            "for the purposes of this determination."
            % (entity.name))


def define_s128Period(contract):
    contract.forResidentialProperty = bool_input("Was the credit provided under the contract to be used for the purchase "
                                                 "of a residential property? ")
    if contract.forResidentialProperty:
        contract.securedByMortgageOverPurchasedProperty = bool_input("Was the credit to be secured by a mortgage over "
                                                                     "the property? ")
        if contract.securedByMortgageOverPurchasedProperty:
            contract.s128_period = 120
