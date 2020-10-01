from Definitions import *
from Functions import *
import NCCPA
import config
import Results
import time
import textwrap

def main():
    wrap = textwrap.TextWrapper(width=150)
    print("\n"*4)
    print("Last Updated: 29 September 2020")
    print("""
  _____       _                          _____          _         
 |  __ \     | |                        / ____|        | |        
 | |__) |   _| | ___  ___    __ _ ___  | |     ___   __| | ___    
 |  _  / | | | |/ _ \/ __|  / _` / __| | |    / _ \ / _` |/ _ \   
 | | \ \ |_| | |  __/\__ \ | (_| \__ \ | |___| (_) | (_| |  __/   
 |_|  \_\__,_|_|\___||___/  \__,_|___/  \_____\___/ \__,_|\___|   
                                                                  
                                                                                                                                                                                                    
        """)
    print("""
  _   _  _____ _____ _____                 _                      _____ _                 _              _____ _____ _____ 
 | \ | |/ ____/ ____|  __ \      /\       | |                    / ____| |               | |            |_   _|_   _|_   _|
 |  \| | |   | |    | |__) |    /  \   ___| |_   ______ ______  | |    | |__   __ _ _ __ | |_ ___ _ __    | |   | |   | |  
 | . ` | |   | |    |  ___/    / /\ \ / __| __| |______|______| | |    | '_ \ / _` | '_ \| __/ _ \ '__|   | |   | |   | |  
 | |\  | |___| |____| |       / ____ \ (__| |_                  | |____| | | | (_| | |_) | ||  __/ |     _| |_ _| |_ _| |_ 
 |_| \_|\_____\_____|_|      /_/    \_\___|\__|                  \_____|_| |_|\__,_| .__/ \__\___|_|    |_____|_____|_____|
                                                                                   | |                                     
                                                                                   |_|                                     
    """)
    print("===========================================================================================================")
    print("")
    print("RULES AS CODE -- Selected Provisions of Chapter III of the National Consumer Credit Protection Act 2009 "
          "(Cth)\n")
    print("===========================================================================================================")
    print("")

    print("Please respond to the input prompts in order to generate a determination.\n")
    para = ("Most questions will be of a Boolean type (True/False) or a 'Yes'/'No' type. For ease of answering, "
            "these questions can be answered with binary input, where 1 = Positive (True/Yes) and 0 = Negative "
            "(False/No). Response can be "
            "submitted by pressing 'enter'.\n"
            )
    wrappedDecision = wrap.wrap(text=para)
    for line in wrappedDecision:
        print(line)
    para = ("To accomodate for the reality that not all facts of a scenario are always known, these questions can also "
            "be answered as 'Indeterminate'. To answer 'unknown', input a '?' or simply press 'enter' without "
            "responding. If a response is not recognised, it will be registered as 'indeterminate' and a warning will "
            "be displayed. \n"
            )
    wrappedDecision = wrap.wrap(text=para)
    for line in wrappedDecision:
        print(line)
    para = ("Other inputs will have specific format requirements which are displayed with the question, such as "
            "[dd/mm/yyyy]. Please respond in these exact formats to ensure the determination is correctly made. ")
    wrappedDecision = wrap.wrap(text=para)
    for line in wrappedDecision:
        print(line)
    print("")
    begin = None
    while (not begin):
        begin = bool_input("Please respond to this prompt with a positive input to begin: ")
        if (not begin):
            if begin == None:
                print("You entered 'Indeterminate' please try again.")
            else:
                try:
                    print("You entered '" + str(begin) + "' please try again.")
                except:
                    print("You entered 'Indeterminate' please try again.")


    # Initial Inputs
    Parties = ["Provider", "Debtor"]
    Entities = []
    Trusts = []
    Contraventions = {}
    civilUnits = int(0)
    criminalUnits = int(0)
    strictLiability = ["s126(1)","s126(2)","s126(4), s127(1)","s127(2)","s127(4)", "s132(1)", "s132(2)", "s132(4)"]
    acceptedTypes = config.bodyCorporate + config.individualTypes

    for party in Parties:
        numTrusteesInput = 0
        trustExists = False
        nameInput = input("%s Name: " % party)
        typeInput = input("%s Type: " % party)
        if typeInput:
            type = str.casefold(typeInput)
        else: type = None
        if type == "trust":
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
        if (type in acceptedTypes) == False:
            typeClarify = None
            while (not typeClarify):
                typeClarify = bool_input("Is the entity best described as a body corporate (1) or a "
                                         "natural person/individual(0)? [1/0] ")
                if typeClarify == 1:
                    type = "corporate"
                elif typeClarify == 0:
                    type = "natural person"
                else:
                    type = None
                    Results.Uncertainties.append(
                        "\t\t\t --The type of entity that %s is. For the purposes of this determination, "
                        "this is assumed to be a corporate body." % Entities[0].name)
        Entities.append(Entity(nameInput, type))
        Trusts.append(Trust(nameInput, numTrusteesInput, trustExists))

    # Define the parties
    isPerson(Entities[0], Trusts[0])
    isPerson(Entities[1], Trusts[1])
    if isLicensee(Entities[0]) == None:
        Results.Uncertainties.append("\t\t\t --Whether %s held a license. For the purposes of this determination, "
                                     "this is assumed to be true." % Entities[0].name)
        Entities[0].licensee = True
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

    if contract.exists:
        isSmallAmountCreditContract(contract, Entities[0])
        define_s128Period(contract)
        reverseMortgageCredit(contract)

    # Evaluate s126
    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and contract.exists
            and (contract.assigned == False)):
        s126vars = NCCPA.s126(Entities[0], Entities[1], contract, civilUnits, criminalUnits)
        creditGuide = s126vars[0]
        Contraventions.update(s126vars[1])
        civilUnits = s126vars[2]
        criminalUnits = s126vars[3]

    # Evaluate s127
    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and (contract.assigned == True)):
        s127vars = NCCPA.s127(Entities[0], Entities[1], contract, civilUnits, criminalUnits)
        creditGuide = s127vars[0]
        Contraventions.update(s127vars[1])
        civilUnits = s127vars[2]
        criminalUnits = s127vars[3]

    # Evaluate s128
    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and contract.exists):
        #TODO add 'or' that licensee increased or represented possiblity to increase limit
        s128vars = NCCPA.s128(Entities[0], Entities[1], contract, civilUnits, criminalUnits, ADIProviders)
        assessment = s128vars[0]
        Contraventions.update(s128vars[1])
        civilUnits = s128vars[2]
        criminalUnits = s128vars[3]
        contract = s128vars[4]

    #Evaluate s131
    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and contract.exists and assessment.exists):
        s131vars = NCCPA.s131(Entities[0], Entities[1], contract, assessment, civilUnits, criminalUnits)
        contract = s131vars[0]
        Entities[1] = s131vars[1]
        Contraventions.update(s131vars[2])
        civilUnits = s131vars[3]
        criminalUnits = s131vars[4]

    #Evaluate s132
    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and contract.exists and assessment.exists):
        s132vars = NCCPA.s132(Entities[0], Entities[1], contract, civilUnits, criminalUnits)
        contract = s132vars[0]
        Contraventions.update(s132vars[3])
        civilUnits = s132vars[1]
        criminalUnits = s132vars[2]

    #Evaluate s133
    if (Entities[0].creditProvider and Entities[0].licensee and Entities[1].consumer and contract.exists and assessment.exists):
        s133vars = NCCPA.s133(Entities[0], Entities[1], contract, civilUnits, criminalUnits)
        Contraventions.update(s133vars[0])
        civilUnits = s133vars[1]
        criminalUnits = s133vars[2]

    time.sleep(1)

    if Entities[0].type in config.bodyCorporate:
        criminalUnits = criminalUnits*5

    # State compliance
    print('\n\nDetermination: \n')
    print("The following determination takes into account " + config.consideredLaw)

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
    print("")
    input("Press 'enter' to close...")