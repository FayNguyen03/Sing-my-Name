import pandas as pd
import string
#1
def findName(name, outputFile):

  allNames = pd.read_csv("allNames.csv", sep = '\t') #Convert the csv file into data frame
  colNames = ["name","artist","song","year"] #A list of the columns 
  findNamesInfo = allNames[colNames] #Select the subset of columns "name", "artist", "song", "year"
  findNamesInfo.drop_duplicates() #Delete the duplicate
  findNamesInfo.to_csv(outputFile,index = False) #Convert the dataframe to csv file
  

#2
def findRepeatedNameSongs(threshold, outputFile):
  
  allNames = pd.read_csv("allNames.csv", sep = '\t') #Convert the csv file into data frame
  colNames = ["name","artist","song"]
  repeatedNameSongs = allNames[colNames] #Get a subset
  repeatedNameSongs = repeatedNameSongs.groupby(colNames).size().reset_index(name='times') # Count the occurences of the names in songs
  colNames.append("times")
  repeatedNameSongs = repeatedNameSongs.loc[repeatedNameSongs["times"] >= threshold, colNames] # Check the condition
  repeatedNameSongs = repeatedNameSongs.sort_values("times",ascending = False) #Sort the value into the decreasing order
  repeatedNameSongs.to_csv(outputFile,index = False) #Convert the dataframe to csv file

#3
def findUniqueNameSongs(threshold, outputFile):
  
  allNames = pd.read_csv("allNames.csv", sep = '\t') #Convert the csv file into data frame
  colNames = ["name","artist","song"]
  colNames1 = ["artist","song"]
  uniqueNameSongs = allNames[colNames] #Get a subset
  uniqueNameSongs = pd.DataFrame({'count' : uniqueNameSongs.groupby(colNames).size()}).reset_index() #Create a new data frame
  uniqueNameSongs = uniqueNameSongs.groupby(colNames1).size().reset_index(name='number') #Count the number of distinct names in songs
  colNames1.append("number")
  uniqueNameSongs = uniqueNameSongs.loc[uniqueNameSongs["number"] >= threshold,colNames1] # Check the condition
  uniqueNameSongs = uniqueNameSongs.sort_values("number",ascending = False) #Sort the value into the decreasing order
  uniqueNameSongs.to_csv(outputFile,index = False) #Convert the dataframe to csv file
  

#4
def countNameDecades(name, outputFile):
  allNames = pd.read_csv("allNames.csv", sep = "\t") # Convert the csv fie into data frame
  allNames["decade"] = allNames["year"] // 10 * 10 # Create a new column with the decade
  colNames = ["name","decade"]
  nameDecades = allNames.loc[allNames["name"] == name,  colNames]
  nameDecades = nameDecades.groupby("decade").size().reset_index(name = "count") # Count the number of name in each decade
  nameDecades["decade"] = nameDecades["decade"].astype("int") #Convert the value in column decade into integer
  nameDecades.to_csv(outputFile, index = False) #Convert the dataframe to csv file
  
#5 

def countStartLetter(outputFile):
  
  onlyNames = pd.read_csv("onlyNames.csv", sep = "\t")  # Convert the csv file into data frame
  allNames = pd.read_csv("allNames.csv", sep = "\t") # Convert the csv fie into data frame

  onlyNames = onlyNames.loc[onlyNames["count"] >= 5000,["name","count"]] # Filter the data set 
  onlyNames["firstLetter"] = onlyNames["name"].str.get(0)#create a new column with the value as the first letter in the name
  letterInfo = onlyNames.groupby(by = "firstLetter").size().reset_index(name = "number")
  sum1 = letterInfo['number'].sum() # Calculate the sum of the occurrences of all first letters
  letterInfo['proportion'] = letterInfo['number'] / sum1 # Create a new column with the proportion of each first letter
  del letterInfo["number"]
  #letterInfo.to_csv(outputFile,index = False)
  
  allNames["firstLetter"] = allNames["name"].str.get(0) # Create a new column with the value as the first letter in the name
  colNames = ["name","firstLetter"]
  allNames = allNames[colNames]
  allNames = allNames.groupby(colNames).size().reset_index(name='number') # Drop the duplicates
  del allNames["number"]
  letterInfo2 = allNames.groupby("firstLetter").size().reset_index(name='count') #Count the occurrence of each first letter
  sum2 = letterInfo2['count'].sum() # Count the sum of occurrence of all letters

  letterInfo2['proportion'] = letterInfo2['count'] / sum2 # Calculate the propotion
  del letterInfo2["count"]

  if (len(letterInfo2["firstLetter"]) >= len(letterInfo["firstLetter"])): # Check which dataframe has more rows of letters
    dir = "left"
  else:
    dir = "right"
    
  result = pd.merge(letterInfo2,letterInfo,how = dir, on = "firstLetter") # Create a new dataframe merged from two dataframes
  result = result.fillna(0) # fill NA with 0
  result["difProportion"] = round(result["proportion_x"] - result["proportion_y"],4) # Create a new column of difference in proportions
  result[["firstLetter","difProportion"]].to_csv(outputFile,index = False)



