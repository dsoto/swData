% analyzeSBAll.m
% loops through all files in ./data/ and calls
% analyzeSB.m on each .data file


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
logFileHandle = fopen('20090127-sws7-nc.data','w');

formatString20 = '% 20s\t';
formatString15 = '% 15s\t';

% columnHeaders{column} = {line1,line2,line3,formatstring}
columnHeaders{1} = {'Data',       'File',      'Name',    formatString20};
columnHeaders{2} = {'Trajectory', 'File',      'Name',    formatString20};
columnHeaders{3} = {'Sample',     '',          ''    ,    formatString15};
columnHeaders{4} = {'Cantilever', '',          ''    ,    formatString15};
columnHeaders{5} = {'Cantilever', 'Deflection','(um)',   formatString15};
columnHeaders{6} = {'Stage',      'Preload',   '(um)',    formatString15};
columnHeaders{7} = {'Preload',    'Force',     '(uN)',    formatString15};
columnHeaders{8} = {'Microwedge', 'Deflection','(um)',    formatString15};
columnHeaders{9} = {'Spring',     'Constant',  '(N/m)',    formatString15};

% loop through cell array to construct headers
for i = 1:3			% line loop
	for j = 1:9		% column loop
		% indexed by columnHeaders{column}(line)
		fprintf(logFileHandle,char(columnHeaders{j}(4)),char(columnHeaders{j}(i)));
	end
	fprintf(logFileHandle,'\n');
end

% loop through data files and call analyzeLS.m
for i = 1:numFiles
	fileName = ['./data/',listFiles(i).name];
	fprintf('Processing File %d of %d : % 10s\n',i,numFiles,fileName);
	figure = gcf;
	axes = gca;
	analyzeNC(fileName, logFileHandle, figure, axes);
	close(figure);
end
