% analyzeSBAll.m
% loops through all files in ./data/ and calls
% analyzeSB.m on each .data file


% FIXME : put this in function for use in all scripts
% function getDataFiles();
% go into data directory
cd('data');
% grab list of files
listFiles = dir('*.txt');
% go back to parent directory
cd('..');
% count files
numFiles = length(listFiles);

% open data file for logging of files and parameters
% to create index of data
% write header columns 
logFileHandle = fopen('20080823_sws6_ls.data','w');
% line 1
fprintf(logFileHandle,'% 15s\t','Sample');
fprintf(logFileHandle,'% 15s\t','Cantilever');
fprintf(logFileHandle,'% 15s\t','Pulloff');
fprintf(logFileHandle,'% 15s\t','Max');
fprintf(logFileHandle,'% 15s\t','Max');
fprintf(logFileHandle,'\n');
% line 2
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'% 15s\t','Angle');
fprintf(logFileHandle,'% 15s\t','Adhesion');
fprintf(logFileHandle,'% 15s\t','Shear');
fprintf(logFileHandle,'\n');
% line 3
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'\t');
fprintf(logFileHandle,'% 15s\t','(deg)');
fprintf(logFileHandle,'% 15s\t','(uN)');
fprintf(logFileHandle,'% 15s\t','(uN)');
fprintf(logFileHandle,'\n');

for i = 1:numFiles
	fileName = ['./data/',listFiles(i).name];
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
	analyzeLS(fileName,logFileHandle,figure,axes);
	close(figure);
end