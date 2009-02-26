% parseManualAll.m

pathString = './data/';

cd(pathString);
% grab list of files
listFiles = dir('*.data');
% go back to parent directory
cd('..');
% count files
numFiles = length(listFiles);

% open data file for logging of files and parameters
% to create index of data
logFileHandle = fopen('parsed.data','w');

formatString20 = '% 20s\t';
formatString15 = '% 15s\t';

% columnHeaders{column} = {line1,line2,line3,formatstring}
columnHeaders{1} = {'dataFileName',     formatString20};
columnHeaders{2} = {'indexContact',     formatString15};
columnHeaders{3} = {'indexMaxPreload',  formatString15};
columnHeaders{4} = {'indexMaxAdhesion', formatString15};


% loop through cell array to construct headers
for i = 1:1			% line loop
	for j = 1:4		% column loop
		% indexed by columnHeaders{column}(line)
		fprintf(logFileHandle,char(columnHeaders{j}(2)),char(columnHeaders{j}(i)));
	end
	fprintf(logFileHandle,'\n');
end

% loop through data files and call analyzeLS.m
for i = 1:numFiles
	fileName = [pathString,listFiles(i).name];
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
%	analyzeSlantTest(fileName,logFileHandle,figure,axes);
	parseManual(fileName,logFileHandle);
	close(figure);
end
