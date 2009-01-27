% go into data directory
cd('data');

% grab list of files
listFiles = dir('*.data');

% go back to parent directory
cd('..');

numFiles = length(listFiles);

% open data file for logging of files and parameters
% to create index of data
% write header columns 
logFileHandle = fopen('experiment.outputLog','w');
fprintf(logFileHandle,'% 15s\t','Nominal');
fprintf(logFileHandle,'% 15s\t','Drag');
fprintf(logFileHandle,'% 15s\t','Pulloff');
fprintf(logFileHandle,'% 15s\t','Measured');
fprintf(logFileHandle,'% 15s\t','Measured');
fprintf(logFileHandle,'% 15s\t','Max');
fprintf(logFileHandle,'% 15s\t','Max');
fprintf(logFileHandle,'% 15s\t','Max');
fprintf(logFileHandle,'% 15s\t','Normal');
fprintf(logFileHandle,'\n');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'% 15s\t','Distance');
fprintf(logFileHandle,'% 15s\t','Angle');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'% 15s\t','Compression');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'% 15s\t','Adhesion');
fprintf(logFileHandle,'% 15s\t','Shear');
fprintf(logFileHandle,'% 15s\t','Spring');
fprintf(logFileHandle,'\n');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(deg)');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(uN)');
fprintf(logFileHandle,'% 15s\t','(uN)');
fprintf(logFileHandle,'% 15s\t','(uN)');
fprintf(logFileHandle,'% 15s\t','Constant');
fprintf(logFileHandle,'\n');


% loop through all files in directory
% and call plotForceTraceLS.m
for i = 1:numFiles
	fileName = listFiles(i).name;
	fileName = ['./data/' fileName];
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
	plotForceTraceLoadDragPull(fileName,figure,axes,logFileHandle);
	close(figure);
end