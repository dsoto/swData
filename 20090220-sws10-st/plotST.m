% open file
% strip first three lines
% dump into array

dataFileName = ('analyzed.data');
fileHandle = fopen(dataFileName,'r');
%dummyLine = fgetl(fileHandle);
%dummyLine = fgetl(fileHandle);
%dummyLine = fgetl(fileHandle);


dataArray = textscan(fileHandle, '%s%f%f%f');

angleSlant = dataArray{1,2};
shearForce =  dataArray{1,4};
normalForce  =  dataArray{1,3};
fclose(fileHandle);

plot(angleSlant,shearForce,'gd',angleSlant,normalForce,'bo');

xlabel('Goniometer Reading');
ylabel('Max Force (microNewtons)');
title({'Slant Dependence'}, ...
       'Interpreter','None');
legend('Max Shear','Max Normal');

axis([-26 26 -5 10]);
x = get(gca,'XLim');
y = get(gca,'YLim');
grid on;
axis(gca,[x,y]);
line(x,[0 0],[0 0],'Color','k','LineWidth',2);
line([0 0],y,[0 0],'Color','k','LineWidth',2);

formatPlot(gcf,gca,'Times New Roman',24);
plotFilename = 'slantTest';
printPlot(gcf,plotFilename,8,6);
