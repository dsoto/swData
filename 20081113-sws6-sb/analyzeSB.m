function plotHandle = analyzeSB ( dataFileName, logFileHandle, ... 
                                             figureHandle, axesHandle);
% this file calculates the shear compliance spring constant
% of a single wedge tested on the dual cantilever instrument

% flag to perform analysis
analyze = 1;
stdOutput = 0;

% open data file and strip off headers
fileHandle = fopen(dataFileName,'r');
date = fgetl(fileHandle);
cantilever         = fgetl(fileHandle);
trajectoryFileName = fgetl(fileHandle);
latAmp             = fgetl(fileHandle); 
norAmp             = fgetl(fileHandle);
% deal with blank line
fgetl(fileHandle);
token              = fgetl(fileHandle);
dataHeaders        = fgetl(fileHandle);

% call function to get cantilever parameters
[normalStiffness, lateralStiffness, ...
 normalDisplacement, lateralDisplacement] = ...
 getCantileverData(cantilever);

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

% now displacement is corrected for gain setting on box 
defaultAmplification = 100;
lateralDisplacement = lateralDisplacement * lateralAmplification / ...
                      defaultAmplification;
normalDisplacement = normalDisplacement * normalAmplification / ...
                     defaultAmplification;

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

spikeFactor = 3;
lateralVoltage = filterSpikes(lateralVoltage, spikeFactor);
normalVoltage = filterSpikes(normalVoltage, spikeFactor);


% subtract background
% currently there is 100 samples quiet
% FIXME : need to automate this
endTare = 100;
lateralVoltageBias = mean(lateralVoltage(1:endTare));
lateralVoltage = lateralVoltage - lateralVoltageBias;
normalVoltageBias = mean(normalVoltage(1:endTare));
normalVoltage = normalVoltage - normalVoltageBias;

% use cantilever values to convert voltages to forces
lateralForceMicroNewton = ... 
	lateralVoltage * lateralStiffness / lateralDisplacement;
normalForceMicroNewton = ... 
	normalVoltage * normalStiffness / normalDisplacement;

noiseFloorLateral = std ( lateralForceMicroNewton(1:endTare) );


if (analyze)
	% find max, this is preload
	[maxPreloadMicroNewton,indexMaxPreload] = ...
		max(lateralForceMicroNewton);
	
	% to find contact point, using a minumum does not work
	% in the shear bending case
  % [lateralForceAtContactMicroNewton, indexContact] = ...
	%	      min(lateralForceMicroNewton(1:indexMaxPreload));
	% i will instead use a threshold to find the point
	% using find >threshold ...
	
	threshold = 5.0 * noiseFloorLateral;
	indexStartSearch = 1;
	indexEndSearch = length ( lateralForceMicroNewton );
	indexContact = find (lateralForceMicroNewton ...
	  (indexStartSearch:indexEndSearch) > threshold, 1, 'first');
	indexContact = indexContact + indexStartSearch - 1;
  lateralForceAtContactMicroNewton = lateralForceMicroNewton(indexContact);
		
	% preload force is difference between these two
	totalPreloadForceMicroNewton = ... 
		maxPreloadMicroNewton - lateralForceAtContactMicroNewton;

	% calculate distance stage traveled between initial contact
	% and maximum preload force 
	positionContactMicron = positionLateralMicron(indexContact);
	positionPreloadMicron = positionLateralMicron(indexMaxPreload);
	stagePreloadMicron = positionPreloadMicron - positionContactMicron;
	
	% find zero of cantilever deflection voltage
	% this zero is the voltage of cantilever at contact
	cantileverContactDeflectionMicron = ...
		lateralForceMicroNewton(indexContact) / lateralStiffness;

	% calculate deflection of cantilever at max preload
	cantileverPreloadDeflectionMicron = ...
		lateralForceMicroNewton(indexMaxPreload) / lateralStiffness;
	
	cantileverDeflectionMicron = cantileverPreloadDeflectionMicron - cantileverContactDeflectionMicron;
	
	% calculate deflection of microwedge
	microwedgeDeflectionMicron = stagePreloadMicron - cantileverDeflectionMicron;
	
	% calculate spring constant 
	lateralSpringConstant = ... 
		totalPreloadForceMicroNewton / microwedgeDeflectionMicron;
	
	% output to stdout
	if (stdOutput)
		fprintf('Force at preload = %3.3f\n',maxPreloadMicroNewton);
		fprintf('Force at contact = %3.3f\n',lateralForceAtContactMicroNewton);
		fprintf('Cant Deflection at preload = %3.3f\n', ...
			cantileverPreloadDeflectionMicron);
		fprintf('Cant Deflection at contact = %3.3f\n', ...
			cantileverContactDeflectionMicron);
		fprintf('Stage position at preload = %3.3f\n',positionPreloadMicron);	fprintf('Stage position at contact = %3.3f\n',positionContactMicron);
		fprintf('Cantilever Deflection = %3.3f\n',cantileverDeflectionMicron);
		fprintf('Stage Preload = %3.3f\n',stagePreloadMicron);
		fprintf('Total Preload Force = %3.3f\n',totalPreloadForceMicroNewton);
		fprintf('Microwedge Deflection = %3.3f\n',microwedgeDeflectionMicron);
		fprintf('Spring Constant = %3.3f\n',lateralSpringConstant);
	end

	% output to log file
	fprintf(logFileHandle, '% 15s\t',   sample);
	fprintf(logFileHandle, '% 15s\t',   cantilever);
	fprintf(logFileHandle, '% 15.3f\t', cantileverDeflectionMicron);
	fprintf(logFileHandle, '% 15.3f\t', stagePreloadMicron);
	fprintf(logFileHandle, '% 15.3f\t', totalPreloadForceMicroNewton);
	fprintf(logFileHandle, '% 15.3f\t', microwedgeDeflectionMicron);
	fprintf(logFileHandle, '% 15.3f\t', lateralSpringConstant);
	fprintf(logFileHandle, '\n');
	
end

% assemble plot file name and title from the tokens above 
plotFileName = sprintf('sb_x%s_y%s_v%s',x,y,velocity);
titleString = plotFileName;


% plot normal and shear traces 
plot(axesHandle,lateralForceMicroNewton,'g');
hold on;
plot(axesHandle,normalForceMicroNewton,'b');

if (analyze) 
	% plot maximum points 
	plot(indexMaxPreload,maxPreloadMicroNewton,'ko');
	plot(indexContact,lateralForceMicroNewton(indexContact),'ko');
	
	% annotate graph with max preload position
	plotString = sprintf('Max Preload position');
	textLabel = text(indexMaxPreload + 50, maxPreloadMicroNewton, plotString);
	set(textLabel,'FontName','Times New Roman');
	
	% annotate graph with contact position
	plotString = sprintf('Initial Contact Position');
	textLabel = text(indexContact + 50, ...
		lateralForceMicroNewton(indexContact), plotString);
	set(textLabel,'FontName','Times New Roman');
	
	xLimits = get(gca,'XLim');
	yLimits = get(gca,'YLim');
	location = [0.5 0.2];
	xCoordinate = (xLimits(2) - xLimits(1)) * location(1) + xLimits(1); 
	yCoordinate = (yLimits(2) - yLimits(1)) * location(2) + yLimits(1); 
	
	
	% annotate graph with calculated spring constant 
	plotString = sprintf('Lateral Spring Constant = %3.3f', ...
		lateralSpringConstant);
	textLabel = text(xCoordinate,yCoordinate,plotString);
	set(textLabel,'FontName','Times New Roman');
end

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