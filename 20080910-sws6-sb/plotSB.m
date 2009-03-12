% plotSB.m
% this script takes the output from analyzeSBAll.m
% and plots the measured compression against the required
% force to achieve that compression
% 19 November 2008 08:33:42 PST

close all;
clear all;

% open file
fileHandle = fopen('20080910_sws6_sb.data','r');
fgetl(fileHandle);
fgetl(fileHandle);
fgetl(fileHandle);
% read data
a = textscan(fileHandle,'%s %s %f %f %f %f %f');

plot(a{6},a{5},'bo');
hold on;
xlabel('Measured Compression (\mum)');
ylabel('Preload Force (\muN)');
title({'Shear Microwedge Force vs. Microwedge Deflection';'Cantilever 629a03 - Sample SWS6';'20080910_sws6_sb'},'Interpreter','None');

xMax = 5;
yMax = 1;
x = 0:0.5:xMax;
xLoc = 4.0;
yOffset = 0.05;
m = 0.05;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.05');
m = 0.10;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.10');
m = 0.20;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.20');

axis([0 xMax 0 yMax]);


formatPlot( gcf, gca, 'Times New Roman', 12 );
printPlot(gcf, 'springConstant', 4.0, 3.0);
