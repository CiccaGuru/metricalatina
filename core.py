## VERSI DISPONIBILI:
##      ESAMETRO
##      PENTAMETRO
##      ASCLEPIADEO MAGGIORE
##      ENDECASILLABO FALECIO
##      ENDECASILLABO SAFFICO
##      TRIMETRO GIAMBICO SCAZONTE
##      GLICONEO
##      FERECRATEO
##      ADONIO


import re
from copy import copy

def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in range(len(lst)-n+1))

class VersoIncompatibile(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Verso:
    vocali = "aeiouyAEIOUY"
    consonanti = "bcdfghjklmnpqrstvxzBCDFGHJKLMNPQRSTVXZ"
    mute = "bpcgdtfBPCGTD"
    liquide = "rlRL"
    desinenzeSeconda = ["us", "i", "um", "o", "e","orum","is","os"]
    dittonghi = ["ae", "au", "oe", "eu"]
    dittongoEi = ["hei","dein","deinde","proin","proinde"]
    dittongoUi = ["hui","cui","huic"]
   
    def __init__(self, verso):
        self.versoOriginale = verso.strip()
        self.verso = ""
        self.sillabe = []
        self.quantita = []
        self.accenti =  []
        self.lunghezze = []
        self.dove_h = []
        self.dove_j = []
        self.dove_m = []
        self.dove_x = []
        self.soluzioni = []
        
    def __str__(self):
        return "-".join(self.versoSillabato)
    
    def lunghePrecedenti(self, quantita, index):
        count = 0
        index = index - 1
        if index == 0:
            return 1
        if index < 0:
            return -1
        while quantita[index] == 1 and index >= 0:
            count += 1
            index -= 1
        return count

    def __contains_sublist(self, lst, sublst):
        n = len(sublst)
        return any((sublst == lst[i:i+n]) for i in range(len(lst)-n+1))

    def dividiInSillabe(self):

        verso = self.versoOriginale
        verso = re.sub("[^a-zA-Z ]", "", verso)
        
        self.dove_h = [m.start() for m in re.finditer('h', verso)]
        self.dove_h = [self.dove_h[x] - x for x in range(0, len(self.dove_h))]
        verso = re.sub("h", "", verso)
        
        self.dove_m = [m.start() for m in re.finditer("m ["+self.vocali+"]", verso)]
        self.dove_m = [self.dove_m[x] - x for x in range(0, len(self.dove_m))]
        verso = re.sub("m ["+self.vocali+"]", lambda x:x.group(0).replace('m',''), verso)

        self.dove_x = [m.start() for m in re.finditer('x', verso)]
        self.dove_x = [self.dove_x[x] + x for x in range(0, len(self.dove_x))]
        verso = re.sub("x", "cs", verso)

        self.dove_j = [m.start() + 2 for m in re.finditer("[^u]["+self.vocali+" ][iI]["+self.vocali+"]", verso)]
        self.dove_j = [self.dove_j[x] - x for x in range(0, len(self.dove_j))]
        verso = re.sub("[^u]["+self.vocali+" ][iI]["+self.vocali+"]", lambda x:x.group(0).replace('i','j').replace('I', "J"), verso)

        ##self.dove_j.extend([m.start() + 2 for m in re.finditer("[^u]["+self.vocali+"n]i["+self.vocali+"]", verso)])
        ##verso = re.sub("[^u]["+self.vocali+"n]i["+self.vocali+"]", lambda x:x.group(0).replace('i','j'), verso)

        if verso[0]=="i" and verso[1] in self.vocali:
            self.dove_j.append(0)
            verso = "j"+verso[1:]

        verso = verso.split()
        self.lunghezze = [len(x)-1 for x in verso]
        for x in range(1,len(self.lunghezze)):
            self.lunghezze[x]+=self.lunghezze[x-1]+1
        for x in range(0, len(self.lunghezze)):
            self.lunghezze[x]-=len(verso[x])-1
            
        verso ="".join(verso)
        self.verso = verso
        i = 1
        while i<(len(verso)-1):
            l = verso[i]
            if verso[i] in self.consonanti:
                if verso[i-1] in self.consonanti:
                        if (verso[i-1] in self.mute and verso[i] in self.liquide ) and not i in self.lunghezze or i == 1:
                            self.sillabe.append(i-2 +1)
                        else:
                            self.sillabe.append(i-1 +1)
                        while(verso[i] in self.consonanti):
                                i+=1
                elif verso[i-1] in self.vocali and verso[i+1] in self.vocali:
                    self.sillabe.append(i-1 +1)
            if verso[i] in self.vocali:
                if verso[i-1] in self.vocali:
                    if ((not (verso[i-1]+verso[i]).lower() in self.dittonghi) and not \
                            (verso[i-1] in "uU" and verso[i-2] in "cqCQ") and not \
                            (verso[i-1] in "uU" and verso[i-2] in "gG" and verso[i-3] in "nN" ))and not \
                            i in self.lunghezze :
                         self.sillabe.append(i-1 +1)
            i+=1
        if verso[-1] in self.vocali and verso[-2] in self.vocali and ((not (verso[i-1]+verso[i]).lower() in self.dittonghi) and not \
                            (verso[i-1] in "uU" and verso[i-2] in "cqCQ") and not \
                            (verso[i-1] in "uU" and verso[i-2] in "gG" and verso[i-3] in "nN" ))and not \
                            i in self.lunghezze :
            self.sillabe.append(-1)

        self.__mostraSillabe()
    
    def __mostraSillabe(self):
        risultato = []
        p = 0;
        for x in self.sillabe:
            risultato.append(self.verso[p:x])
            p = x
        risultato.append(self.verso[p:(len(self.verso))])
        self.versoSillabato = risultato
        return
        
    def ripristina(self, accenti):
        verso = self.versoSillabato[:]
        i = 0;
        while i<len(accenti):
            if accenti[i]:
                if 'Ae' in verso[i]:
                    verso[i] = verso[i].replace("Ae", "Àe", 1)
                elif 'Eu' in verso[i]:
                    verso[i] = verso[i].replace("Au", "Àu", 1)
                elif 'Oe' in verso[i]:
                    verso[i] = verso[i].replace("Oe", "Òe", 1)
                elif 'Eu' in verso[i]:
                    verso[i] = verso[i].replace("Eu", "Èu", 1)
                elif 'A' in verso[i]:
                    verso[i] = verso[i].replace("A", "À", 1)
                elif 'E' in verso[i]:
                    verso[i] = verso[i].replace("E", "È", 1)
                elif 'I' in verso[i]:
                    verso[i] = verso[i].replace("I", "Ì", 1)
                elif 'O' in verso[i]:
                    verso[i] = verso[i].replace("O", "Ò", 1)
                elif 'U' in verso[i]:
                    verso[i] = verso[i].replace("U", "Ù", 1)
                elif 'Y' in verso[i]:
                    verso[i] = verso[i].replace("Y", "Ý", 1)
                elif 'ae' in verso[i]:
                    verso[i] = verso[i].replace("ae", "àe", 1)
                elif 'eu' in verso[i]:
                    verso[i] = verso[i].replace("eu", "èu", 1)
                elif 'oe' in verso[i]:
                    verso[i] = verso[i].replace("oe", "òe", 1)
                elif 'Cui' in verso[i]:
                    verso[i] = verso[i].replace("Cui", "Cùi", 1)
                elif 'cui' in verso[i]:
                    verso[i] = verso[i].replace("cui", "cùi", 1)
                elif 'a' in verso[i]:
                    verso[i] = verso[i].replace("a", "à", 1)
                elif 'e' in verso[i]:
                    verso[i] = verso[i].replace("e", "è", 1)
                elif 'i' in verso[i]:
                    verso[i] = verso[i].replace("i", "ì", 1)
                elif 'o' in verso[i]:
                    verso[i] = verso[i].replace("o", "ò", 1)
                elif 'u' in verso[i]:
                    verso[i] = verso[i].replace("u", "ù", 1)
                elif 'y' in verso[i]:
                    verso[i] = verso[i].replace("y", "ý", 1)
                
            i+=1
        unito_dopo = "".join(verso)

        i = 0
        unito_lunghezze = ""
        while i < len(unito_dopo):
          if i in self.lunghezze and i>0:
              unito_lunghezze += " "
          unito_lunghezze += unito_dopo[i]
          i+=1
        
        i = 0
        
        unito_j = ""
        while i < len(unito_lunghezze):
            if i in self.dove_j:
                unito_j += "i"
            else:
                unito_j += unito_lunghezze[i]
            i+=1
            
        i = 0
        unito_x = ""
        while i < len(unito_j):
            if i in self.dove_x:
              unito_x += "x"
              i += 1
            else:
                unito_x += unito_j[i]
            i+=1

        i = 0
        unito_m = ""
        while i < len(unito_x):
            if i in self.dove_m:
              unito_m += "m"
            unito_m += unito_x[i]
            i+=1

        i = 0
        unito_h = ""
        print(self.dove_h)
        while i < len(unito_m):
            print(unito_h + "\t" + str(i))
            if i in self.dove_h:
              unito_h += "h"
            unito_h += unito_m[i]
            i+=1   
        return unito_h


class Esametro(Verso):
    def __init__(self, verso):
        super().__init__(verso)
        self.versoOriginale = verso

    def accenta(self, quantita):
        accenti = [0 for x in quantita]
        accenti[0] = 1
        accenti[-2] = 1
        accenti[-5] = 1
        i = 1
        while i<len(self.quantita)-2:
            if quantita[i] == 1:
                if quantita[i+1] == 0:
                    accenti[i] = 1
                if quantita[i+1] == 1:
                    if self.lunghePrecedenti(quantita, i) % 2 == 0:
                        accenti[i] = 1
            i+=1
        return accenti

    def __coerente(self):
        a = self.accenta(self.quantita)
        return not contains_sublist(self.quantita, [1, 0, 1]) and a.count(1) == 6 and not contains_sublist(a, [1,1]) and not contains_sublist(a, [0,0,0])

         
    def __poniLunghezze(self):
        quantita = self.quantita
        #print(lunghezze)
        if quantita.count(-1) == len(quantita):
            quantita[0]=1
            quantita[-1]=1
            quantita[-2]=1
            quantita[-3]=0
            quantita[-4]=0
            quantita[-5]=1
        i=1
        while i<len(self.versoSillabato)-1:
            if self.versoSillabato[i][-1] in self.consonanti:
                quantita[i] = 1
            for s in self.dittonghi:
                dove = self.versoSillabato[i].find(s)
                if dove>0:
                    pos = len("".join(self.versoSillabato[:i])) + dove +1
                    if not pos in self.lunghezze:
                        quantita[i]=1
            i+=1
            
        i=1
        while i<len(self.versoSillabato)-2:
            if quantita[i-1] == 1 and quantita[i+1]==1:
                 quantita[i] = 1
            i += 1

        i=2
        while i<len(self.versoSillabato)-2:
            if quantita[i-2] == 1 and quantita[i-1]==0:
                 quantita[i] = 0
                 quantita[i+1] = 1
            i+=1

        if quantita[2] == 0:
            quantita[1]=0;

        if quantita[-8] == 1 and quantita[-7] == 0 and quantita[-9] == 1:
            quantita[-10] = 1;
        self.quantita = quantita

    def risolvi(self):
        self.versoSillabato = [x for x in self.versoSillabato if x != ""]
        self.quantita = [-1 for x in range(0, len(self.versoSillabato))]
        self.risolvi_ricorsivo()
        self.soluzioni = list(set(map(tuple, self.soluzioni)))
        accentati = [self.accenta(x) for x in self.soluzioni]
        ripristinati = [self.ripristina(x) for x in accentati]
        return ripristinati
    
    def risolvi_ricorsivo(self):
        self.__poniLunghezze()
        if self.quantita.count(-1) == 0:
            if self.__coerente():
                self.soluzioni.append(self.quantita)
            return
        indice = self.quantita.index(-1)
        listaA = self.quantita[:]
        listaB = self.quantita[:]
        listaA[indice] = 0
        listaB[indice] = 1
        self.quantita = listaA[:]
        self.risolvi_ricorsivo()
        self.quantita = listaB[:]
        self.risolvi_ricorsivo()

class Pentametro(Verso):
    
    def __init__(self, verso ):
        super().__init__(verso)
        self.versoOriginale = verso
        self.numeroSillabe = 12

    def dividiInSillabe(self):
        super().dividiInSillabe()
        print(self.sillabe)
        print(len(self.sillabe))
        if len(self.sillabe)<11:
            raise VersoIncompatibile("Verso non compatibile!")

    def risolvi(self):
        self.versoSillabato = [x for x in self.versoSillabato if x != ""]
        print(self.versoSillabato)
        self.quantita = [-1 for x in range(0, len(self.versoSillabato))]
        self.poniLunghezze()
        self.soluzioni = list(set(map(tuple, self.soluzioni)))
        accentati = [self.accenta(x) for x in self.soluzioni]
        ripristinati = [self.ripristina(x) for x in accentati]
        return ripristinati
        
    def poniLunghezze(self):
        self.quantita = [-1 for x in range(0,len(self.versoSillabato))]
        self.quantita[0]=1
        self.quantita[-1]=1
        self.quantita[-2]=0
        self.quantita[-3]=0
        self.quantita[-4]=1
        self.quantita[-5]=0
        self.quantita[-6]=0
        self.quantita[-7]=1
        self.quantita[-8]=1
        i=1
        while i<len(self.versoSillabato)-8:
            if self.versoSillabato[i][-1] in self.consonanti:
                self.quantita[i] = 1
            for s in self.dittonghi:
                dove = self.versoSillabato[i].find(s)
                if dove>0:
                    pos = len("".join(verso[:i])) + dove +1
                    if not pos in self.lunghezze:
                        self.quantita[i]=1
            i+=1
            
        i=1
        while i<len(self.versoSillabato)-8:
            if self.quantita[i-1] == 1 and self.quantita[i+1]==1:
                 self.quantita[i] = 1
            i += 1
            
        i=2
        while i<len(self.versoSillabato)-8:
            if self.quantita[i-2] == 1 and self.quantita[i-1]==0:
                 self.quantita[i] = 0
                 self.quantita[i+1] = 1
            i+=1

        if self.quantita[2] == 0:
            self.quantita[1]=0;


        if self.quantita.count(-1)==0:
            self.soluzioni.append(self.quantita)
        else:
            prima_parte = len(self.versoSillabato) - 8
            if prima_parte == 4:
                self.quantita[0]=1
                self.quantita[1]=1
                self.quantita[2]=1
                self.quantita[3]=1
                self.soluzioni.append(self.quantita)
            if prima_parte == 6:
                self.quantita[0]=1
                self.quantita[1]=0
                self.quantita[2]=0
                self.quantita[3]=1
                self.quantita[4]=0
                self.quantita[5]=0
                self.soluzioni.append(self.quantita)
            if prima_parte == 5:
                if self.quantita[1:5].count(1) == 0:
                    self.quantita[0]=1
                    self.quantita[1]=0
                    self.quantita[2]=0
                    self.quantita[3]=1
                    self.quantita[4]=1
                    self.soluzioni.append(self.quantita)
                    self.quantita[0]=1
                    self.quantita[1]=1
                    self.quantita[2]=1
                    self.quantita[3]=0
                    self.quantita[4]=0
                    self.soluzioni.append(self.quantita)
                else:
                    dove = self.quantita[1:5].index(1) +1 
                    if dove == 1 or dove == 2:
                        self.quantita[0]=1
                        self.quantita[1]=1
                        self.quantita[2]=1
                        self.quantita[3]=0
                        self.quantita[4]=0
                        self.soluzioni.append(self.quantita)
                    if dove ==3 or dove == 4:
                        self.quantita[0]=1
                        self.quantita[1]=0
                        self.quantita[2]=0
                        self.quantita[3]=1
                        self.quantita[4]=1
                        self.soluzioni.append(self.quantita)
                    
    def accenta(self, verso):
        accenti = [0 for x in range(0, len(verso))]
        accenti[0] = 1
        accenti[-1] = 1
        accenti[-4] = 1
        accenti[-7] = 1
        accenti[-8] = 1
        if(verso[1] == 1):
            accenti[2] = 1
        else:
            accenti[3] = 1
        return accenti

class VersoFisso(Verso):
    def __init__(self, verso):
        super().__init__(verso)
        self.versoOriginale = verso

    def dividiInSillabe(self):
        super().dividiInSillabe()
        self.versoSillabato = [x for x in self.versoSillabato if x != ""]
        if len(self.versoSillabato)!=len(self.accentati):
            raise VersoIncompatibile("Verso non compatibile!")

    def risolvi(self):
        ripristinati = self.ripristina(self.accentati)
        return [ripristinati]
        

class AsclepiadeoMaggiore(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [1,0,1,0,0,1,1,0,0,1,1,0,0,1,0,1]


class AsclepiadeoMinore(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [1,0,1,0,0,1,1,0,0,1,0,1]
        
    
class EndecasillaboFalecio(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [1,0,1,0,0,1,0,1,0,1,0]

class EndecasillaboSaffico(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [1,0,1,0,1,0,0,1,0,1,0]
        
class TrimetroGiambicoScazonte(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [0,1,0,1,0,1,0,1,0,1,1,0]
        
class Gliconeo(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [1,0,1,0,0,1,0,1]

class Ferecrateo(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [1,0,1,0,0,1,0]

class Adonio(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [1,0,0,1,0]

class EnneasillaboAlcaico(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [0,1,0,1,0,1,0,1,0]

class DecasillaboAlcaico(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [1,0,0,1,0,0,1,0,1,0]

class EndecasillaboAlcaico(VersoFisso):
    def __init__(self, verso):
        super().__init__(verso)
        self.accentati = [0,1,0,1,0,1,0,0,1,0,1]

def main():
    file = open("input.txt")
    elenco = file.readlines()
    elenco = [x.strip() for x in elenco]

    for versoOriginale in elenco:
        verso = EndecasillaboFalecio(versoOriginale)
        verso.dividiInSillabe()
        ##print(verso)
        soluzioni = verso.risolvi()
        if len(soluzioni) == 0:
            print("\t NESSUNA SOLUZIONE ("+str(verso)+")")
        if len(soluzioni) == 1:
            print(soluzioni[0])
        else:
            [print("\t"+str(x)) for x in soluzioni]

if __name__ == "__main__":
    main()
