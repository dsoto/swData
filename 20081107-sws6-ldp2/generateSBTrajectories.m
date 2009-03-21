% generateNCTrajectories.m
% trajectories to test normal compliance of single microwedge
% first created 17 November 2008 15:52:53 PST

% NC = Normal Compliance
% x = maximum x excursion (micron)
% y = maximum y excursion (micron)
% v = velocity of loading (micron/second)

% i have messed this file up and need to revert it to an earlier revision


formatString = 'NC_x%02.0f_v%02.0f';

xMicron = [0:1:10];
yMicron = [10:1:20];
velocityMicronPerSecond = [20 20 20 20];

for i = 1:length(xMicron)
	for j = 1:length(yMicron)
		x = xMicron(i);
		y = yMicron(j);
		vertices = [0 0; ...
								x 0; ...
								x y; ...
								x 0; ...
								0 0];
		trajectoryFileName = ... 
			sprintf(formatString, x, y, velocityMicronPerSecond(2));
		generateTrajectory(vertices, velocityMicronPerSecond, trajectoryFileName);
	end
end
