% grab list of files
listFiles = dir('*.txt');
numFiles = length(listFiles);

% loop through all files in directory
% and call shearBendingAnalysis.m
for i = 1:numFiles
	fileName = listFiles(i).name;
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
	shearBendingAnalysis(fileName,figure,axes);
	close(figure);
end