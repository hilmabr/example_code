%skapa bildmatris
img = imread("bjorn.jpeg");
gray = rgb2gray(img);
A = double(gray);

%singulärvärdesuppdela
[Y, S, X] = svd(A);

%plotta singulärvärden
s = svd(A);
figure(1)
plot(s)

%komprimeringsfunktion (endast reell matris)
function A_kompr = komprimera(X, Y, S, n)
   S_kompr = S(1:n, 1:n);
   Y_kompr = Y(:, 1:n);
   X_kompr = X(:, 1:n);
   A_kompr = Y_kompr*S_kompr*X_kompr';
end

%Olika komprimeringar av A
A1 = komprimera(X, Y, S, 5);
A2 = komprimera(X, Y, S, 20);
A3 = komprimera(X, Y, S, 60);

figure(2)
subplot(2, 2, 1)
imshow(A,[0 255])
title("Fullskalig")

subplot(2, 2, 2)
imshow(A1, [0 255])
title("s=5")

subplot(2, 2, 3)
imshow(A2, [0 255])
title("s=20")

subplot(2, 2, 4)
imshow(A3, [0 255])
title("s=60")
