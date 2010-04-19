#!/usr/bin/env python

def main():
    import sys
    sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
    import roxanne
    import glob
    import os.path
    import numpy

    parseFileIn = open('../037-sps06-ls/data/parsed.dat',
                       'r')
    parseDict = roxanne.readDataFileArray(parseFileIn)
    #print parseDict.keys()

    fOut = open('analyzed.data','w')
    fileNameList = glob.glob('../037-sps06-ls/data/separated/*.data')
    outputList = ['fileName',
                  'pulloffAngle',
                  'forceMaxAdhesion',
                  'forceMaxShear',
                  'forcePreload']

    # removed angle pulloff from output list
    sep = '\t'
    headerString = sep.join(outputList)
    fOut.write(headerString)
    fOut.write('\n')

    for dataFileName in fileNameList:

        print 'processing file : ' + dataFileName

        # read in data file
        fileIn = open(dataFileName)
        headerDict = roxanne.getHeader(fileIn)
        dataDict = roxanne.readDataFileArray(fileIn)
        # this dataDict needs to be converted to floats
        for key in dataDict.keys():
            dataDict[key] = map(float, dataDict[key])

        # angle value should be in headerDict
        pulloffAngle = float(headerDict['pulloffAngle'])

        # get indices from the parsed.data file
        # get location of filename in parseDict
        # and pull data from same index in the other arrays
        parsedFileNames = parseDict['dataFileName']
        dataFileNameNoPath = os.path.split(dataFileName)[1]
        #fileNameNoPath = fileNames
        indexFileName = parsedFileNames.index(dataFileNameNoPath)

        indexContact     = parseDict['indexContact'][indexFileName]
        indexPreload     = parseDict['indexMaxPreload'][indexFileName]
        indexMaxAdhesion = parseDict['indexMaxAdhesion'][indexFileName]

        indexContact     = int(indexContact)
        indexPreload     = int(indexPreload)
        indexMaxAdhesion = int(indexMaxAdhesion)

        # pull force values at those indices
        # data will be in dataDict
        normalForceContactMuN = dataDict['forceNormalMicroNewton'][indexContact]
        normalForcePreloadMuN = dataDict['forceNormalMicroNewton'][indexPreload]
        normalForcePulloffMuN = dataDict['forceNormalMicroNewton'][indexMaxAdhesion]

        shearForceContactMuN  = dataDict['forceLateralMicroNewton'][indexContact]
        shearForcePreloadMuN  = dataDict['forceLateralMicroNewton'][indexPreload]
        shearForcePulloffMuN  = dataDict['forceLateralMicroNewton'][indexMaxAdhesion]

        # correct for force at contact
        # adhesion force = maxAdhesion - force at contact
        maxAdhesionMuN = (normalForcePulloffMuN -
                          normalForceContactMuN)
        # shear force = maxShear - force at contact
        maxShearMuN = (shearForcePulloffMuN -
                       shearForceContactMuN)

        # force at preload - force at contact = force of preload
        forcePreload = normalForcePreloadMuN - normalForceContactMuN

        fOut.write(dataFileNameNoPath + '\t')
        fOut.write('% 5.1f\t' % pulloffAngle )
        fOut.write('% 5.3f\t' % maxAdhesionMuN)
        fOut.write('% 5.3f\t' % maxShearMuN)
        fOut.write('% 5.3f\t' % forcePreload)
        fOut.write('\n')

    fOut.close()

if __name__ == '__main__':
    main()
