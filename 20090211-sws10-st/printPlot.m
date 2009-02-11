function output = printPlot ( figureHandle, filename, xSize, ySize )

% printPlot.m
% function output = printPlot ( figureHandle, filename, xSize, ySize )
% sets paper size and saves a copy of figureHandle
% with filename.pdf

%if nargin < 2 
%	filename = 'output_plot.pdf';
%end

% xSize = 8;
% ySize = 6;

doPrintPDF = 1;
doPrintFIG = 0;

set ( figureHandle, 'PaperUnits', 'inches' );
set ( figureHandle, 'PaperSize', [xSize ySize] );
set ( figureHandle, 'PaperPositionMode', 'manual' );
set ( figureHandle, 'PaperPosition', [0.0 0.0 xSize ySize] );

[pathstr, name, ext, versn] = fileparts(filename);

if (doPrintPDF == 1) 
	%plotFilename = strcat( pathstr, '/', name, '.pdf' );
	plotFilename = strcat( name, '.pdf' );
	saveas( figureHandle, plotFilename, 'pdf' )
end

if (doPrintFIG ==1)
	plotFilename = strcat( name, '.fig' );
	saveas( figureHandle, plotFilename, 'fig' )
end

%plotFilename = strcat( name, '.eps' );
%saveas( figureHandle, plotFilename, 'eps' )

