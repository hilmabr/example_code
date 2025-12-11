%Ställer upp systemet
%Simulerar 2 fjädrar i dämpningssystem på ett däck av en bil ("quarter"car)

%Konstanter
m1 = 475; %kg
m2 = 53; %kg
k1 = 5400; %kg/s^2
k2 = 135000; %kg/s^2
c1 = 310; %kg/s
c2 = 1200; %kg/s
v = 65/3.6; %m/s
H = 0.24; %m
L = 1; %m

%Funktioner
function Answer = Heaviside(t,L,v)
    if t <= L/v
        Answer = 1;
    else
        Answer = 0;
    end
end

f_varden = @(t) (H/2) * (1 - cos(2 * pi * v * t/L)) * Heaviside(t,L,v);
f_varden_prick = @(t) (H * pi * v/L) * sin(2 * pi * v * t/L) * (Heaviside(t,L,v));
F = @(t) [0; 0; 0; (k2 * f_varden(t) + c2 * f_varden_prick(t))];

A = [0 0 1 0; 0 0 0 1; -k1/m1 k1/m1 -c1/m1 c1/m1; k1/m2 -(k1 + k2)/m2 c1/m2 -(c1+c2)/m2];
g = @(t) F(t)/m2;

%Systemet
f = @(t, y) A*y + g(t);