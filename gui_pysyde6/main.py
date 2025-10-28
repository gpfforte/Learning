import sys
import random
from PySide6.QtGui import QAction, QStandardItem, QStandardItemModel, QImage, QPixmap
from PySide6.QtCore import Qt, QSize, QTimer

from PySide6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QTextEdit,
    QTimeEdit,
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
- Una scheda con Checkbox, Radiobutton, Listbox e Combobox.
- Schede aggiuntive per widget numerici, di data/ora e altri controlli.

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
        tabs.addTab(tab_uno, "Layout Orizzontale")

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
        tabs.addTab(tab_due, "Layout Verticale")

        # --- Tab 3: Tabella ---
        tab_tre = QWidget()
        layout_tab_tre = QVBoxLayout()
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
        layout_tab_tre.addLayout(layout_bottoni)
        self.tabella = QTableWidget()
        layout_tab_tre.addWidget(self.tabella)
        tab_tre.setLayout(layout_tab_tre)
        tabs.addTab(tab_tre, "Tabella Dati")

        # --- Tab 4: Tabella con QTableView ---
        tab_quattro = QWidget()
        layout_tab_quattro = QVBoxLayout()
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

        cut_action.triggered.connect(self.testo_multilinea.cut)
        copy_action.triggered.connect(self.testo_multilinea.copy)
        paste_action.triggered.connect(self.testo_multilinea.paste)

        # --- Tab 6: Immagine ---
        tab_sei = QWidget()
        layout_tab_sei = QVBoxLayout()
        self.image_label = QLabel("Caricamento immagine...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        layout_tab_sei.addWidget(self.image_label)
        tab_sei.setLayout(layout_tab_sei)
        tabs.addTab(tab_sei, "Immagine")

        # --- Tab 7: Altri Widget ---
        tab_sette = QWidget()
        layout_tab_sette = QVBoxLayout()
        checkbox_group = QGroupBox("Linguaggi di Programmazione Preferiti")
        checkbox_layout = QVBoxLayout()
        self.checkbox1 = QCheckBox("Python")
        self.checkbox1.stateChanged.connect(self.checkbox_state_changed)
        self.checkbox2 = QCheckBox("Java")
        self.checkbox2.stateChanged.connect(self.checkbox_state_changed)
        self.checkbox3 = QCheckBox("C++")
        self.checkbox3.stateChanged.connect(self.checkbox_state_changed)
        checkbox_layout.addWidget(self.checkbox1)
        checkbox_layout.addWidget(self.checkbox2)
        checkbox_layout.addWidget(self.checkbox3)
        checkbox_group.setLayout(checkbox_layout)
        layout_tab_sette.addWidget(checkbox_group)
        radio_group = QGroupBox("Sistema Operativo")
        radio_layout = QHBoxLayout()
        self.radio1 = QRadioButton("Windows")
        self.radio1.toggled.connect(self.radio_button_toggled)
        self.radio2 = QRadioButton("macOS")
        self.radio2.toggled.connect(self.radio_button_toggled)
        self.radio3 = QRadioButton("Linux")
        self.radio3.toggled.connect(self.radio_button_toggled)
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        radio_group.setLayout(radio_layout)
        layout_tab_sette.addWidget(radio_group)
        self.listbox = QListWidget()
        self.listbox.addItems(["Mela", "Banana", "Arancia", "Uva"])
        self.listbox.itemClicked.connect(self.listbox_item_clicked)
        layout_tab_sette.addWidget(self.listbox)
        self.combobox = QComboBox()
        self.combobox.addItems(["Gennaio", "Febbraio", "Marzo", "Aprile"])
        self.combobox.currentTextChanged.connect(self.combobox_text_changed)
        layout_tab_sette.addWidget(self.combobox)
        tab_sette.setLayout(layout_tab_sette)
        tabs.addTab(tab_sette, "Altri Widget")

        # --- Tab 8: Input Numerici ---
        tab_otto = QWidget()
        layout_tab_otto = QVBoxLayout()
        slider_group = QGroupBox("Slider e Dial")
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.slider_value_changed)
        slider_layout.addWidget(self.slider)
        self.dial = QDial()
        self.dial.valueChanged.connect(self.dial_value_changed)
        slider_layout.addWidget(self.dial)
        slider_group.setLayout(slider_layout)
        layout_tab_otto.addWidget(slider_group)
        spinbox_group = QGroupBox("SpinBox")
        spinbox_layout = QHBoxLayout()
        self.spinbox = QSpinBox()
        self.spinbox.valueChanged.connect(self.spinbox_value_changed)
        spinbox_layout.addWidget(QLabel("Intero:"))
        spinbox_layout.addWidget(self.spinbox)
        self.double_spinbox = QDoubleSpinBox()
        self.double_spinbox.valueChanged.connect(self.doublespinbox_value_changed)
        spinbox_layout.addWidget(QLabel("Double:"))
        spinbox_layout.addWidget(self.double_spinbox)
        spinbox_group.setLayout(spinbox_layout)
        layout_tab_otto.addWidget(spinbox_group)
        tab_otto.setLayout(layout_tab_otto)
        tabs.addTab(tab_otto, "Input Numerici")

        # --- Tab 9: Data e Ora ---
        tab_nove = QWidget()
        layout_tab_nove = QVBoxLayout()
        date_time_group = QGroupBox("Date e Time Edits")
        date_time_layout = QHBoxLayout()
        self.date_edit = QDateEdit()
        self.date_edit.dateChanged.connect(self.date_changed)
        date_time_layout.addWidget(QLabel("Data:"))
        date_time_layout.addWidget(self.date_edit)
        self.time_edit = QTimeEdit()
        self.time_edit.timeChanged.connect(self.time_changed)
        date_time_layout.addWidget(QLabel("Ora:"))
        date_time_layout.addWidget(self.time_edit)
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.dateTimeChanged.connect(self.datetime_changed)
        date_time_layout.addWidget(QLabel("Data e Ora:"))
        date_time_layout.addWidget(self.datetime_edit)
        date_time_group.setLayout(date_time_layout)
        layout_tab_nove.addWidget(date_time_group)
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.calendar_date_changed)
        layout_tab_nove.addWidget(self.calendar)
        tab_nove.setLayout(layout_tab_nove)
        tabs.addTab(tab_nove, "Data e Ora")

        # --- Tab 10: Controlli Vari ---
        tab_dieci = QWidget()
        layout_tab_dieci = QVBoxLayout()
        progress_group = QGroupBox("Barra di Avanzamento")
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        start_progress_btn = QPushButton("Avvia")
        start_progress_btn.clicked.connect(self.start_progress)
        progress_layout.addWidget(start_progress_btn)
        progress_group.setLayout(progress_layout)
        layout_tab_dieci.addWidget(progress_group)
        splitter = QSplitter(Qt.Horizontal)
        left_text = QTextEdit("Pannello Sinistro")
        right_text = QTextEdit("Pannello Destro")
        splitter.addWidget(left_text)
        splitter.addWidget(right_text)
        layout_tab_dieci.addWidget(splitter)
        tab_dieci.setLayout(layout_tab_dieci)
        tabs.addTab(tab_dieci, "Controlli Vari")

        self.setCentralWidget(tabs)
        self.tabs = tabs
        self.tabs.currentChanged.connect(self.update_status_bar_with_tab_name)

        self.load_local_image()

    def load_local_image(self):
        local_image_path = "nasa-october-2025-4k-3840x2160-1.webp"
        self.original_pixmap = None
        try:
            image = QImage(local_image_path)
            if not image.isNull():
                self.original_pixmap = QPixmap.fromImage(image)
                self.update_image_display()
                self.status_bar.showMessage(f"Immagine '{local_image_path}' caricata.", 3000)
            else:
                self.status_bar.showMessage(f"Impossibile caricare l'immagine da '{local_image_path}'.", 3000)
                self.image_label.setText(f"Errore: Impossibile caricare l'immagine.")
        except Exception as e:
            self.status_bar.showMessage(f"Errore caricamento immagine: {e}", 3000)
            self.image_label.setText(f"Errore: {e}")

    def update_image_display(self):
        if self.original_pixmap and not self.original_pixmap.isNull():
            target_size = self.image_label.size() if self.image_label.size().width() > 0 else QSize(600, 400)
            scaled_pixmap = self.original_pixmap.scaled(target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image_display()

    def mostra_messaggio(self):
        sender = self.sender()
        QMessageBox.information(self, "Info", f"Hai cliccato: '{sender.text()}'")
        self.status_bar.showMessage(f"Azione: Cliccato '{sender.text()}'", 3000)

    def riempi_tabella(self):
        headers = [f"Colonna {i+1}" for i in range(5)] + ["SKU", "Prezzo", "Quantità", "Categoria", "Disponibile"]
        self.tabella.setRowCount(10)
        self.tabella.setColumnCount(10)
        self.tabella.setHorizontalHeaderLabels(headers)
        for riga in range(10):
            for colonna in range(10):
                dato = f"Dato-{riga+1}-{colonna+1}"
                item = QTableWidgetItem(dato)
                self.tabella.setItem(riga, colonna, item)
        self.tabella.resizeColumnsToContents()
        self.status_bar.showMessage("Tabella riempita.", 3000)

    def pulisci_tabella(self):
        self.tabella.setRowCount(0)
        self.status_bar.showMessage("Tabella pulita.", 3000)

    def mostra_selezione(self):
        ranges = self.tabella.selectedRanges()
        if not ranges:
            QMessageBox.warning(self, "Errore", "Nessun elemento selezionato!")
            return
        # ... (logica per mostrare selezione)
        self.status_bar.showMessage("Selezione tabella mostrata.", 3000)

    def riempi_tabella_view(self):
        self.modello.clear()
        headers = [f"Colonna {i+1}" for i in range(5)] + ["SKU", "Prezzo", "Quantità", "Categoria", "Disponibile"]
        self.modello.setHorizontalHeaderLabels(headers)
        for riga in range(10):
            riga_items = [QStandardItem(f"Dato-{riga+1}-{c+1}") for c in range(10)]
            self.modello.appendRow(riga_items)
        self.vista_tabella.resizeColumnsToContents()
        self.status_bar.showMessage("Tabella (View) riempita.", 3000)

    def pulisci_tabella_view(self):
        self.modello.setRowCount(0)
        self.status_bar.showMessage("Tabella (View) pulita.", 3000)

    def mostra_selezione_view(self):
        selection_model = self.vista_tabella.selectionModel()
        if not selection_model.hasSelection():
            QMessageBox.warning(self, "Errore", "Nessun elemento selezionato!")
            return
        # ... (logica per mostrare selezione)
        self.status_bar.showMessage("Selezione tabella (View) mostrata.", 3000)

    def update_status_bar_with_tab_name(self, index):
        self.status_bar.showMessage(f"Tab selezionata: {self.tabs.tabText(index)}", 2000)

    def open_text_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Apri File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    self.testo_multilinea.setText(f.read())
                self.status_bar.showMessage(f"File '{file_name}' aperto.", 3000)
            except Exception as e:
                self.status_bar.showMessage(f"Errore apertura file: {e}", 3000)

    def save_text_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Salva File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write(self.testo_multilinea.toPlainText())
                self.status_bar.showMessage(f"File '{file_name}' salvato.", 3000)
            except Exception as e:
                self.status_bar.showMessage(f"Errore salvataggio file: {e}", 3000)

    def checkbox_state_changed(self, state):
        sender = self.sender()
        status = "selezionata" if state == Qt.Checked else "deselezionata"
        self.status_bar.showMessage(f"Checkbox '{sender.text()}' {status}.", 2000)

    def radio_button_toggled(self, checked):
        if checked:
            sender = self.sender()
            self.status_bar.showMessage(f"Radio button '{sender.text()}' selezionato.", 2000)

    def listbox_item_clicked(self, item):
        self.status_bar.showMessage(f"Elemento '{item.text()}' cliccato.", 2000)

    def combobox_text_changed(self, text):
        self.status_bar.showMessage(f"Combobox: '{text}'.", 2000)

    def slider_value_changed(self, value):
        self.status_bar.showMessage(f"Slider: {value}", 1000)

    def dial_value_changed(self, value):
        self.status_bar.showMessage(f"Dial: {value}", 1000)

    def spinbox_value_changed(self, value):
        self.status_bar.showMessage(f"SpinBox: {value}", 1000)

    def doublespinbox_value_changed(self, value):
        self.status_bar.showMessage(f"DoubleSpinBox: {value}", 1000)

    def date_changed(self, date):
        self.status_bar.showMessage(f"Data: {date.toString(Qt.ISODate)}", 2000)

    def time_changed(self, time):
        self.status_bar.showMessage(f"Ora: {time.toString(Qt.ISODate)}", 2000)

    def datetime_changed(self, dt):
        self.status_bar.showMessage(f"Data e Ora: {dt.toString(Qt.ISODate)}", 2000)

    def calendar_date_changed(self):
        date = self.calendar.selectedDate()
        self.status_bar.showMessage(f"Calendario: {date.toString(Qt.ISODate)}", 2000)

    def start_progress(self):
        self.progress_bar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 5)
        else:
            self.timer.stop()
            self.status_bar.showMessage("Avanzamento completato.", 2000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    colore = sys.argv[1] if len(sys.argv) > 1 else None
    window = MainWindow(background_color=colore)
    window.showMaximized()
    sys.exit(app.exec())
