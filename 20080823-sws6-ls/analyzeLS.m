function plotHandle = analyzeLS ( dataFileName, logFileHandle, ... 
                                             figureHandle, axesHandle);
% this function analyzes data from a limit surface
% test of a single wedge structure
% outputs logfile entries of data values

% flags to perform analysis and plotting
analyze = 1;
stdOutput = 0;
filterSpikes = 0;

% open data file and strip off headers
fileHandle = fopen(dataFileName,'r');
date = fgetl(fileHandle);
cantilever         = fgetl(fileHandle);
trajectoryFileName = fgetl(fileHandle);
latAmp             = fgetl(fileHandle); 
norAmp             = fgetl(fileHandle);
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

% extract parameters from headers
% uses cell arrays so char must be used
% data stored as strings
angleToken = regexp(trajectoryFileName,'_a(\d*)','tokens');
angle = char(angleToken{1,1});

sampleToken = regexp(dataFileName,'_(sws\d*)','tokens');
sample = char(sampleToken{1,1});

velocityToken = regexp(trajectoryFileName,'_v(\d*)','tokens');
velocity = char(velocityToken{1,1});

preloadToken = regexp(trajectoryFileName,'_p(\d*)','tokens');
preload = char(preloadToken{1,1});

token = regexp(latAmp,'(\d*)','tokens');
lateralAmplification = char(token{1,1});
lateralAmplification = str2num(lateralAmplification);

token = regexp(norAmp,'(\d*)','tokens');
normalAmplification = char(token{1,1});
normalAmplification = str2num(normalAmplification);

% call function to get cantilever parameters
[normalStiffness, lateralStiffness, ...
 normalDisplacement, lateralDisplacement] = ...
 getCantileverData(cantilever);

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

% filter spikes
if (filterSpikes == 1)
	spikeFactor = 3;
	lateralVoltage = filterSpikes(lateralVoltage, spikeFactor);
	normalVoltage = filterSpikes(normalVoltage, spikeFactor);
end

% use cantilever values to convert voltages to forces
lateralForceMicroNewton = ... 
	lateralVoltage * lateralStiffness / lateralDisplacement;
normalForceMicroNewton = ... 
	normalVoltage * normalStiffness / normalDisplacement;

if (analyze)

	% find maximum (negative) adhesion value; this is pulloff
	[maxAdhesionUncompensatedMicroNewton,indexMaxAdhesion] = ...
		min(normalForceMicroNewton);


	% store shear value corresponding to max adhesion
	maxShearMicroNewton = lateralForceMicroNewton(indexMaxAdhesion);
	
	% back up and find maximum normal value; this is max preload
	[maxPreloadMicroNewton,indexMaxPreload] = ...
		max(normalForceMicroNewton(1:indexMaxAdhesion));

	% back up and find min normal value; this is point of contact
	[normalForceContactMicroNewton, indexContact] = ...
		min(normalForceMicroNewton(1:indexMaxPreload));

	% adhesion force = maxAdhesion - force at contact
	maxAdhesionMicroNewton = ...
		maxAdhesionUncompensatedMicroNewton - normalForceContactMicroNewton;
	
	% output to stdout
	if (stdOutput)
		fprintf('Max Normal Adhesion %3.3f\n',maxAdhesionMicroNewton);
	end

	% output to log file
	fprintf(logFileHandle, '% 15s\t',   sample);
	fprintf(logFileHandle, '% 15s\t',   cantilever);
	fprintf(logFileHandle, '% 15s\t',   angle);
	fprintf(logFileHandle, '% 15.3f\t', maxAdhesionMicroNewton);
	fprintf(logFileHandle, '% 15.3f\t', maxShearMicroNewton);
	fprintf(logFileHandle, '\n');
	
end

% assemble plot file name and title from the tokens above
% FIXME : what the hell is FS?
plotFileName = sprintf('./plots/%s_p%s_a%s_FS',sample,preload,angle);
titleString = sprintf('%s preload %s angle %s FS',... 
											 sample,preload,angle);
fprintf('Plotting File %s\n',plotFileName);

% plot normal and shear traces 
plot(axesHandle,lateralForceMicroNewton,'g');
hold on;
plot(axesHandle,normalForceMicroNewton,'b');

% graph annotation with extracted points
if (analyze) 
	% plot maximum adhesion point
	plot(indexMaxAdhesion, maxAdhesionUncompensatedMicroNewton,'ko');

	% plot corresponding max shear point
	plot(indexMaxAdhesion, maxShearMicroNewton,'ko');
	
	% plot maximum preload point
	plot(indexMaxPreload, maxPreloadMicroNewton,'ko');

	% plot contact position
	plot(indexContact, normalForceContactMicroNewton,'ko');
end



hold off;

xlabel(axesHandle, 'Time (ms)');
ylabel(axesHandle, 'Force (microNewtons)');
legend('Shear','Normal');			
title({'Limit Surface';titleString;'Cantilever 629a03 Sample SWS6'; ...
	'2008023_sws6_ls'},'Interpreter','None');

formatPlot( figureHandle, axesHandle, 'Times New Roman', 8 );
printPlot ( figureHandle, plotFileName, 5.0, 3.0);