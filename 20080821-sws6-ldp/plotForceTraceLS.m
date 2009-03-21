function plot_handle = plotForceTraceLS ( fileName, figureHandle, ... 
                                          axesHandle, logFileHandle );
% this function reads in data
% performs a simple analysis
% outputs logfile entries for data values	
% plots force traces and writes plot file
% function is called by plotAllForceTraceLS.m

% cantilever calibration constants
lateralStiffness = 0.307;   % newtons per meter 
normalStiffness = 0.313;
lateralDisplacement = 0.473; % volts per micron
normalDisplacement = 0.148;

% open data file and strip off headers
fileHandle = fopen(fileName,'r');
date = fgetl(fileHandle);
cantilever         = fgetl(fileHandle);
trajectoryFileName = fgetl(fileHandle);
latAmp             = fgetl(fileHandle);
norAmp             = fgetl(fileHandle);
token              = fgetl(fileHandle);
dataHeaders        = fgetl(fileHandle);

% load data from file into array
dataArray = textscan(fileHandle, '%s %15.7f %15.7f %15.7f %15.7f');
fclose(fileHandle);

data1 = -dataArray{1,2};
data2 = dataArray{1,3};
positionNormalMicron  = dataArray{1,4}*10;
positionLateralMicron  = dataArray{1,5}*10;

% pull out relevant data section
dataStart = 1;
dataEnd = length(data1);
lateralVolt = data1(dataStart:dataEnd); %???
normalVolt = data2(dataStart:dataEnd); %???

% subtract background 
lateralVoltBias = mean(lateralVolt(1:500));
lateralVolt = lateralVolt - lateralVoltBias;
normalVoltBias = mean(normalVolt(1:500));
normalVolt = normalVolt - normalVoltBias;

% use cantilever values to convert voltages to forces
lateralForceMicroNewton = lateralVolt * lateralStiffness / lateralDisplacement;
normalForceMicroNewton = normalVolt * normalStiffness / normalDisplacement;

% find preload and max adhesion and shear values 
% this is a crude way currently but is reasonably accurate
% for the cases i've encountered so far 
[maxPreloadMicroNewton,indexMaxPreload] = max(normalForceMicroNewton);
[maxAdhesionMicroNewton,indexMaxAdhesion] = min(normalForceMicroNewton);

% maxPullIn is max value of attraction during approach 
[maxPullIn, indexMaxPullIn] = ...
	min(normalForceMicroNewton(1:indexMaxPreload));

indexContact = ...
	find(normalForceMicroNewton(indexMaxPullIn:indexMaxPreload)>0,1,'first');
indexContact = indexContact + indexMaxPullIn - 1;

distanceContactMicron = positionNormalMicron(indexContact);
distanceMaxPreload = positionNormalMicron(indexMaxPreload);
deflectionMaxPreload = ...
	normalForceMicroNewton(indexMaxPreload) / normalStiffness;

measuredPreloadMicron = distanceMaxPreload - distanceContactMicron;
measuredCompressionMicron = ...
	distanceMaxPreload - distanceContactMicron - deflectionMaxPreload ;

normalSpringConstant = maxPreloadMicroNewton / measuredCompressionMicron;

[maxShear,indexMaxShear] = max(lateralForceMicroNewton);

% pull out values for preload, drag, and sample name from 
% trajectory filename and data filename
% uses cell arrays so char must be used
% data stored as strings
preloadToken = regexp(trajectoryFileName,'_p(\d*)_','tokens');
preload = char(preloadToken{1,1});
angleToken = regexp(trajectoryFileName,'_a(\d*)','tokens');
angle = char(angleToken{1,1});
sampleToken = regexp(fileName,'_(sws\d*)','tokens');
sample = char(sampleToken{1,1});

% output to logfile 
fprintf(logFileHandle, '% 15s\t',   preload);
fprintf(logFileHandle, '% 15s\t',   angle);
fprintf(logFileHandle, '% 15.3f\t', measuredPreloadMicron);
fprintf(logFileHandle, '% 15.3f\t', measuredCompressionMicron);
fprintf(logFileHandle, '% 15.3f\t', maxPreloadMicroNewton);
fprintf(logFileHandle, '% 15.3f\t', maxAdhesionMicroNewton);
fprintf(logFileHandle, '% 15.3f\t', maxShear);
fprintf(logFileHandle, '% 15.3f\t', normalSpringConstant);
fprintf(logFileHandle, '\n');

% assemble plot file name and title from the tokens above 
plotFileName = sprintf('%s_p%s_a%s_FS',sample,preload,angle);
titleString = sprintf('Limit Surface %s preload %s angle %s FS',... 
											 sample,preload,angle);

% plot normal and shear traces 
plot(axesHandle,lateralForceMicroNewton,'g');
hold on;
plot(axesHandle,normalForceMicroNewton,'b');

% plot maximum points 
plot(indexMaxShear,maxShear,'ko');

plot(indexMaxPreload,maxPreloadMicroNewton,'ko');
plotString = sprintf('Max Preload position = %3.3f',positionNormalMicron(indexMaxPreload));
text(indexMaxPreload,maxPreloadMicroNewton,plotString);

plot(indexMaxAdhesion,maxAdhesionMicroNewton,'ko');
plot(indexMaxPullIn,maxPullIn,'ko');

plot(indexContact,normalForceMicroNewton(indexContact),'ko');
plotString = sprintf('Initial Contact Position = %3.3f',...
                     positionNormalMicron(indexContact));
text(indexContact,normalForceMicroNewton(indexContact),plotString);

hold off;

xlabel(axesHandle, 'Time (ms)');
ylabel(axesHandle, 'Force (microNewtons)');
legend('Shear','Normal');			
title(titleString);

formatPlot( figureHandle, axesHandle, 'Times New Roman', 24 );
printPlot(figureHandle, plotFileName, 11.0, 8.5);

