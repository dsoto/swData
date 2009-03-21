
load('lsPoints.log');
plot(lsPoints(:,5),lsPoints(:,4),'ko');

xlabel('Shear Force (microNewtons)');
ylabel('Normal Force (microNewtons)');
title('Single Microwedge Limit Surface');

axis([0 10 -5 0.5]);
x = get(gca,'XLim');
y = get(gca,'YLim');
grid on;
axis(gca,[x,y]);
line(x,[0 0],[0 0],'Color','k','LineWidth',2);
line([0 0],y,[0 0],'Color','k','LineWidth',2);

formatPlot(gcf,gca,'Times New Roman',24);
plotFilename = 'SWS_6_limitSurface';
printPlot(gcf,plotFilename,8,6);
