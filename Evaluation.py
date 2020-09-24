from Definitions import *
from Functions import *
import NCCPA
import config
import Results

import textwrap

def main():
    # Initial Inputs
    Parties = ["Provider", "Debtor"]
    Entities = []
    Trusts = []
    Contraventions = {}
    civilUnits = int(0)
    criminalUnits = int(0)
    strictLiability = ["s126(1)","s126(2)","s126(4), s127(1)","s127(2)","s127(4)"]

    for party in Parties:
        numTrusteesInput = 0
        trustExists = False
        nameInput = input("%s Name: " % party)
        typeInput = input("%s Type: " % party)
        if str.casefold(typeInput) == "trust":
            numTrusteesInput = input("How many trustees did %s have at the relevant time? " % nameInput)
            try:
                numTrusteesInput = int(numTrusteesInput)
            except ValueError:
                if numTrusteesInput == "":
                    pass
                else:
                    print("Warning: Response was unclear. Answer has been marked as 'Unknown'.")
                numTrusteesInput = 2
                Results.Uncertainties.append("\t\t\t --The number of trustees held by %s. This has been assumed to be at least "
                                     "2, so as to allow %s to be considered a 'person' as defined in the Act."
                                     % (nameInput,nameInput))
            trustExists = True
        Entities.append(Entity(nameInput, typeInput))
        Trusts.append(Trust(nameInput, numTrusteesInput, trustExists))

    # Define the parties
    isPerson(Entities[0], Trusts[0])
    isPerson(Entities[1], Trusts[1])
    if isLicensee(Entities[0]) == None:
        Results.Uncertainties.append("\t\t\t --Whether %s held a license." % Entities[0].name) #TODO ASSUMPTION?
    isConsumer(Entities[1])
    ADIVars = holdsWithADI(Entities[1], Entities[0])
    ADIProviders = ADIVars

    # Define the agreement
    contract = contractExists(Entities[0], Entities[1])
    if contract.exists:
        creditProvided(Entities[0], Entities[1], contract)
    else:
        contract.represented = (bool_input("Did %s make an unconditional representation to %s that they consider %s is "
                                           "eligible to enter into a credit contract with them? "
                                           %(Entities[0].name, Entities[1].name, Entities[1].name)))
        if contract.represented == None:
            Results.Uncertainties.append("\t\t\t --Whether a contract existed or was represented. This has been assumed "
                                 "true so as to assume the existence of a credit contract for the purposes of the Act.")



    isSmallAmountCreditContract(contract, Entities[0])

    # Evaluate s126
    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and contract.exists
            and (contract.assigned == False)):
        s126vars = NCCPA.s126(Entities[0], Entities[1], contract, civilUnits, criminalUnits)
        creditGuide = s126vars[0]
        Contraventions.update(s126vars[1])
        civilUnits = s126vars[2]
        criminalUnits = s126vars[3]

    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and (contract.assigned == True)):
        s127vars = NCCPA.s127(Entities[0], Entities[1], contract, civilUnits, criminalUnits)
        creditGuide = s127vars[0]
        Contraventions.update(s127vars[1])
        civilUnits = s127vars[2]
        criminalUnits = s127vars[3]

    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and contract.exists):
        #TODO add 'or' that licensee increased or represented possiblity to increase limit
        s128vars = NCCPA.s128(Entities[0], Entities[1], contract, civilUnits, criminalUnits, ADIProviders)
        assessment = s128vars[0]
        Contraventions.update(s128vars[1])
        civilUnits = s128vars[2]
        criminalUnits = s128vars[3]




    print(contract.__dict__)
    print(Entities[0].__dict__)
    print(Entities[1].__dict__)

    # State compliance
    wrap = textwrap.TextWrapper(width=100)

    print('\n\nDetermination: \n')

    if Contraventions:
        para = (Entities[0].name + " has failed to be fully compliant with Chapter III of the National Consumer Credit "
                                 "Protection Act 2009 (Cth). Specifically, the following sections have been "
                                   "contravened: " + ', '.join(Contraventions.keys()) + ".")
        wrappedDecision = wrap.wrap(text=para)
        for line in wrappedDecision:
            print(line)

        for section in Contraventions:
            ReasonsList = []
            thisSection = Contraventions[section]
            #lastReason =  thisSection[-1]
            #del thisSection[-1]
            ReasonsList.append(Entities[0].name + " breached " + section + " by " + "".join(thisSection) + ".")

            para = ("".join(ReasonsList))
            wrappedDecision = wrap.wrap(text=para)
            print("")
            for line in wrappedDecision:
                print(line)
            if section in strictLiability:
                print("Breaching " + section + " is an offense of strict liability.")

        para = (Entities[0].name + " faces " + format(civilUnits, ",") + " civil penanlty units and " +
                format(criminalUnits, ",") + " criminal penalty units as a result.")
        wrappedDecision = wrap.wrap(text=para)
        print("")
        for line in wrappedDecision:
            print(line)
        #Partnership and Trust individually liable?
    else:
        para = ("Subject to the accuracy of the inputted facts, it appears " + Entities[0].name +
                " has not breached " + config.sectionsCovered + ".")
        wrappedDecision = wrap.wrap(text=para)
        for line in wrappedDecision:
            print(line)

    if Results.Uncertainties:
        print("")
        para = ("The above determination assumes all information supplied is correct. It is limited due to "
                "uncertainties and/or assumptions in relevant facts, including the following:")
        wrappedDecision = wrap.wrap(text=para)
        for line in wrappedDecision:
            print(line)

        for item in Results.Uncertainties:
            para = (item)
            wrappedDecision = wrap.wrap(text=para)
            for line in wrappedDecision:
                print(line)

    if config.unitTesting == True:
        return(Contraventions, Results.Uncertainties)

if config.unitTesting == True:
    pass
else:
    main()