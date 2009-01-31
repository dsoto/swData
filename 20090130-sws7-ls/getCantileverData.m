% 11 November 2008 08:22:59 PST

function [normalStiffness, lateralStiffness, normalDisplacement, lateralDisplacement] = getCantileverData(cantileverName);
% this function takes the cantilever name from the data file 
% as an argument and returns the normal and lateral stiffnesses
% in units of N/m and returns the normal and lateral displacement
% sensitivities in units of V/um at 100x

cantileverName = lower(cantileverName);

if strcmp(cantileverName,'529b02')
	lateralStiffness    = 3.898;   % newtons per meter 
	normalStiffness     = 0.659;
	lateralDisplacement = 1.148; % volts per micron
	normalDisplacement  = 0.224;
end

if strcmp(cantileverName,'629a03')
	lateralStiffness = 0.307;   % newtons per meter 
	normalStiffness = 0.313;
	lateralDisplacement = 0.473; % volts per micron
	normalDisplacement = 0.148;
end

