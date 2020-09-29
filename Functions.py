from tribool import Tribool
import config

def bool_input(string):
    preConversionInput = input(string)
    if (preConversionInput == "") or (preConversionInput == "?"):
        preConversionInput = None
    try:
        convertedAnswer = Tribool(bool(int(preConversionInput)))
    except TypeError:
        convertedAnswer = Tribool(preConversionInput)
    except ValueError:
        try:
            convertedAnswer = Tribool(preConversionInput)
        except:
            print("Warning: Response was unclear. Answer has been marked as 'Unknown'.")
            convertedAnswer = Tribool()
    finally:
        convertedAnswerVal = convertedAnswer.value
        if config.unitTesting:
            print("\t" * 10 + str(convertedAnswer))
        return convertedAnswerVal

def imprisonment2PenaltyUnits(months):
    #This function relies on a non-formalist approach which considers
    # the Explanatory Memorandum, Crimes Legislation Amendment Bill 1987 (Cth) 11
    penaltyUnits = months*5 #Crimes Act 1914 s4B(2)-(3)
    return penaltyUnits
