import sys
import re
from collections import Counter

class Föremål():
    def __init__(self, rad, filnamn):
        """Initialiserar föremål-objekt. Tar emot en filrad uppdelad i en lista 
        och tilldelar rätt element till rätt attribut."""
        self.namn = rad[0]
        self.kontext = rad[1]
        self.originalmuseum = rad[2]
        self.id = rad[3]
        self.antal_sökningar = rad[4]
        self.beskrivning = rad[5]
        self.filnamn = filnamn
    
    def visa_föremål(self):
        """Skriver ut objektets attribut på ett läsbart sätt"""
        print(self.namn, self.id)
        print(f"Kontext: {self.kontext}")
        if self.originalmuseum != "n.a":
            print(f"Utlånat från: {self.originalmuseum}")
        print(f"Antal sökningar: {self.antal_sökningar}")
        print(f"Beskrivning: {self.beskrivning}")

    def redigera_föremål(self, typ, ändring):
        """Redigerar beskrivning eller kontext, eller ökar antal sökningar med 1.
        Ändrar i filen och i det levande objektets attribut."""
        if typ == "k":
            index_att_ändra = 1
            self.kontext = ändring
        elif typ == "b":
            index_att_ändra = 5
            ändring_om_ej_sist_och_besk = ändring + "\n"
            self.beskrivning = ändring
        elif typ == "ökasök":
            index_att_ändra = 4
            ändring = str(int(self.antal_sökningar) + 1)
            self.antal_sökningar = ändring
        with open(self.filnamn, "r") as handle:
            rader = handle.readlines()
            nyarader = []
            for rad in rader:
                rad_som_lista = rad.split("/")
                if self.namn == rad_som_lista[0] and rader.index(rad) < (len(rader) - 1) and typ == "b":
                    rad_som_lista[index_att_ändra] = ändring_om_ej_sist_och_besk
                elif self.namn == rad_som_lista[0]:
                    rad_som_lista[index_att_ändra] = ändring
                nyrad = "/".join(rad_som_lista)
                nyarader.append(nyrad)
            with open(self.filnamn, "w+") as handle:
                for rad in nyarader:
                    handle.write(rad)
                handle.close()


