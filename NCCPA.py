from datetime import datetime, timedelta
from Definitions import *
from Functions import *
from tribool import Tribool
import Results
import config

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
            creditGuideRequirements[req] = bool_input(req) #TODO UNCERTAINTY
            if creditGuideRequirements[req] == False:
                creditGuideContraventions.append(req)
            elif creditGuideRequirements[req] == None:
                Results.Uncertainties.append("\t\t\t --Whether the credit guide" + req[1:-1] + ". This is relevant for "
                                                                                               "determining whether "
                                                                                               "s126(2) has been "
                                                                                               "breached.")
        creditGuide.regulationManner = bool_input("Was the credit guide provided in the manner (if any) prescribed "
                                                 "by the regulations? ")
        if creditGuide.regulationManner == None:
            Results.Uncertainties.append(
                "\t\t\t --Whether the credit guide was given in the manner (if any) prescribed by the regulations. "
                "This is relevant for determining whether s126(4) has been breached.")
        elif creditGuide.regulationManner == False:
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
            creditGuideRequirements[req] = bool_input(req) #TODO UNCERTAINTY
            if creditGuideRequirements[req] == False:
                creditGuideContraventions.append(req)
            elif creditGuideRequirements[req] == None:
                Results.Uncertainties.append("\t\t\t --Whether the credit guide" + req[1:-1] + ". This is relevant for "
                                                                                               "determining whether "
                                                                                               "s127(2) has been "
                                                                                               "breached.")
        creditGuide.regulationManner = bool_input("Was the credit guide provided in the manner (if any) prescribed "
                                                 "by the regulations? ")
        if creditGuide.regulationManner == None:
            Results.Uncertainties.append(
                "\t\t\t --Whether the credit guide was given in the manner (if any) prescribed by the regulations. "
                "This is relevant for determining whether s127(4) has been breached.")
        elif creditGuide.regulationManner == False:
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

    assessmentRequirements = {"  specified the period the assessment covers ": assessment.specifiesPeriod,
                               "  assessed whether the credit contract would be unsuitable for %s if the contract was "
                               "entered into or the credit limit increased during the specified period " %consumer.name:
                                   assessment.assesses,
                               "  covered the period in which the credit day occurs " : assessment.coversCreditDay
                               }

    contract.creditDay = datetime.strptime(input("On what day was the credit contract entered into? (dd/mm/yyyy) " ),'%d/%m/%Y')
    assessment = document(
        bool_input("Did %s make an assessment regarding the suitability of the credit contract? " % licensee.name))

    if assessment.exists:
        assessment.day = datetime.strptime(input("On what day was the assessment made? (dd/mm/yyyy) " ),'%d/%m/%Y')
        if (contract.creditDay - assessment.day).days > contract.s128_period:
            if contract.s128_period == 120:
                c128.append("failing to assess the suitability of the credit contract within 120 days of the credit day")
            else:
                c128.append("failing to assess the suitability of the credit contract within 90 days of the credit day")
        print("Which of the following are true? The assessment: ")
        for req in assessmentRequirements:
            assessmentRequirements[req] = bool_input(req)
            if assessmentRequirements[req] == False:
                assessmentContraventions.append(req)
            elif assessmentRequirements[req] == None:
                Results.Uncertainties.append("\t\t\t --Whether the assessment" + req[1:-1] + ". This is relevant for "
                                                                                               "determining whether "
                                                                                               "s128(c) has been "
                                                                                               "breached.")
    else:
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
    if c128:
        localContraventions["s128"] = c128
    if c128_c:
        localContraventions["s128(c)"] = c128_c
    if c128_d:
        localContraventions["s128(d)"] = c128_d

    if localContraventions:
        civilUnits += 5000

    return assessment, localContraventions, civilUnits, criminalUnits, contract

