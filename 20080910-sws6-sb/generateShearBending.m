% generateShearBending.m
% trajectories to test shear bending stiffness of single microwedge
% details found in lab book DRS_2008_1 pg 62-63
% 10 September 2008 12:10:19 PDT

% SB = shear bending
% x = maximum x excursion (micron)
% y = maximum y excursion (micron)
% v = velocity of loading (micron/second)

formatString = 'SB_x%02.0f_y%02.0f_v%02.0f';

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
		generatePointsLDP(vertices, velocityMicronPerSecond, trajectoryFileName);
	end
end
