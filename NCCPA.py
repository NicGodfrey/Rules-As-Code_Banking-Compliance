from datetime import datetime
from Definitions import *
from Functions import *
from tribool import Tribool
import Results

def s126(licensee, consumer, contract, civilUnits, criminalUnits):
    localContraventions = {}
    c126_1 = []
    c126_2 = []
    c126_4 = []
    creditGuideContraventions = []
    creditGuide = document(False)

    creditGuideRequirements = {"  was in writing ": creditGuide.writing,
                               "  was in the form (if any) prescribed by the regulations ": creditGuide.regulationForm,
                               "  specified %s's name and contact details " %licensee.name: creditGuide.licenseeDetails,
                               "  specified %s's Australian credit license number " %licensee.name:
                                   creditGuide.creditLicense,
                               "  contained information surrounding %s's disputes procedure " %licensee.name:
                                   creditGuide.licenseeProcedures,
                               "  included contact details for %s to access %s's internal dispute resolution procedure "
                               %(consumer.name, licensee.name): creditGuide.internalDisResProc,
                               "  included contact details for %s to access the Australian Financial Complaints "
                               "Authority scheme " %consumer.name: creditGuide.theAFCAScheme,
                               "  included information about %s's obligations under sections 132 and 133 of the "
                               "National Consumer Credit Protection Act 2009 (Cth) " %licensee.name:
                                   creditGuide.licenseeObligations,
                               "  complied with all other requirements prescribed by the regulations ":
                                   creditGuide.otherRegulations
                               }

    apparentDate = datetime.strptime(input("On what day did it become apparent that %s was likely to enter into a "
                                           "credit contract with %s as the debtor? (dd/mm/yyyy) "
                                           %(licensee.name, consumer.name)),'%d/%m/%Y')
    contract.apparentDate = apparentDate

    creditGuide = document(bool_input("Did %s provide %s with their credit guide? " % (licensee.name, consumer.name)))
    if creditGuide.exists:
        suppliedDate = datetime.strptime(input("On what day was the credit guide provided? (dd/mm/yyyy) "),'%d/%m/%Y')
        creditGuide.dateProvided = suppliedDate
        # As soon as practicable?
        if s126_127__practicable(licensee, consumer, apparentDate, suppliedDate):
            pass
        else:
            c126_1.append("failing to provide %s with the credit guide within a time period which was as soon as "
                          "practicable" %consumer.name)
        # 126(2)
        print("Which of the following are true? The provided credit guide: ")
        for req in creditGuideRequirements:
            creditGuideRequirements[req] = bool_input(req)
            if not creditGuideRequirements[req]:
                creditGuideContraventions.append(req)
        if bool_input("Was the credit guide provided in the manner (if any) prescribed by the regulations? "):
            creditGuide.regulationManner = True
        else:
            c126_4.append("failing to provide %s with the credit guide in the manner prescribed by the regulations"
                          % consumer.name)
    elif creditGuide.exists == None:
        Results.Uncertainties.append("\t\t\t --Whether %s provided %s with their credit guide. This is relevant for "
                                        "determining whether s126 has been breached by %s."
                                        % (licensee.name, consumer.name, licensee.name))
    else:
        c126_1.append("failing to provide %s with the credit guide" % consumer.name)

    if c126_1:
        localContraventions["s126(1)"] = c126_1
    if creditGuideContraventions:
        creditGuideContraventions = [x[2:-1] for x in creditGuideContraventions] # Remove space at the end of each item
        creditGuideContraventionsLast = creditGuideContraventions[-1]
        del creditGuideContraventions[-1]
        if creditGuideContraventions:
            c126_2.append("failing to provide a credit guide which " + ', '.join(creditGuideContraventions) +
                          ' and ' + creditGuideContraventionsLast)
        else:
            c126_2.append("failing to provide a credit guide which " + creditGuideContraventionsLast)
        localContraventions["s126(2)"] = c126_2

    if c126_4:
        localContraventions["s126(4)"] = c126_4

    if localContraventions:
        civilUnits += 5000
        criminalUnits += 50

    return creditGuide, localContraventions, civilUnits, criminalUnits


