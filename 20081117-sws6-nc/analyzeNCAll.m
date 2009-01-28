% analysisNCAll.m
% loops through all files in ./data/ and calls
% analysisNC.m on each .data file


% FIXME : put this in function for use in all scripts
% function getDataFiles();
% go into data directory
cd('data');
% grab list of files
listFiles = dir('*.data');
% go back to parent directory
cd('..');
% count files
numFiles = length(listFiles);

% open data file for logging of files and parameters
% to create index of data
% write header columns 
logFileHandle = fopen('2008xxxx-nc.data','w');
% line 1
fprintf(logFileHandle,'% 15s\t','Sample');
fprintf(logFileHandle,'% 15s\t','Cantilever');
fprintf(logFileHandle,'% 15s\t','Cantilever');
fprintf(logFileHandle,'% 15s\t','Stage');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'% 15s\t','Microwedge');
fprintf(logFileHandle,'% 15s\t','Spring');
fprintf(logFileHandle,'\n');
% line 2
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'% 15s\t','Deflection');
fprintf(logFileHandle,'% 15s\t','Preload');
fprintf(logFileHandle,'% 15s\t','Force');
fprintf(logFileHandle,'% 15s\t','Deflection');
fprintf(logFileHandle,'% 15s\t','Constant');
fprintf(logFileHandle,'\n');
% line 3
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(uN)');
fprintf(logFileHandle,'% 15s\t','(um)');
fprintf(logFileHandle,'% 15s\t','(N/m)');
fprintf(logFileHandle,'\n');

% loop through all files in directory
% and call shearBendingAnalysis.m
for i = 1:numFiles
	fileName = ['./data/',listFiles(i).name];
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
	analyzeNC(fileName, logFileHandle, figure, axes);
	close(figure);
end
