quartercar

%Kör funktioner
E1 = Euler(f, [0 5], [0 0 0 0], 5*10^-3);
E2 = Euler(f, [0 5], [0 0 0 0], 5*10^-4);
T = implicita_trapetsmetoden(A, g, [0 5], [0 0 0 0], 0.001);

options = odeset("RelTol",1e-6,"AbsTol",1e-7, "Refine",1);
[t, y] = ode45(f, [0.000000001 5], [0 0 0 0], options);

%Plotta hastighet av fjäder 1 och fjäder 2 över tid
subplot(4, 1, 1);
plot(E1(1, :), E1(2:3, :))
title("Euler, h = 5*10^-3")

subplot(4, 1, 2);
plot(E2(1, :), E2(2:3, :))
title("Euler, h = 5*10^-4")

subplot(4, 1, 3);
plot(T(1, :), T(2:3, :))
title("Implicita Trapetsmetoden")

subplot(4, 1, 4);
plot(t, y(:, 1:2))
title("ODE45")
