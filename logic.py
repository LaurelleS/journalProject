from journal import *
from PyQt6.QtWidgets import *
from book import *


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.entry_dict: dict = {}
        self.radio_list: list = [
            self.radio_sci,
            self.radio_rom,
            self.radio_hor,
            self.radio_fic,
            self.radio_fan
        ]
        self.book_index: int = -1
        self.save_edit: bool = False
        self.delete_mode: bool = False
        self.button_new.hide()
        self.radio_tbd.hide()
        self.button_save.clicked.connect(lambda: self.save())
        self.button_clear.clicked.connect(lambda: self.clearEntry())
        self.list_saved.itemClicked.connect(lambda: self.display())
        self.button_edit.clicked.connect(lambda: self.edit())
        self.button_del.clicked.connect(lambda: self.delete())
        self.button_new.clicked.connect(lambda: self.new_clicked())

    def save(self):
        """
        Saves a new book note to be accessed later
        """
        if self.line_title.text().strip() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Please give your idea a title and try again.")
            msg.exec()
        else:
            if self.save_edit:
                self.book_index -= 1
                self.entry_dict.pop(self.list_saved.currentRow())
                self.list_saved.takeItem(self.list_saved.currentRow())
                num = 0
                for i in self.entry_dict.copy():
                    self.entry_dict[num] = self.entry_dict[i]
                    num += 1
            new_book = Book(self.line_title.text(), self.multi_notes.toPlainText(), self.radio_to_genre())
            self.book_index += 1
            self.entry_dict[self.book_index] = new_book
            self.list_saved.addItem(new_book.get_title())
            self.save_to_file(new_book)
            self.clearEntry()

            self.save_edit = False

    def edit(self):
        """
        Allows the selected book note to be edited
        """
        self.save_edit = True
        self.button_save.setEnabled(True)
        self.button_clear.setEnabled(True)
        self.line_title.setReadOnly(False)
        self.multi_notes.setReadOnly(False)
        for i in self.radio_list:
            i.setEnabled(True)
            i.setCheckable(True)

    def delete(self):
        """
        Deletes selected book note
        """
        self.delete_mode = True
        self.entry_dict.pop(self.list_saved.currentRow())
        self.list_saved.takeItem(self.list_saved.currentRow())
        self.book_index -= 1
        self.clearEntry()
        if len(self.entry_dict) == 0:
            self.button_del.setEnabled(False)
            self.button_edit.setEnabled(False)

        num = 0
        for i in self.entry_dict.copy():
            self.entry_dict[num] = self.entry_dict[i]
            num += 1

    def display(self):
        """
        Configures display for selected book note
        """
        if self.save_edit or self.delete_mode:
            self.delete_mode = False
            return
        self.button_save.setEnabled(False)
        self.button_clear.setEnabled(False)

        self.button_del.setEnabled(True)
        self.button_edit.setEnabled(True)

        cur_book = self.entry_dict.get(self.list_saved.currentRow())
        self.line_title.setText(cur_book.get_title())
        self.multi_notes.setText(cur_book.get_notes())
        self.line_title.setReadOnly(True)
        self.multi_notes.setReadOnly(True)
        radio_check = self.genre_to_radio(cur_book.get_genre())
        for i in self.radio_list:
            if not i == radio_check:
                i.setEnabled(False)
        self.button_new.show()

    def clearEntry(self):
        """
        Clears entry boxes and radio buttons
        """
        self.line_title.clear()
        self.line_title.setFocus()
        self.multi_notes.clear()
        for i in self.radio_list:
            i.setAutoExclusive(False)
        for j in self.radio_list:
            j.setChecked(False)
        for k in self.radio_list:
            k.setAutoExclusive(True)
        for h in self.radio_list:
            h.setCheckable(True)

    def new_clicked(self):
        """
        Shifts from viewing saved notes to creating new notes
        """
        for i in self.radio_list:
            i.setEnabled(True)
        self.line_title.setReadOnly(False)
        self.multi_notes.setReadOnly(False)
        self.button_save.setEnabled(True)
        self.button_clear.setEnabled(True)

        self.button_new.hide()
        self.clearEntry()

    def radio_to_genre(self) -> Genre:
        """
        Maps from radio buttons to specific Genre
        :return: Genre
        """
        sel_gen = Genre.TBD
        if self.radio_fan.isChecked():
            sel_gen = Genre.FANTASY
        elif self.radio_fic.isChecked():
            sel_gen = Genre.FICTION
        elif self.radio_hor.isChecked():
            sel_gen = Genre.HORROR
        elif self.radio_rom.isChecked():
            sel_gen = Genre.ROMANCE
        elif self.radio_sci.isChecked():
            sel_gen = Genre.SCIFI
        return sel_gen

    def genre_to_radio(self, gen: Genre) -> QRadioButton:
        """
        Checks the corresponding radio button to a Genre
        :param gen: Genre
        :return: QRadioButton
        """
        if gen == Genre.FANTASY:
            self.radio_fan.setChecked(True)
            return self.radio_fan
        elif gen == Genre.FICTION:
            self.radio_fic.setChecked(True)
            return self.radio_fic
        elif gen == Genre.HORROR:
            self.radio_hor.setChecked(True)
            return self.radio_hor
        elif gen == Genre.ROMANCE:
            self.radio_rom.setChecked(True)
            return self.radio_rom
        elif gen == Genre.SCIFI:
            self.radio_sci.setChecked(True)
            return self.radio_sci
        else:
            return self.radio_tbd

    def save_to_file(self, book_note: Book):
        """
        Saves created book to a file
        :param book_note: Book
        """
        with open('ideas.txt', 'a') as file:
            file.write(str(book_note))
