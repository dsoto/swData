#!/usr/bin/env python

# plotting script that expects a header line with labels for 
# each column of data
# these columns of data will be assigned to a dictionary
# returned values are all strings



def readIndexFile(fileName):
	fileIn = open(fileName,'r')
	
	tempLine = fileIn.readline()
	tempLine = tempLine.rstrip()
	headers = tempLine.split('\t')
	
	numColumns = len(headers)
	
	columnList = []
	for i in range(numColumns):
		columnList.append([])
	
	tempData = fileIn.readlines()

	# loop through data and append arrays
	for line in tempData:
		line=line.replace('\n','')
		value=line.split('\t')
		for i in range(numColumns):
			columnList[i].append(value[i])

	columnDict = {}
	for i in range(numColumns):
		columnDict[headers[i]] = columnList[i]
	
	# tidy up and return values
	fileIn.close()
	return columnDict

def main():
	fileName = 'test.data'
	columnDict = readIndexFile(fileName)
	
	angleSlant = columnDict['angle']
	shearForce = columnDict['maxShear']
	normalForce = columnDict['maxAdhesion']
	
	import matplotlib.pyplot
	
	matplotlib.pyplot.plot(angleSlant,shearForce,'gd')
	matplotlib.pyplot.plot(angleSlant,normalForce,'bo')
	matplotlib.pyplot.xlabel('Goniometer Reading (deg)')
	matplotlib.pyplot.ylabel('Max Adhesion (microNewtons)')
	matplotlib.pyplot.title('sws10 - 529b02 - slant')
	matplotlib.pyplot.savefig('mplSlantTest.pdf',transparent=True)
	matplotlib.pyplot.show()

# TODO : format plot with fonts and size

if __name__ == '__main__':
	main()


