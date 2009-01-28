% plotNC.m
% this script takes the output from analyzeNCAll.m
% and plots the measured compression against the required
% force to achieve that compression
% 19 November 2008 08:33:42 PST

close all;
clear all;

% open file
fileHandle = fopen('20081118-nc.data','r');
fgetl(fileHandle);
fgetl(fileHandle);
fgetl(fileHandle);
% read data
a = textscan(fileHandle,'%s %s %f %f %f %f %f');

plot(a{6},a{5},'bo');
hold on;
xlabel('Measured Compression (\mum)');
ylabel('Preload Force (\muN)');
title({'Normal Microwedge Force vs. Compression'; ...
	'Cantilever 629a03 - Sample SWS6';'20081118-nc'});

x = 0:0.5:3;
xLoc = 2.5;
yOffset = 0.2;
m = 0.25;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.25');
m = 0.5;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.5');
m = 1.0;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=1.0');

axis([0 3 0 3]);


formatPlot( gcf, gca, 'Times New Roman', 12 );
printPlot(gcf, 'springConstant', 4.0, 3.0);
