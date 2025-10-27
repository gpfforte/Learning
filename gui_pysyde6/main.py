import sys
import random
from PySide6.QtGui import QAction, QStandardItem, QStandardItemModel, QImage, QPixmap
from PySide6.QtCore import Qt, QSize

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

"""
Questo script implementa un'applicazione PySide6 che dimostra vari widget e layout UI.
Presenta una finestra principale con una barra dei menu, una barra di stato e un widget a schede.
Ogni scheda mostra diverse funzionalità:
- Layout orizzontali e verticali con pulsanti.
- Un QTableWidget per visualizzare e manipolare i dati.
- Un QTableView con un QStandardItemModel per una gestione più avanzata dei dati della tabella.
- Un QTextEdit multilinea per l'inserimento di testo.

L'applicazione include anche interazioni di base come finestre di messaggio e aggiornamenti della barra di stato
basati sulle azioni dell'utente.
"""
class MainWindow(QMainWindow):
    def __init__(self, background_color=None):
        super().__init__()
        self.setWindowTitle("La mia App con i Tab")
        self.setGeometry(100, 100, 800, 600)

        if background_color:
            self.setStyleSheet(f"background-color: {background_color};")

        # --- Menu Bar ---
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")

        # File menu actions
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        open_action.triggered.connect(self.open_text_file)
        file_menu.addAction(save_action)
        save_action.triggered.connect(self.save_text_file)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Edit menu actions
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)

        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # --- Status Bar ---
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

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

        # --- Tab 5: Testo Multilinea ---
        tab_cinque = QWidget()
        layout_tab_cinque = QVBoxLayout()
        self.testo_multilinea = QTextEdit()
        self.testo_multilinea.setPlaceholderText("Inserisci il tuo testo qui...")
        layout_tab_cinque.addWidget(self.testo_multilinea)
        tab_cinque.setLayout(layout_tab_cinque)
        tabs.addTab(tab_cinque, "Testo Multilinea")

        # Connetti le azioni di modifica al QTextEdit
        cut_action.triggered.connect(self.testo_multilinea.cut)
        copy_action.triggered.connect(self.testo_multilinea.copy)
        paste_action.triggered.connect(self.testo_multilinea.paste)

        # --- Tab 6: Immagine da URL ---
        tab_sei = QWidget()
        layout_tab_sei = QVBoxLayout()
        self.image_label = QLabel("Caricamento immagine...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False) # Ensure it doesn't scale contents automatically
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) # Allow it to shrink
        layout_tab_sei.addWidget(self.image_label)
        tab_sei.setLayout(layout_tab_sei)
        tabs.addTab(tab_sei, "Immagine da URL")

        self.setCentralWidget(tabs)
        self.tabs = tabs # Make tabs an instance variable to access it in the slot
        self.tabs.currentChanged.connect(self.update_status_bar_with_tab_name)

        # Carica l'immagine locale all'avvio
        local_image_path = "nasa-october-2025-4k-3840x2160-1.webp"
        self.original_pixmap = None # Initialize original_pixmap
        try:
            image = QImage(local_image_path)
            if not image.isNull():
                self.original_pixmap = QPixmap.fromImage(image)
                self.update_image_display() # Call a new method to handle initial display and resizing
                self.status_bar.showMessage(f"Immagine '{local_image_path}' caricata con successo.", 3000)
            else:
                self.status_bar.showMessage(f"Impossibile caricare l'immagine da '{local_image_path}'.", 3000)
                self.image_label.setText(f"Errore: Impossibile caricare l'immagine da '{local_image_path}'.")
        except Exception as e:
            self.status_bar.showMessage(f"Errore nel caricamento dell'immagine locale: {e}", 3000)
            self.image_label.setText(f"Errore: {e}")

    def update_image_display(self):
        if self.original_pixmap and not self.original_pixmap.isNull():
            if self.image_label.size().width() > 0 and self.image_label.size().height() > 0:
                target_size = self.image_label.size()
            else:
                target_size = QSize(600, 400) # Default size if label is not yet laid out

            scaled_pixmap = self.original_pixmap.scaled(target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        self.update_image_display()
        super().resizeEvent(event)

    def mostra_messaggio(self):
        """Crea e mostra una messagebox con il testo del bottone che l'ha chiamata."""
        # self.sender() restituisce l'oggetto che ha emesso il segnale
        bottone_cliccato = self.sender()
        messaggio = QMessageBox(self)
        messaggio.setWindowTitle("Info Bottone")
        messaggio.setText(f"Hai cliccato il bottone: '{bottone_cliccato.text()}'")
        messaggio.exec()
        self.status_bar.showMessage(f"Ultima azione: Hai cliccato il bottone: '{bottone_cliccato.text()}'", 3000)

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
        self.status_bar.showMessage("Tabella riempita con dati casuali.", 3000)

    def pulisci_tabella(self):
        """Rimuove tutte le righe dalla tabella, lasciando gli header."""
        self.tabella.setRowCount(0)
        self.status_bar.showMessage("Tabella pulita.", 3000)

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
        QMessageBox.information(self, "Dati Selezionati", testo_messaggio)
        self.status_bar.showMessage("Selezione tabella mostrata.", 3000)

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
        self.status_bar.showMessage("Tabella (View) riempita con dati casuali.", 3000)

    def pulisci_tabella_view(self):
        """Rimuove tutte le righe dal modello."""
        self.modello.setRowCount(0)
        self.status_bar.showMessage("Tabella (View) pulita.", 3000)

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

        QMessageBox.information(self, "Dati Selezionati", testo_messaggio)
        self.status_bar.showMessage("Selezione tabella (View) mostrata.", 3000)

    def update_status_bar_with_tab_name(self, index):
        tab_name = self.tabs.tabText(index)
        self.status_bar.showMessage(f"Tab selezionata: {tab_name}", 3000)

    def open_text_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Apri File di Testo", "", "File di Testo (*.txt);;Tutti i File (*)")
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    self.testo_multilinea.setText(f.read())
                self.status_bar.showMessage(f"File '{file_name}' aperto con successo.", 3000)
            except Exception as e:
                self.status_bar.showMessage(f"Errore nell'apertura del file: {e}", 3000)

    def save_text_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Salva File di Testo", "", "File di Testo (*.txt);;Tutti i File (*)")
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write(self.testo_multilinea.toPlainText())
                self.status_bar.showMessage(f"File '{file_name}' salvato con successo.", 3000)
            except Exception as e:
                self.status_bar.showMessage(f"Errore nel salvataggio del file: {e}", 3000)

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
