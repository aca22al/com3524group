# Dimensions: 2

# --- Set up executable path, do not edit ---

import sys
import inspect
import random
import datetime

import numpy as np

# NEW 
import os

this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

# ---

from capyle.ca import Grid2D, Neighbourhood, randomise2d
import capyle.utils as utils
   
ResultsPath = main_dir_loc + "results"

# NEW
ParametersPath = main_dir_loc


CHAPARRAL = 0
LAKE = 1
FOREST = 2
CANYON_SCRUBLAND = 3
TOWN_BLACK = 4
FIRST_FLAME_YELLOW = 5
MEDIUM_FLAME_ORANGE = 6
HIGH_FLAME_BRIGHT_RED = 7
GREY_BRUNT_OUT = 8

timeTrack = np.zeros((200, 200))
timestep = 0
reached_town = False
Task_Name = ""

# change the wind direction.
windDirectionALL = ["north","south","east","west","northeast","northwest","southeast","southwest"]
# Below value is used for first time run. Subsequently it is read from param file (TaskName_param.txt).
windDirection = windDirectionALL[1]

#change values to change wind effect on spread, towards and against
fromWProb = 2.5
OppWProb = 0.3

# ******  VITAL INFORMATION *******

# power generating plant that is situated approximately 45km to the north of TOWN
# waste incinerator - approximately 60km north-east of the TOWN

# chaparral -   catch fire quite easily, each square km can burn for a period of several DAYS
# canyon -  ignites very easily, each square km burns for a period of several HOURS 
# Dense forest - don’t ignite very easily -  each km square can burn for up to ONE MONTH.


def setup(args):
    """Set up the config object used to interact with the GUI"""
    config_path = args[0]


    config = utils.load(config_path)
    # -- THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED --
    config.title = "Task2_WindDirection"
    config.dimensions = 2

    global Task_Name
    Task_Name = config.title
   
    
    config.states = (CHAPARRAL, LAKE, FOREST, CANYON_SCRUBLAND, TOWN_BLACK, FIRST_FLAME_YELLOW
                     , MEDIUM_FLAME_ORANGE, HIGH_FLAME_BRIGHT_RED, GREY_BRUNT_OUT)
    
    config.wrap = False

    config.state_colors = [
        (0.6, 0.6, 0), # 0 Chaparral
        (0.2, 0.6, 1), # 1 lake
        (0.1, 0.2, 0),# 2 Dense forest
        (1, 1, 0), # 3 canyon with high flamable srcubland
        (0, 0, 0), # 4 town (black)
        (1, 0.9, 0.2), # 5 LOW first flame bright yellow
        (1.0, 0.33, 0.0), #6 MEDIUM orange flame 
        (0.7, 0, 0.1), #7 HIGH bright red burning
        (0.4, 0.4, 0.4) # 8 Brunt out/ dark gray
        ] 
    
    global geneNum
    config.num_generations = 1000
    geneNum = config.num_generations
    # countNum = 0
    
    # The given region is of size 50 kms by 50 Kms
    # 1 km = 4 cells (50 X 4 = 200) i,e each cell is equal to .25 km 
    config.grid_dims = (200, 200)
    global gridray
    gridray = np.zeros((200, 200))
    # ----------------------------------------------------------------------

#all chaparal (0), done when creating a np.zeros array  

    # for y in range(0, 200):
    #     for x in range(0, 200):
    #         gridray[y][x] = 2#
    
    for y in range(30,40):
        for x in range(0, 40):
            gridray[y][x] = FOREST 

    for y in range(30,160):
        for x in range(40,80):
            gridray[y][x] = FOREST
    
    for y in range(60,80):
        for x in range(120,170):
            gridray[y][x] = FOREST

    for y in range(160,170):
        for x in range(60,120):
            gridray[y][x] = LAKE
    
    for y in range(110,160):
        for x in range(170,180):
            gridray[y][x] = LAKE

    for y in range(90,100):
        for x in range(100,170):
            gridray[y][x] = CANYON_SCRUBLAND  

    for y in range(135,145):
        for x in range(95,105):
            gridray[y][x] = TOWN_BLACK 


    #ONLY Start fire at incinerator :
    for i in range(0, 20):
        x = random.randint(195, 199)
        y = random.randint(0, 5)
        gridray[y][x] = FIRST_FLAME_YELLOW
    
    # # Start fire at power plant here:
    # for i in range(0, 20):
    #     x = random.randint(15, 25)
    #     y = random.randint(55, 65)
    #     gridray[y][x] = FIRST_FLAME_YELLOW
    

    # NEW
    # Load task parameters - Wind Direction
    # from file Task2_WindDirection_Param.txt   OR
    # set the windDirection variable value in the begining of this code file
    readTaskParameters(Task_Name)


    # the GUI calls this to pass the user defined config
    # into the main system with an extra argument
    # do not change

    config.set_initial_grid(gridray)

    if len(args) == 2:
        config.save()
        sys.exit()

    return config