class Museum():
    def __init__(self, filens_namn):
        """Skapar museum. Läser in filen och initialiserar ett föremål för varje rad.
        Föremålen läggs till i museets lista."""
        self.filnamn = filens_namn
        self.innehåll = []
        while True:
            try:
                with open(self.filnamn) as handle:
                    for row in handle:
                        row_som_lista = row.split("/")
                        row_som_lista[0] = Föremål(row_som_lista, self.filnamn)
                        self.innehåll.append(row_som_lista[0])
                    break
            except FileNotFoundError:
                with open(self.filnamn, "w") as handle:
                    handle.write("format: namn/kontext/originalmuseum/000000/antal_sökningar/beskrivning")

 ### FUNKTIONALITET ###  - - - - - - - - - - - - - - - - - - - -
    def skapa_föremål(self, namn, kontext, originalmuseum, beskrivning):
        """Tar emot attribut (utom id, som genereras) och skapar ett föremål av dem.
        Skapar en ny rad i filen och initialiserar den."""
        id_lista = ["0", "0", "0", "0", "0", "0"]
        with open(self.filnamn, "r") as handle:
            rader = handle.readlines()
            sista_raden_som_lista = rader[-1].split("/")
            nytt_föremåls_siffra = str(int(sista_raden_som_lista[3]) + 1)
            for i in range(len(nytt_föremåls_siffra)):
                id_lista[(-i)-1] = nytt_föremåls_siffra[(-i)-1]
            handle.close()
        id = "".join(id_lista)
        nyrad_som_lista = [namn, kontext, originalmuseum, id, "0", beskrivning]
        with open(self.filnamn, "a") as handle:
            handle.write("\n" + "/".join(nyrad_som_lista))
            handle.close()
        self.innehåll.append(Föremål(nyrad_som_lista, self.filnamn))

    def enkel_sök(self, typ, sökord):
        """Linjärsöker namn eller kontext-attributen hos alla föremål för ett viss sökord.
        Returnerar en lista med objekt som matchar."""
        returnerade_objekt_lista =[]
        for objekt in self.innehåll:
            if typ == "namn":
                variabel_att_checka = str.lower(objekt.namn)
            elif typ == "kontext":
                variabel_att_checka = str.lower(objekt.kontext).split(",")
            if (sökord in variabel_att_checka and typ == "kontext") or sökord == variabel_att_checka:
                if typ == "namn":
                    return([objekt])
                returnerade_objekt_lista.append(objekt)
        return(returnerade_objekt_lista)

    def besk_sök(self, ordlista: list):
        """Söker i alla objekts beskrivningar efter ett/flera sökord (lagrade i en lista).
        Returnerar en lista av de objekt som innehåller orden, i fallande ordning av antal sökord som matchar."""
        föremål_som_matchar_prel = []
        föremål_som_matchar_fin = []
        for objekt in self.innehåll:
            beskrivning_ord = list(set(list(filter(None, re.split(r'[ -.,!?*;:)(&\n]', str.lower(objekt.beskrivning))))))
            for sökord in ordlista:
                for besk_ord in beskrivning_ord:
                    if sökord == besk_ord:
                        föremål_som_matchar_prel.append(self.enkel_sök("namn", str.lower(objekt.namn))[0])
        while len(föremål_som_matchar_prel) > 0:
            vanligast = Counter(föremål_som_matchar_prel).most_common(1)[0][0]
            föremål_som_matchar_fin.append(vanligast)
            while True:
                if vanligast in föremål_som_matchar_prel:
                    föremål_som_matchar_prel.remove(vanligast)
                else:
                    break
        return föremål_som_matchar_fin

        
    def radera_föremål(self, objekt):
        """Raderar objektets motsvarande rad från filen, och tar bort objektet från museets lista.
        Dödar det levande objektet."""
        with open(self.filnamn, "r") as handle:
            rader = handle.readlines()
            handle.close()
        output_rader = []
        for rad in rader:
            är_raden_sist = 0
            rad_som_lista = rad.split("/")
            if rad_som_lista[0] != objekt.namn:
                output_rader.append(rad)
            elif rad_som_lista[0] == objekt.namn and rad == rader[-1]:
                är_raden_sist = 1
        if är_raden_sist == 1:
            nya_sista_raden_lista = list(output_rader[-1])
            for i in range(2):
                nya_sista_raden_lista.remove(nya_sista_raden_lista[-1])
            output_rader[-1] = "".join(nya_sista_raden_lista)
        with open(self.filnamn, "w+") as handle:
            for rad in output_rader:
                handle.write(rad)
            handle.close()
        for föremål in self.innehåll:
            if föremål == objekt:
                self.innehåll.remove(föremål)
                del objekt
                break
 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

 ### HJÄLPFUNKTIONER ### - - - - - - - - - - - - - - - - - - - - -
    def fortsätt_fråga(self, attribut):
        """Hjälpfunktion som fortsätter att fråga om input tills det inte innehåller ett snedstreck.
        Returnerar det första accepterade svaret."""
        while True:
            print(f"{attribut}: ")
            svar = input()
            if ("/" or "\\") in svar:
                gör_nu = str.lower(input("\n\nInput får inte innehålla snedstreck. \n\nF - Försök igen. \nAnnan tangent - Avbryt. \nVal:"))
                print("")
                if gör_nu != "f":
                    self.startmeny()
            else:
                return svar
            
    def sålla_utlånat(self, typ, objektlista: list):
        """Tar emot en lista av objekt och returnerar en lista av endast de objekt som har den önskade utlånadsstatusen
        (specificerad i typ). Behåller originalordningen."""
        outputlista = []
        if typ == "e":
            for objekt in objektlista:
                if objekt.originalmuseum == "n.a":
                    outputlista.append(objekt)
        if typ == "u":
            for objekt in objektlista:
                if objekt.originalmuseum != "n.a":
                    outputlista.append(objekt)
        elif typ == "a":
            for objekt in objektlista:
                outputlista.append(objekt)
        return(outputlista)
 #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

 ### HUBBAR TILL STARTMENYN ### - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def redigera_hub(self):
        """Kör redigera-delen av startmenyn. Frågar vilket föremål som ska redigeras och visar det. Frågar vilken del som ska
        redigeras, och vad det ska ändras till. Skickar vidare detta till redigera_föremål, som utför det.
        Använder fortsätt_fråga för att kontrollera input."""
        while True:
            föremål = str.lower(input("\nRedigera\nAnge namn: "))
            returnerad_lista = self.enkel_sök("namn", föremål)
            if returnerad_lista != []:
                print(" ")
                hittat_föremål = returnerad_lista[0]
                hittat_föremål.visa_föremål()
                typ = str.lower(input("K - Redigera kontext \nB - Redigera beskrivning \nAnnan tangent - Tillbaka\nVal: "))
                if typ == "b" or typ == "k":
                    if typ == "b":
                        ändring = self.fortsätt_fråga("\nNy beskrivning (får ej innehålla snedstreck)")
                    elif typ == "k":
                        ändring = self.fortsätt_fråga("\nSeparera med komma utan mellanslag. Får ej innehålla snedstreck. \nNy kontext")
                    hittat_föremål.redigera_föremål(typ, ändring)
                    print("\nSå här ser det ut nu: ")
                    hittat_föremål.visa_föremål()
                    input("\nTryck för att förtsätta.")
                    self.startmeny()
                else:
                    self.startmeny()
            else:
                svar = str.lower(input(f"\nFöremålet '{föremål}' kunde inte hittas. \n\nS - Sök igen. \nAnnan tangent - Gå tillbaka. \nVal: "))
                if svar != "s":
                    self.startmeny()
    
    def ta_bort_hub(self):
        """Kör ta bort-delen av startmenyn. Frågar vad som ska raderas och visar det.
        Frågar om änvändaren är säker. Aktiverar då radera_föremål. Skriver ut bekräftelsemeddelande."""
        while True:
            föremål = str.lower(input("\nTa bort\nAnge namn: "))
            returnerad_lista = self.enkel_sök("namn", föremål)
            if returnerad_lista != []:
                print("")
                hittat_föremål = returnerad_lista[0]
                hittat_föremål.visa_föremål()
                while True:
                    säker = str.lower(input("\nÄr du säker på att du vill radera detta föremål? j/n: "))
                    if säker == "j":
                        self.radera_föremål(hittat_föremål)
                        print("Föremålet har raderats.\n")
                        input("Tryck för att fortsätta.")
                        self.startmeny()
                    elif säker == "n":
                        print("Föremålet raderades inte.\n")
                        input("Tryck för att fortsätta.")
                        self.startmeny()
                    else:
                        print("Det alternativet finns inte. \n")
            else:
                svar = str.lower(input(f"\nFöremålet '{föremål}' kunde inte hittas. \n\nS - Sök igen \nAnnan tangent - Gå tillbaka. \nVal: "))
                if svar != "s":
                    self.startmeny()
    
    def nytt_objekt_hub(self):
        """Kör nytt objekt-delen av startmenyn. Samlar input, felhanterar det, och skickar det till nytt_föremål.
        Visar föremålet i databasen."""
        print("\nNytt objekt. \nNotera att inga snedstreck får inkluderas.")
        while True:
            namn = self.fortsätt_fråga("\nUnikt namn")
            if self.enkel_sök("namn", namn) != []:
                gör_nu = str.lower(input("\n Namnet finns redan. \nF - försök igen. \nAnnan tangent - Avbryt. \nVal: "))
                if gör_nu == "f":
                    break
                else:
                    self.startmeny()
            else:
                break
        kontext = self.fortsätt_fråga("\nKontext/er (separerade av komma, utan mellanslag)")
        originalmuseum = self.fortsätt_fråga("\nOriginalmuseum (om inget, ange 'n.a'):")
        beskrivning = self.fortsätt_fråga("\nBeskrivning")
        self.skapa_föremål(namn, kontext, originalmuseum, beskrivning)
        print(f"\n\nFöremålet {namn} lades till. \nDenna information lagrades: \n")
        self.innehåll[-1].visa_föremål()
        input("\nTryck för att fortsätta.")
        self.startmeny()
 #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

 ### MENYFUNKTIONER ### - - - - - - - - - - - - - - - - - - - - - -
    def startmeny(self):
        """Presenterar alternativ. Tar emot svar och aktiverar motsvarande hubfunktion.
        Promptar igen om alternativet inte finns."""
        print("\nStartmeny\nVälj ett av följande alternativ:")
        print("S - Sök... \nR - Redigera föremål \nT - Ta bort föremål \nN - Nytt föremål \nA - Avsluta \n")
        startmeny_alternativ = {
        "s": self.sökmeny,
        "a": sys.exit,
        "r": self.redigera_hub,
        "t": self.ta_bort_hub,
        "n": self.nytt_objekt_hub}

        val = str.lower(input("Val: "))
        if val in startmeny_alternativ:
            startmeny_alternativ[val]()
        else:
            print("Det valet existerar inte. \nVälj bland något av alternativen i startmenyn.\n")
            self.startmeny()


    def sökmeny(self):
        """Presenterar alternativen i sökmenyn. Frågar om utlånadsstatus som ska sökas bland.
        Ber om sökord och utför sökningen. Sållar bland lista från sökord och visar endast de objekt med önskad utlånadsstatus."""
        print("\n\nSökmeny. \nVälj bland följande alternativ.")
        val = str.lower(input("N - Namnsök \nK - Sök utifrån sammanhang \nB - Sök i beskrivningar \nAnnan tangent - Tillbaka \nVal: "))
        if val == "n" or val == "k" or val == "b":
            sökplats = str.lower(input("\nSök bland... \nE - Eget \nU - Utlånat \nA - Allt \nAnnan tagent - Tillbaka \nVal: "))
            if sökplats == "e" or sökplats == "u" or sökplats == "a":
                while True:
                    if val == "n":
                        sökord = str.lower(input(f"\nAnge namnet du vill söka efter: "))
                        resultat_prel = self.enkel_sök("namn", sökord)
                    elif val == "k":
                        sökord = str.lower(input(f"\nAnge kontexten du vill söka efter: "))
                        resultat_prel = self.enkel_sök("kontext", sökord)
                    elif val == "b":
                        söklista = str.lower(input("\nSkriv orden du vill söka efter, separerade av ett komma utan mellanslag: \nOrd: ")).split(",")
                        resultat_prel = self.besk_sök(söklista)
                    resultat_sållat = self.sålla_utlånat(sökplats, resultat_prel)
                    if resultat_prel != [] and resultat_prel != [[]] and resultat_sållat != []:
                        for objekt in resultat_sållat:
                            print("")
                            objekt.redigera_föremål("ökasök", "null")
                            objekt.visa_föremål()
                        input("\nTryck för att fortsätta.")
                        self.sökmeny()
                        break  
                    else:
                        gör_nu = str.lower(input(f"\nFöremålet kunde inte hittas. \n\nS - Sök igen. \nAnnan tangent - Tillbaka. \nVal : "))
                        if gör_nu != "s":
                            self.sökmeny()
            else:
                self.sökmeny()
        else:
            self.startmeny()
 #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                        
                        
def main():
    """Välkomstmeddelande. Initierar museet. Kör startmenyn."""
    mitt_museum = Museum("föremål.txt")
    print("\nVälkommen till museet!")
    print("Här kan du söka bland föremål, och hantera innehållet.\nAnvänd startmenyn för att navigera.")
    mitt_museum.startmeny()


main()