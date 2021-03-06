%function plotHandle = shearBendingAnalysis ( dataFileName, figureHandle, ... 
%                                          axesHandle);
function plotHandle = shearBendingAnalysis ( fileName, figureHandle, ... 
                                          axesHandle, logFileHandle );

% open data file and strip off headers
fileHandle = fopen(dataFileName,'r');
date = fgetl(fileHandle);
cantilever         = fgetl(fileHandle);
trajectoryFileName = fgetl(fileHandle);
latAmp             = fgetl(fileHandle); 
norAmp             = fgetl(fileHandle);
token              = fgetl(fileHandle);
dataHeaders        = fgetl(fileHandle);

% extract parameters from headers
% uses cell arrays so char must be used
% data stored as strings
xToken = regexp(trajectoryFileName,'_x(\d*)_','tokens');
x = char(xToken{1,1});

yToken = regexp(trajectoryFileName,'_y(\d*)','tokens');
y = char(yToken{1,1});

velocityToken = regexp(trajectoryFileName,'_v(\d*)','tokens');
velocity = char(velocityToken{1,1});

sampleToken = regexp(dataFileName,'_(sws\d*)','tokens');
sample = char(sampleToken{1,1});

token = regexp(latAmp,'(\d*)','tokens');
lateralAmplification = char(token{1,1});
lateralAmplification = str2num(lateralAmplification);

token = regexp(norAmp,'(\d*)','tokens');
normalAmplification = char(token{1,1});
normalAmplification = str2num(normalAmplification);

% cantilever calibration constants
lateralStiffness = 0.307;   % newtons per meter 
normalStiffness = 0.313;

% displacement is in actual piezo voltage per micron 
defaultAmplification = 100;
lateralDisplacement = 0.473 / defaultAmplification;
normalDisplacement = 0.148 / defaultAmplification;

% now displacement is corrected for gain setting on box 
lateralDisplacement = lateralDisplacement * lateralAmplification;
normalDisplacement = normalDisplacement * normalAmplification;

% load data from file into array
dataArray = textscan(fileHandle, '%s %15.7f %15.7f %15.7f %15.7f');
fclose(fileHandle);

lateralVoltage         = -dataArray{1,2};
normalVoltage          =  dataArray{1,3};
positionNormalMicron   =  dataArray{1,4} * 10;
positionLateralMicron  =  dataArray{1,5} * 10;

% pull out relevant data section
% as written this is redundant but 
% this section can be adjusted easily to look at 
% a subset of the data
dataStart = 1;
dataEnd = length(lateralVoltage);
lateralVoltage = lateralVoltage(dataStart:dataEnd); %???
normalVoltage = normalVoltage(dataStart:dataEnd); %???

% subtract background 
lateralVoltageBias = mean(lateralVoltage(1:500));
lateralVoltage = lateralVoltage - lateralVoltageBias;
normalVoltageBias = mean(normalVoltage(1:500));
normalVoltage = normalVoltage - normalVoltageBias;

% use cantilever values to convert voltages to forces
lateralForceMicroNewton = ... 
	lateralVoltage * lateralStiffness / lateralDisplacement;
normalForceMicroNewton = ... 
	normalVoltage * normalStiffness / normalDisplacement;

% want to find contact point
% find min, this is pulloff
[maxPulloffMicroNewton,indexMaxPulloff] = min(lateralForceMicroNewton);

% backup, find max, this is preload
[maxPreloadMicroNewton,indexMaxPreload] = ...
	max(lateralForceMicroNewton(1:indexMaxPulloff));
	
% backup, find min, this is pullin
[maxPullInMicroNewton,indexMaxPullIn] = ...
	min(lateralForceMicroNewton(1:indexMaxPreload));
	
% find zero, this is contact point
indexContact = ...
	find(lateralForceMicroNewton(indexMaxPullIn:indexMaxPreload)>0,1,'first');
indexContact = indexContact + indexMaxPullIn - 1;

% calculate distance stage traveled between initial contact
% and maximum preload force 
distanceContactMicron = positionLateralMicron(indexContact);
distanceMaxPreload = positionLateralMicron(indexMaxPreload);
measuredPreloadMicron = distanceMaxPreload - distanceContactMicron;

% calculate deflection of cantilever
cantileverDeflectionMicron = ...
	lateralForceMicroNewton(indexMaxPreload) / lateralStiffness;

% calculate deflection of microwedge
microwedgeDeflectionMicron = measuredPreloadMicron - cantileverDeflectionMicron;

% calculate spring constant 
lateralSpringConstant = maxPreloadMicroNewton / microwedgeDeflectionMicron;

% assemble plot file name and title from the tokens above 
plotFileName = sprintf('sb_x%s_y%s_v%s_a%3.0f', ...
	x,y,velocity,lateralAmplification);
titleString = plotFileName;


% plot normal and shear traces 
plot(axesHandle,lateralForceMicroNewton,'g');
hold on;
plot(axesHandle,normalForceMicroNewton,'b');

% plot maximum points 
plot(indexMaxPulloff,maxPulloffMicroNewton,'ko');
plot(indexMaxPullIn,maxPullInMicroNewton,'ko');
plot(indexMaxPreload,maxPreloadMicroNewton,'ko');
plot(indexContact,lateralForceMicroNewton(indexContact),'ko');

% annotate graph with max preload position
plotString = sprintf('Max Preload position = %3.3f', ...
	positionLateralMicron(indexMaxPreload));
textLabel = text(indexMaxPreload + 50, maxPreloadMicroNewton, plotString);
set(textLabel,'FontName','Times New Roman');

% annotate graph with contact position
plotString = sprintf('Initial Contact Position = %3.3f', ...
	positionNormalMicron(indexContact));
textLabel = text(indexContact + 50, ...
	lateralForceMicroNewton(indexContact), plotString);
set(textLabel,'FontName','Times New Roman');

xLimits = get(gca,'XLim');
yLimits = get(gca,'YLim');
location = [0.5 0.2];
xCoordinate = (xLimits(2) - xLimits(1)) * location(1) + xLimits(1); 
yCoordinate = (yLimits(2) - yLimits(1)) * location(2) + yLimits(1); 

% annotate graph with calculated spring constant 
plotString = sprintf('Spring Constant = %3.3f', ...
	lateralSpringConstant);
textLabel = text(xCoordinate,yCoordinate,plotString);
set(textLabel,'FontName','Times New Roman');


% add code to create normalized plot coordinates for text placement
% get range of plot
% plot coord = (max - min) normalized coord + min 


hold off;

xlabel(axesHandle, 'Time (ms)');
ylabel(axesHandle, 'Force (microNewtons)');
legend('Shear','Normal');			
title(titleString,'Interpreter','None');

formatPlot( figureHandle, axesHandle, 'Times New Roman', 8 );
printPlot ( figureHandle, plotFileName, 5.0, 3.0);