def transition_function(grid, neighbourstates, neighbourcounts):
 
    """Function to apply the transition rules
    and return the new grid"""
    # YOUR CODE HERE

    randomNumber = np.random.rand(200, 200)
    toBurn = generateProbability(grid, neighbourstates, neighbourcounts[FIRST_FLAME_YELLOW]) > randomNumber

    burning = (grid == FIRST_FLAME_YELLOW) | (grid == MEDIUM_FLAME_ORANGE) |(
               grid == HIGH_FLAME_BRIGHT_RED) | (grid == GREY_BRUNT_OUT)

    itemindex = np.where(burning == True)
    timeTrack[itemindex] += 1

#FIRST_FLAME_YELLOW -> MEDIUM_FLAME_ORANGE -> HIGH_FLAME_BRIGHT_RED -> GREY_BRUNT_OUT

# chaparral -   catch fire quite easily, each square km can burn for a period of several DAYS
# canyon -  ignites very easily, each square km burns for a period of several HOURS 
# Dense forest - don’t ignite very easily -  each km square can burn for up to ONE MONTH.    
#from 0 to [0] yellow flame -> [1] value is orange flame -> [2] value is red flame -> [3] is gray brunt out
    # Fuel Time is 1 hour = 1 Time step 
    # i.e For Forest 30 days * 24 hrs = 720 hrs, for Chaparal 4 days * 24 hrs = 96 hrs
    #  for canyon 6 hours

# NCB Check the split in time again
    CANYON_SCRUBLAND_FUEL_TIME = [2,4,6]
    CHAPARAL_FUEL_TIME = [25,60,96]
    FOREST_FUEL_TIME = [75,250,720]
    # same as Chaparal because in and around first fire is Chaparal, get rid of inital flames REDO 
    FIRST_FLAME_YELLOW_FUEL_TIME = [25,60,96]

    # gridray is the original/initial with states
    
    changeToMediumFlame = ((timeTrack == CANYON_SCRUBLAND_FUEL_TIME[0]) & (gridray == CANYON_SCRUBLAND)) |(
                (timeTrack == CHAPARAL_FUEL_TIME[0]) & (gridray == CHAPARRAL)) | (
                (timeTrack == FOREST_FUEL_TIME[0]) & (gridray == FOREST)) | (
                (timeTrack == FIRST_FLAME_YELLOW_FUEL_TIME[0]) & (gridray == FIRST_FLAME_YELLOW))  

    changeToHighFlame = ((timeTrack == CANYON_SCRUBLAND_FUEL_TIME[1]) & (gridray == CANYON_SCRUBLAND)) |(
                (timeTrack == CHAPARAL_FUEL_TIME[1]) & (gridray == CHAPARRAL)) | (
                (timeTrack == FOREST_FUEL_TIME[1]) & (gridray == FOREST)) | (
                (timeTrack == FIRST_FLAME_YELLOW_FUEL_TIME[1]) & (gridray == FIRST_FLAME_YELLOW))  

    burntOut = ((timeTrack == CANYON_SCRUBLAND_FUEL_TIME[2]) & (gridray == CANYON_SCRUBLAND)) |(
                (timeTrack == CHAPARAL_FUEL_TIME[2]) & (gridray == CHAPARRAL)) | (
                (timeTrack == FOREST_FUEL_TIME[2]) & (gridray == FOREST)) | (
                (timeTrack == FIRST_FLAME_YELLOW_FUEL_TIME[2]) & (gridray == FIRST_FLAME_YELLOW)) 
                     

    grid[toBurn] = FIRST_FLAME_YELLOW
    grid[changeToMediumFlame] = MEDIUM_FLAME_ORANGE
    grid[changeToHighFlame] = HIGH_FLAME_BRIGHT_RED
    grid[burntOut] = GREY_BRUNT_OUT


    global timestep
    timestep += 1
    global reached_town
    if (reached_town == False) & ((grid == TOWN_BLACK) & (neighbourcounts[FIRST_FLAME_YELLOW] >= 1)).any():
    #    printResultToFile("Task1", timestep)
       printResultToFile(Task_Name, timestep)  
       print("** Wind Direction = " + windDirection + " , The fire reached the town at: " + str(timestep) + " hours")
       reached_town = True
   
    return grid


# the function of generate the probability of firing and change different wind directions,

def generateProbability(grid, neighbourstates, burningNeighbourCount):

    # chaparral -   catch fire quite easily, each square km can burn for a period of several DAYS
    # canyon -  ignites very easily, each square km burns for a period of several HOURS 
    # Dense forest - don’t ignite very easily -  each km square can burn for up to ONE MONTH.
        
    # flammability parameter is set based on catch fire 
    flammability_FOREST = 0.03
    flammability_CHAPARAL = 0.15
    flammability_CANYON_SCRUBLAND = 0.5

