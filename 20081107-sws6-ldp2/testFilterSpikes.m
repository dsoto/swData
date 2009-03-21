% go into data directory
%cd('data');
%
% grab list of files
%listFiles = dir('*.txt');
%
% go back to parent directory
%cd('..');
%
%numFiles = length(listFiles);
%
% loop through all files in directory
% and call plotForceTraceLS.m
%for i = 1:numFiles
%	fileName = listFiles(i).name;
%	fileName = ['./data/' fileName];
%	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
%	figure = gcf;
%	axes = gca;
%figureHandle = gcf;
%axesHandle = gca;

fileName = './data/ldp_sws6_20081107_182534.txt';

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

% load data from file into array
dataArray = textscan(fileHandle, '%s %15.7f %15.7f %15.7f %15.7f');
fclose(fileHandle);

data1 = -dataArray{1,2};
data2 = dataArray{1,3};
positionNormalMicron = dataArray{1,4}*10;
positionLateralMicron = dataArray{1,5}*10;

% pull out relevant data section
dataStart = 1;
dataEnd = length(data1);
lateralVolt = data1(dataStart:dataEnd); %???
normalVolt = data2(dataStart:dataEnd); %???

% subtract background 
% FIXME : this bias section needs to be done more intelligently
lateralVoltBias = mean(lateralVolt(1:500));
lateralVolt = lateralVolt - lateralVoltBias;
normalVoltBias = mean(normalVolt(1:500));
normalVolt = normalVolt - normalVoltBias;

lateralVoltNoSpike = filterSpikes(lateralVolt,5);
normalVoltNoSpike = filterSpikes(normalVolt,5);

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


% assemble plot file name and title from the tokens above
plotFileName = sprintf('./plots/%s_p%s_d%s_a%s_v%s', ...
                        sample,preload,drag,angle,velocity);
titleString = sprintf('%s preload %s drag %s angle %s velocity %s', ... 
											 sample,preload,drag,angle,velocity);
fprintf('Plotting File %s\n',plotFileName);

%lateralForceMicroNewton = diff(lateralForceMicroNewton);
%normalForceMicroNewton = diff(normalForceMicroNewton);
%lateralForceMicroNewton = diff(lateralForceMicroNewton);
%normalForceMicroNewton = diff(normalForceMicroNewton);


% plot normal and shear traces 
subplot(2,1,1);
plot(lateralVolt,'gx');
hold on;
plot(normalVolt,'bx');
hold off;

subplot(2,1,2);
plot(lateralVoltNoSpike,'gx');
hold on;
plot(normalVoltNoSpike,'bx');
hold off;

input('press return');
	close(figure);
	
%end% test filter spikes

