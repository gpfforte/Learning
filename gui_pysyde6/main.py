import sys
import random
from PySide6.QtGui import QStandardItem, QStandardItemModel

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self, background_color=None):
        super().__init__()
        self.setWindowTitle("La mia App con i Tab")
        self.setGeometry(100, 100, 800, 600)

        if background_color:
            self.setStyleSheet(f"background-color: {background_color};")

        # Crea il gestore dei tab
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)

        # --- Tab 1: Layout Orizzontale ---
        tab_uno = QWidget()
        layout_orizzontale = QHBoxLayout()
        layout_orizzontale.addWidget(QLabel("Questa è un'etichetta:"))
        bottone1 = QPushButton("Bottone 1")
        bottone1.clicked.connect(self.mostra_messaggio)
        layout_orizzontale.addWidget(bottone1)
        bottone2 = QPushButton("Bottone 2")
        bottone2.clicked.connect(self.mostra_messaggio)
        layout_orizzontale.addWidget(bottone2)
        tab_uno.setLayout(layout_orizzontale)

        # --- Tab 2: Layout Verticale ---
        tab_due = QWidget()
        layout_verticale = QVBoxLayout()
        layout_verticale.addWidget(QLabel("Scegli un'opzione:"))
        opzione_a = QPushButton("Opzione A")
        opzione_a.clicked.connect(self.mostra_messaggio)
        layout_verticale.addWidget(opzione_a)
        opzione_b = QPushButton("Opzione B")
        opzione_b.clicked.connect(self.mostra_messaggio)
        layout_verticale.addWidget(opzione_b)
        opzione_c = QPushButton("Opzione C")
        opzione_c.clicked.connect(self.mostra_messaggio)
        layout_verticale.addWidget(opzione_c)
        tab_due.setLayout(layout_verticale)

        # Aggiungi i tab (ora con i loro layout e widget)
        tabs.addTab(tab_uno, "Layout Orizzontale")
        tabs.addTab(tab_due, "Layout Verticale")

        # --- Tab 3: Tabella ---
        tab_tre = QWidget()
        layout_tab_tre = QVBoxLayout()

        # Layout per i bottoni
        layout_bottoni = QHBoxLayout()
        riempi_btn = QPushButton("Riempi Tabella")
        riempi_btn.clicked.connect(self.riempi_tabella)
        pulisci_btn = QPushButton("Pulisci Tabella")
        pulisci_btn.clicked.connect(self.pulisci_tabella)
        mostra_selezione_btn = QPushButton("Mostra Selezione")
        mostra_selezione_btn.clicked.connect(self.mostra_selezione)
        layout_bottoni.addWidget(riempi_btn)
        layout_bottoni.addWidget(pulisci_btn)
        layout_bottoni.addWidget(mostra_selezione_btn)

        # Aggiungo il layout dei bottoni al layout principale del tab
        layout_tab_tre.addLayout(layout_bottoni)

        # Creo la tabella e la aggiungo al layout
        self.tabella = QTableWidget()
        layout_tab_tre.addWidget(self.tabella)

        tab_tre.setLayout(layout_tab_tre)
        tabs.addTab(tab_tre, "Tabella Dati")

        # --- Tab 4: Tabella con QTableView ---
        tab_quattro = QWidget()
        layout_tab_quattro = QVBoxLayout()

        # Layout per i bottoni
        layout_bottoni_view = QHBoxLayout()
        riempi_btn_view = QPushButton("Riempi Tabella (View)")
        riempi_btn_view.clicked.connect(self.riempi_tabella_view)
        pulisci_btn_view = QPushButton("Pulisci Tabella (View)")
        pulisci_btn_view.clicked.connect(self.pulisci_tabella_view)
        mostra_selezione_btn_view = QPushButton("Mostra Selezione (View)")
        mostra_selezione_btn_view.clicked.connect(self.mostra_selezione_view)
        layout_bottoni_view.addWidget(riempi_btn_view)
        layout_bottoni_view.addWidget(pulisci_btn_view)
        layout_bottoni_view.addWidget(mostra_selezione_btn_view)

        layout_tab_quattro.addLayout(layout_bottoni_view)

        # Creo il modello e la vista
        self.modello = QStandardItemModel()
        self.vista_tabella = QTableView()
        self.vista_tabella.setModel(self.modello)
        layout_tab_quattro.addWidget(self.vista_tabella)

        tab_quattro.setLayout(layout_tab_quattro)
        tabs.addTab(tab_quattro, "Tabella Dati (View)")

        self.setCentralWidget(tabs)

    def mostra_messaggio(self):
        """Crea e mostra una messagebox con il testo del bottone che l'ha chiamata."""
        # self.sender() restituisce l'oggetto che ha emesso il segnale
        bottone_cliccato = self.sender()
        messaggio = QMessageBox(self)
        messaggio.setWindowTitle("Info Bottone")
        messaggio.setText(f"Hai cliccato il bottone: '{bottone_cliccato.text()}'")
        messaggio.exec()

    def riempi_tabella(self):
        """Popola la tabella con 10 righe e 10 colonne di dati casuali."""
        headers = [f"Colonna {i+1}" for i in range(5)] + ["SKU", "Prezzo", "Quantità", "Categoria", "Disponibile"]
        self.tabella.setRowCount(10)
        self.tabella.setColumnCount(10)
        self.tabella.setHorizontalHeaderLabels(headers)

        for riga in range(10):
            for colonna in range(10):
                if colonna < 5: # Colonne con stringhe
                    dato = f"Dato-{riga+1}-{colonna+1}"
                elif colonna == 5: # SKU
                    dato = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
                elif colonna in [6, 7]: # Prezzo e Quantità
                    dato = str(random.randint(1, 500))
                elif colonna == 8: # Categoria
                    dato = random.choice(["Elettronica", "Casa", "Giardino"])
                else: # Disponibile
                    dato = random.choice(["Sì", "No"])
                
                item = QTableWidgetItem(dato)
                self.tabella.setItem(riga, colonna, item)
        
        self.tabella.resizeColumnsToContents()

    def pulisci_tabella(self):
        """Rimuove tutte le righe dalla tabella, lasciando gli header."""
        self.tabella.setRowCount(0)

    def mostra_selezione(self):
        """Mostra in una messagebox il valore o i valori selezionati nella tabella."""
        ranges = self.tabella.selectedRanges()
        if not ranges:
            QMessageBox.warning(self, "Errore", "Nessun elemento selezionato!")
            return

        # Analizziamo il primo range di selezione per semplicità
        selection_range = ranges[0]
        testo_messaggio = ""

        # Controlla se è una riga intera
        if selection_range.rowCount() == 1 and self.tabella.columnCount() == selection_range.columnCount():
            riga = selection_range.topRow()
            dati_riga = []
            for col in range(self.tabella.columnCount()):
                item = self.tabella.item(riga, col)
                dati_riga.append(item.text() if item else "")
            testo_messaggio = f"Riga {riga + 1} selezionata:\n" + ", ".join(dati_riga)

        # Controlla se è una colonna intera
        elif selection_range.columnCount() == 1 and self.tabella.rowCount() == selection_range.rowCount():
            colonna = selection_range.leftColumn()
            nome_colonna = self.tabella.horizontalHeaderItem(colonna).text()
            dati_colonna = []
            for riga in range(self.tabella.rowCount()):
                item = self.tabella.item(riga, colonna)
                dati_colonna.append(item.text() if item else "")
            testo_messaggio = f"Colonna '{nome_colonna}' selezionata:\n" + "\n".join(dati_colonna)

        # Altrimenti, mostra i dati delle celle selezionate
        else:
            dati_selezionati = []
            for r in range(selection_range.topRow(), selection_range.bottomRow() + 1):
                for c in range(selection_range.leftColumn(), selection_range.rightColumn() + 1):
                    item = self.tabella.item(r, c)
                    if item and item.isSelected():
                        dati_selezionati.append(item.text())
            testo_messaggio = "Valori selezionati:\n" + ", ".join(dati_selezionati)

        QMessageBox.information(self, "Dati Selezionati", testo_messaggio)

    def riempi_tabella_view(self):
        """Popola la QTableView usando un QStandardItemModel."""
        self.modello.clear()
        headers = [f"Colonna {i+1}" for i in range(5)] + ["SKU", "Prezzo", "Quantità", "Categoria", "Disponibile"]
        self.modello.setHorizontalHeaderLabels(headers)

        for riga in range(10):
            riga_items = []
            for colonna in range(10):
                if colonna < 5: # Colonne con stringhe
                    dato = f"Dato-{riga+1}-{colonna+1}"
                elif colonna == 5: # SKU
                    dato = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
                elif colonna in [6, 7]: # Prezzo e Quantità
                    dato = str(random.randint(1, 500))
                elif colonna == 8: # Categoria
                    dato = random.choice(["Elettronica", "Casa", "Giardino"])
                else: # Disponibile
                    dato = random.choice(["Sì", "No"])
                
                item = QStandardItem(dato)
                riga_items.append(item)
            self.modello.appendRow(riga_items)
        
        self.vista_tabella.resizeColumnsToContents()

    def pulisci_tabella_view(self):
        """Rimuove tutte le righe dal modello."""
        self.modello.setRowCount(0)

    def mostra_selezione_view(self):
        """Mostra in una messagebox il valore o i valori selezionati nella QTableView."""
        selection_model = self.vista_tabella.selectionModel()
        indexes = selection_model.selectedIndexes()

        if not indexes:
            QMessageBox.warning(self, "Errore", "Nessun elemento selezionato!")
            return

        testo_messaggio = ""
        # print(indexes)
        # print(indexes[0].row(), indexes[0].column())
        # print(indexes[0].data())
        # Per semplicità, controlliamo la selezione basandoci sul primo indice
        first_index = indexes[0]
        riga = first_index.row()
        colonna = first_index.column()

        # Controlla se è una riga intera
        if selection_model.isRowSelected(riga, first_index.parent()):
            dati_riga = [self.modello.item(riga, col).text() for col in range(self.modello.columnCount())]
            testo_messaggio = f"Riga {riga + 1} selezionata:\n" + ", ".join(dati_riga)

        # Controlla se è una colonna intera
        elif selection_model.isColumnSelected(colonna, first_index.parent()):
            nome_colonna = self.modello.horizontalHeaderItem(colonna).text()
            dati_colonna = [self.modello.item(riga, colonna).text() for riga in range(self.modello.rowCount())]
            testo_messaggio = f"Colonna '{nome_colonna}' selezionata:\n" + "\n".join(dati_colonna)

        # Altrimenti, mostra i dati delle celle selezionate
        else:
            dati_selezionati = []
            # Usiamo una lista di indici già recuperata
            for index in indexes:
                dati_selezionati.append(index.data())
            testo_messaggio = "Valori selezionati:\n" + ", ".join(dati_selezionati)

        QMessageBox.information(self, "Dati Selezionati", testo_messaggio)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Controlliamo se è stato passato un argomento per il colore
    colore = None
    if len(sys.argv) > 1:
        # Il primo argomento è sys.argv[1]
        # (sys.argv[0] è il nome dello script)
        colore = sys.argv[1]
        print(f"Colore di sfondo impostato a: {colore}")

    window = MainWindow(background_color=colore)
    window.show()
    sys.exit(app.exec())
