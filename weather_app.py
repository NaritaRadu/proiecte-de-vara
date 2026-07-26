import sys
import requests
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout,QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

load_dotenv()

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.setWindowIcon(QIcon("img_weather.png"))
        # Elementele UI
        self.city_label =QLabel("Enter city name: ",self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton("Get Weather",self)
        
        self.temperature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.details_label = QLabel(self) # Pentru umiditate/vânt
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setFixedSize(420, 580)
        #Layout principal
        main_layout=QVBoxLayout()
        main_layout.setContentsMargins(25,25,25,25)
        main_layout.setSpacing(15)
        
        #card principal pentru aspect modern
        self.card = QFrame(self)
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)
        
        card_layout.addWidget(self.city_label)
        card_layout.addWidget(self.city_input)
        card_layout.addWidget(self.get_weather_button)
        card_layout.addWidget(self.temperature_label)
        card_layout.addWidget(self.emoji_label)
        card_layout.addWidget(self.description_label)
        card_layout.addWidget(self.details_label)
        
        main_layout.addWidget(self.card)
        self.setLayout(main_layout)
        
        #aliniere text
        for widget in [self.city_label, self.city_input, self.temperature_label, 
                        self.emoji_label, self.description_label, self.details_label]:
            widget.setAlignment(Qt.AlignCenter)
        
        self.city_input.setPlaceholderText("Enter city (e.g. Bucharest)")
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.details_label.setObjectName("details_label")
        
        self.apply_style("#1e1e2e", "#2b2b3b")
        
        
        
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)
    
    #CSS style
    def apply_style(self,bg_color,card_color):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QFrame#card {{
                background-color: {card_color};
                border-radius: 16px;
            }}
            
            QLabel#city_label {{
                font-size: 20px;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 5px;
            }}
            
            QLineEdit#city_input {{
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
            
            QLineEdit#city_input::placeholder {{
                color: #a6adc8;
                font-style: italic;
            }}
            QLineEdit#city_input:focus {{
                border: 1.5px solid #89b4fa;
                background-color: #1e1e2e;
            }}
            
            QPushButton#get_weather_button {{
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                background-color: #89b4fa;
                color: #11111b;
                border: none;
            }}
            QPushButton#get_weather_button:hover {{
                background-color: #b4befe;
            }}
           
            QLabel#temperature_label {{
                font-size: 48px;
                font-weight: bold;
                color: #ffffff;
            }}
            QLabel#emoji_label {{
                font-size: 70px;
            }}
            QLabel#description_label {{
                font-size: 20px;
                color: #cdd6f4;
                text-transform: capitalize;
            }}
            QLabel#details_label {{
                font-size: 13px;
                color: #a6adc8;
            }}
        """)
    
    def update_theme(self, temp_c):
        
        if temp_c <= 5:
            # Rece / Iarnă (Nuanțe de albastru/întunecat)
            self.apply_style("#0f172a", "#1e293b")
        elif 5 < temp_c <= 22:
            # Plăcut / Primăvară (Nuanțe moderați)
            self.apply_style("#181825", "#313244")
        else:
            # Cald / Vară (Nuanțe calde subtile)
            self.apply_style("#2d1517", "#421d20")
    
        
    def get_weather(self):
        if not self.api_key:
            self.display_error("API Key Missing!\nCheck your .env file")
            return
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        try:
            response=requests.get(url)
            response.raise_for_status()#uneori try block nu gaseste singur exceptia
            data=response.json()
            
            if data["cod"]==200:
                self.display_weather(data)
                
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\n Please check your input")
                case 401:
                    self.display_error("Unauthorized\n Invalid API Key")
                case 403:
                    self.display_error("Forbidden\n Access denied")
                case 404:
                    self.display_error("Not Found\n City not found")
                case 500:
                    self.display_error("Internel server error\n Please try again later ")
                case 502:
                    self.display_error("Bad Gateway\n Invalid response from server")
                case 503:
                    self.display_error("Service Unavailable\n Server is down")
                case 504:
                    self.display_error("Gateway Timeout\n No response from the server")
                case _:
                    self.display_error(f"HTTP error occured\n{http_error}")
                
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\n Check your internet connection")
        except requests.Timeout:
            self.display_error("Timeout Error:\n The request timed out")
        except requests.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")
            
    
    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.details_label.clear()
    
    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:75px;")
        temp_k=data["main"]["temp"]
        temp_c=temp_k-273.15
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_id=data["weather"][0]["id"]
        weather_desc=data["weather"][0]["description"]
        
        self.update_theme(temp_c)
        
        self.temperature_label.setText(f"{temp_c:.0f}°C")
        self.description_label.setText(weather_desc)
        self.details_label.setText(f"💧 Humidity: {humidity}%   |   💨 Wind: {wind_speed} m/s")
        self.emoji_label.setText(self.get_emoji(weather_id))
    
    @staticmethod
    def get_emoji(weather_id):
        if weather_id>=200 and weather_id<=232:
            return "⛈️"
        elif weather_id>=300 and weather_id<=321:
            return "☁️"
        elif weather_id>=500 and weather_id<=531:
            return "🌧️"
        elif weather_id>=600 and weather_id<=622:
            return "❄️"
        elif weather_id>=701 and weather_id<=741:
            return "🌁"
        elif weather_id==762:
            return "🌋"
        elif weather_id==771:
            return "💨"
        elif weather_id==781:
            return "🌪️"
        elif weather_id==800:
            return "🌞"
        elif weather_id>=801 and weather_id<=804:
            return "⛅"
        else :
            return ""
    
        
        
        
if __name__=="__main__":
    app= QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    