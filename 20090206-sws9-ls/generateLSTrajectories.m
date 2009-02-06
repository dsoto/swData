% generateLSTrajectories.m
% this script creates trajectories to test 
% the limit surface of a single microwedge

% modified - 11 December 2008 09:26:05 PST

% LS = Limit Surface
% p = nominal preload (micron)
% a = angle of pulloff (degree)
% angle of pulloff is measured from horizontal (0 deg is drag)
% v = velocity of pulloff (micron/second)

formatString = 'LS_p%02.0f_a%02.0f_v%02.0f';

preloadMicron = [30:1:35];
angleDegree = [0:1:10 20:10:90];
angleRadian = angleDegree * pi / 180;
drag = 80;
velocityMicronPerSecond = [20 20 100 100];

for i = 1:length(preloadMicron)
	for j = 1:length(angleDegree)
		depth = preloadMicron(i);
		angle = angleRadian(j);
		% here we check if the pulloff will cause negative values
		if (depth-drag*sin(angle) >= 0)
			vertices = [0                       0; ...
									depth                   0; ...
									depth - drag*sin(angle) drag*cos(angle); ...
									0                       drag*cos(angle); ...
									0                       0];
		else
			vertices = [0                       0; ...
									depth                   0; ...
									0                       drag*cos(angle); ...
									0                       drag*cos(angle); ...
									0                       0];
		end		
		filename = sprintf(formatString, preloadMicron(i), ...
			angleDegree(j), velocityMicronPerSecond(2));
		generateTrajectory(vertices, velocityMicronPerSecond, filename);
	end
end
