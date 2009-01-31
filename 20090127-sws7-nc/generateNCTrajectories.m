% generateNCTrajectories.m
% loops to create a set of 
% trajectories to test normal compliance of single microwedge
% 17 November 2008 15:55:57 PST


% NC = normal compliance
% x = maximum x excursion (micron)
% v = velocity of loading (micron/second)
% drawing on page 82 of 2008_1

formatString = 'nc_x%02.0f_v%02.0f';

xMicron = [0:1:30];
velocityMicronPerSecond = [20 20];

for i = 1:length(xMicron)
		x = xMicron(i);
		% simple three vertex path in and out  
		vertices = [0 0; ...
								x 0; ...
								0 0];
		trajectoryFileName = ... 
			sprintf(formatString, x, velocityMicronPerSecond(1));
		generateTrajectory(vertices, velocityMicronPerSecond, trajectoryFileName);
end
