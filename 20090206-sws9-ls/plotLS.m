% open file
% strip first three lines
% dump into array

dataFileName = ('20090130-sws7-ls.data');
fileHandle = fopen(dataFileName,'r');
dummyLine = fgetl(fileHandle);
dummyLine = fgetl(fileHandle);
dummyLine = fgetl(fileHandle);


%dataArray = textscan(fileHandle, ... 
%            '%20s %20s %15s %15s %15s %15.3f %15.3f %15.3f');
dataArray = textscan(fileHandle, ... 
            '%s%s%s%s%s%f%f%f');

shearForce =  dataArray{1,7};
normalForce  =  dataArray{1,6};
fclose(fileHandle);

plot(shearForce,normalForce,'ko');

xlabel('Shear Force (microNewtons)');
ylabel('Normal Force (microNewtons)');
title({'Single Microwedge Limit Surface'; ...
       'Cantilever 529b02 Sample sws9';... 
       '20090206-sws9-ls'}, ...
       'Interpreter','None');

%axis([0 20 -5 0.5]);
x = get(gca,'XLim');
y = get(gca,'YLim');
grid on;
axis(gca,[x,y]);
line(x,[0 0],[0 0],'Color','k','LineWidth',2);
line([0 0],y,[0 0],'Color','k','LineWidth',2);

formatPlot(gcf,gca,'Times New Roman',24);
plotFilename = 'limitSurface';
printPlot(gcf,plotFilename,8,6);
