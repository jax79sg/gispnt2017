Usage:
python Main.py
OR
python Main.py gui=true polyfile=testdata/testPoly.csv testpt=0,0 testptfile=testdata/testPoints.csv

gui=true or false   -determines which mode to run. Default is True
polyfile=testPoly.csv   -the file path to the polygon file. Optional (Program will request for it if missing)
testptfile=testPoints.csv -the file path to the test point file. Optional (Program will request user to enter points)
testpt=1,1|2,2|3,3  -Set of additional points to test. Optional (Program will request for it if no points loaded)



NOTABLE FEATURES
- Command line mode (CMD) and GUI mode (Graphical User Interface)
- Loading of polygon file (x,y)
- Loading of test point file (x,y)
- Manual entry of test points, will be appended to the test point file’s points
- In-screen display of PIP results (GUI mode only)
- Display PIP results graphically. (Red- OUTSIDE, GREEN- INSIDE, BLACK- BOUNDARY)
- Display PIP results textually.
- Error checking to avoid crashes.
- arguments on program start



If you encounter problems running this program, please try to run this on Desktop@UCL's ArgGIS's python installation. Its tested there. 
("c:\Program Files (x86)\ArcGIS\Python27\ArcGIS10.3\python.exe" Main.py)


Common problems.
1. Syntax errors running the program
- You may be running Python 3.
- This is written in Python 2.7. Thus, it is NOT compatible with Python 3.

2. Some error to do with importing TKagg.
- This is common on OSX or MacOS python 2.x installations
- Resolution is to install python 2.7.12 using Brew and making that the default Python installation.
- brew install python -universal - framework

3. Python crashes on start
- Make sure nothing is changed to the import codes, this is critical.
- If problem exists, try running on another python setup.

Python Software Foundation Documentation
- Most of the coding were learned from there.