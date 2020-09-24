from tribool import Tribool

def bool_input(string):
    preConversionInput = input(string)
    if preConversionInput == "":
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
        print("\t" * 10 + str(convertedAnswer))
        return convertedAnswerVal