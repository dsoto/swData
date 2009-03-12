% this script takes the output from plotAllForceTraceLS.m
% and plots the measured compression against the required
% force to achieve that compression
% 10 September 2008 11:38:12 PDT

close all;
clear all;

fileHandle = fopen('lsPoints.log','r');
fgetl(fileHandle);
fgetl(fileHandle);
fgetl(fileHandle);
a = textscan(fileHandle,'%f %f %f %f %f %f %f %f');

plot(a{4},a{5},'ko');
hold on;
xlabel('Measured Compression (\mum)');
ylabel('Preload Force (\muN)');
axis([0 2 0 4]);
title('Normal Microwedge Force vs. Compression');

x = 0:0.5:2;
plot(x,x,'--k');
text(1.7,1.2,'k=1');
plot(x,2*x,'--k');
text(1.7,2.9,'k=2');
plot(x,3*x,'--k');
text(1.3,3.7,'k=3');

formatPlot( gcf, gca, 'Times New Roman', 12 );
printPlot(gcf, 'springConstant', 4.0, 3.0);
