quartercar

%Undersök stabilitet av systemet för olika steglängder h

%För varje ekvation måste h<-2Re(r)/r^2 (r=egenvärde)
%Största tillåtna för systemet = minsta av dessa

%Finn max_h
lambda = eig(A);
h_vektor = zeros(length(lambda), 1);
for i = 1:length(lambda)
    h_i = (-2) * real(lambda(i)) / (abs(lambda(i)))^2;
    h_vektor(i) = h_i;
end

max_h = min(h_vektor);
disp('Största tillåtna h-värdet för konvergens är:')
disp(max_h)

%Jämför med olika multiplar av max_h
subplot(4, 1, 1); %0.9*h_max
E1 = Euler(f, [0 5], [0 0 0 0], 0.9*max_h);
plot(E1(1,:), E1(2:3, :))

subplot(4, 1, 2); %1*h_max
E2 = Euler(f, [0 5], [0 0 0 0], max_h);
plot(E2(1,:), E2(2:3, :))

subplot(4, 1, 3); %1.1*h_max
E3 = Euler(f, [0 5], [0 0 0 0], 1.1*max_h);
plot(E3(1,:), E3(2:3, :))

subplot(4, 1, 4); %1.5*h_max
E4 = Euler(f, [0 5], [0 0 0 0], 1.5*max_h);
plot(E4(1,:), E4(2:3, :))

