# CAPyLE
CAPyLE is a cross-platform teaching tool designed and built as part of a final year computer science project. It aims to aid the teaching of cellular automata and how they can be used to model natural systems.

It is written completely in python with minimal dependencies.

![CAPyLE Screenshot on macOS](http://pjworsley.github.io/capyle/sample.png)

## Installation
The installation guide can be found on the [CAPyLE webpages](http://pjworsley.github.io/capyle/installationguide.html)

## Usage
Detailed usage can be found on the [CAPyLE webpages](http://pjworsley.github.io/capyle/).

See below for a quickstart guide:

1. `git clone https://github.com/pjworsley/capyle.git [target-directory]`
2. `cd [target-directory]`
3. Execute main.py either by:
    * `run.bat` / `run.sh`
    * `python main.py`
2. Use the menu bar to select File -> Open. This will open in the folder `./ca_descriptions`.
3. Open one of the example files;
  
   - `task1_relativeTime.py`    For Task1 - Relative Time
      "The Result will be stored under "Results" Folder under Main project directory
      "File name will be TasktitleName.
      "The input parameter "fireStartAt" can be in param file "Task1_RelativeTime_Param.txt"
      "fireStartAt=I, for Fire at Incinator or fireStartAt=P for Fire at Power plant. The default value will be P in the code.


   - `task2_windDirection.py`    For Task2 - Relative Time when changing wind direction
      "The Result will be stored inside "Results" Folder under Main project directory
      "File name will be TasktitleName.
      "The input parameter "windDirection" can be set in param file "task2_windDirection_Param.txt"
      "All possible values windDirectionALL = ["north","south","east","west","northeast","northwest","southeast","southwest"]
      "windDirection=0 is for north, windDirection=1 is for south and so on.. The default value will be "north" in the code.      

   - `task3_ShortTerm.py`    For Task3 - Short Term  - Water Drop
      "The Result will be stored inside "Results" Folder under Main project directory
      "File name will be TasktitleName.
      "windDirection" can be set in  task3_ShortTerm_Param.txt". Refer to Task2 instruction above

    - `task4_LongTerm.py`    For Task4 - Long Term Solution
      "The Result will be stored inside "Results" Folder under Main project directory
      "File name will be TasktitleName.
      "windDirection" can be set in  task4_LongTerm_Param.txt". Refer to Task2 instruction above


4. The main GUI elements will now load, feel free to customise the CA parameters on the left hand panel
5. Run the CA with your parameters by clicking the bottom left button 'Apply configuration & run CA'
6. The progress bar will appear as the CA is run
7. After the CA has been run, use the playback controls at the top and the slider at the bottom to run through the simulation.
8. You may save an image of the currently displayed output using the 'Take screenshot' button

## Acknowledgements
Special thanks to [Dr Dawn Walker](http://staffwww.dcs.shef.ac.uk/people/D.Walker/) for proposing and supervising this project.

Also thanks to the COM2005 2016/2017 cohort for being the guinea-pigs!

## Licence
CAPyLE is licensed under a BSD licence, the terms of which can be found in the LICENCE file.

Copyright 2017 Peter Worsley
