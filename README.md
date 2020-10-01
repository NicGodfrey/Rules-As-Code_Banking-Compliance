# Digitising Chapter III of the NCCP Act 2009 (Cth)

This repository attempts to convert selected provisions of the [National Consumer Credit Protection Act 2009 (Cth)](https://www.legislation.gov.au/Details/C2020C00215) ("the Act") as in force at 23 June 2020.

## Quick Installation (Run as an executable)

Clone or download the repository as a ZIP. Navigate to 'dist\Evaluation.exe and run.

## Installation (Run as a python application)
Clone or download the repository as above. 
In a virtual environment, ensure all dependencies are installed. At current, the only package not native to python is [tribool](https://pypi.org/project/tribool/). This can be installed through [pip](https://pip.pypa.io/en/stable/):

```bash
pip install tribool
```
Run Evaluation.py.

## File Overview
**Definition.py** defines legal concepts and entities according to the relevant law.\
**Evaluation.py** contains the main() function of the application.\
**Functions.py** contains other functions relevant for the operation of the application.\
**NCCPA.py** contains relevant provisions of the Act broken into individual functions.\
**Results.py** currently contains only the 'Uncertainties' list which defines missing facts. Future updates will likely see the civilUnits and criminalUnits lists moved here to avoid any need to pass them as arguments into each function.\
**Unit_Testing.py** contains tests with various facts as inputs.\
**config.py** contains various variables accessed throughout all other files.


## License
TODO

## Project Status
This is a work in progress.