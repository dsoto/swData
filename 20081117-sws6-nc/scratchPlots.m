% scratchPlots.m
% analyzes data from load pull experiment
% and plots for inspection

clear all
close all

% get configuration data
run ./configure.m

% make FID for text report
textReportFID = fopen(filenameDataSummaryText,'w');

for i = 1:length(distancePreloadMicron)
	for j = 1:length(anglePulloffDegree)
		for k = 1:numTrials
	
			% Get trajectory file
			trajectoryFilename = sprintf(trajFormatString,...
											             distancePreloadMicron(i),...
											             anglePulloffDegree(j),k);
			trajData = load(trajectoryFilename);
			
			% trajectory file appears to be just the times and vertices of trajectory
			% put this in function with description
			% time = trajData( row, col );
			t = trajData(:,1);
			tTare      = trajData(1,1); % begin tare
			tStart     = trajData(2,1); % end tare    - begin preload
			tPreload   = trajData(3,1); % end preload - begin pulloff
			tPulloff   = trajData(4,1); % end pulloff - begin home
			tClearance = trajData(5,1); % end home
			
			% Load data
			% NOTE: add code for directory stuff here
			testFilename = sprintf(testFormatString,...
											       distancePreloadMicron(i),...
											       anglePulloffDegree(j),k);
			testData = load(testFilename);
			fprintf('Analyzing file : %s\n',testFilename);
			
			% Extract data
			[time Dx Dy Dz Ax Ay Az Fx Fy Fz Mx My Mz] = getTraces ( testData );
			
			% each of the above are column vectors
			% force is in units of Newtons
			forceXRaw = Fx;
			forceYRaw = Fy;
			forceZRaw = Fz;
			
			% Get vertex indices
			% find takes the logical expression and returns the index of the 
			% first occurence in the array that satisfies the expression
			index0 =         find( ( time >= tTare ),      1, 'first' );
			indexStart =     find( ( time >= tStart ),     1, 'first' );
			indexPreload =   find( ( time >= tPreload ),   1, 'first' );
			indexPulloff =   find( ( time >= tPulloff ),   1, 'first' );
			indexClearance = find( ( time >= tClearance ), 1, 'first' );
			
			
			% Tare data using initial idle time
			biasX = mean ( forceXRaw( 1:indexStart ));
			biasY = mean ( forceYRaw( 1:indexStart ));
			biasZ = mean ( forceZRaw( 1:indexStart ));
			
			% takes the mean along the column direction and returns a row vector
			forceXTared = forceXRaw - biasX;
			forceYTared = forceYRaw - biasY;
			forceZTared = forceZRaw - biasZ;	
			
			% Filter data
			[numd,dend] = butter(3,.1);
			forceXFiltered = filtfilt(numd,dend,forceXTared);
			forceYFiltered = filtfilt(numd,dend,forceYTared);
			forceZFiltered = filtfilt(numd,dend,forceZTared);
			
			DPlot = 0;
    	if DPlot
				plot(time,Dx,'r');
				hold on;
				plot(time,Dy,'g');
				hold on;
				plot(time,Dz,'b');
				hold on;
				title('desired position');
				legend('x','y','z');
			end  

	    APlot = 0;
			if APlot
				plot(time,Ax,'r');
				hold on;
				plot(time,Ay,'g');
				hold on;
				plot(time,Az,'b');
				hold on;
				title('reported position');
				legend('x','y','z');
			end
			
			FPlot = 1;
			if FPlot
				plot(time,forceXFiltered,'r');
				hold on;
				plot(time,forceYFiltered,'g');
				hold on;
				plot(time,forceZFiltered,'b');
				hold on;
				title('force traces');
				legend('x','y','z');
            end
        end
	end
end

formatPlot(gcf,gca,'Times New Roman',24);
printPlot(gcf,'All Force Plots',8,6);
		
