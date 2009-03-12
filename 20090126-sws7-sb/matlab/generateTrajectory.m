function outputvector = generateTrajectory(verticesMicron,velocityMicronPerSecond,pathFileName);

% code to generate points for piezo movement

% verticesMicron = M by 2 list of vertices
% velocityMicronPerSecond = M-1 by 1 list of velocities
% pathFileName = file name under which points are saved


% adds quiet period of zeros to start and end of trajectory data
addTails = true;
timeTareMSec = 100;
timeSettleMSec = 100;

outdt = 1;   %time between output data points in milliseconds
acqdt = 1;    %time between acquired data points in milliseconds

numlegs = length(velocityMicronPerSecond);

path = [];
% put in initial series of zeros
numSteps = timeTareMSec / outdt;
tpath = zeros( numSteps, 2 );
path = [path; tpath];

path = [path; verticesMicron(1,:)];    %adds starting point to the path
for i = 1:numlegs  % loop through coordinates vector    
    d = sqrt( (verticesMicron(i+1,1) - verticesMicron(i,1))^2 + ...
              (verticesMicron(i+1,2) - verticesMicron(i,2))^2 );
    legtime = ( d/velocityMicronPerSecond(i) ) * 1000; %time in ms
    numsteps = ceil ( legtime / outdt );
    tpath = [ [1:numsteps]' [1:numsteps]' ];
    stepdist = (verticesMicron(i+1,:) - verticesMicron(i,:)) ./ numsteps;
    tpath(:,1) = stepdist(1) .* tpath(:,1) + verticesMicron(i,1);
    tpath(:,2) = stepdist(2) .* tpath(:,2) + verticesMicron(i,2);
    path = [path;tpath];
end

% put in trailing series of zeros
numSteps = timeSettleMSec / outdt;
tpath = zeros( numSteps, 2 );
path = [path; tpath];


% output file
outputvector = [ outdt acqdt; path ];
filename = [ pathFileName '.traj' ];
fid = fopen(filename, 'wt');
fprintf(fid, '%-6.2f\t%-6.2f\n', outputvector');
fclose(fid);

% show plot of trajectory
figure(1);
lov = size(outputvector,1);
plot(outputvector(2:lov,1),outputvector(2:lov,2),'b.');
set(gca,'XDir','reverse');
set(gca,'YDir','reverse');
shg;