def countEndLetter(outputFile):
  
  onlyNames = pd.read_csv("onlyNames.csv", sep = "\t")  # Convert the csv fie into data frame
  allNames = pd.read_csv("allNames.csv", sep = "\t") # Convert the csv fie into data frame

  onlyNames = onlyNames.loc[onlyNames["count"] >= 5000,["name","count"]] # Filter the data set 
  onlyNames["lastLetter"] = onlyNames["name"].str.get(-1)#create a new column with the value as the last letter in the name
  letterInfo = onlyNames.groupby(by = "lastLetter").size().reset_index(name = "number")
  sum1 = letterInfo['number'].sum() # Calculate the sum of the occurrences of all last letters
  letterInfo['proportion'] = letterInfo['number'] / sum1 # Create a new column with the proportion of each last letter
  del letterInfo["number"]
  #letterInfo.to_csv(outputFile,index = False)
  
  allNames["lastLetter"] = allNames["name"].str.get(-1) # Create a new column with the value as the last letter in the name
  colNames = ["name","lastLetter"]
  allNames = allNames[colNames]
  allNames = allNames.groupby(colNames).size().reset_index(name='number') # Drop the duplicates
  del allNames["number"]
  letterInfo2 = allNames.groupby("lastLetter").size().reset_index(name='count') #Count the occurrence of each last letter
  sum2 = letterInfo2['count'].sum() # Count the sum of occurrence of all letters

  letterInfo2['proportion'] = letterInfo2['count'] / sum2 # Calculate the propotion
  #letterInfo2.to_csv(outputFile,index = False)
  del letterInfo2["count"]

  if (len(letterInfo2["lastLetter"]) >= len(letterInfo["lastLetter"])): # Check which dataframe has more rows of letters
    dir = "left"
  else:
    dir = "right"
    
  result = pd.merge(letterInfo2,letterInfo,how = dir, on = "lastLetter") # Create a new dataframe merged from two dataframes
  result = result.fillna(0) # fill NA with 0
  result["difProportion"] = round(result["proportion_x"] - result["proportion_y"],4) # Create a new column of difference in proportions
  result[["lastLetter","difProportion"]].to_csv(outputFile,index = False)

  
def main():
  
  #popular names
  findName("Jack", "tests/jack.csv")
  findName("Mary", "tests/mary.csv")
  findName("Peter", "tests/peter.csv")
  #Repeated name songs
  findRepeatedNameSongs(55,"tests/repeat.55.csv")
  findRepeatedNameSongs(40,"tests/repeat.40.csv")
  findRepeatedNameSongs(30,"tests/repeat.30.csv")
  findRepeatedNameSongs(20,"tests/repeat.20.csv")
  #Timeless names
  countNameDecades("Abby", "tests/abby.decades.csv")
  countNameDecades("Mary", "tests/mary.decades.csv")
  countNameDecades("Joe", "tests/joe.decades.csv")
  #Unique names
  findUniqueNameSongs(25, "tests/unique.25.csv")
  findUniqueNameSongs(20, "tests/unique.20.csv")
  findUniqueNameSongs(15, "tests/unique.15.csv")
  #Lettering
  countStartLetter("tests/names.start.csv")
  print(countEndLetter("tests/names.end.csv"))

if __name__ == "__main__":
  main()
  