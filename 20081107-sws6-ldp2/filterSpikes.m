% filter spikes function
function forceTraceOut = filterSpikes(forceTraceIn,spikeFactor);
% look for diff that is factor of X greater than rms
% if followed by opposite diff within X% of magnitude of first
% then go back and take out point and replace with mean of neighboring points


forceTrace = forceTraceIn;

% get background for signal
rms = std(forceTrace(1:100));

derivative = abs(diff(forceTrace));

spikes = find(derivative > spikeFactor * rms);
for i = 1:length(spikes)-1
	% test if values are adjacent
	if spikes(i)==(spikes(i+1)-1)
		% remember location
		index = spikes(i);
		% use neighbors from 2 over since not all spikes are single data point
		forceTrace(index+1) = (forceTrace(index-1)+forceTrace(index+3))/2;
	% skip ahead to i+2
		end
end

forceTraceOut = forceTrace;
