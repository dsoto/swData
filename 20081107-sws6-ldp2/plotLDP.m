% plotLDP.m
% this script takes the output from analyzeLDPAll.m

close all;
clear all;

% open file
fileHandle = fopen('20081117-nc.data','r');
fgetl(fileHandle);
fgetl(fileHandle);
fgetl(fileHandle);
% read data
a = textscan(fileHandle,'%s %s %f %f %f %f %f');

plot(a{6},a{5},'bo');
hold on;
xlabel('Measured Compression (\mum)');
ylabel('Preload Force (\muN)');
title('Effective Preload vs. Max Adhesion');


formatPlot( gcf, gca, 'Times New Roman', 12 );
printPlot(gcf, 'effectivePreload', 4.0, 3.0);
