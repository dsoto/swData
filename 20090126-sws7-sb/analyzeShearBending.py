#!/usr/bin/env python



def main():
    import sys
    sys.path.append('../roxanne')
    import roxanne
    import glob
    import os.path
    import numpy

    parseFileIn = open('parsed.data','r')
    parseDict = roxanne.readDataFileArray(parseFileIn)
    print parseDict.keys()
    print parseDict
    
    fOut = open('analyzed.data','w')
    fileNameList = glob.glob('./data/*sws*.data')
    outputList = ['fileName',
                  'cantileverDeflection',
                  'stagePreload',
                  'maxPreload',
                  'microwedgeDeflection',
                  'lateralSpringConstant']
    sep = '\t'
    headerString = sep.join(outputList)
    fOut.write(headerString)
    
    for fileName in fileNameList:

        print 'processing file : ' + fileName
        fileIn = open(fileName)
        headerDict = roxanne.readDataFileHeader(fileIn)
        dataDict = roxanne.readDataFileArray(fileIn)

        fullFileName = os.path.abspath(fileName)
        shortFileName = os.path.split(fullFileName)[1]
        #shortFileName = os.path.splitext(shortFileName)[0]

        voltageLateral        =  map(float,dataDict['voltageForceLateral'])
        voltageNormal         =  map(float,dataDict['voltageForceNormal'])
        positionNormalMicron  =  map(float,dataDict['voltagePositionX']) * 10
        positionLateralMicron =  map(float,dataDict['voltagePositionY']) * 10

        voltageLateral        = -numpy.array(voltageLateral)
        voltageNormal         =  numpy.array(voltageNormal)
        positionNormalMicron  =  numpy.array(positionNormalMicron) * 10
        positionLateralMicron =  numpy.array(positionLateralMicron) * 10

        cantileverDict = roxanne.getCantileverData(headerDict['cantilever'])

        normalStiffness      = cantileverDict['normalStiffness']
        lateralStiffness     = cantileverDict['lateralStiffness']
        normalDisplacement   = cantileverDict['normalDisplacement']
        lateralDisplacement  = cantileverDict['lateralDisplacement']
        lateralAmplification = float(headerDict['latAmp'])
        normalAmplification  = float(headerDict['norAmp'])
        rollAngle            = float(headerDict['rollAngle'])
        pitchAngle           = float(headerDict['pitchAngle'])

        defaultAmplification = 100
        lateralDisplacement = (lateralDisplacement * lateralAmplification /
                               defaultAmplification)
        normalDisplacement = (normalDisplacement * normalAmplification /
                              defaultAmplification)

        # use cantilever values to convert voltages to forces
        lateralForceMuN = (voltageLateral *
                           lateralStiffness / lateralDisplacement)
        normalForceMuN  = (voltageNormal * normalStiffness /
                           normalDisplacement)

        # get location of filename in parseDict
        # and pull data from same index in the other arrays
        fileName = os.path.splitext(fileName)
        fileName = fileName[0]
        fileNames = parseDict['dataFileName']
        indexFileName = fileNames.index(shortFileName)

        indexContact     = parseDict['indexContact'][indexFileName]
        indexPreload     = parseDict['indexMaxPreload'][indexFileName]
        indexMaxAdhesion = parseDict['indexMaxAdhesion'][indexFileName]
        
        indexContact = int(indexContact)
        indexPreload = int(indexPreload)
        indexMaxAdhesion = int(indexMaxAdhesion)

        # get forces at contact, preload, pulloff
        normalForceContactMuN = normalForceMuN[indexContact]
        normalForcePreloadMuN = normalForceMuN[indexPreload]
        normalForcePulloffMuN = normalForceMuN[indexMaxAdhesion]

        shearForceContactMuN  = lateralForceMuN[indexContact]
        shearForcePreloadMuN  = lateralForceMuN[indexPreload]
        shearForcePulloffMuN  = lateralForceMuN[indexMaxAdhesion]

        normalCantileverVoltageContact     = voltageNormal[indexContact]
        normalCantileverVoltagePreload     = voltageNormal[indexPreload]
        normalCantileverVoltageMaxAdhesion = voltageNormal[indexMaxAdhesion]

        shearCantileverVoltageContact     = voltageLateral[indexContact]
        shearCantileverVoltagePreload     = voltageLateral[indexPreload]
        shearCantileverVoltageMaxAdhesion = voltageLateral[indexMaxAdhesion]

        normalStagePositionContact     = positionNormalMicron[indexContact]
        normalStagePositionPreload     = positionNormalMicron[indexPreload]
        normalStagePositionMaxAdhesion = positionNormalMicron[indexMaxAdhesion]

        shearStagePositionContact     = positionLateralMicron[indexContact]
        shearStagePositionPreload     = positionLateralMicron[indexPreload]
        shearStagePositionMaxAdhesion = positionLateralMicron[indexMaxAdhesion]



        # calculate preload
        # in the shear bending test, this is from the shear trace
        stagePreload = shearStagePositionPreload - shearStagePositionContact
        
        
        # calculate deflection
        cantileverDeflection = ((shearCantileverVoltagePreload - 
                                 shearCantileverVoltageContact) / 
                                 lateralDisplacement)

        # calculate effective microwedge deflection (effective preload)
        microwedgeDeflection = stagePreload + cantileverDeflection

        # preload force 
        maxPreload = (normalForcePreloadMuN - normalForceContactMuN)
        

        fOut.write(fileName + '\t')
        fOut.write('% 5.1f\t' % cantileverDeflection)
        fOut.write('% 5.3f\t' % stagePreload)
        fOut.write('% 5.3f\t' % maxPreload)
        fOut.write('% 5.3f\t' % microwedgeDeflection)
        fOut.write('% 5.3f\t' % lateralSpringConstant)
        fOut.write('\n')

    fOut.close()

if __name__ == '__main__':
    main()
