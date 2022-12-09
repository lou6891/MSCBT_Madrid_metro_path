
def Exercise(startStation , endStation):
    import extraFunctions
    
    print("\n")
    print("This program returns you a possible journey, from ", startStation, "to " , endStation)
    print("This journey probably not going to be efficient, if you value your time use Google Maps")
    print("\n")


    try:
        # Array to be reutnred by the function
        returnArr = []

        #Get all the stations from all files
        stations = extraFunctions.OpenAllFiles()
        
        
        # loop though the stations to find the one we are starting from and the one we are ending in 
        # with relative line numbers

        startStationLines = []
        endStationLines = []

        for line in range(1,13):
            for station in stations[line]:
                if(station == startStation):
                    startStationLines.append(line)
                if(station == endStation):
                    endStationLines.append(line)
        
        # Checks that the imput is correct, if the previus loop produced len(startStationLines) or len(endStationLines) 
        # it means the input was not in the cvs files
        if (not startStationLines or not endStationLines) :
            print("The input stations are not in the cvs, please check them!")
            return False;
                
        
        # Chekc if both stations are on the same line use the stations in that line
        sameLine = False;
        
        for startLine in startStationLines:
            for endLine in endStationLines:
                if(startLine == endLine):
                    sameLine = startLine
                    break;
        
        # If they share a line the code just goes though the stations in the line
    
        if(sameLine):
            #Also check if the start station is before the ending station in the ist, 
            # if not we need to loop in the other way around
            returnArr = extraFunctions.GetSameLineReturnArray( 0,startStation, endStation, stations[sameLine])                

        
        elif(not sameLine):

            networkNodes = extraFunctions.findNetworkNodes(stations)

            # 1 find a node that has both lines
            # Not Found? 
            # Find a common line in the nodes

            startingNodes = {}
            endingNodes = {}
            
            for statName, linesArr in networkNodes.items():
                for s in startStationLines:
                    if (s in linesArr):
                        startingNodes[statName] = linesArr
                
                for s in endStationLines:
                    if (s in linesArr):
                        endingNodes[statName] = linesArr

            sharedNode = False
            # 1. Look if they share a node
            for startNode in startingNodes:
                for endNode in endingNodes:
                    if(startNode == endNode) :
                        sharedNode = startNode
            

            if (not sharedNode):

            
                # If sharedNode is still False
                # 2 Check if some nodes share line
                # To do so fist we get the lines connected to the nodes found for stating and ending station
                startStationNodeLines = list(startingNodes.values())
                startStationNodeLines = set([val for sublist in startStationNodeLines for val in sublist])
                
                endStationNodeLines = list(endingNodes.values())
                endStationNodeLines = set([val for sublist in endStationNodeLines for val in sublist])

                # Compare the two sets for common lines
                sharedLines = startStationNodeLines.intersection(endStationNodeLines)


                if len(sharedLines) == 0:
                    middleNode = None
                    # if there are no shared lines in the curret nodes, 
                    # add a line that has a common node betweeen one of the lines of the starting and ending station
                    # since I wasn't able to find a case where there are more than 3 lines to switch I'll stop here
                    
                    for sNodeLines in startStationNodeLines:
                        for eNodeLines in endStationNodeLines:
                            for key,nodeArr in networkNodes.items():
                                if sNodeLines in nodeArr and eNodeLines in nodeArr: 
                                    middleNode = {key : nodeArr}
                                    break;
                
                    # CHeck that the middle station was found, if not no route id available at the moment
                    #if it's different than none it means we din't find any middle none thus the stations cannot be connected
                    
                    if middleNode != None and len(middleNode) == 1:
                        print("if middleNode != None and len(middleNode) == 1")
                        # If a middle node was found  it means we need to 
                        # go though that node to connect the stations
                        # get the keys for each
    

                        # to select the node of the starting and ending line we need to check
                        # that node shares the line with the middle node
                        # This is done for the case in which there are multiple nodes in the starting or ending line

                        # Journey
                        # start to node start
                        # node start to middle node
                        # middle node to end node
                        # end node to end
                        returnArr = []
                        startingNode = None # a node that shares line with the middle node
                        endingNode = None # a nonde that shares line with the middle node
                        middleNodeKey =  next((x for x in middleNode.keys()))

                        for key, lines in startingNodes.items():
                            for line in lines:
                                if line in list(middleNode.values())[0]:
                                    startingNode =[key , lines]
                        
                        for key, lines in endingNodes.items():
                            for line in lines:
                                if line in list(middleNode.values())[0]:
                                    endingNode = [key , lines]
                        

                        # This is the part that returns the startions for each part of the journey
                        returnArr = returnArr + extraFunctions.GetSameLineReturnArrayWrapped("single", startStationLines, startStation, startingNode[0], stations)
                        returnArr = returnArr + extraFunctions.GetSameLineReturnArrayWrapped("single", startingNode[1], startingNode[0], middleNodeKey, stations)[1:]
                        returnArr = returnArr + extraFunctions.GetSameLineReturnArrayWrapped("double", middleNode.items(), middleNodeKey, endingNode[0], stations)[1:]
                        returnArr = returnArr + extraFunctions.GetSameLineReturnArrayWrapped("single", endingNode[1], endingNode[0], endStation, stations)[1:]
                        
                        
                    elif len(middleNode) > 1:
                        print("___ Something went wrong ___")
                        print("Debugging variable middlenode", middleNode)
                        return False

                    
                    else:
                        # End the function with no solution
                        print("No route was found")
                        return False
                
                elif len(sharedLines) > 0:  

                    # The two lines of the two selected stations have some nodes with that share a line, so there we need to switch line twice
                    # starting from the startingNodes find the first node station that is the closest
                    # and  has a shared line with the ending station
                    
                    # THe flow is going from start station to a node that has the shared line
                    # We find also the node in the ending line
                    # THen we have the beginning and ending for the middle line

                    # 1 find the node station in the starting line that can connect to the shared line 
                    # (if there are multiple shared line just take one we re not interested in speed)
                    firstPartJourneyStations , secondPartJourneyStations, ThirdPartJourneyStations = None, None, None
                    sharedLineTester = list(sharedLines)[0]

                    endStationStartingLine = None

                    for key, lines in startingNodes.items():
                        if  sharedLineTester in lines:
                            endStationStartingLine = key

                    # 2. Do the same of 1 but for the end station
                    endStationEndLine = None
                    for key, lines in endingNodes.items():
                        if sharedLineTester in lines:
                            endStationEndLine = key

                    # Fist stations between start and node
                    firstPartJourneyStations = extraFunctions.GetSameLineReturnArrayWrapped("single", startStationLines, startStation, endStationStartingLine, stations)
                    
                    # Now find the stations between the two nodes endStationStartingLine and endStationEndLine
                    secondPartJourneyStations = extraFunctions.GetSameLineReturnArray(0,endStationStartingLine, endStationEndLine, stations[sharedLineTester])[1:]
                    
                    # same for the ending station
                    ThirdPartJourneyStations = extraFunctions.GetSameLineReturnArrayWrapped("single", endStationNodeLines, endStationEndLine , endStation, stations)[1:]


                    #put all together in the right order
                    returnArr = firstPartJourneyStations + secondPartJourneyStations + ThirdPartJourneyStations

                # Debuggind stuff
                #print("------------")
                #print("startingNodes", startingNodes)
                #print("endingNodes", endingNodes)
                #print("startStationNodeLines ",startStationNodeLines)
                #print("endStationNodeLines ", endStationNodeLines)
                #print("sharedLines ", sharedLines)
                #print("------------")

            
            else:

                returnArr = []
                # From the starting station to shared node, and from shared node to the ending station
                # 1. Since the startStationLines can be more than 1 we need to check for each one to find the sharedNode
                # 2. This process is done twice since we can travel in both ways up or down the metro
                returnArr = returnArr + extraFunctions.GetSameLineReturnArrayWrapped("single", startStationLines, startStation, sharedNode, stations)
                
                # Now we do the same thing but from the shared node to the end station
                returnArr = returnArr + extraFunctions.GetSameLineReturnArrayWrapped("single", endStationLines, sharedNode, endStation, stations)[1:]
            
        
        # Debuggind stuff
        #print("returnArr: ",returnArr)
        #print("startStationLines: ", startStationLines)
        #print("endStationLines: ",endStationLines)
        #print("startStation", startStation)
        #print("endStation", endStation)
        print("The journey is: \n")
        print(returnArr)
        print("\n")

        return returnArr
    
    except (TypeError, ValueError) as error: 
        print("There was an error, retry if the error persist contact an admin")
        print(error)
        return False

   

def main():
    import extraFunctions
    
    Exercise("Pitis", "Las Suertes")
    
    # Tests the Exercise to see if for n number of random metro station 
    # the program is able to find a path
    # Change this variable to change the number of tests
    simulationNumber = 500
    extraFunctions.ExerciseTester(simulationNumber)


    # Examples of destinations, try them on reverse as well!
    # WARNING THE ROUTE MIGHT NOT BE THE FASTEST WE ADVIDE TO USE GOOGLE MAPS IF YOU ARE NOT DEPRESSED, 
    # IF YOU ARE DEPRESSED TRY OUR ROUTE WHILE LISTENING TO JOYLESS (BAND NOT SPONSORED)
    # stations on different lines with common station in between
    #  -> Exercise("Gran Vía", "Gregorio Marañón") or  Exercise("Cuatro Vientos", "Barajas")
    # station on same line:
    #  ->  Exercise("Gran Vía", "Bambú") and reversed Exercise( "Bambú", "Gran Vía",)
    # stations not sharing any node:
    #  -> #Exercise(  "La Peseta", "Parque Oeste")
    # No route was found 
    #  -> #Exercise(  "La", "Parque Oeste") or Exercise( "Parque Oeste",  "La")


if __name__ == "__main__":
    main()