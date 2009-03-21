function plot_handle = plotForceSpace ( filename, figureHandle, axesHandle );
% function plot_handle = plotForceSpace ( filename, figureHandle, axesHandle );

data = load ( filename );
[time dy dy dz ax ay az fx fy fz mx my mz] = getTraces( data );

fxBias = mean(fx(1:1000));
fyBias = mean(fy(1:1000));
fzBias = mean(fz(1:1000));
fx = fx - fxBias;
fy = fy - fyBias;
fz = fz - fzBias;

[numd, dend] = butter( 3, .02 );
fx_filt = filtfilt( numd, dend, fx );
fy_filt = filtfilt( numd, dend, fy );
fz_filt = filtfilt( numd, dend, fz );

plot( axesHandle, -fy_filt, -fz_filt, 'x' );
title  ( axesHandle, 'Force Space' );
xlabel ( axesHandle, 'Shear Force (N)');
ylabel ( axesHandle, 'Normal Force (N)');

formatPlot( figureHandle, axesHandle, 'Times New Roman', 24 );
