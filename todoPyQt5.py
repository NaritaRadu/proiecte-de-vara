from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QLineEdit,QListWidget,QPushButton,QComboBox,QLabel,QFrame,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import sys
import json

def incarca_lista():
    try:
        with open("task2.json","r") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []

def salveaza_lista(taskuri):
    with open('task2.json','w') as f:
        json.dump(taskuri,f,indent=4)

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("todo.png"))
        self.list_label=QLabel("Enter a task:",self)
        self.list_input=QLineEdit(self)
        self.list_widget=QListWidget(self)
        self.btn_adauga=QPushButton("Adauga Task",self)
        self.btn_marcheaza=QPushButton("Marcheaza ca finalizat",self)
        self.btn_sterge=QPushButton("Sterge Task",self)
        self.initUI()
        self.taskuri=incarca_lista()
        for task in self.taskuri:
            status='[X]' if task['completat'] else '[ ]'
            self.list_widget.addItem(f"{status} {task['titlu']}")
    
    def initUI(self):
        self.setWindowTitle("To-Do List")
        self.setFixedSize(420, 580)
        
        
        main_layout=QVBoxLayout()
        main_layout.setContentsMargins(25,25,25,25)
        main_layout.setSpacing(15)
        
        self.card = QFrame(self)
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)  
        
        card_layout.addWidget(self.list_label)
        
        input_layout=QHBoxLayout()
        input_layout.addWidget(self.list_input)
        input_layout.addWidget(self.btn_adauga)
        card_layout.addLayout(input_layout)
        
          
        card_layout.addWidget(self.list_widget)
        
        action_layout=QHBoxLayout()
        action_layout.addWidget(self.btn_marcheaza)
        action_layout.addWidget(self.btn_sterge)
        card_layout.addLayout(action_layout)
        
        
        main_layout.addWidget(self.card)
        self.setLayout(main_layout)
        
        self.list_label.setAlignment(Qt.AlignCenter)
        self.list_input.setAlignment(Qt.AlignCenter)
        
        self.list_label.setObjectName("label")
        self.list_input.setObjectName("input")
        self.list_widget.setObjectName("widget")
        self.btn_adauga.setObjectName("btn_adauga")
        self.btn_marcheaza.setObjectName("btn_marcheaza")
        self.btn_sterge.setObjectName("btn_sterge")
        
        
        self.btn_adauga.clicked.connect(self.adauga_task)
        self.btn_marcheaza.clicked.connect(self.marcheaza_task)
        self.btn_sterge.clicked.connect(self.sterge_task)
        self.list_input.returnPressed.connect(self.adauga_task)
        self.apply_style("#1D0A86", "#09a5a5")
    
    #09a5a5
    def adauga_task(self):
        text=self.list_input.text()
        if text:
            task_nou={'titlu':text,'completat':False}
            self.taskuri.append(task_nou)
            salveaza_lista(self.taskuri)
            self.list_widget.addItem(f'[ ] {text}')
            self.list_input.clear()
    
    def marcheaza_task(self):
        rand_selectat=self.list_widget.currentRow()
        if rand_selectat>=0:
            stare_curenta=self.taskuri[rand_selectat]['completat']
            self.taskuri[rand_selectat]['completat']=not stare_curenta
            salveaza_lista(self.taskuri)
            titlu=self.taskuri[rand_selectat]['titlu']
            status='[X]' if self.taskuri[rand_selectat]['completat'] else '[ ]'
            self.list_widget.item(rand_selectat).setText(f'{status} {titlu}')
            
    
    def sterge_task(self):
        rand_selectat=self.list_widget.currentRow()
        if rand_selectat>=0:
            try:
                self.taskuri.pop(rand_selectat)
                salveaza_lista(self.taskuri)
                self.list_widget.takeItem(rand_selectat)
            except IndexError:
                print("lista de taskuri este goala!")
                
    def apply_style(self,bg_color,card_color):
        self.setStyleSheet(f"""
                        QWidget {{
                                background-color: {bg_color};
                                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                                    }}
                        QFrame#card {{
                                background-color: {card_color};
                                border-radius: 10px;
                                    }}
                        QLabel#label {{
                                font-size: 20px;
                                font-weight: 600;
                                color: #ffffff;
                                margin-bottom: 5px;
                                    }}
                        QLineEdit#input {{
                                font-size: 16px;
                                font-weight: 500;
                                padding: 12px 16px;
                                border-radius: 8px;
                                border: 1px solid #45475a;
                                background-color: #11111b; 
                                color: #ffffff;
                                selection-background-color: #89b4fa;
                                selection-color: #11111b;            
                                    }}
                        QLineEdit#input::placeholder {{
                                color: #a6adc8;
                                font-style: italic;
                                    }}
                        QLineEdit#input:focus {{
                                border: 1.5px solid #89b4fa;
                                background-color: #1e1e2e;
                                    }}
                        QPushButton#btn_adauga {{
                                font-size: 16px;
                                font-weight: bold;
                                padding: 10px;
                                border-radius: 8px;
                                background-color: #89b4fa;
                                color: #11111b;
                                border: none;
                                    }}
                        QPushButton#btn_adauga:hover {{
                                background-color: #b4befe;
                                    }}
                        QPushButton#btn_marcheaza {{
                                font-size: 16px;
                                font-weight: bold;
                                padding: 10px;
                                border-radius: 8px;
                                background-color: #e6b800;
                                color: #11111b;
                                border: none;
                                    }}
                        QPushButton#btn_marcheaza:hover {{
                                background-color: #ffeb99;
                                    }}
                                    
                        QPushButton#btn_sterge {{
                                font-size: 16px;
                                font-weight: bold;
                                padding: 10px;
                                border-radius: 8px;
                                background-color: #e60000;
                                color: #11111b;
                                border: none;
                                    }}
                        QPushButton#btn_sterge:hover {{
                                background-color: #ff6666;
                                    }}
                                    
                        QListWidget#widget{{
                            font-size: 16px;
                            font-weight: 500;
                            padding: 12px 16px;
                            border-radius: 8px;
                            border: 1px solid #45475a;
                            background-color: #11111b; 
                            color: #ffffff;
                            selection-background-color: #89b4fa;
                            selection-color: #11111b; 
                        }}
                        
                        
                        """)
            
        


if __name__=="__main__":
    app= QApplication(sys.argv)
    todo=ToDoList()
    todo.show()
    sys.exit(app.exec_())