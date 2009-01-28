% shearBendingAnalysisAll.m
% loops through all files in ./data/ and calls
% shearBendingAnalysis.m on each .data file


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


% loop through all files in directory
% and call shearBendingAnalysis.m
for i = 1:numFiles
	fileName = ['./data/',listFiles(i).name];
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
	shearBendingAnalysis(fileName,figure,axes);
	close(figure);
end