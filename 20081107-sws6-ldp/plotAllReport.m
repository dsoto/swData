% this script goes through the files specified in configure.m and 
% creates pdf files with the trajectory, force space, and force time traces

tic

clear all
close all

run ./configure.m

for i = 1 : length(distancePreloadMicron)
	for j = 1 : length(anglePulloffDegree)
  	for k = 1 : numTrials;

			% Get trajectory file
			filename = sprintf(testFormatString,...
											 distancePreloadMicron(i),...
											 anglePulloffDegree(j),k);
			plotname = sprintf(plotFormatString,...
								 distancePreloadMicron(i),...
								 anglePulloffDegree(j),k);
								 
			fprintf('Generating : %s.pdf\n',plotname);
			
			figureHandle = figure;
			forceSpaceHandle = subplot(2,2,3);
			forceTraceHandle = subplot(2,2,1:2);
			trajectoryHandle = subplot(2,2,4);
			
			plotTrajectory(filename,figureHandle,trajectoryHandle);
			plotForceSpace(filename,figureHandle,forceSpaceHandle);
			plotForceTrace(filename,figureHandle,forceTraceHandle);
			
			title(filename,'Interpreter','None');
			printPlot(figureHandle, plotname, 11.0, 8.5);
			close(figureHandle)

		end
	end
end

toc



