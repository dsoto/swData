function returnValue = analyzeSlantTestManual ( dataFileName, logFileHandle);

% this function will determine
% max preload
% max adhesion
% max shear
% effective preload
% 

debug = 0;
if debug
fprintf(1,'entered analyzeLS\n');
end

% flags to perform analysis and plotting
analyze = 1;       % perform analysis of forces
stdOutput = 0;     % output to command line
filterSpikes = 0;  % filter sharp piezo spikes
doDisplayPlot = 1;  % display plot
doPrintPlot = 1;     % output a pdf plot 
% doDisplayPlot doesn't work

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


% extract parameters from headers
% uses cell arrays so char must be used
% data stored as strings
angleToken = regexp(trajectoryFileName,'_a(\d*)','tokens');
dragAngle = char(angleToken{1,1});

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

token = regexp(pitchAngle,'= (.*)','tokens');
pitchAngle = char(token{1,1});

token = regexp(rollAngle,'= (.*)','tokens');
rollAngle = char(token{1,1});

% assemble plot file name and title from the tokens above
plotFileName = sprintf('./plots/%s_p%s_pa%s_ra%s_ls', ...
											 sample,preload,pitchAngle,rollAngle);
titleString = sprintf('%s preload %s pitch angle %s roll angle %s ls',... 
											 sample,preload,pitchAngle,rollAngle);



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

if debug
lateralVoltage(1)
end

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

%
% automated point detection 

% find maximum (negative) adhesion value; this is pulloff
[maxAdhesionUncompensatedMicroNewton,indexMaxAdhesion] = ...
	min(normalForceMicroNewton);
% store shear value corresponding to max adhesion
maxShearUncompensatedMicroNewton = lateralForceMicroNewton(indexMaxAdhesion);
% back up and find maximum normal value; this is max preload
[maxPreloadMicroNewton,indexMaxPreload] = ...
	max(normalForceMicroNewton(1:indexMaxAdhesion));
% back up and find min normal value; this is point of contact
[normalForceContactMicroNewton, indexContact] = ...
	min(normalForceMicroNewton(1:indexMaxPreload));
% find corresponding value of contact for shear
shearForceContactMicroNewton = lateralForceMicroNewton(indexContact);

%
% automated plot presentation

% plot normal and shear traces 
plot(lateralForceMicroNewton,'g');
hold on;
plot(normalForceMicroNewton,'b');

% plot maximum adhesion point
plot(indexMaxAdhesion, maxAdhesionUncompensatedMicroNewton,'bo');

% plot corresponding max shear point
plot(indexMaxAdhesion, maxShearUncompensatedMicroNewton,'go');

% plot maximum preload point
plot(indexMaxPreload, maxPreloadMicroNewton,'ro');

% plot normal contact position
plot(indexContact, normalForceContactMicroNewton,'bd');

% plot shear contact position
plot(indexContact, shearForceContactMicroNewton,'gd');
hold off;

xlabel('Time (ms)');
ylabel('Force (microNewtons)');
legend('Shear','Normal','Max Normal Adhesion', ...
       'Max Shear Adhesion', 'Max Preload', ...
       'Normal Contact Point', 'Shear Contact Point');		
title({titleString},'Interpreter','None');

%
% check if automated detection was acceptable

fprintf(1,'Are these points acceptable? (y/n) \n');
response = input(' : ','s');
isAcceptable = strcmp('y',response);

if (isAcceptable == 1)
	fprintf(1,'You accepted\n');
