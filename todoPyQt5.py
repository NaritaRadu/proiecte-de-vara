from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QLineEdit,QListWidget,QPushButton,QComboBox,QLabel,QFrame,QHBoxLayout
from PyQt5.QtGui import QIcon,QFont,QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox,QListWidgetItem
import os
import sys
import json

PRIORITATI = {
    "Ridicata": {"emoji": "🔴", "color": "#f38ba8"},
    "Medie": {"emoji": "🟡", "color": "#f9e2af"},
    "Scazuta": {"emoji": "🟢", "color": "#a6e3a1"}
}

def incarca_lista():
    try:
        with open("task2.json","r", encoding="utf-8") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []

def salveaza_lista(taskuri):
    with open('task2.json','w', encoding="utf-8") as f:
        json.dump(taskuri,f,indent=4)

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.taskuri=incarca_lista()
        
        self.setWindowIcon(QIcon("todo.png"))
        self.list_label=QLabel("To-Do List:",self)
        self.list_input=QLineEdit(self)
        
        self.prio_combo=QComboBox(self)
        self.prio_combo.addItems(['Ridicata','Medie','Scazuta'])
        self.prio_combo.setCurrentText('Medie')
        
        self.list_widget=QListWidget(self)
        
        self.btn_adauga=QPushButton("➕ Adauga Task",self)
        self.btn_marcheaza=QPushButton("☑️ Marcheaza ca finalizat",self)
        self.btn_sterge=QPushButton("🗑 Sterge Task",self)
        
        self.filter_label=QLabel("Filtru:",self)
        self.filter_combo=QComboBox(self)
        self.filter_combo.addItems(['📋 Toate','⏳ Active','✅ Finalizate'])
        
        
        self.initUI()
        self.refresh_list()
        
   
    
    def initUI(self):
        self.setWindowTitle("To-Do List")
        self.resize(480, 680)
        self.setMinimumSize(440, 600)
        
        
        main_layout=QVBoxLayout()
        main_layout.setContentsMargins(18,18,18,18)
        
        
        self.card = QFrame(self)
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(14)  
        
        card_layout.addWidget(self.list_label)
        
        
        self.list_input.setPlaceholderText("Scrie un task nou...")
      
        card_layout.addWidget(self.list_input)
        
        prio_layout=QHBoxLayout()
        prio_layout.setSpacing(10)
        
        prio_label=QLabel('Prioritate:',self)
        prio_label.setObjectName('sub_label')
        
        prio_layout.addWidget(prio_label)
        prio_layout.addWidget(self.prio_combo, stretch=1)
        prio_layout.addWidget(self.btn_adauga, stretch=1)
        card_layout.addLayout(prio_layout)
        
        
        filter_layout=QHBoxLayout()
        filter_layout.setSpacing(10)
        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.filter_combo,stretch=1)
        card_layout.addLayout(filter_layout)
        
          
        card_layout.addWidget(self.list_widget,stretch=1)
        
        action_layout=QHBoxLayout()
        action_layout.setSpacing(12)
        action_layout.addWidget(self.btn_marcheaza,stretch=1)
        action_layout.addWidget(self.btn_sterge,stretch=1)
        card_layout.addLayout(action_layout)
        
        
        main_layout.addWidget(self.card)
        self.setLayout(main_layout)
        
        self.list_label.setAlignment(Qt.AlignCenter)
        self.list_input.setAlignment(Qt.AlignCenter)
        
        self.list_label.setObjectName("label")
        self.filter_label.setObjectName("filter_label")
        self.list_input.setObjectName("input")
        self.list_widget.setObjectName("widget")
        self.btn_adauga.setObjectName("btn_adauga")
        self.btn_marcheaza.setObjectName("btn_marcheaza")
        self.btn_sterge.setObjectName("btn_sterge")
        self.prio_combo.setObjectName("prio_combo")
        self.filter_combo.setObjectName("filter_combo")
        
        
        self.btn_adauga.clicked.connect(self.adauga_task)
        self.btn_marcheaza.clicked.connect(self.marcheaza_task)
        self.btn_sterge.clicked.connect(self.sterge_task)
        self.list_input.returnPressed.connect(self.adauga_task)
        self.filter_combo.currentIndexChanged.connect(self.refresh_list)
        
        self.apply_style("#11111b", "#1e1e2e")
    
    def refresh_list(self):
        self.list_widget.clear()
        fai_filtrare=self.filter_combo.currentText()
            
        for index,task in enumerate(self.taskuri):
            if fai_filtrare=='Active' and task['completat']:
                continue
            if fai_filtrare=='Finalizat' and not task['completat']:
                continue
            
            prio=task.get('prioritate','Medie')
            emoji=PRIORITATI.get(prio,{}).get('emoji','🟡')
            text_afișat = f"{emoji}  {task['titlu']}"
            
            item=QListWidgetItem(text_afișat)
            item.setData(Qt.UserRole,index)
                
            font=item.font()
            if task['completat']:
                font.setStrikeOut(True)
                item.setForeground(QColor("#6c7086"))
            else:
                hex_color=PRIORITATI.get(prio,{}).get('color','#ffffff')
                item.setForeground(QColor(hex_color))
                
            item.setFont(font)
            self.list_widget.addItem(item)
            
    def adauga_task(self):
        text=self.list_input.text().strip()
        prioritate=self.prio_combo.currentText()
        if text:
            task_nou={'titlu':text,'completat':False,'prioritate': prioritate}
            self.taskuri.append(task_nou)
            salveaza_lista(self.taskuri)
            self.refresh_list()
            self.list_input.clear()
    
    def marcheaza_task(self):
        item_curent=self.list_widget.currentItem()
        if item_curent:
            index=item_curent.data(Qt.UserRole)
            
            self.taskuri[index]['completat']=not self.taskuri[index]['completat']
            salveaza_lista(self.taskuri)
            self.refresh_list()
            
            
    
    def sterge_task(self):
        item_curent=self.list_widget.currentItem()
        if item_curent:
            index=item_curent.data(Qt.UserRole)
            reply = QMessageBox.question(
                self, 'Ștergere Task', 
                f"Ești sigur că vrei să ștergi task-ul:\n\"{self.taskuri[index]['titlu']}\"?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.taskuri.pop(index)
                salveaza_lista(self.taskuri)
                self.refresh_list()
            
                
    def apply_style(self,bg_color,card_color):
        self.setStyleSheet(f"""
                        QWidget {{
                                background-color: {bg_color};
                                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                                color: #cdd6f4;
                                    }}
                        QFrame#card {{
                                background-color: {card_color};
                                border-radius: 12px;
                                    }}
                        QLabel#label {{
                                font-size: 22px;
                                font-weight: bold;
                                color: #cdd6f4;
                                margin-bottom: 5px;
                                    }}
                        QLabel#filter_label, QLabel#sub_label {{
                                font-size: 14px;
                                font-weight: 600;
                                color: #a6adc8;
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
                                    
                        QComboBox {{
                                background-color:#313244;
                                border: 1px solid #45475a;
                                border-radius: 8px;
                                padding: 6px 12px;
                                color: #ffffff;
                                font-size: 13px;
                                font-weight: 500;
                            
                        }}      
                        QComboBox:hover {{
                            border:1px solid #89b4fa;
                        }}
                        QComboBox::drop-down{{
                            subcontrol-origin:padding;
                            subcontrol-position:top right;
                            width: 20px;
                            border-left-width:0px;
                        }}      
                        
                        QComboBox QAbstractItemView {{
                            background-color: #181825;
                            border: 1px solid #45475a;
                            selection-background-color:#45475a;
                            color:#ffffff;
                            padding:5px;
                            
                        }}
                                    
                        QPushButton {{
                                font-size: 16px;
                                font-weight: bold;
                                padding: 8px 12px;
                                border-radius: 8px;
                                border: none;
                                    }}
                                    
                        QPushButton#btn_adauga {{
                            
                                background-color: #89b4fa;
                                color: #11111b;
                                
                                    }}
                        QPushButton#btn_adauga:hover {{
                                background-color: #b4befe;
                                    }}
                        QPushButton#btn_marcheaza {{

                                
                                background-color: #e6b800;
                                color: #11111b;
                                
                                    }}
                        QPushButton#btn_marcheaza:hover {{
                                background-color: #ffeb99;
                                    }}
                                    
                        QPushButton#btn_sterge {{
                                
                                background-color: #e60000;
                                color: #11111b;
                                
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