function plotHandle = analysisNC ( dataFileName, logFileHandle, ...
                                   figureHandle, axesHandle);
% this file calculates the normal compliance spring constant
% of a single wedge tested on the dual cantilever instrument

% flag to perform analysis
analyze = 1;
stdOutput = 0;
doPrintPlot = 0;

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

% need to extract only file name from trajectory file name
% since the file string is on a PC this is all fucked 
% search for PC path separator
index = strfind(trajectoryFileName,'\');
% get last one
index = index(length(index));
% rest of string is the actual filename
trajectoryFileName = trajectoryFileName(index+1:length(trajectoryFileName));

% get short filenames
[pathstr, shortTrajectoryFileName, ext, ver] = fileparts(trajectoryFileName);
[pathstr, shortDataFileName, ext, ver] = fileparts(dataFileName);

% call function to get cantilever parameters
[normalStiffness, lateralStiffness, ...
 normalDisplacement, lateralDisplacement] = ...
 getCantileverData(cantilever);

% extract parameters from headers
% uses cell arrays so char must be used
% data stored as strings
xToken = regexp(trajectoryFileName,'_x(\d*)_','tokens');
x = char(xToken{1,1});

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

token = regexp(pitchAngle,'(\d*)','tokens');
pitchAngle = char(token{1,1});
pitchAngle = str2num(pitchAngle);

token = regexp(rollAngle,'(\d*)','tokens');
rollAngle = char(token{1,1});
rollAngle = str2num(rollAngle);

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

% subtract background
% currently there is 100 samples quiet
% FIXME : need to automate this
lateralVoltageBias = mean(lateralVoltage(1:100));
lateralVoltage = lateralVoltage - lateralVoltageBias;
normalVoltageBias = mean(normalVoltage(1:100));
normalVoltage = normalVoltage - normalVoltageBias;

% use cantilever values to convert voltages to forces
lateralForceMicroNewton = ... 
	lateralVoltage * lateralStiffness / lateralDisplacement;
normalForceMicroNewton = ... 
	normalVoltage * normalStiffness / normalDisplacement;

if (analyze)
	% find max, this is preload
	[maxPreloadMicroNewton,indexMaxPreload] = ...
		max(normalForceMicroNewton);
	
	% backup, find min, this is contact point
	[normalForceAtContactMicroNewton, indexContact] = ...
		min(normalForceMicroNewton(1:indexMaxPreload));
	
	% preload force is difference between these two
	totalPreloadForceMicroNewton = ... 
		maxPreloadMicroNewton - normalForceAtContactMicroNewton;

	% calculate distance stage traveled between initial contact
	% and maximum preload force 
	positionContactMicron = positionNormalMicron(indexContact);
	positionPreloadMicron = positionNormalMicron(indexMaxPreload);
	stagePreloadMicron = positionPreloadMicron - positionContactMicron;
	
	% find zero of cantilever deflection voltage
	% this zero is the voltage of cantilever at contact
	cantileverContactDeflectionMicron = ...
		normalForceMicroNewton(indexContact) / normalStiffness;

	% calculate deflection of cantilever at max preload
	cantileverPreloadDeflectionMicron = ...
		normalForceMicroNewton(indexMaxPreload) / normalStiffness;
	
	cantileverDeflectionMicron = cantileverPreloadDeflectionMicron - cantileverContactDeflectionMicron;
	
	% calculate deflection of microwedge
	microwedgeDeflectionMicron = stagePreloadMicron - cantileverDeflectionMicron;
	
	% calculate spring constant 
	normalSpringConstant = ... 
		totalPreloadForceMicroNewton / microwedgeDeflectionMicron;
	
	% output to stdout
	if (stdOutput)
		fprintf('Force at preload = %3.3f\n',maxPreloadMicroNewton);
		fprintf('Force at contact = %3.3f\n',normalForceAtContactMicroNewton);
		fprintf('Cant Deflection at preload = %3.3f\n', ...
			cantileverPreloadDeflectionMicron);
		fprintf('Cant Deflection at contact = %3.3f\n', ...
			cantileverContactDeflectionMicron);
		fprintf('Stage position at preload = %3.3f\n',positionPreloadMicron);	fprintf('Stage position at contact = %3.3f\n',positionContactMicron);
		fprintf('Cantilever Deflection = %3.3f\n',cantileverDeflectionMicron);
		fprintf('Stage Preload = %3.3f\n',stagePreloadMicron);
		fprintf('Total Preload Force = %3.3f\n',totalPreloadForceMicroNewton);
		fprintf('Microwedge Deflection = %3.3f\n',microwedgeDeflectionMicron);
		fprintf('Spring Constant = %3.3f\n',normalSpringConstant);
	end

	% output to log file
	fprintf(logFileHandle, '% 20s\t',   shortDataFileName);
	fprintf(logFileHandle, '% 20s\t',   shortTrajectoryFileName);
	fprintf(logFileHandle, '% 15s\t',   sample);
	fprintf(logFileHandle, '% 15s\t',   cantilever);
	fprintf(logFileHandle, '% 15.3f\t', cantileverDeflectionMicron);
	fprintf(logFileHandle, '% 15.3f\t', stagePreloadMicron);
	fprintf(logFileHandle, '% 15.3f\t', totalPreloadForceMicroNewton);
	fprintf(logFileHandle, '% 15.3f\t', microwedgeDeflectionMicron);
	fprintf(logFileHandle, '% 15.3f\t', normalSpringConstant);
	fprintf(logFileHandle, '% 15.3d\t', rollAngle);
	fprintf(logFileHandle, '% 15.3d\t', pitchAngle);
	fprintf(logFileHandle, '\n');
	
end
	
% assemble plot file name and title from the tokens above 
plotFileName = sprintf('sb_x%s_v%s_p%03d_r%03d', ... 
	x,velocity,pitchAngle, rollAngle);
titleString = plotFileName;	

% plot normal and shear traces 
plot(axesHandle,lateralForceMicroNewton,'g');
hold on;
plot(axesHandle,normalForceMicroNewton,'b');

if (analyze) 
	% plot maximum points 
	plot(indexMaxPreload,maxPreloadMicroNewton,'ko');
	plot(indexContact,normalForceMicroNewton(indexContact),'ko');
	
	% annotate graph with max preload position
	plotString = sprintf('Max Preload position = %3.3f', ...
		positionLateralMicron(indexMaxPreload));
	textLabel = text(indexMaxPreload + 50, maxPreloadMicroNewton, plotString);
	set(textLabel,'FontName','Times New Roman');
	
	% annotate graph with contact position
	plotString = sprintf('Initial Contact Position = %3.3f', ...
		positionNormalMicron(indexContact));
	textLabel = text(indexContact + 50, ...
		normalForceMicroNewton(indexContact), plotString);
	set(textLabel,'FontName','Times New Roman');
	
	xLimits = get(gca,'XLim');
	yLimits = get(gca,'YLim');
	location = [0.5 0.2];
	xCoordinate = (xLimits(2) - xLimits(1)) * location(1) + xLimits(1); 
	yCoordinate = (yLimits(2) - yLimits(1)) * location(2) + yLimits(1); 
	
	
	% annotate graph with calculated spring constant 
	plotString = sprintf('Spring Constant = %3.3f', ...
		normalSpringConstant);
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

if (doPrintPlot == 1)
	formatPlot( figureHandle, axesHandle, 'Times New Roman', 8 );
	printPlot ( figureHandle, plotFileName, 5.0, 3.0);
end