def s127(licensee, consumer, contract, civilUnits, criminalUnits):
    localContraventions = {}
    c127_1 = []
    c127_2 = []
    c127_4 = []
    creditGuideContraventions = []
    creditGuide = document(False)

    creditGuideRequirements = {"  was in writing ": creditGuide.writing,
                               "  was in the form (if any) prescribed by the regulations ": creditGuide.regulationForm,
                               "  specified %s's name and contact details " %licensee.name: creditGuide.licenseeDetails,
                               "  specified %s's Australian credit license number " %licensee.name:
                                   creditGuide.creditLicense,
                               "  contained information surrounding %s's disputes procedure " %licensee.name:
                                   creditGuide.licenseeProcedures,
                               "  included contact details for %s to access %s's internal dispute resolution procedure "
                               %(consumer.name, licensee.name): creditGuide.internalDisResProc,
                               "  included contact details for %s to access the Australian Financial Complaints "
                               "Authority scheme " %consumer.name: creditGuide.theAFCAScheme,
                               "  complied with all other requirements prescribed by the regulations ":
                                   creditGuide.otherRegulations
                               }

    apparentDate = datetime.strptime(input("On what day did it become apparent that %s was likely to enter into a "
                                           "credit contract with %s as the debtor? (dd/mm/yyyy) "
                                           %(licensee.name, consumer.name)),'%d/%m/%Y')
    contract.apparentDate = apparentDate

    creditGuide = document(bool_input("Did %s provide %s with their credit guide? " % (licensee.name, consumer.name)))
    if creditGuide.exists:
        suppliedDate = datetime.strptime(input("On what day was the credit guide provided? (dd/mm/yyyy) "),'%d/%m/%Y')
        creditGuide.dateProvided = suppliedDate
        # As soon as practicable?
        if s126_127__practicable(licensee, consumer, apparentDate, suppliedDate):
            pass
        else:
            c127_1.append("failing to provide %s with the credit guide within a time period which was as soon as "
                          "practicable" %consumer.name)
        # 127(2)
        print("Which of the following are true? The provided credit guide: ")
        for req in creditGuideRequirements:
            creditGuideRequirements[req] = bool_input(req)
            if not creditGuideRequirements[req]:
                creditGuideContraventions.append(req)
        if bool_input("Was the credit guide provided in the manner (if any) prescribed by the regulations? "):
            creditGuide.regulationManner = True
        else:
            c127_4.append("failing to provide %s with the credit guide in the manner prescribed by the regulations"
                          % consumer.name)
    elif creditGuide.exists == None:
        Results.Uncertainties.append("\t\t\t --Whether %s provided %s with their credit guide. This is relevant for "
                                        "determining whether s127 has been breached by %s."
                                        % (licensee.name, consumer.name, licensee.name))
    else:
        c127_1.append("failing to provide %s with the credit guide" % consumer.name)

    if c127_1:
        localContraventions["s127(1)"] = c127_1
    if creditGuideContraventions:
        creditGuideContraventions = [x[2:-1] for x in creditGuideContraventions] # Remove space at the end of each item
        creditGuideContraventionsLast = creditGuideContraventions[-1]
        del creditGuideContraventions[-1]
        if creditGuideContraventions:
            c127_2.append("failing to provide a credit guide which " + ', '.join(creditGuideContraventions) +
                      ' and ' + creditGuideContraventionsLast)
        else:
            c127_2.append("failing to provide a credit guide which " + creditGuideContraventionsLast)
        localContraventions["s127(2)"] = c127_2
    if c127_4:
        localContraventions["s127(4)"] = c127_4

    if localContraventions:
        civilUnits += 5000
        criminalUnits += 50

    return creditGuide, localContraventions, civilUnits, criminalUnits