def s130(licensee, consumer, contract, civilUnits, ADIProviders):
    c130 = []

    s130_1_a = bool_input("Did %s make reasonable inquiries about %s's requirements and objectives in relation to the "
                          "credit contract? " % (licensee.name, consumer.name))
    if s130_1_a == False:
        c130.append("failing to make reasonable inquiries about %s's requirements and objectives in relation to the "
                    "credit contract" %consumer.name)
    elif s130_1_a == None:
        Results.Uncertainties.append("\t\t\t --Whether reasonable inquiries were made regarding"
                                     " %s's requirements and objectives in relation to the credit contract."
                                     %consumer.name)

    s130_1_b = bool_input("Did %s make reasonable inquiries about %s's financial situation? "
                          % (licensee.name, consumer.name))
    if s130_1_b == False:
        c130.append("failing to make reasonable inquiries about %s's financial situation" %consumer.name)
    elif s130_1_b == None:
        Results.Uncertainties.append("\t\t\t --Whether reasonable inquiries were made regarding"
                                         " %s's financial situation, and whether reasonable steps were taken by %s to "
                                         "verify this." % consumer.name, licensee.name)
    else:
        s130_1_c = bool_input("Did %s take reasonable steps to verify %s's financial situation? "
                              % (licensee.name, consumer.name))
        if s130_1_c == False:
            c130.append("failing to take reasonable steps to verify %s's financial situation" %consumer.name)
        elif s130_1_c == None:
            Results.Uncertainties.append("\t\t\t --Whether reasonable steps were taken by %s to verify %s's financial"
                                         "situation." % licensee.name, consumer.name)

    if contract.isForReverseMortgage:
        print("Did %s make reasonable inquiries about %s's requirements and objectives in meeting possible future "
              "needs, including: " %(licensee.name, consumer.name))
        r28HA_2_a = bool_input("  a possible need for aged care accomodation? ") #TODO
        r28HA_2_b = bool_input("  whether %s prefers to leave equity in the dwelling or land to their estate? "
                               %consumer.name)
        if r28HA_2_a == False:
            c130.append("failing to make reasonable inquiries about %s's possible need for aged care accomodation in "
                        "the future"
                % consumer.name)
        elif r28HA_2_a == None:
            Results.Uncertainties.append("\t\t\t --Whether %s made reasonable inquiries about %s's possible need for "
                                         "aged care accomodation in the future. This is prescribed by r28HA(2)(a) of "
                                         "the National Consumer Credit Protection Regulations 2010 and its absence "
                                         "constitutes a breach of s130(d) of the Act. "
                                         % (licensee.name, consumer.name))
        if r28HA_2_b == False:
            c130.append("failing to make reasonable inquiries whether %s prefers to leave equity in the dwelling or "
                        "land to their estate"
                % consumer.name)
        elif r28HA_2_b == None:
            Results.Uncertainties.append("\t\t\t --Whether %s made reasonable inquiries about whether %s prefers to "
                                         "leave equity in the dwelling or land to their estate. This is prescribed by "
                                         "r28HA(2)(b) of the National Consumer Credit Protection Regulations 2010 and "
                                         "its absence constitutes a breach of s130(d) of the Act. "
                                         % (licensee.name, consumer.name))

    r28JA = bool_input("Did %s make reasonable inquiries about the maximum credit limit %s required? "
                              % (licensee.name, consumer.name))
    if r28JA == False:
        c130.append("failing to make reasonable inquiries about the maximum credit limit required by %s"
                    % consumer.name)
    elif r28JA == None:
        Results.Uncertainties.append("\t\t\t --Whether %s made reasonable inquiries about the maximum credit limit "
                                     "required by %s. This is prescribed by r28JA of the National Consumer Credit "
                                     "Protection Regulations 2010 and its absence constitutes a breach of s130(d) of "
                                     "the Act. " % (licensee.name, consumer.name))

    s130_1_d_other = bool_input("Did %s make all other inquiries prescribed by the regulations? "
                          % licensee.name)
    if s130_1_d_other == False:
        c130.append("failing to make all other inquiries prescribed by the regulations")
    elif s130_1_d_other == None:
        Results.Uncertainties.append("\t\t\t --Whether %s made all other inquiries prescribed by the regulations."
                                     % licensee.name)

    s_130_e = bool_input("Did %s take all steps prescribed by the regulations to verify any prescribed matters? "
                      %licensee.name)
    if s_130_e == False:
        c130.append("failing to take all steps prescribed by the regulations to verify any prescribed matters")
    elif s_130_e == None:
        Results.Uncertainties.append("\t\t\t --Whether %s took all steps prescribed by the regulations to verify any "
                                     "prescribed matters."
                                     % licensee.name)

    #130(1A)
    c130_1A_breach = False
    if (contract.smallAmountCredit and consumer.holdsWithADI):
        for ADIProvider in ADIProviders:
            if not (bool_input("In making the required inquiries, did %s obtain and consider account statements that "
                               "cover the immediately preceding period of 90 days from %s? "
                               %(licensee.name, ADIProvider.name))):
                c130.append("failing to obtain and consider account statements covering the immediately preceding 90"
                            " days from %s" %ADIProvider.name)

    if c130:
        civilUnits += 5000
        return False, c130
    else:
        return True, c130


