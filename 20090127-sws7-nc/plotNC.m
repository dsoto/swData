% plotNC.m
% this script takes the output from analyzeNCAll.m
% and plots the measured compression against the required
% force to achieve that compression
% 19 November 2008 08:33:42 PST

close all;
clear all;

% open file
fileHandle = fopen('20090127-sws7-nc.data','r');
fgetl(fileHandle);
fgetl(fileHandle);
fgetl(fileHandle);
% read data
a = textscan(fileHandle,'%s %s %s %s %f %f %f %f %f %f %f');

plot(a{8},a{7},'bo');
hold on;
xlabel('Measured Compression (\mum)');
ylabel('Preload Force (\muN)');
title({'Normal Microwedge Force vs. Compression'; ...
	'Cantilever 529b02 - Sample SWS7';'20000127-sws7-nc'});

x = 0:0.5:4;
xLoc = 2.0;
yOffset = 0.2;
m = 1.0;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=1.0');
m = 2.0;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=2.0');
m = 5.0;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=5.0');

axis([0 4 0 11]);


formatPlot( gcf, gca, 'Times New Roman', 12 );
printPlot(gcf, 'springConstant', 4.0, 3.0);
