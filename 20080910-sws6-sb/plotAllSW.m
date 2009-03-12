% plotAllSW.m
% i don't know what this was for

listFiles = dir('*.txt');

numFiles = length(listFiles);

% open data file for logging of files and parameters
% to create index of data

for i = 1:numFiles
	fileName = listFiles(i).name;
	fprintf('Processing File %d of %d : %s\n',i,numFiles,fileName);
	
	fileHandle = fopen(fileName,'r');
	date = fgetl(fileHandle);
	cantilever         = fgetl(fileHandle);
	trajectoryFileName = fgetl(fileHandle);
	latAmp             = fgetl(fileHandle);
	norAmp             = fgetl(fileHandle);
	token              = fgetl(fileHandle);
	dataHeaders        = fgetl(fileHandle);
	
	dataArray = textscan(fileHandle, '%s %15.7f %15.7f %15.7f %15.7f');
  fclose(fileHandle);

	data1 = dataArray{1,2};
	data2 = dataArray{1,3};
	capX  = dataArray{1,4};
	capY  = dataArray{1,5};
	
	lateralVolt = data1; %???
	normalVolt = data2; %???
	
	lateralVoltBias = mean(lateralVolt(1:500));
	lateralVolt = lateralVolt - lateralVoltBias;
	normalVoltBias = mean(normalVolt(1:500));
	normalVolt = normalVolt - normalVoltBias;
	
% % filter data
%	[numd,dend] = butter(3,.02);
%	lateralVolt = filtfilt(numd,dend,lateralVolt);
%	normalVolt = filtfilt(numd,dend,normalVolt);
	
	preloadToken = regexp(trajectoryFileName,'_p(\d*)','tokens');
	preload = char(preloadToken{1,1});

	dragToken = regexp(trajectoryFileName,'_d(\d*)','tokens');
	drag = char(dragToken{1,1});

	sampleToken = regexp(fileName,'_(sws\d*)','tokens');
	sample = char(sampleToken{1,1});
	
	plotFileName = sprintf('%s_p%s_d%s',sample,preload,drag);
	
	figureHandle = figure;
	title(plotFileName,'Interpreter','None');
	
	forceTraceHandle = subplot(1,2,1);
	hold on;
	plot(forceTraceHandle,lateralVolt,'b');
	plot(forceTraceHandle,normalVolt,'k');
	plot(forceTraceHandle,capX,'g');
	plot(forceTraceHandle,capY,'r');
	legend('lateralVolt','normalVolt','capX','capY');
	hold off;
	titleString = sprintf('Force Trace %s %s preload %s drag',...
	                       sample, preload, drag);
	title(titleString);

	forceSpaceHandle = subplot(1,2,2);
	plot(forceSpaceHandle,-lateralVolt,normalVolt);
	title('Force Space');
	

			

	printPlot(figureHandle, plotFileName, 11.0, 8.5);
	close(figureHandle)


	

	

	
end

hold off