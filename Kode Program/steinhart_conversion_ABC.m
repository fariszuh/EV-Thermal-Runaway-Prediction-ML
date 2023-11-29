%% https://aleksandarhaber.com/calibration-of-thermistors-conversion-of-readings-into-temperature/

clear,pack,clc
% data taken from: https://www.digikey.com/en/products/detail/ametherm/ACC101/5967501?s=N4IgTCBcDaIIYFsCmAXAFkgTggBHAxvgIwAMRO6WCAlgM4oD2mIAugL5A
R = [75780, 39860, 21860, 12460, 7352.8, 4481.5, 2812.8, 2252, 1814.4, 1199.6, 811.40, 560.30, 394.55, 282.63, 206.13, 152.75, 114.92, 87.671, 67.77, 52.983, 41.881];
T =273.15+[-40,-30,-20,-10,0,10,20,25,30,40,50,60,70,80,90,100,110,120,130,140,150];
 
%T=T(6:end)
%R=R(6:end)
 
plot(R,T)
 
% getting the calibration constants:a,b,c
% 1/T=a+b*log(R)+c*(log(R))^3
% y=a+b*x+c*x^3
% x=log(R)
% y=1/T
% Steinhart–Hart equation
%https://en.wikipedia.org/wiki/Thermistor
 
x=log(R)
z=1./T
s1=numel(R)
 
for i=1:s1
    A(i,1)=1
    A(i,2)=x(i)
    A(i,3)=x(i)^3
end
 
parameters=inv(A'*A)*A'*z'