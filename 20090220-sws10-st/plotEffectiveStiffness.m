% open file
% strip first three lines
% dump into array

dataFileName = ('test.data');
fileHandle = fopen(dataFileName,'r');
%dummyLine = fgetl(fileHandle);
%dummyLine = fgetl(fileHandle);
%dummyLine = fgetl(fileHandle);


dataArray = textscan(fileHandle, '%f%f%f%f');

angleSlant          = dataArray{1,1};
effectiveStiffness  = dataArray{1,4};
fclose(fileHandle);

plot(angleSlant,effectiveStiffness,'gd');

xlabel('Goniometer Reading (deg)');
ylabel('Effective Stiffness (N/m)');
title({'Slant Dependence','SWS10 - 629a03'}, 'Interpreter','None');
grid on;

axis([-30 25 0.10 0.15]);

formatPlot(gcf,gca,'Times New Roman',12);
plotFilename = 'slantTestEffectiveStiffness';
printPlot(gcf,plotFilename,4,3);
