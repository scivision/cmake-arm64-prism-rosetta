function r = is_prism()
% Detecting CPU arch on Windows is non-trivial.
% Return true if running under Microsoft Prism emulation (x64 on ARM64).

r = false;

if ~ispc
  return
end

% Method 1: Check PROCESSOR_ARCHITEW6432 (set only under WoW64/Prism)
a = getenv('PROCESSOR_ARCHITEW6432');
if isempty(a)
  a = getenv('PROCESSOR_ARCHITECTURE');
end

if lower(a) ~= "amd64"
  return
end

[~, result] = system('powershell -command "(Get-CimInstance Win32_Processor).Architecture"');
i = str2double(result);  

r = i(1) == 12;

end

