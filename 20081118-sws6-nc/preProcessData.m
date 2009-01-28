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
