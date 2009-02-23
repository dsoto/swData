% analyzeLSAll.m
% loops through all files in ./data/ and calls
% analyzeLS.m on each .data file


% FIXME : put this in function for use in all scripts
% function getDataFiles();
% go into data directory

pathString = './data/310/';

cd(pathString);
% grab list of files
listFiles = dir('*.data');
% go back to parent directory
cd('../..');

% count files
numFiles = length(listFiles);

for i = 1:numFiles
	fileName = [pathString,listFiles(i).name];
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
	plotRawForceTrace(fileName,figure,axes);
	close(figure);
end