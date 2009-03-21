debug = 0;

% go into data directory
cd('data');

% grab list of files
listFiles = dir('*.data');

% go back to parent directory
cd('..');

numFiles = length(listFiles);

% columns of logfile 
% sample 
% cantilever
% stage preload (micron)
% microwedge preload (micron)
% preload force (uN)
% max adhesion (uN)
% effective preload (micron)

% open data file for logging of files and parameters
% to create index of data
% write header columns 
logFileHandle = fopen('experiment.outputLog','w');
% line 1
fprintf(logFileHandle,'% 15s\t','Sample');
fprintf(logFileHandle,'% 15s\t','Cantilever');
fprintf(logFileHandle,'% 15s\t','Stage');
fprintf(logFileHandle,'% 15s\t','Microwedge');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'% 15s\t','Max');
fprintf(logFileHandle,'% 15s\t','Effective');
fprintf(logFileHandle,'\n');
% line 2
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'% 15s\t','Force');
fprintf(logFileHandle,'% 15s\t','Adhesion');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'\n');
% line 3
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(uN)');
fprintf(logFileHandle,'% 15s\t','(uN)');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'\n');


% loop through all files in directory
% and call plotForceTraceLS.m

for i = 1:numFiles
	fileName = listFiles(i).name;
	fileName = ['./data/' fileName];
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
	analyzeLDP(fileName,logFileHandle,figure,axes);
	close(figure);
	if debug
		break
	end
end