# probability multiplies based on burningNeighbourCount (how many neighbouring cells are on fire (yellow))
    probability_Chaparal = np.where(grid == CHAPARRAL, flammability_CHAPARAL * burningNeighbourCount, 0)
    probability_Forest = np.where(grid == FOREST, flammability_FOREST * burningNeighbourCount, 0)
    probability_Canyon = np.where(grid == CANYON_SCRUBLAND, flammability_CANYON_SCRUBLAND * burningNeighbourCount, 0)   
    probability_all = probability_Chaparal + probability_Forest + probability_Canyon 
    
    # Return the NW N NE, W self E, SW S SE neighbourgrids
    # unpack the state arrays
    #initializes cell's neighbours (8 directions)
    NW, N, NE, W, E, SW, S, SE = neighbourstates

    # current cell, ignites faster if its north cell is on fire by x2, 
    # ignites slower if its south cell is on fire by 0.5x,

    if windDirection == "north":
        prob_WD = np.where((N == FIRST_FLAME_YELLOW), probability_all * fromWProb, probability_all)
        prob_WD = np.where((S == FIRST_FLAME_YELLOW), prob_WD * OppWProb, prob_WD)
            
    elif windDirection == "south":
        prob_WD = np.where((S == FIRST_FLAME_YELLOW), probability_all * fromWProb, probability_all)
        prob_WD = np.where((N == FIRST_FLAME_YELLOW), prob_WD * OppWProb, prob_WD)

    elif windDirection == "east":
        prob_WD = np.where((E == FIRST_FLAME_YELLOW), probability_all * fromWProb, probability_all)
        prob_WD = np.where((W == FIRST_FLAME_YELLOW), prob_WD * OppWProb, prob_WD)

    elif windDirection == "west":
        prob_WD = np.where((W == FIRST_FLAME_YELLOW), probability_all * fromWProb, probability_all)
        prob_WD = np.where((E == FIRST_FLAME_YELLOW), prob_WD * OppWProb, prob_WD)

    elif windDirection == "northwest":
        prob_WD = np.where((NW == FIRST_FLAME_YELLOW), probability_all * fromWProb, probability_all)
        prob_WD = np.where((SE == FIRST_FLAME_YELLOW), prob_WD * OppWProb, prob_WD)

    elif windDirection == "northeast":
        prob_WD = np.where((NE == FIRST_FLAME_YELLOW), probability_all * fromWProb, probability_all)
        prob_WD = np.where((SW == FIRST_FLAME_YELLOW), prob_WD * OppWProb, prob_WD)

    elif windDirection == "southwest":
        prob_WD = np.where((SW == FIRST_FLAME_YELLOW), probability_all * fromWProb, probability_all)
        prob_WD = np.where((NE == FIRST_FLAME_YELLOW), prob_WD * OppWProb, prob_WD)

    elif windDirection == "southeast":
        prob_WD = np.where((SE == FIRST_FLAME_YELLOW), probability_all * fromWProb, probability_all)
        prob_WD = np.where((NW == FIRST_FLAME_YELLOW), prob_WD * OppWProb, prob_WD)

    else:
        prob_WD = probability_all

    return prob_WD


def readTaskParameters(Task_Name):
    
    if os.path.isfile(ParametersPath + "/" + Task_Name + "_Param.txt"): 

        f = open(ParametersPath + "/" + Task_Name + "_Param.txt", "r") 
        params = f.readline().split('=')
  
        if params[0] != "":
            if int(params[1]) >= 0 and int(params[1]) <= 7:
                global windDirection
                windDirection = windDirectionALL[int(params[1])]
                # print( windDirection)
        f.close()
    else:
        f = open(ParametersPath + "/" + Task_Name + "_Param.txt", "a") 
        f.writelines("windDirection=1")
        f.close()



def printResultToFile(task, timestep):

    # NEW
    if not os.path.exists(ResultsPath): 
      
        # if the demo_folder directory is not present  
        # then create it. 
        print ( "Results folder does not exists - Created")
        os.makedirs(ResultsPath) 
        
    # else :
    #     print ( "Results folder exists")

    f = open(ResultsPath + "/" + task + "results.txt", "a") 

    current_time = datetime.datetime.now()
    text = "*** Simulation Run at - " + str(current_time) + "\n" + "Wind Direction = " + windDirection + \
           "\n" + " The fire reached the town at : " + str(timestep) + " hours" + "\n"
    f.writelines(text)
    f.close()


def main():
    """ Main function that sets up, runs and saves CA"""
    # Get the config object from set up
    config = setup(sys.argv[1:])

    grid = Grid2D(config, transition_function)


    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # Save updated config to file
    config.save()
    # Save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()

