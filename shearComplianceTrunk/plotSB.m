% plotSB.m
% this script takes the output from analyzeSBAll.m
% and plots the measured compression against the required
% force to achieve that compression
% 19 November 2008 08:33:42 PST

close all;
clear all;

% open file
fileHandle = fopen('2008xxxx-sb.data','r');
fgetl(fileHandle);
fgetl(fileHandle);
fgetl(fileHandle);
% read data
a = textscan(fileHandle,'%s %s %f %f %f %f %f');

plot(a{6},a{5},'bo');
hold on;
xlabel('Measured Compression (\mum)');
ylabel('Preload Force (\muN)');
title('Shear Microwedge Force vs. Microwedge Deflection');

x = 0:0.5:7;
xLoc = 6.0;
yOffset = 0.3;
m = 0.5;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.5');
m = 1.0;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=1.0');
m = 1.5;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=1.5');

axis([0 7 0 10]);


formatPlot( gcf, gca, 'Times New Roman', 12 );
printPlot(gcf, 'springConstant', 4.0, 3.0);