def s128(licensee, consumer, contract, civilUnits, criminalUnits, ADIProviders):
    c128 = []
    c128_c = []
    c128_d = []
    assessment = document(False)
    assessmentContraventions = []
    localContraventions = {}

    assessmentRequirements = {"  specifies the period the assessment covers ": assessment.specifiesPeriod,
                               "  assesses whether the credit contract will be unsuitable for %s if the contract is "
                               "entered into or the credit limit increases during the specified period " %consumer.name:
                                   assessment.assesses,
                               "  covers the period in which the credit day occurs " : assessment.coversCreditDay
                               }

    creditDay = datetime.strptime(input("On what day was the credit contract entered into? (dd/mm/yyyy) " ),'%d/%m/%Y')
    if bool_input("Did %s make an assessment regarding the suitability of the credit contract? " %licensee.name):
        assessment = document(True)
        assessmentDay = datetime.strptime(input("On what day was the assessment made? (dd/mm/yyyy) " ),'%d/%m/%Y')
        if (creditDay - assessmentDay).days > 90:
            c128.append("failing to assess the suitability of the credit contract within 90 days of the credit day")
        print("Which of the following are true? The provided credit guide: ")
        for req in assessmentRequirements:
            assessmentRequirements[req] = bool_input(req)
            if not assessmentRequirements[req]:
                assessmentContraventions.append(req)
    else:
        creditContract = document(False)
        c128_c.append("failing to assess the suitability of the credit contract with %s" % consumer.name)

    s130vars = s130(licensee, consumer, contract, civilUnits, ADIProviders)
    s130Contraventions = s130vars[1] #TODO .join (and) (last)
    if not s130vars[0]:
        c128_d.append("failing to make inquiries and verification in accordance with s130, including " +
                      ", ".join(s130Contraventions))


    if assessmentContraventions:
        assessmentContraventions = [x[2:-1] for x in assessmentContraventions] # Remove space at the end of each item
        assessmentContraventionsLast = assessmentContraventions[-1]
        del assessmentContraventions[-1]
        if assessmentContraventions:
            c128_c.append("failing to make an assessment which " + ', '.join(assessmentContraventions) +
                          ' and ' + assessmentContraventionsLast)
        else:
            c128_c.append("failing to make an assessment which " + assessmentContraventionsLast)
    if c128_c:
        localContraventions["s128(c)"] = c128_c
    if c128_d:
        localContraventions["s128(d)"] = c128_d

    if localContraventions:
        civilUnits += 5000

    return assessment, localContraventions, civilUnits, criminalUnits

def s130(licensee, consumer, contract, civilUnits, ADIProviders):
    c130 = []
    if not bool_input("Did %s make reasonable inquiries about %s's requirements and objectives in relation to the "
                          "credit contract? " % (licensee.name, consumer.name)):
        c130.append("failing to make reasonable inquiries about %s's requirements and objectives in relation to the "
                    "credit contract" %consumer.name)

    if not bool_input("Did %s make reasonable inquiries about %s's financial situation? "
                          % (licensee.name, consumer.name)):
        c130.append("failing to make reasonable inquiries about %s's financial situation" %consumer.name)
    else:
        if not bool_input("Did %s take reasonable steps to verify %s's financial situation? "
                              % (licensee.name, consumer.name)):
            c130.append("failing to take reasonable steps to verify %s's financial situation" %consumer.name)

    if not bool_input("Did %s make all inquiries prescribed by the regulations? "
                          % licensee.name):
        c130.append("failing to make all inquiries prescribed by the regulations")

    if not bool_input("Did %s ake all steps prescribed by the regulations to verify any prescribed matters? "
                      %licensee.name):
        c130.append("failing to take all steps prescribed by the regulations to verify any prescribed matters")

    #130(1A)
    c130_1A_breach = False
    if (contract.smallAmountCredit and consumer.holdsWithADI):
        for ADIProvider in ADIProviders:
            if not (bool_input("In making the required inquiries, did %s obtain and consider account statements that "
                               "cover the immediately preceding period of 90 days from %s? "
                               %(licensee.name, ADIProvider.name))):
                c130.append("failing to to obtain and consider account statements covering the immediately preceding 90"
                            " days from %s" %ADIProvider.name)

    if c130:
        civilUnits += 5000
        return False, c130
    else:
        return True, c130


def s126_127__practicable(licensee, consumer, apparentDate, suppliedDate):
    #Some function to determine if the time taken to supply credit guide was "as soon as practicable"
    return True #TODO


