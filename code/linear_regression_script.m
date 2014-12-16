X = [x ones(N,1)]; % Add column of 1's to include constant term in regression
a = regress(y,X)   % = [a1; a0]
plot(x,X*a,'r-');  % This line perfectly overlays the previous fit line