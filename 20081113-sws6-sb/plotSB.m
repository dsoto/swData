% plotSB.m
% this script takes the output from analyzeSBAll.m
% and plots the measured compression against the required
% force to achieve that compression
% 19 November 2008 08:33:42 PST

close all;
clear all;

% open file
fileHandle = fopen('20081113-1-sb.data','r');
fgetl(fileHandle);
fgetl(fileHandle);
fgetl(fileHandle);
% read data
a = textscan(fileHandle,'%s %s %f %f %f %f %f');

plot(a{6},a{5},'bo');
hold on;
xlabel('Measured Compression (\mum)');
ylabel('Preload Force (\muN)');
title({'Shear Microwedge Force vs. Microwedge Deflection'; ...
		'Cantilever 529b02 - Sample SWS6';'20081113-1-sb'},'Interpreter','None');

x = 0:0.5:15;
xLoc = 12.0;
yOffset = 0.1;
m = 0.05;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.05');
m = 0.10;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.10');
m = 0.20;
plot(x,m*x,':k');
text(xLoc,xLoc*m-yOffset,'k=0.20');

axis([0 15 0 3]);


formatPlot( gcf, gca, 'Times New Roman', 12 );
printPlot(gcf, 'springConstant', 4.0, 3.0);
