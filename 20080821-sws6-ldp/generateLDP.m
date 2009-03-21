




formatString = 'LS_p%02.0f_a%02.0f_v20';

preloadMicron = [80:5:100];
angleDegree = [0:5:90];
angleRadian = angleDegree * pi / 180;
drag = 80;
velocities = [20 20 20 100];

for i = 1:length(preloadMicron)
	for j = 1:length(angleDegree)
		depth = preloadMicron(i);
		angle = angleRadian(j);
		vertices = [0                       0; ...
								depth                   0; ...
								depth - drag*sin(angle) drag*cos(angle); ...
								0                       drag*cos(angle); ...
								0                       0];
		filename = sprintf(formatString, preloadMicron(i), angleDegree(j));
		generatePointsLDP(vertices, velocities, filename);
	end
end
