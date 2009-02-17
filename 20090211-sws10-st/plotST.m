% open file
% strip first three lines
% dump into array

dataFileName = ('20090211-sws10-st.data');
fileHandle = fopen(dataFileName,'r');
dummyLine = fgetl(fileHandle);
dummyLine = fgetl(fileHandle);
dummyLine = fgetl(fileHandle);


%dataArray = textscan(fileHandle, ... 
%            '%20s %20s %15s %15s %15s %15.3f %15.3f %15.3f');
dataArray = textscan(fileHandle, ... 
            '%s%s%s%s%f%f%f%f%f');

angleSlant = dataArray{1,5};
shearForce =  dataArray{1,8};
normalForce  =  dataArray{1,7};
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