def s131(licensee, consumer, contract, assessment, civilUnits, criminalUnits):

    c131=[]
    localContraventions = {}

    isUnsuitableVars = isUnsuitable(contract, consumer, licensee, assessment.day)
    contract = isUnsuitableVars[0]
    consumer = isUnsuitableVars[1]

    contract.askSuitabilityAgain = bool_input("Between the assessment day (%s) and the day the "
                                              "contract was entered into or the credit limit was "
                                              "increased (%s), would the response to any of the "
                                              "immediately previous checks have changed?"
                                              %(assessment.day.strftime('%d %b %Y'),
                                                contract.creditDay.strftime('%d %b %Y')))


    contract.deemedUnsuitable = bool_input("Did %s deem the contract to be unsuitable for %s? "
                                           %(licensee.name, consumer.name))

    if ((contract.isUnsuitable) and (contract.deemedUnsuitable == False)):
        c131.append("failing to correctly assess the credit contract as unsuitable for %s" %consumer.name)

        if c131:
            localContraventions["s131"] = c131

        if localContraventions:
            civilUnits += 5000

    return contract, consumer, localContraventions, civilUnits, criminalUnits


def s132(licensee, consumer, contract, civilUnits, criminalUnits):
    c132_1 = []
    c132_2 = []
    c132_3 = []
    c132_4 = []
    localContraventions = {}
    #(1)
    consumerRequestedAssessmentPriorToCreditDay = bool_input("Did %s request a copy of the assessment from %s prior to %s? "
                  %(consumer.name, licensee.name, contract.creditDay.strftime('%d %b %Y')))
    if consumerRequestedAssessmentPriorToCreditDay:
        consumerGivenAssessmentPriorToCreditDay = bool_input("For each request, did %s give %s a written copy of the assessment prior "
                                                             "to %s? "
                  %(licensee.name, consumer.name, contract.creditDay.strftime('%d %b %Y')))
        if consumerGivenAssessmentPriorToCreditDay == False:
            civilUnits += 5000
            c132_1.append("failing to give %s a copy of the assessment prior to entering the contract as requested"
                          %consumer.name)
    #(2)
    consumerRequestedAssessmentWithin2Years = bool_input("Did %s request a copy of the assessment from %s between %s "
                                                         "and %s? " %
                                                     (consumer.name, licensee.name,
                                                      contract.creditDay.strftime('%d %b %Y'),
                                                      (contract.creditDay+timedelta(days=365*2)).strftime('%d %b %Y')))
    if consumerRequestedAssessmentWithin2Years:
        consumerGivenAssessmentWithin7Days = bool_input("For each request, did %s give %s a written copy of the "
                                                        "assessment within 7 business days? " #TODO LOOP FOR ALL REQUESTS
                                                             % (licensee.name, consumer.name))
        if consumerGivenAssessmentWithin7Days == False:
            civilUnits += 5000
            criminalUnits += 50
            c132_2.append("failing to give %s a copy of the assessment within 7 business days of %s's request(s)"
                          % (consumer.name, consumer.name))

    consumerRequestedAssessmentWithinPeriod = bool_input("Did %s request a copy of the assessment from %s between %s "
                                                         "and %s? " %
                                                         (consumer.name, licensee.name,
                                                          (contract.creditDay + timedelta(days=365 * 2)).strftime(
                                                              '%d %b %Y'),
                                                          (contract.creditDay + timedelta(days=365 * 7)).strftime(
                                                              '%d %b %Y')))
    if consumerRequestedAssessmentWithinPeriod:
        consumerGivenAssessmentWithin21Days = bool_input("For each request, did %s give %s a written copy of the "
                                                        "assessment within 21 business days? "  # TODO LOOP FOR ALL REQUESTS
                                                        % (licensee.name, consumer.name))
        if consumerGivenAssessmentWithin21Days == False:
            civilUnits += 5000
            criminalUnits += 50
            c132_2.append("failing to give %s a copy of the assessment within 21 business days of %s's request(s)"
                          % (consumer.name, consumer.name))

    #(3)
    assessmentGivenAsPrescribed = bool_input("In all cases, did %s give %s the copy of the assessment in accordance "
                                             "with any manner prescribed by the regulations? "
                                             %(licensee.name, consumer.name))
    if assessmentGivenAsPrescribed == False:
        c132_3.append("failing to give %s a copy of the assessment in accordance with the manner prescribed by the "
                      "regulations"
                      % consumer.name)

    #(4)
    assessmentPaymentAsked = bool_input("In any cases, did %s request or demand payment from %s for giving %s a copy "
                                        "of the assessment? " %(licensee.name, consumer.name, consumer.name))
    if assessmentPaymentAsked == False:
        c132_4.append("requesting or demanding payment from %s for giving a copy of the assessment "
                      % consumer.name)
        civilUnits += 5000
        criminalUnits += 50

    if c132_1:
        localContraventions["s132(1)"] = c132_1

    if c132_2:
        localContraventions["s132(2)"] = c132_2

    if c132_3:
        localContraventions["s132(3)"] = c132_3

    if c132_4:
        localContraventions["s132(4)"] = c132_4

    return contract, civilUnits, criminalUnits, localContraventions


