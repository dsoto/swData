function plotHandle = plotRawForceTrace ( dataFileName, ... 
                                             figureHandle, axesHandle);

% this function plots the raw voltages from a 
% data run of roxanne data
% plot title and filename is same as data file name

% flags to perform analysis and plotting
stdOutput = 0;     % output to command line
doPrintPlot = 1;     % output a pdf plot 

% open data file and strip off headers
fileHandle = fopen(dataFileName,'r');
date = fgetl(fileHandle);


cantilever         = fgetl(fileHandle);
trajectoryFileName = fgetl(fileHandle);
latAmp             = fgetl(fileHandle); 
norAmp             = fgetl(fileHandle);
pitchAngle         = fgetl(fileHandle);
rollAngle          = fgetl(fileHandle);
token              = fgetl(fileHandle);
dataHeaders        = fgetl(fileHandle);

% load data from file into array
dataArray = textscan(fileHandle, '%s %15.7f %15.7f %15.7f %15.7f');
fclose(fileHandle);

lateralVoltage         = -dataArray{1,2};
normalVoltage          =  dataArray{1,3};
positionNormalMicron   =  dataArray{1,4} * 10;
positionLateralMicron  =  dataArray{1,5} * 10;

[pathstr, shortDataFileName, ext, ver] = fileparts(dataFileName);


% assemble plot file name and title from the tokens above
plotFileName = shortDataFileName;
titleString = shortDataFileName;

% plot normal and shear traces 
plot(axesHandle,lateralVoltage,'g');
hold on;
plot(axesHandle,normalVoltage,'b');
hold off;

xlabel(axesHandle, 'Sample');
ylabel(axesHandle, 'Signal Voltage');
legend('Shear','Normal');			
title(titleString,'Interpreter','None');

if (doPrintPlot == 1)
	fprintf('Printing Plot File %s\n',plotFileName);
	formatPlot( figureHandle, axesHandle, 'Times New Roman', 8 );
	printPlot ( figureHandle, plotFileName, 5.0, 3.0);
end

end