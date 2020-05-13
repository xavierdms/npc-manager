import sys
import os
import json
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QFileDialog, QLabel, QComboBox
from PySide2.QtCore import QFile, QObject

# Global vars
npc_obj = {}
all_npcs = {}
display_npcs = []
npc_names = []
campaigns = []

class StartWindow(QObject):
    def __init__(self, ui_file, parent=None):
        super(StartWindow, self).__init__(parent)
        global npc_obj, all_npcs, display_npcs, npc_names, campaigns

        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.main_window = loader.load(ui_file)
        self.main_window.setWindowTitle("NPC Manager")

        ui_file.close()

        add_button = self.main_window.findChild(QPushButton, 'add_button')
        add_button.clicked.connect(self.load_json_file)

        # Campaign Drop down
        campaigns = ["All"]
        display_npcs = []
        for npc in all_npcs:
            display_npcs.append(npc)
       
        self.campaign_list = self.main_window.findChild(QComboBox, 'campaign_list')        
        self.campaign_list.insertItems(0, campaigns)
        self.campaign_list.currentIndexChanged.connect(self.load_npc_list)

        # NPC Drop down
        npc_names = []
        for npc in all_npcs:
            npc_names.append(npc["name"])

        npc_list = self.main_window.findChild(QComboBox, 'npc_list')
        npc_list.insertItems(0, npc_names)
        npc_list.currentIndexChanged.connect(self.load_npc_info)

        # Arrows
        next_button = self.main_window.findChild(QPushButton, 'next_button')
        next_button.clicked.connect(self.next_card)
        previous_button = self.main_window.findChild(QPushButton, 'previous_button')
        previous_button.clicked.connect(self.previous_card)


    def next_card(self):
        npc_list = self.main_window.findChild(QComboBox, 'npc_list')
        curr_ind = npc_list.currentIndex()
        max_ind = npc_list.count() - 1
        if curr_ind == max_ind:
            npc_list.setCurrentIndex(0)
        else:
            npc_list.setCurrentIndex(curr_ind + 1)

    def previous_card(self):
        npc_list = self.main_window.findChild(QComboBox, 'npc_list')
        curr_ind = npc_list.currentIndex()
        max_ind = npc_list.count() - 1
        if curr_ind == 0:
            npc_list.setCurrentIndex(max_ind)
        else:
            npc_list.setCurrentIndex(curr_ind - 1)

    def load_json_file(self):
        global all_npcs, campaigns
        self.campaign_list = self.main_window.findChild(QComboBox, 'campaign_list')        

        npc_json_path = QFileDialog.getOpenFileName(self.main_window, filter="JSON files (*.json)")
        npc_json_path = npc_json_path[0]

        with open(npc_json_path, 'r') as j:
            npc_json = json.loads(j.read())

        all_npcs = npc_json["npcs"]

        for npc in all_npcs:
            if npc["campaign"] not in campaigns:
                if npc["campaign"] != "":           #allows for unassigned NPCs
                    campaigns.append(npc["campaign"])

        self.campaign_list.clear()
        self.campaign_list.insertItems(0, campaigns)
        self.load_npc_list()  

    def load_npc_list(self):
        global npc_obj, all_npcs, display_npcs, npc_names
        
        campaign_list = self.main_window.findChild(QComboBox, 'campaign_list')
        npc_list = self.main_window.findChild(QComboBox, 'npc_list')

        current_campaign = campaign_list.currentText()
        npc_names.clear()
        npc_list.clear()
        display_npcs.clear()

        if current_campaign == "All":
            for npc in all_npcs:
                display_npcs.append(npc)
                npc_names.append(npc["name"])
        else:
            for npc in all_npcs:
                if npc["campaign"] == current_campaign:
                    display_npcs.append(npc)
                    npc_names.append(npc["name"])
            
        npc_list.insertItems(0, npc_names)

    def load_npc_info(self):
        # Update card text to match currently selected NPC
        npc_list = self.main_window.findChild(QComboBox, 'npc_list')
        name_label = self.main_window.findChild(QLabel, 'name_label')
        age_label = self.main_window.findChild(QLabel, 'age_label')
        gender_label = self.main_window.findChild(QLabel, 'gender_label')
        race_label = self.main_window.findChild(QLabel, 'race_label')
        class_label = self.main_window.findChild(QLabel, 'class_label')
        alignment_label = self.main_window.findChild(QLabel, 'alignment_label')
        background_label = self.main_window.findChild(QLabel, 'background_label')
        profession_label = self.main_window.findChild(QLabel, 'profession_label')
        location_label = self.main_window.findChild(QLabel, 'location_label')

        if (npc_list.count()) >= 1:
            npc_index = npc_list.currentIndex()
            name_label.setText(display_npcs[npc_index]["name"])
            age_label.setText(str(display_npcs[npc_index]["age"]))
            gender_label.setText(display_npcs[npc_index]["gender"])
            race_label.setText(display_npcs[npc_index]["race"])
            class_label.setText(display_npcs[npc_index]["class"])
            alignment_label.setText(display_npcs[npc_index]["alignment"])
            background_label.setText(display_npcs[npc_index]["background"])
            profession_label.setText(display_npcs[npc_index]["profession"])
            location_label.setText(display_npcs[npc_index]["location"])


def main():
    app = QApplication(sys.argv)
    main = StartWindow('StartWindow.ui')
    main.main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()