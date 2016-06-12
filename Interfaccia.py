import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from core import *

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.sorgente = ""
        self.versiDaFare = "" 
        self.sorgente = os.getcwd()+"/input.txt"
        self.scrivi = QTextEdit()
        self.scrivi.setFixedHeight(250)
        self.risultato = QTextEdit()
        self.risultato.setFixedHeight(250)
        self.setMinimumWidth(600)
        
        scegliFileLayout = QHBoxLayout()
        scegliButton = QPushButton("Apri..")
        scegliButton.clicked.connect(self.scegliFile)
        self.tField = QLineEdit(".../input.txt")
        self.tField.textChanged.connect(self.cambiaPercorso)
        btnRisolvi = QPushButton("RISOLVI")
        btnRisolvi.clicked.connect(self.iniziaRisoluzione)
        scegliFileLayout.addWidget(scegliButton)
        scegliFileLayout.addWidget(self.tField)
        self.listaVersi = QComboBox()
        self.listaVersi.addItem("Esametro")
        self.listaVersi.addItem("Pentametro")
        self.listaVersi.addItem("Asclepiadeo maggiore")
        self.listaVersi.addItem("Asclepiadeo minore")        
        self.listaVersi.addItem("Endecasillabo falecio")
        self.listaVersi.addItem("Endecasillabo saffico")
        self.listaVersi.addItem("Trimetro giambico scazonte")
        self.listaVersi.addItem("Gliconeo")
        self.listaVersi.addItem("Ferecrateo")
        self.listaVersi.addItem("Enneasillabo alcaico")
        self.listaVersi.addItem("Decasillabo alcaico")
        self.listaVersi.addItem("Endecasillabo alcaico")
        self.listaVersi.addItem("Adonio")
        
        mainLayout = QFormLayout()
        mainLayout.addRow(QLabel("Verso/strofa"), self.listaVersi)
        mainLayout.addRow(QLabel("Scegli file"), scegliFileLayout)
        mainLayout.addRow(None, QLabel("oppure"))
        cleanLayout = QVBoxLayout()
        btnClear = QPushButton("Pulisci")
        btnClear.clicked.connect(self.pulisciTesto)
        cleanLayout.addWidget(QLabel("Scrivi testo"))
        cleanLayout.addStretch(1)
        cleanLayout.addWidget(btnClear)
        cleanLayout.setAlignment(Qt.AlignTop)
        layoutTemp = QHBoxLayout()
        layoutTemp.addLayout(cleanLayout)
        layoutTemp.addWidget(self.scrivi)
        salvaLayout = QVBoxLayout()
        btnSalva = QPushButton("Salva")
        btnSalva.clicked.connect(self.salvaRisultato)
        layoutTempSalva = QHBoxLayout()
        salvaLayout.addWidget(QLabel("Risultato"))
        salvaLayout.addStretch(1)
        salvaLayout.addWidget(btnSalva)
        salvaLayout.setAlignment(Qt.AlignTop)
        layoutTempSalva.addLayout(salvaLayout)
        layoutTempSalva.addWidget(self.risultato)
        mainLayout.addRow(layoutTemp)
        mainLayout.addRow(None, btnRisolvi)
        mainLayout.addRow(layoutTempSalva)
        self.setLayout(mainLayout)
        self.setWindowTitle("Metrica Latina")

    def salvaRisultato(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Salva file', "output.txt", "File di testo (*.txt)")
            out_file = open(fname[0],"w")
            daScrivere = self.risultato.toPlainText().replace("<font color='red'", "").replace("<font color='blue'>", "").replace("</font>","")
            out_file.write(daScrivere)
            out_file.close()
        except Exception:
            self.mostraErrore("Si è verificato un errore!")
        else:
            self.mostraErrore("Salvataggio avvenuto con successo!", 2, "Info")
        
    def cambiaPercorso(self):
        self.sorgente = self.tField.text().replace("...", os.getcwd())

    def pulisciTesto(self):
        self.scrivi.setText("")

    def mostraErrore(self, testo, tipo = 0, titolo = "Errore!"):
        msg = QMessageBox()
        if tipo == 0:
            msg.setIcon(QMessageBox.Warning)
        elif tipo == 1:
            msg.setIcon(QMessageBox.Critical)
        elif tipo == 2:
            msg.setIcon(QMessageBox.Information)
        msg.setText(testo)
        msg.setWindowTitle(titolo)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(msg.close)
        msg.exec_()


    def iniziaRisoluzione(self):
        if self.scrivi.toPlainText() != "":
            self.versiDaFare = self.scrivi.toPlainText().split("\n")
        elif self.sorgente != "":
            if(os.path.isfile(self.sorgente)):
                file = open(self.sorgente)
                self.versiDaFare = [x.strip() for x in file.readlines()]
                self.scrivi.setPlainText("\n".join(self.versiDaFare))
            else:
                self.mostraErrore("Il file selezionato non esiste! \n Scegliere un file esistente.")
                return
        else:
            self.mostraErrore("Nessuna sorgente valida selezionata. \n Scegliere una sorgente valida.")
            return
        scriviFuturo = []
        for versoOriginale in self.versiDaFare:
            if self.listaVersi.currentText() == "Esametro":
                verso = Esametro(versoOriginale)
            if self.listaVersi.currentText() == "Pentametro":
                verso = Pentametro(versoOriginale)
            if self.listaVersi.currentText() == "Endecasillabo saffico":
                verso = EndecasillaboSaffico(versoOriginale)
            if self.listaVersi.currentText() == "Adonio":
                verso = Adonio(versoOriginale)
            if self.listaVersi.currentText() == "Endecasillabo alcaico":
                verso = EndecasillaboAlcaico(versoOriginale)
            if self.listaVersi.currentText() == "Decasillabo alcaico":
                verso = DecasillaboAlcaico(versoOriginale)
            if self.listaVersi.currentText() == "Enneasillabo alcaico":
                verso = EnneasillaboAlcaico(versoOriginale)
            if self.listaVersi.currentText() == "Ferecrateo":
                verso = Ferecrateo(versoOriginale)
            if self.listaVersi.currentText() == "Gliconeo":
                verso = Gliconeo(versoOriginale)
            if self.listaVersi.currentText() == "Trimetro giambico scazonte":
                verso = TrimetroGiambicoScazonte(versoOriginale)
            if self.listaVersi.currentText() == "Endecasillabo falecio":
                verso = EndecasillaboFalecio(versoOriginale)
            if self.listaVersi.currentText() == "Asclepiadeo minore":
                verso = AsclepiadeoMinore(versoOriginale)
            if self.listaVersi.currentText() == "Asclepiadeo maggiore":
                verso = AsclepiadeoMaggiore(versoOriginale)
            try:
                verso.dividiInSillabe()
                soluzioni = verso.risolvi()
            except VersoIncompatibile:
                self.mostraErrore("Il tipo di verso selezionato non è compatibile con i versi della sorgente. \nControllare che non vi siano errori nella sorgente e che il tipo di verso selezionato sia corretto.", 1)
                self.risultato.setPlainText("")
                break
            else:
                soluzioni = [x.replace("à","<font color='red'>à</font>") for x in soluzioni]
                soluzioni = [x.replace("è","<font color='red'>è</font>") for x in soluzioni]
                soluzioni = [x.replace("ì","<font color='red'>ì</font>") for x in soluzioni]
                soluzioni = [x.replace("ò","<font color='red'>ò</font>") for x in soluzioni]
                soluzioni = [x.replace("ù","<font color='red'>ù</font>") for x in soluzioni]
                soluzioni = [x.replace("À","<font color='red'>À</font>") for x in soluzioni]
                soluzioni = [x.replace("È","<font color='red'>È</font>") for x in soluzioni]
                soluzioni = [x.replace("Ì","<font color='red'>Ì</font>") for x in soluzioni]
                soluzioni = [x.replace("Ò","<font color='red'>Ò</font>") for x in soluzioni]
                soluzioni = [x.replace("Ù","<font color='red'>Ù</font>") for x in soluzioni]
                soluzioni = [x.replace("Ý","<font color='red'>Ý</font>") for x in soluzioni]
                soluzioni = [x.replace("ý","<font color='red'>ý</font>") for x in soluzioni]
                if len(soluzioni) == 0:
                    self.risultato.append("<font color='blue'>\t NESSUNA SOLUZIONE ("+str(verso)+")</font>")
                if len(soluzioni) == 1:
                    self.risultato.append(soluzioni[0])
                else:
                    [self.risultato.append("\t"+str(x)) for x in soluzioni]
                
        #self.risultato.setPlainText("\n".join(scriviFuturo))
        
    def scegliFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Apri file', "input.txt", "File di testo (*.txt)")
        self.tField.setText(fname[0].replace(os.getcwd(), "..."))
        self.sorgente = fname[0]

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    screen = Form()
    screen.show()
    sys.exit(app.exec_())
