from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

from widgets import MedicalCard
import json
import shutil
import os

Window.size = (330, 550)


class MainApp(MDApp):
    data = DictProperty()

    def build(self):
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager, select_path=self.create_card
        )

        if os.path.isfile("data/account.json"):
            with open("data/account.json", 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "account": {
                    "avatar": "data/лиссс.png"
                },
                "documents": [],
            }

        return Builder.load_file("kv_files/mainapp.kv")

    def on_start(self):
        for index in range(len(self.data.documents)):
            self.add_card(index)

    def add_card(self, index):
        document = self.data["documents"][index]
        self.root.ids.main_scroll.add_widget(
            MedicalCard(name=document["title"], date=document["date"], status=document["status"],
                        image=os.path.abspath(document["scan"]))
        )

    def exit_file_manager(self, *args):
        self.file_manager.close()
        self.manager_open = False

    def open_file_manager(self):
        self.file_manager.show(
            os.path.expanduser("~")
        )
        self.manager_open = True

    def warn(self, text):
        MDSnackbar(
            MDSnackbarText(
                text=text,
            ),
            md_bg_color=self.theme_cls.backgroundColor,
            pos_hint={"center_x": 0.5},
            y=dp(50),
            size_hint_x=0.8,
            size_hint_y=0.05,
            padding=dp(-5),
        ).open()

    def create_card(self, path):
        self.manager_open = False
        self.file_manager.close()

        if not os.path.isfile(path):
            self.warn("Невозможно получить изображение")
            return

        format = path.split('.')[1]
        filename = path.split("\\")[-1].split("/")[-1]

        if format not in ["png", "jpg", "jpeg"]:
            self.warn("Невозможно получить изображение")
            return

        shutil.copy2(path, os.path.abspath("data\\images") + "\\" + filename)

        document = {
            "title": "Без названия",
            "date": "20.02.2000",
            "status": 0,
            "scan": "data\\images\\" + filename,
        }

        self.data.documents.append(document)
        print(os.path.abspath(document["scan"]))

        self.add_card(-1)

    def on_stop(self):
        with open("data/account.json", "w", encoding='utf-8') as f:
            f.write(json.dumps(self.data))


if __name__ == '__main__':
    MainApp().run()
