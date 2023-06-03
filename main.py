from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
from random import shuffle

DEFAULT_NUMBER_WORDS = 15
MAXIMUM_NUMBER_WORDS = 50

"""Окно игры"""
class Ui_Game(QtWidgets.QDialog, uic.loadUiType("uis/game.ui")[0]):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        app.setStyleSheet("QLineEdit{font-size: 14pt;}")
        self.vbox = QtWidgets.QVBoxLayout()  # Вертикальная разметка

        # Настройка скроллинга
        self.input_lines_scroll_area = self.findChild(QtWidgets.QScrollArea, "input_lines_scroll_area")
        self.input_lines_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.input_lines_scroll_area.setWidgetResizable(True)

        # Создание полей для ввода слов
        for i in range(DEFAULT_NUMBER_WORDS):
            object = QtWidgets.QLineEdit() # Создаём поле
            self.vbox.addWidget(object) # Добавляем поле в вертикальный виджет vbox

        self.widget = QtWidgets.QWidget()  # Виджет для ввода слов в объект scroll area
        self.widget.setLayout(self.vbox)  # задать виджету вертикульную позицию
        self.input_lines_scroll_area.setWidget(self.widget)  # установка виджета в область прокрутки SetScrollArea

        # Кнопка Выход
        self.quit_button = self.findChild(QtWidgets.QPushButton, "quit_button")  # объект кнопки "Выход" с UI файла
        self.quit_button.setIcon(QtGui.QIcon('source/icons8-close-window-64.png'))
        self.quit_button.setIconSize(QtCore.QSize(40, 40))
        self.quit_button.clicked.connect(lambda: self.close())  # обработчик при нажатии на кнопку "Выход"

        # Кнопка Проверить результат
        self.check_button = self.findChild(QtWidgets.QPushButton, "check_button")
        self.check_button.clicked.connect(self.check_words)  # обработчик кнопки Проверить

        # Кнопка Сохранить результат
        self.save_result_button = self.findChild(QtWidgets.QPushButton, "save_result_button")
        self.save_result_button.clicked.connect(self.save_result_to_file)  # обработчик кнопки Проверить

        self.generated_words = []  # Переменная для хранения сгенерированных слов

    # Обработчик события закрытия окна
    def closeEvent(self, event):
        main_window = Ui_Main_Window()  # Создаём объект главное меню для его отображения после закрытия окна "Игра"
        main_window.show_main_window()
        event.accept()  # Позволяем окну закрыться

    # Метод проверки какие слова были введены верно
    def check_words(self):
        found_wrong_words = 0  # счетчик неверно угаданных слов
        found_right_words = 0  # счетчик верно угаданных слов
        for i in range(DEFAULT_NUMBER_WORDS):

            # сравниваем текст Qlable главного окна с текстом в поле QlineEdit виджета vbox
            if self.generated_words[i] == self.vbox.itemAt(i).widget().text().lower().strip():
                self.vbox.itemAt(i).widget().setStyleSheet("border: 1.5px solid green;")
                found_right_words += 1
            else:
                self.vbox.itemAt(i).widget().setStyleSheet("border: 1.5px solid red;")
                found_wrong_words += 1

        # Открываем файл для чтения списка сохраненных результатов
        with open("result_save.txt", "r", encoding="UTF-8") as file:
            current_results = file.read().split("\n")
            current_results = [int(result) for result in current_results if result]

        self.result_label.setFont(QFont("Arial", 12))

        if found_wrong_words == 0: #если нет ошибок при проверке
            if found_right_words > max(current_results):  # Проверка если счёт найденных слов больше максимального результату в файле
                self.result_label.setText(f"Всё правильно!\nУ вас новый рекорд. {found_right_words} запомненных слов")
            else:
                self.result_label.setText(f"Всё правильно!")
        else:
            if found_right_words > max(current_results):  # Проверка если счёт найденных слов больше максимального результату в файле
                self.result_label.setText(f"Есть ошибки\nУ вас новый рекорд. {found_right_words} запомненных слов")
            else:
                self.result_label.setText("Есть ошибки!")

    "Метод сохранения результата"
    def save_result_to_file(self):
        found_wrong_words = 0  # счетчик неверно угаданных слов
        found_right_words = 0  # счетчик верно угаданных слов
        for i in range(DEFAULT_NUMBER_WORDS):
            # сравниваем текст Qlable главного окна с текстом в поле QlineEdit виджета vbox
            if self.generated_words[i] == self.vbox.itemAt(i).widget().text().lower().strip():
                found_right_words += 1
            else:
                found_wrong_words += 1

        # Открываем файл для чтения списка сохраненных результатов
        with open("result_save.txt", "r", encoding="UTF-8") as file:
            current_results = file.read().split("\n")
            current_results = [int(result) for result in current_results if result]

        if found_right_words>0:
            #открываем файл для записи результата
            with open("result_save.txt", "a+", encoding="UTF-8") as file:
                if found_right_words not in current_results:
                    file.write(f"{found_right_words}\n")

        self.result_label.setText("Результат сохранён.")


