import os
import filecmp
from dateutil.relativedelta import *
from datetime import date


def getData(file):
# get a list of dictionary objects from the file
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys are from the first row in the data. and the values are each of the other rows
	data = []

	file_data = open(file,'r')
	header_line = file_data.readline()
	line = file_data.readline()
	while line:
		line_dict = {}
		for col in range(len(header_line.strip().split(','))):
			line_dict[header_line.strip().split(',')[col]] = line.strip().split(',')[col]
		data.append(line_dict)
		line = file_data.readline()
	file_data.close()
	return data

def mySort(data,col):
# Sort based on key/column
#Input: list of dictionaries and col (key) to sort on
#Output: Return the first item in the sorted list as a string of just: firstName lastName
	sorted_data = sorted(data, key = lambda line: line[col])
	return(sorted_data[0]['First']+' '+sorted_data[0]['Last'])


def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
	numFreshman = 0
	numSophmores = 0
	numJuniors = 0
	numSeniors = 0

	for line in data:
		classType = line['Class']
		if classType == 'Freshman':
			numFreshman += 1
		elif classType == 'Sophomore':
			numSophmores += 1
		elif classType == 'Junior':
			numJuniors += 1
		elif classType == 'Senior':
			numSeniors += 1
	result = sorted([('Freshman',numFreshman),('Sophomore',numSophmores),('Junior',numJuniors),('Senior',numSeniors)], key=lambda x:x[1], reverse=True)
	return result


def findMonth(a):
# Find the most common birth month form this data
# Input: list of dictionaries
# Output: Return the month (1-12) that had the most births in the data
	monthFreq = {}
	for line in a:
		bDayMonth = int(line['DOB'].split('/')[0])
		if bDayMonth in monthFreq:
			monthFreq[bDayMonth] += 1
		else:
			monthFreq[bDayMonth] = 1
	return sorted(monthFreq.keys(), key=lambda x: monthFreq[x], reverse=True)[0]

def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as fist,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written
	sorted_data = sorted(a, key = lambda line: line[col])
	file = open(fileName,'w')
	for line in sorted_data:
		file.write(line['First']+','+line['Last']+','+line['Email']+'\n')
	file.close()

def findAge(a):
# def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.
	ageSum = 0

	for line in a:
		ageSum += 2018 - int(line['DOB'].split('/')[2])
	return round(ageSum/len(a))


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()