def s133(licensee, consumer, contract, civilUnits, criminalUnits):
    localContraventions = {}
    c133_1 = []

    if contract.askSuitabilityAgain == True:
        isUnsuitableVars = isUnsuitable(contract, consumer, licensee, contract.creditDay)
        contract = isUnsuitableVars[0]
        consumer = isUnsuitableVars[1]

    if contract.isUnsuitable:
        regulationsPrescribeNotUnsuitable = bool_input("Do the regulations prescribe any particular situation matching "
                                                       "the currently considered circumstances in which a credit "
                                                       "contract is taken not to be unsuitable for a consumer? ")
        if regulationsPrescribeNotUnsuitable == False:
            c133_1.append("entering into a contract with %s as a debtor which is unsuitable for %s")
            civilUnits += 5000
            criminalUnits += imprisonment2PenaltyUnits(12*2)

    if c133_1:
        localContraventions["s133(1)"] = c133_1

    return localContraventions, civilUnits, criminalUnits, contract, consumer

# s133AC is not called yet as it is a WIP
def s133AC(licensee, consumer, civilUnits, criminalUnits):
    licensee.hasWebsiteForHomeLoans = bool_input("Did %s have a website that could be accessed by consumers to apply "
                                                 "for or make inquiries about one or more of its standard home loans? "
                                                 %licensee.name)

def s126_127__practicable(licensee, consumer, apparentDate, suppliedDate):
    #Some function to determine if the time taken to supply credit guide was "as soon as practicable"
    return True #TODO

def isUnsuitable(contract, consumer, licensee, relevantDate):
    #Some function to determine if contract was unsuitable: (at current, ask user)
    unsuitableChecks = {
                        #"  %s would be unable to comply with their financial obligations under the contract without"
                        #" substantial hardship" %consumer.name, #TODO 131(3)
                              "  the contract would not meet %s's requirements or objectives " % consumer.name :
                                  contract.notMeetRequirements,
                              "  any other circumstances prescribed by the regulations in which the contract is "
                              "unsuitable " : contract.otherwiseUnsuitable
                              }

    contract.isCreditCard = bool_input("Was the contract a credit card contract? ")

    print("Based off the inquiries made and using only information that %s had reason to believe was true, "
          "which of the following were likely on %s if the contract was entered into or the credit limit increased "
          "during the period covered by the assessment?: " %(licensee.name, relevantDate.strftime('%d %b %Y')))

    substantialHardshipResidence = bool_input("  %s would only be able to comply with their financial obligations by "
                                              "selling their principal place of residence " % consumer.name)

    if (contract.isCreditCard):
        substantialHardshipCreditCard = bool_input("  %s would be unable to comply with an obligation to repay"
                                                            " $%s within %s days "
                                                            %(consumer.name, contract.creditLimit,
                                                              config.ASIC_160F_131))
        if substantialHardshipCreditCard:
            contract.likelySubstantialHardship = True

    if contract.smallAmountCredit:
        consumer.debtorInDefaultOfOtherSmallAmount = bool_input("  %s was in default as debtor under another small "
                                                                "amount credit contract " %consumer.name)
        consumer.debtorUnder2SmallAmountIn90 = bool_input("  %s was a debtor under 2 or more other "
                                                          "small amount credit contracts between "
                                                          "%s and %s " %(consumer.name,
                                                          (relevantDate -
                                                           timedelta(days=90)).strftime('%d %b %Y'),
                                                          relevantDate.strftime('%d %b %Y')))

    substantialHardshipOther = bool_input("  any other factors indicating that %s would suffer substantial hardship "
                                          "in meeting their financial obligations under the credit contract "
                                          %consumer.name)
    if substantialHardshipOther:
        contract.likelySubstantialHardship = True


    for check in unsuitableChecks:
        unsuitableChecks[check] = bool_input(check)
        if unsuitableChecks[check]:
            contract.isUnsuitable = True

    if substantialHardshipResidence and (not contract.likelySubstantialHardship):
        substantialHardshipResidenceRefute = bool_input("Can it be proven that selling their principal place of "
                                                        "residence to comply with their financial obligations"
                                                        " would not have inflicted "
                                                        "substantial hardship on %s? " %consumer.name)
        if substantialHardshipResidenceRefute == False:
            contract.likelySubstantialHardship = True

    if ((consumer.debtorInDefaultOfOtherSmallAmount or consumer.debtorUnder2SmallAmountIn90) and
            (not contract.likelySubstantialHardship)):
        substantialHardshipDebtorRefute = bool_input("Can it be proven that %s's circumstances as a current small amount"
                                                     " credit contract debtor did not indicate that compliance with "
                                                     "the new credit contract would cause substantial hardship? "
                                                     %consumer.name)
        if substantialHardshipDebtorRefute == False:
            contract.likelySubstantialHardship = True

    if contract.likelySubstantialHardship:
        contract.isUnsuitable = True

    return contract, consumer




