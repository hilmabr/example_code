#Komplett bild
#Sätt ihop alla ovanstående funktioner till en bild. Bilden ska innehålla minst en av varje.
#Ett minimalt exempel är att dela in bilden i 2 rektanglar för himmel och gräsig mark,
#rita en gul sol, ett hus med triangeltak, en ram som ett fönster, en rektangel som en dörr,
#en gran på tomten. Om du vill göra en mer avancerad bild så är ska vi inte begränsa din
#kreativitet, men se till att du skulle våga visa den för en arbetsgivar

# Impoprtera
import math
from tkinter import *
import itertools as it

# Fönsterstorlek
WIDTH = 800
HEIGHT = 600


# Definierar x- och y-koordinater som andel av skärmen. Konverterar värdet av
# koordinaten till ett visst antal pixlar in på skärmen.
def n_t_p(n: float) -> int:
    return int(n * WIDTH)


# Pixel -> andel av skärmen
def p_t_n(p: int) -> float:
    return p / WIDTH


# Triangelfunktioner ----------------------------------
# Sträcka mellan 2 godtyckliga punkter
def sträcka_2_punkter(punkt1: tuple[float, float], punkt2: tuple[float, float]):
    x_koord = [n_t_p(punkt1[0]), n_t_p(punkt2[0])]
    y_koord = [n_t_p(punkt1[1]), n_t_p(punkt2[1])]
    sträcka = math.sqrt((max(x_koord) - min(x_koord))**2 + (max(y_koord) - min(y_koord))**2)
    return sträcka

# Beräkna area av 3 punkter
def a_av_3_punkter(pr1: tuple[float, float], pr2: tuple[float,float], pr3: tuple[float, float]):
    a = sträcka_2_punkter(pr1, pr2)
    b = sträcka_2_punkter(pr1, pr3)
    c = sträcka_2_punkter(pr2, pr3)
    s = (a + b + c)/2
    A = math.sqrt(abs(s*(s-a)*(s-b)*(s-c)))
    return A

# Kolla om en punkt är i triangeln
def är_punkt_inne(p: tuple[float, float], p1: tuple[float, float], p2: tuple[float,float], p3: tuple[float, float]):
    A_tot = a_av_3_punkter(p1, p2, p3)
    A1 = a_av_3_punkter(p, p2, p3)
    A2 = a_av_3_punkter(p, p1, p3)
    A3 = a_av_3_punkter(p, p1, p2)
    if abs(A_tot - A1 - A2 - A3) < 0.0001:
        return True
    else:
        return False 

# Definierar triangelfunktionen
def triangel(img, pf1: tuple[float, float], pf2: tuple[float,float], pf3: tuple[float, float], color: str="#000000"):
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            p = (p_t_n(x), p_t_n(y))
            if är_punkt_inne(p, pf1, pf2, pf3) == True:
                img.put(color, (x, y))
            else:
                pass
# --------------------------------------

# Rektangel!
def rektangel(img, upper_left: tuple[float, float], lower_right: tuple[float, float], color: str="#B8860B"):
    for y in range(n_t_p(upper_left[1]), n_t_p(lower_right[1])):
        for x in range(n_t_p(upper_left[0]), n_t_p(lower_right[0])):
            img.put(color, (x, y))

# Cirkel!
def cirkel(img, r:float, mittpunkt: tuple[float, float], color: str="#000000"):
    x_mitt = n_t_p(mittpunkt[0])
    y_mitt = n_t_p(mittpunkt[1])
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if ((x - x_mitt)**2 + (y - y_mitt)**2) <= n_t_p(r)**2:
                img.put(color, (x, y))
            else:
                pass

# Ram
def ram(img, tj: float, upper_left: tuple[float, float], lower_right: tuple[float, float], color: str="#000000"):
    x1 = n_t_p(upper_left[0])
    x2 = n_t_p(lower_right[0])
    y1 = n_t_p(upper_left[1])
    y2 = n_t_p(lower_right[1])
    tj_pix = n_t_p(tj)
    for x in range(x1, x2):
        for y in it.chain(range(y1, y1 + tj_pix), range(y2 - tj_pix, y2)):
            img.put(color, (x, y))
    for y in range(y1, y2):
        for x in it.chain(range(x1, x1 + tj_pix), range(x2 - tj_pix, x2)):
            img.put(color, (x, y))

# Gran
def gran(img, hörn: tuple[float, float], höjd, bredd, color: str="#000000"):
    b = n_t_p(bredd)
    h = n_t_p(höjd)
    x_hörn = n_t_p(hörn[0])
    y_hörn = n_t_p(hörn[1])
    rektangel(img, (p_t_n(x_hörn + (0.45 * b)), p_t_n(y_hörn + (0.9 * h))), (p_t_n(x_hörn + (0.55 * b)), p_t_n(y_hörn + h)), "#5E2612")
    for i in range(0, 3):
        p1 = (p_t_n(x_hörn + (b * 0.5)), p_t_n(y_hörn + (i * 0.3 * h)))
        p2 = (p_t_n(x_hörn), p_t_n(y_hörn + ((i + 1)* 0.3 * h)))
        p3 = (p_t_n(x_hörn + b), p_t_n(y_hörn + ((i + 1)* 0.3 * h)))
        triangel(img, p1, p2, p3, color)


# Definierar ram och bakgrund. Ritar bild genom att anropa funktioner.
def main():
    # Förbereder allt.
    window = Tk()
    canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#27408B")
    canvas.pack()
    img = PhotoImage(width=WIDTH, height=HEIGHT)
    canvas.create_image((WIDTH / 2, HEIGHT / 2), image=img, state="normal")
    # Under detta anropas funktioner för att rita.
    # Gräs
    rektangel(img, (0, 0.5), (1, 1), "#556B2F")
    # Huskropp
    rektangel(img, (0.6, 0.4), (0.9, 0.6), "#8B3626")
    ram(img, 0.005, (0.6, 0.395), (0.9, 0.6), "#5E2612")
    # Tak
    triangel(img, (0.57, 0.4), (0.75, 0.25), (0.93, 0.4), "#5E2612")
    # Dörr
    rektangel(img, (0.8, 0.5), (0.85, 0.6), "#8B5742")
    ram(img, 0.005, (0.8, 0.5), (0.85, 0.6), "#5E2612")
    # Handtag
    cirkel(img, 0.0045, (0.815, 0.56), "#5E2612")
    # Innanför fönster
    rektangel(img, (0.64, 0.45), (0.77, 0.55), "#36648B")
    # Husfönster
    ram(img, 0.005, (0.7, 0.45), (0.77, 0.55), "#5E2612")
    ram(img, 0.005, (0.64, 0.5), (0.77, 0.55), "#5E2612")
    ram(img, 0.005, (0.64, 0.45), (0.77, 0.55), "#5E2612")
    # Måne
    cirkel(img, 0.075, (0.12, 0.12), "#CDBA96")
    # Träd
    gran(img, (0.1, 0.2), 0.3, 0.2, "#006400")
    gran(img, (0.375, 0.25), 0.25, 0.15, "#006400")
    # Ändra ej efter detta.
    mainloop()


if __name__ == '__main__':
    main()
