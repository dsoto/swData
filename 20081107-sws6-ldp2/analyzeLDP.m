function plot_handle = analyzeLDP (fileName, logFileHandle, ...
                                   figureHandle, axesHandle);
% this function reads in data
% performs a simple analysis
% outputs logfile entries for data values	
% plots force traces and writes plot file
% function is called by plotAllForceTraceLoadDragPull.m

% flags for type of output
 createPlot = 1;
 annotatePlot = 1;

% open data file and strip off headers
fileHandle = fopen(fileName,'r');
date = fgetl(fileHandle);
cantilever         = fgetl(fileHandle);
trajectoryFileName = fgetl(fileHandle);
latAmp             = fgetl(fileHandle);
norAmp             = fgetl(fileHandle);
token              = fgetl(fileHandle);
% FIXME: need to figure out how to handle different length header files
fgetl(fileHandle);
dataHeaders        = fgetl(fileHandle);

% call function to get cantilever parameters
[normalStiffness, lateralStiffness, ...
 normalDisplacement, lateralDisplacement] = ...
 getCantileverData(cantilever);

% need to extract only file name from trajectory file name
% since the file string is on a PC this is all fucked 
% search for PC path separator
index = strfind(trajectoryFileName,'\');
% get last one
index = index(length(index));
% rest of string is the actual filename
trajectoryFileName = trajectoryFileName(index+1:length(trajectoryFileName));

% pull out values for preload, drag, and sample name from 
% trajectory filename and data filename
% uses cell arrays so char must be used
% data stored as strings
preloadToken = regexp(trajectoryFileName,'_p(\d*)','tokens');
preload = char(preloadToken{1,1});

dragToken = regexp(trajectoryFileName,'_d(\d*)','tokens');
drag = char(dragToken{1,1});

angleToken = regexp(trajectoryFileName,'_a(\d*)','tokens');
angle = char(angleToken{1,1});

velocityToken = regexp(trajectoryFileName,'_v(\d*)','tokens');
velocity = char(velocityToken{1,1});

sampleToken = regexp(fileName,'_(sws\d*)','tokens');
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

lateralVolt = -dataArray{1,2};
normalVolt = dataArray{1,3};
positionNormalMicron = dataArray{1,4}*10;
positionLateralMicron = dataArray{1,5}*10;

lateralVolt = filterSpikes(lateralVolt,3);
normalVolt = filterSpikes(normalVolt,3);

% convert to displacement
lateralDeflectionMicron = lateralVolt / lateralDisplacement;
normalDeflectionMicron = normalVolt / normalDisplacement;

% use cantilever values to convert voltages to forces
lateralForceMicroNewton = lateralDeflectionMicron * lateralStiffness;
normalForceMicroNewton = normalDeflectionMicron * normalStiffness;

%------------------------------------------------
% begin analysis
%------------------------------------------------

% find maximum normal preload
[maxPreloadMicroNewton,indexMaxPreload] = max(normalForceMicroNewton);

% backup, find min, this is contact point (in cases with voltage drift)
[normalForceAtContactMicroNewton, indexContact] = ...
	min(normalForceMicroNewton(1:indexMaxPreload));

% find pulloff point of maximum normal adhesion
% find from minimum value after max preload
[maxAdhesionMicroNewton, indexMaxAdhesion] = ...
	min(normalForceMicroNewton(indexMaxPreload:length(normalForceMicroNewton)));
indexMaxAdhesion = indexMaxAdhesion + indexMaxPreload - 1;

% preload force is difference between max preload and contact
totalPreloadForceMicroNewton = ... 
	maxPreloadMicroNewton - normalForceAtContactMicroNewton;



% calculate distance stage traveled between initial contact
% and maximum preload force 
positionContactMicron = positionNormalMicron(indexContact);
positionPreloadMicron = positionNormalMicron(indexMaxPreload);
stagePreloadMicron = positionPreloadMicron - positionContactMicron;

% get cantilever deflections
cantileverDeflectionContactMicron = normalDeflectionMicron(indexContact);
cantileverDeflectionPreloadMicron = normalDeflectionMicron(indexMaxPreload);
cantileverDeflectionMaxAdhesionMicron = ...
	normalDeflectionMicron(indexMaxAdhesion);

microwedgePreloadMicron = stagePreloadMicron - ...
	(cantileverDeflectionContactMicron - cantileverDeflectionPreloadMicron);

effectivePreloadMicron = stagePreloadMicron - ...
	(cantileverDeflectionContactMicron - cantileverDeflectionMaxAdhesionMicron);

%------------------------------------------------
% end analysis
%------------------------------------------------


% output to logfile 

fprintf(logFileHandle, '% 15s\t',   sample);
fprintf(logFileHandle, '% 15s\t',   cantilever);
fprintf(logFileHandle, '% 15.3f\t', stagePreloadMicron);
fprintf(logFileHandle, '% 15.3f\t', microwedgePreloadMicron);
fprintf(logFileHandle, '% 15.3f\t', totalPreloadForceMicroNewton);
fprintf(logFileHandle, '% 15.3f\t', maxAdhesionMicroNewton);
fprintf(logFileHandle, '% 15.3f\t', effectivePreloadMicron);
fprintf(logFileHandle, '\n');

if createPlot
	% assemble plot file name and title from the tokens above
	plotFileName = sprintf('./plots/%s_p%s_d%s_a%s_v%s', ...
													sample,preload,drag,angle,velocity);
	titleString = sprintf('%s preload %s drag %s angle %s velocity %s\n%s', ... 
												 sample,preload,drag,angle,velocity,fileName);
	fprintf('Plotting File %s\n',plotFileName);
	
	% plot normal and shear traces 
	plot(axesHandle,lateralForceMicroNewton,'g');
	hold on;
	plot(axesHandle,normalForceMicroNewton,'b');
	
	if annotatePlot
		plot(indexMaxPreload,maxPreloadMicroNewton,'ko');
		plotString = sprintf('Max Preload position');
		text(indexMaxPreload,maxPreloadMicroNewton,plotString);
		
%		plot(indexMaxAdhesion,maxAdhesionMicroNewton,'ko');
%		plot(indexMaxPullIn,maxPullIn,'ko');
		
		plot(indexContact,normalForceMicroNewton(indexContact),'ko');
		plotString = sprintf('Initial Contact Position');
		text(indexContact,normalForceAtContactMicroNewton,plotString);
	end
	
	hold off;
	xlabel(axesHandle, 'Time (ms)');
	ylabel(axesHandle, 'Force (microNewtons)');
	legend('Shear','Normal');			
	title(titleString,'Interpreter','None');
	
	formatPlot( figureHandle, axesHandle, 'Times New Roman', 24 );
	printPlot(figureHandle, plotFileName, 11.0, 8.5);
end
