# ABBREVIATIONS
# NCCPA = National Consumer Credit Protection Act 2009 (Cth)
# AIA = Acts Interpretation Act 1901 (Cth)
# NCC = 'National Credit Code', Schedule 1 of the NCCPA

from Functions import *

# Init Variables
smallCreditLimit = 2000
smallTermLimit = 365 #TODO DEFINE A YEAR

class Contract:
    def __init__(self, exists):
        self.exists = exists
        self.party1 = ""
        self.party2 = ""
        self.credit = False
        self.continuingCredit = False
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
    if bool_input("Does %s hold (alone or jointly with another) an account with a provider other than %s into which "
                  "income payable to them is credited? " %(consumer.name, provider.name)):
        moreProviders = True
        i = 0
        while moreProviders:
            providerName = input("Provider Name: ")
            providerType = input("Provider Type: ")
            otherProviders.append(Entity(providerName, providerType))
            isAuthorisedDepositTakingInstitution(otherProviders[i])
            if otherProviders[i].ADI:
                ADIProviders.append(otherProviders[i])
            moreProviders = bool_input("Are there more providers to list? ")
            i += 1
    consumer.holdsWithADI = True
    return ADIProviders


def isAuthorisedDepositTakingInstitution(provider):
    provider.ADI = bool_input("Is %s a body corporate authorised by the Australian Prudential Regulation Authority to carry on "
                  "banking business in Australia? " %provider.name)
    return provider.ADI

def isContinuingCreditContract(contract):
    if (contract.credit and bool_input("Does the contract contemplate multiple advances of credit? ")
            and (bool_input("Does the amount of credit available under the contract ordinarily increase as the amount "
                            "of credit is reduced? "))):
        contract.continuingCredit = True
        return True


def contractExists(provider, debtor):
    if ((provider.person and debtor.person)):
        contract = Contract((bool_input("Did a contract exist between %s and %s? " % (debtor.name, provider.name))))
        if contract.exists == True:
            contract.party1 = provider.name
            contract.party2 = debtor.name
        else:
            contract = Contract(bool_input("Did a contract exist between %s and a third party from whom %s has been assigned "
                               "the rights of a credit provider? " % (debtor.name, provider.name)))
            contract.party1 = provider.name
            contract.party2 = debtor.name
            contract.assigned = True
    else:
        contract = Contract(False)
    return contract


def creditProvided(provider, debtor, contract):
    # NCCPA s5, NCC s3(1)
    if (provider.person and debtor.person and
            (bool_input("Under the contract, was payment owed by %s to %s? " % (debtor.name, provider.name)))
            or (bool_input("Under the contract, did %s incur a debt to %s? " % (debtor.name, provider.name)))
    ):
        provider.creditProvider = True
        contract.credit = True

        contract.creditLimit = int(input("What is the credit limit, in dollars, of the contract? "))
        contract.term = int(input("What is term, in days, of the contract? "))


def isBodyPolitic(entity):
    # AIA s2C(1)
    if str.casefold(entity.type) == "body politic":
        return True #TODO


def isConsumer(entity):
    if ((str.casefold(entity.type) == "natural person") or isStrataCorporation(entity)):
        entity.consumer = True


def isCorporate(entity):
    # AIA s2C(1)
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
    localEnt = str.casefold(entity.type)
    #  NCCPA ss14-15
    if (localEnt == "natural person" or localEnt == "partnership" or
            (localEnt == "trust" and (trust.numTrustees >= 2 or (trust.numTrustees == 1 and s15_1_b(entity))))
            or (isBodyPolitic(entity)) or (isCorporate(entity))):
        entity.person = True
        return True
    else:
        print(entity.__dict__)
        print(trust.__dict__)


def isSmallAmountCreditContract(contract, provider):
    if not (isContinuingCreditContract(contract) and (not isAuthorisedDepositTakingInstitution(provider))
            and (contract.creditLimit <= smallCreditLimit ) and (contract.termLimit >= 16)
            and (contract.termLimit <= smallTermLimit) and smallAmountCreditContractRegulations(contract)):
        contract.smallAmountCredit = True
        return True
        #TODO conditional upon regulations too
        #TODO SOMETHING




def isStrataCorporation(entity):
    if str.casefold(entity.type) == "strata corporation":
        return True #TODO


def smallAmountCreditContractRegulations(contract):
    #TODO include regulation conditions
    return True

def s15_1_b(entity):
    if bool_input("Was the current sole trustee of %s a trustee at a time when it had two or "
                  "more trustees? " %entity.name):
        return True