else
	fprintf(1,'You rejected\n');

	% replot for user to select
	plot(lateralForceMicroNewton,'g');
	hold on;
	plot(normalForceMicroNewton,'b');
	
	% get contact point
	fprintf('Click on Initial Contact on Normal Trace \n');
	[indexContact, normalForceContactMicroNewton] = ginput(1);
	indexContact = round(indexContact);
	normalForceContactMicroNewton = ...
		normalForceMicroNewton(indexContact);
	% store shear value corresponding to max adhesion
	shearForceContactMicroNewton = lateralForceMicroNewton(indexContact);
	% plot max normal adhesion
	plot(indexContact, normalForceContactMicroNewton,'bo');
	% plot corresponding max shear point
	plot(indexContact, shearForceContactMicroNewton,'go');
	legend('Shear','Normal','Normal Contact Point', ...
	'Shear Contact Point');			
	
	% get max preload
	fprintf('Click on Maximum Preload on Normal Trace \n');
	[indexMaxPreload, maxPreloadMicroNewton] = ginput(1);
	indexMaxPreload = round(indexMaxPreload);
	maxPreloadMicroNewton = normalForceMicroNewton(indexMaxPreload);
	plot(indexMaxPreload, maxPreloadMicroNewton,'ro');		
	legend('Shear','Normal', 'Normal Contact Point', ...
	'Shear Contact Point', 'Max Preload');			
	
	% get pulloff point
	fprintf('Click on Pulloff / Max Adhesion on Normal Trace \n');
	[indexMaxAdhesion,maxAdhesionUncompensatedMicroNewton] = ginput(1);
	indexMaxAdhesion = round(indexMaxAdhesion);
	maxAdhesionUncompensatedMicroNewton = ...
		normalForceMicroNewton(indexMaxAdhesion);
	% plot maximum adhesion point
	plot(indexMaxAdhesion, maxAdhesionUncompensatedMicroNewton,'bo');
	% plot corresponding max shear point
	plot(indexMaxAdhesion, maxShearUncompensatedMicroNewton,'go');	
	hold off;
	xlabel('Time (ms)');
	ylabel('Force (microNewtons)');
	legend('Shear','Normal', 'Normal Contact Point', ...
	       'Shear Contact Point', 'Max Preload', ...
	       'Max Normal Adhesion','Max Shear Adhesion');			
	title({titleString;shortDataFileName},'Interpreter','None');
end

%
% by this point the points should be satisfactorily determined
% and we can perform calculations and log results
%
% calculations based on contact and pulloff points

% get cantilever normal voltage at max adhesion
normalCantileverVoltageMaxAdhesion = normalVoltage(indexMaxAdhesion);
% get stage displacement at max adhesion
normalStagePositionMaxAdhesion = positionNormalMicron(indexMaxAdhesion);
% get cantilever deflection at contact
normalCantileverVoltageContact = normalVoltage(indexContact);
% get stage displacement at contact
normalStagePositionContact = positionNormalMicron(indexContact);
% calculate effective stage preload
normalStagePreload = normalStagePositionMaxAdhesion - ...
	normalStagePositionContact;
% calculate effective cantilever deflection
normalCantileverDeflection = (normalCantileverVoltageContact - ...
	normalCantileverVoltageMaxAdhesion)/normalDisplacement;
% calculate effective microwedge deflection (effective preload)
effectivePreload = normalCantileverDeflection + normalStagePreload;
% adhesion force = maxAdhesion - force at contact
maxAdhesionMicroNewton = ...
	maxAdhesionUncompensatedMicroNewton - normalForceContactMicroNewton;
% shear force = maxShear - force at contact
maxShearMicroNewton = ...
	maxShearUncompensatedMicroNewton - shearForceContactMicroNewton;

% output to log file
fprintf(logFileHandle, '% 20s\t',   shortDataFileName);
fprintf(logFileHandle, '% 20s\t',   shortTrajectoryFileName);
fprintf(logFileHandle, '% 15s\t',   sample);
fprintf(logFileHandle, '% 15s\t',   cantilever);
fprintf(logFileHandle, '% 15s\t',   pitchAngle);
fprintf(logFileHandle, '% 15s\t',   rollAngle);
fprintf(logFileHandle, '% 15.3f\t', maxAdhesionMicroNewton);
fprintf(logFileHandle, '% 15.3f\t', maxShearMicroNewton);
fprintf(logFileHandle, '% 15.3f',   effectivePreload);
fprintf(logFileHandle, '\n');
	
if (doPrintPlot == 1)
	fprintf('Printing Plot File %s\n',plotFileName);
	formatPlot( gcf, gca, 'Times New Roman', 8 );
	printPlot ( gcf, plotFileName, 5.0, 3.0);
end
