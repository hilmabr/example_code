
function Answer = implicita_trapetsmetoden(A, g, t_span, y0, h)
    %Löser Implicita Trampetsmetoden
    n = (t_span(2) - t_span(1))/h;
    t = (t_span(1) + h * (0:n));
    langd = max(length(y0));
    y = zeros(langd, n + 1);
    y(:, 1) = y0;
    for i = 1:n
        y(:, i+1) = (eye(langd) - h/2 * A)\(y(:, i) + h/2 * (A*y(:, i) + g(t(i)) + g(t(i + 1))));
    end
    Answer = [t; y];
end