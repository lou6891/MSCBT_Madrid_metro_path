

def OpenAllFiles():
    '''
    This function reads all the files and returns a dictionary containing : 
    The number of the line and an array with all its stations
    How the function return the values
    {
        1 : [all stations of file 1],
        2 : [all stations of file 2],
        3 : [all stations of file 3],
        ...
        12 : [all stations of file 12],

    }

    TO USE IT.
    In the function of your exercise:
    
    import extraFunctions
    -> (THis imports the functions in the file additional functions, to be placed below the main of your exercise)
    
    variable to be ranemend = extraFunctions.OpenAllFiles() 
    -> (this creates a avariable that is equal to the value returned by openAllFiles)

    '''

    try:
    
        stationsMapDictionary = {}

        for line in range(1,13):
            stationsMapDictionary[line] = []
        
            with open(f"./data/linea-{line}.csv", "r", encoding="utf-8", newline="") as file:
                
                for station in file:
                    stationsMapDictionary[line].append(station.strip())
        
        return stationsMapDictionary
    
    except FileNotFoundError as error:
        print("Check that you are cd into the right folder")
        return False

    
def GetSameLineReturnArray(counter, startStation, endStation, stationsArray):
    #OLD THE RETURN ARRY WAS A VAR IN THE CALLING
    '''
    This program return an list containing the stations that a person must go though
    for going from station A to B given a specific line.
    IT also takes into account the reverse order

    Output:
    list = [A, alpha, beta , gamma, B]
    '''    

    returnArr = []
    firstStationFound = False

    for station in stationsArray:
        # First find the starting station and append it
        if(station == startStation and firstStationFound == False):
            firstStationFound =  True
            returnArr.append(station)
        
        # if we found the first station, and this is not the ending station
        # add the station tot he return array
        if (firstStationFound and station != endStation and station != startStation):
            returnArr.append(station)
        # When we find the ending station add it to the return array and exit the loop
        if(endStation == station and firstStationFound):
            returnArr.append(station)
            break
        # If we find the ending station but the firstStationFound == False, 
        # it means that the guy is going in the opposite direction compared to how the list is ordered
        if(firstStationFound== False and station == endStation): 
            returnArr.append(station)
            break
        

    # checka that the end station is actually in the reuslts
    if ((endStation not in returnArr) or (startStation not in returnArr)):
        returnArr = []
    
    #if the returnArr length is 0 it means we have to go in the reverse direction!
    # the couter is to avoid infinite loops 
    # (it fires the function one, adds to the counter and then fires again for the last time)
    if((len(returnArr) < 1 and counter == 0) ):
        counter = counter + 1
        returnArr = GetSameLineReturnArray( counter ,startStation,endStation, reversed(stationsArray))
        return returnArr
    else:
        return returnArr

    #print("returnArr: ",returnArr)

    
def GetSameLineReturnArrayWrapped ( loopType ,stationLines, start, end, stations):
    '''
    THis function does the same thing of the non-wrapped version,
    the only difference is that it also loops thought the lines for each station node
    to find a possible path

    As before returns an array
    '''

    if loopType == "single":
        
        for line in stationLines:
            # We do this initial loop because we are working with object that might have leght bigger than 1,
            # or might be nodes thsu having multiple lines in the same stations
            # Since we are unsure about the line we are looping though a set containing  probable lines
            # For each line in the stationLines ( a set of line given to the function)
            # Call the fucntion with the start and end station and fromthe cvs the stations on the line
            returnArr = GetSameLineReturnArray(0 , start, end  , stations[line])
            
            # If returnArr len is >1 it menas that there wa a match between the lines and the stations and that we have 
            # found a path between the start and end thus we can return the array
            if len(returnArr) > 0:
                return returnArr

    elif loopType == "double":
        # This does the same thing as before however, since we are working with a dictionary here there is a second loop
        # To loop all the keys and lines in the dictionary
        for keys,lines in stationLines:
                for line in lines:
                    returnArr = GetSameLineReturnArray(0, keys, end, stations[line])
                    if len(returnArr) > 0:
                        return returnArr

    return False




def findNetworkNodes(stationsMapDictionary):
    
    '''
    This fucntion retuns all the nodes in the network
    It needs the stationsMapDictionary created before to run
    the retun is like:
    {
        "station name" : [lines that are in that station]
        "station name" : [lines that are in that station]
        ...
    }
    '''

    #First create a temporary dictionary 
    # that will contain station name -> line number
    tempNodesDict = {}

    # Second create a set where we will store all the stations name, 
    # so that we have a list with all the sattions names without duplicates
    stationSet = set()
    
    #Loop though the the dictionary with each line and relative stations to add them to the set
    for i in stationsMapDictionary:
        stationSet.update(stationsMapDictionary[i])

    # Loop though the set
    for i in stationSet:
        # For each station create a itme in the dictionary
        tempNodesDict[i] = []
        #Loop though the stations in the dictionary with stations and lines
        for line,stations in stationsMapDictionary.items():
            # If we find a station in a given line,
            #  add the line number to an array stored under the dictionary name 
            for statName in stations:
                if(i == statName):
                    tempNodesDict[i].append(line)
            
    # Now we just need to clean the nodes dictionary 
    # to avoid having stations that are in only one line
    # This way we return only the nodes in the network
    # We do this by removing the stations that have a array length less than 2.
    nodesDict = dict(tempNodesDict)
    for x,y in tempNodesDict.items():
        if(len(y) < 2): nodesDict.pop(x)

    #print(nodesDict)
    return nodesDict


def ExerciseTester(simulationNumber):

    '''
    This fucntion has been built to test the exercise fucntion
    It creates an array with all the stations
    then selects two random variables and calls Exercise

    It does in loop for as many times as the user wants

    Output:
    The number of times an error occured (exercise returned false)
    and the % out of the total number of iterations
    '''

    import main
    import random

    try:
        
        

        stationsDict = OpenAllFiles()
        stations = []
        errorNumber = 0
        

        # create array from the dict of stations for the random station seleciton
        for key,stationArr in stationsDict.items():
            stations = stations + stationArr
        
        for i in range (0, simulationNumber):
            start = stations[random.randint(0, len(stations)) -1]
            end = stations[random.randint(0, len(stations)) -1]
            result  = main.Exercise(start, end)
            if(not result) : 
                print("ERRROR WITH STATIONS ", "Start ",start, "End ",end)
                errorNumber += 1
        
        print("-------------------")
        print("Error Number ", errorNumber)
        print("Error % ",errorNumber/simulationNumber * 100 )
    
    except Exception as error:
        print("Something went wrong")
        print(error)


    
