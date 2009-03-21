function plot_handle = plotTrajectory ( filename, figureHandle, axesHandle );
	%filename   data file from stage
	%axesHandle plot handle for location of plot

data = load ( filename );
[time dy dy dz ax ay az fx fy fz mx my mz] = getTraces(data);

plot ( axesHandle, ay, az, 'r' );
axis ( [ -1.1 1.1 -0.5 1.1 ] );
title  ( axesHandle, 'Trajectory' );
xlabel ( axesHandle, 'Shear Direction (mm)');
ylabel ( axesHandle, 'Normal Direction (mm)');
formatPlot( figureHandle, axesHandle, 'Times New Roman', 24 );







