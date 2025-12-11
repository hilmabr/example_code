function Answer=Euler(f, t_range, y0, h)
    %Beräkna n
    a = t_range(1);
    b = t_range(2);
    n = (b-a)/h;
    
    %skapa alla ti värden
    ti = a + h*(0:n);
    %förbered yi vektor att fyllas
    yi = zeros(max(size(y0)), max(size(ti)));
    %lägg in startvärde
    yi(:,1) = y0;
    %Euler-loop
    for i = 1:n
        yi(:, i + 1) = yi(:, i) + h*f(ti(i), yi(:, i));
    end
    Answer = [ti; yi];
end