from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QLineEdit, QInputDialog
from PyQt5.QtGui import QFont
import json
notes = {
    "Добро пожаловать!": {
        "текст" : "Это самое лучшее приложение для заметок в мире!",
        "теги" : ["добро", "инструкция"]
    },

    "Добро пожаловать!": {
        "текст" : "Это самое лучшее приложение для заметок в мире!",
        "теги" : ["добро", "инструкция"]
    }
}
with open("notes_data.jason", "w") as file:
    json.dump(notes, file)








app = QApplication([])
window = QWidget()
window.setWindowTitle('Умные заметки')
main_hline = QHBoxLayout() #главная горизонтальная линия
vleft_line1 = QVBoxLayout()
vright_line2 = QVBoxLayout()
main_hline.addLayout(vleft_line1)
main_hline.addLayout(vright_line2)

TextEdit = QTextEdit()
vleft_line1.addWidget(TextEdit)
label1 = QLabel('список заметок')
vright_line2.addWidget(label1)

ListNotes = QListWidget()
vright_line2.addWidget(ListNotes)
hline1 = QHBoxLayout()
hline2 = QHBoxLayout()

create_note = QPushButton('создать')
del_note = QPushButton('удалить')
save_note = QPushButton('сохранить')
hline1.addWidget(create_note)
hline1.addWidget(del_note)
hline2.addWidget(save_note)

vright_line2.addLayout(hline1)
vright_line2.addLayout(hline2)

label2 = QLabel('Спсисок тегов')
vright_line2.addWidget(label2)


window.setLayout(main_hline)

ListNotes2 = QListWidget()
vright_line2.addWidget(ListNotes2)

hline3 = QHBoxLayout()


ledit = QLineEdit()
ledit.setPlaceholderText('Введите тег')
vright_line2.addWidget(ledit)
add_notes = QPushButton('Добавить к заметку')
Detaches_note = QPushButton('Открепить от заметки')
search_note = QPushButton('искать заметку по тегу')
vright_line2.addLayout(hline3)
hline3.addWidget(add_notes)
hline3.addWidget(Detaches_note)
vright_line2.addWidget(search_note)

def show_note(): 
    name = ListNotes.selectedItems()[0].text() #В переменной лист нотес выбираем предмет
    TextEdit.setText(notes[name]["текст"])#набор текста в словаре тег:значение
    ListNotes2.clear()#отчищаем Listnotes
    ListNotes2.addItems(notes[name]["теги"])#добавляем заново

ListNotes.itemClicked.connect(show_note)


def add_note():
    note_name, ok = QInputDialog.getText(ledit, "Добавить заметку", "Название заметки: ")#создание окна для создания заметок
    if ok and note_name != "":#если равно пустоте
        notes[note_name] = {"текст" : "", "теги" : []}#то текст и тег равно пустоте
        ListNotes.addItem(note_name)#доб. имена из list notes
def save_notes():
    if ListNotes.selectedItems():
        key = ListNotes.selectedItems()[0].text()#добаляем ключ
        notes[key]["текст"] = TextEdit.toPlainText()#в нотес ключ значение = 

        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)


        print(notes)
    else: 
        print("Заметка для сохранения не выбрана")

def del_notes():
    if ListNotes.selectedItems:
        key = ListNotes.selectedItems()[0].text()
        del notes[key]#удаляем ключ из списка
        ListNotes.clear()#чистим
        ledit.clear()#чистим
        TextEdit.clear()#чистим
        ListNotes.addItems(notes)#заново добаляем
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
            print(notes)

    else:
        print('Замтка для удления не выбрана')



del_note.clicked.connect(del_notes)
save_note.clicked.connect(save_notes)
create_note.clicked.connect(add_note)

#добавление тега
def add_tag():
    if ListNotes.selectedItems():#обработка
        key = ListNotes.selectedItems()[0].text()#оброботка выбирания
        tag = ledit.text()
        if not tag in notes[key]["теги"]:#если нет тега в списке
            notes[key]["теги"].append(tag)#добаляем
            ListNotes2.addItem(tag)#добавляем
            ledit.clear()#чистим
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    
    else:
        print("Заметка для добавления не выбрана!")
add_notes.clicked.connect(add_tag)

def del_tag():
    if  ListNotes2.selectedItems():
        key = ListNotes.selectedItems()[0].text()
        tag = ListNotes2.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        ListNotes2.clear()
        ListNotes2.addItems(notes[key]['теги'])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

    else:
        print("Тег для удаления не выбран")

Detaches_note.clicked.connect(del_tag)

def search_tag():
    print(search_note.text())
    tag = ledit.text()
    if search_note.text() == "искать заметку по тегу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        search_note.setText("Сбросить поиск")
        ListNotes.clear()
        ListNotes2.clear()
        TextEdit.clear()
        ListNotes.addItems(notes_filtered)
        print(search_note.text())
    elif search_note.text() == "Сбросить поиск":
        ledit.clear()
        ListNotes.clear()
        ListNotes2.clear()
        TextEdit.clear()
        ListNotes.addItems(notes)
        search_note.setText("искать заметку по тегу")
        print(search_note.text())
    else:
        pass
search_note.clicked.connect(search_tag)














ListNotes.addItems(notes)

window.show()
app.exec_()