""" Окно настроек """
class Ui_Settings(QtWidgets.QDialog, uic.loadUiType("uis/settings.ui")[0]):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.limit_words_input_field = self.findChild(QtWidgets.QLineEdit, "limit_words_input_field") #Поле ввода текста
        self.limit_words_input_field.setText(str(DEFAULT_NUMBER_WORDS))
        self.save_settings_button = self.findChild(QtWidgets.QPushButton, "save_settings_button") #Кнопка Сохранить Результат
        self.save_settings_button.clicked.connect(self.change_limit_words)  # обработчик кнопки "Сохранить" при ее нажатии

    # Обработчик нажатия кнопки "Сохранить" - сохраняет кол-во введенных слов
    def change_limit_words(self):
        self.setStyleSheet("QLineEdit{font-size: 14pt;}")
        global DEFAULT_NUMBER_WORDS
        try:
            if int(self.limit_words_input_field.text()) <= MAXIMUM_NUMBER_WORDS:
                self.limit_words_input_field.setStyleSheet(
                    "border: 1.5px solid green;")  # Обводим поле "Количество слов" зелёным
                DEFAULT_NUMBER_WORDS = int(self.limit_words_input_field.text())  # Берём число с поля "Количество слов"
            else:
                self.limit_words_input_field.setStyleSheet(
                    "border: 1.5px solid red;")
                self.limit_words_input_field.setText("")  # Очищаем поле "Количество слов"
        except:
            self.limit_words_input_field.setStyleSheet(
                "border: 1.5px solid red;")  # Обводим поле "Количество слов" красным
            self.limit_words_input_field.setText("")  # Очищаем поле "Количество слов"


"""Главное меню"""
class Ui_Main_Window(QtWidgets.QWidget):

    def __init__(self):
        super(Ui_Main_Window, self).__init__()
        uic.loadUi('uis/main.ui', self)
        app.setStyleSheet("QLabel{font-size: 14pt;}")

        words = self.load_words()
        shuffle(words)  # Мешаем список слов
        self.widget = QtWidgets.QWidget()  # Виджет для помещения на него слов в объект Scroll Area
        self.vbox = QtWidgets.QVBoxLayout() # Виджет вертикальной разметки

        "Создание слов в гланом меню"
        for word in words[:DEFAULT_NUMBER_WORDS]:
            object = QtWidgets.QLabel(word)  # Создаём слово
            self.vbox.addWidget(object)  # Добавляем в вертикальную разметку текст

        self.widget.setLayout(self.vbox)  # Добавляем вертикальную разметку в виджет

        # Скроллинг
        self.scroll_area = self.findChild(QtWidgets.QScrollArea, "hints_scroll_area")  # Находим объект из ui файла
        self.hints_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.hints_scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)  # Устанавливаем виджет в Scroll Area
        #Кнопка "Начать игру"
        self.start_game_button = self.findChild(QtWidgets.QPushButton, "start_game_button")
        self.start_game_button.clicked.connect(self.show_game_window)
        # Кнопка Перезапустить
        self.restart_button = self.findChild(QtWidgets.QPushButton, "restart_button")
        self.restart_button.clicked.connect(self.restart_game_main_menu)
        # Кнопка Настройки
        self.settings_button = self.findChild(QtWidgets.QPushButton, "settings_button")
        self.settings_button.setIcon(QtGui.QIcon('source/icons8-automatic-50.png'))
        self.settings_button.setIconSize(QtCore.QSize(40, 40))
        self.settings_button.clicked.connect(self.show_settings_window)
        # Кнопка Выход
        self.quit_button = self.findChild(QtWidgets.QPushButton, "quit_button")
        self.quit_button.setIcon(QtGui.QIcon('source/icons8-close-window-64.png'))
        self.quit_button.setIconSize(QtCore.QSize(40, 40))
        self.quit_button.clicked.connect(lambda: self.close())

        self.show()

    "Обработчик кнопки 'Перезапустить игру'"

    def restart_game_main_menu(self):
        words = self.load_words()
        shuffle(words)
        self.widget = QtWidgets.QWidget() # Виджет для помещения на него слов в объект Scroll Area
        self.vbox = QtWidgets.QVBoxLayout() # Виджет вертикальной разметки
        self.widget.setLayout(self.vbox)  # Добавляем вертикальную разметку в виджет
        self.hints_scroll_area.setWidget(self.widget)  # Устанавливаем виджет в Scroll Area

        # обновляем список QLabel
        for word in words[:DEFAULT_NUMBER_WORDS]:
            object = QtWidgets.QLabel(word) # Создаём слово
            self.vbox.addWidget(object) # Добавляем в вертикальную разметку текст

    @staticmethod # Метод для загрузки слов
    def load_words():
        with open("word_rus.txt", "r", encoding="utf-8") as file:
            words = file.read().split("\n")
        return words

    @staticmethod # Метод для отображения окна "Настройки"
    def show_settings_window():
        settings_ui = Ui_Settings()
        settings_ui.exec_()

    "Метод для отображеняи окна 'Игра'"
    def show_game_window(self):
        self.hide()  # Прячем главное меню
        game_window_ui = Ui_Game()  # Создаём окно "Игра"

        #Добавляем  текст из виджета vbox в список generated_words класса Ui_Game
        for i in range(DEFAULT_NUMBER_WORDS):
            game_window_ui.generated_words.append(self.vbox.itemAt(i).widget().text().lower().strip())

        game_window_ui.exec_()

    "Метод для отображения 'Главного меню' приложения"
    def show_main_window(self):
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_Main_Window()
    app.exec_()

