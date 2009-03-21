% open file
% strip first three lines
% dump into array

dataFileName = ('20080823_sws6_ls.data');
fileHandle = fopen(dataFileName,'r');
dummyLine = fgetl(fileHandle);
dummyLine = fgetl(fileHandle);
dummyLine = fgetl(fileHandle);


dataArray = textscan(fileHandle, '%15s %15s %15s %15.7f %15.7f');

shearForce =  dataArray{1,5};
normalForce  =  dataArray{1,4};
fclose(fileHandle);

plot(shearForce,normalForce,'ko');

xlabel('Shear Force (microNewtons)');
ylabel('Normal Force (microNewtons)');
title({'Single Microwedge Limit Surface';'Cantilever 629a03 Sample SWS6';'20080823_sws6_ls'},'Interpreter','None');

axis([0 10 -5 0.5]);
x = get(gca,'XLim');
y = get(gca,'YLim');
grid on;
axis(gca,[x,y]);
line(x,[0 0],[0 0],'Color','k','LineWidth',2);
line([0 0],y,[0 0],'Color','k','LineWidth',2);

formatPlot(gcf,gca,'Times New Roman',24);
plotFilename = 'limitSurface';
printPlot(gcf,plotFilename,8,6);
