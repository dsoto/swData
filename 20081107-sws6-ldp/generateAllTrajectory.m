% generates set of trajectory files
% for LDP on dual axis cantilever setup

% functions called
% generatePointsLDP.m

% this trajectory set is for 20081107-1 data set

% ldp preload drag angle velocity
formatString = 'LDP_p%02.0f_d%02.0f_a%02.0f_v%02.0f';

preloadMicron = [80:1:100];
angleDegree = [0];
angleRadian = angleDegree * pi / 180;
drag = 80;
velocity = [20  10 100 100; ...
						20  20 100 100; ...
            20  50 100 100; ...
            20 100 100 100];
numVelocity = size(velocity,1);
count = 0;
numFiles = length(preloadMicron) * length(angleDegree) * numVelocity;
for i = 1:length(preloadMicron)
	for j = 1:length(angleDegree)
		for k = 1:numVelocity
				count = count + 1;
				depth = preloadMicron(i);
				angle = angleRadian(j);
				dragVelocity = velocity(k,2);
				vertices = [0                       0; ...
										depth                   0; ...
										depth - drag*sin(angle) drag*cos(angle); ...
										0                       drag*cos(angle); ...
										0                       0];
				fileName = sprintf(formatString, depth, drag, angle, dragVelocity);
				fprintf('Processing File %d of %d : % 10s\n',count,numFiles,fileName);
				generateTrajectory(vertices, velocity(k,:), fileName);
			end	
	end
end
