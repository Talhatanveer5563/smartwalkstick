from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.label import Label
import requests
from kivy.core.window import Window
import pyrebase
import requests
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import pyttsx3
import threading

Window.size=(380,630)
config = {
        "apiKey": "AIzaSyCe3jNDTo1E8GTDbZjpaRdh42lQkVsB4Cs",
        "authDomain": "django-fcf5e.firebaseapp.com",
        "databaseURL": "https://django-fcf5e-default-rtdb.firebaseio.com/json",
        "projectId": "django-fcf5e",
        "storageBucket": "django-fcf5e.appspot.com",
        "messagingSenderId": "180613126680",
        "appId": "1:180613126680:web:34eaec3c977b686814416d",
    }
firebase = pyrebase.initialize_app(config)
db = firebase.database()
class WelcomeScreen(Screen):
    pass
class MainScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class SignupScreen(Screen):
    pass
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name = 'loginscreen'))
sm.add_widget(MainScreen(name = 'mainscreen'))
sm.add_widget(LoginScreen(name = 'loginscreen'))
sm.add_widget(SignupScreen(name = 'signupscreen'))


class SmartWalkStickApp(MDApp):
    def build(self):
      
      
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.strng = Builder.load_file('style.kv')
        self.url  = "https://django-fcf5e-default-rtdb.firebaseio.com/.json"
        Clock.schedule_once(self.change_screen, 3)
        # Clock.schedule_interval(self.waterdata, 10)
        self.interval = None
        return self.strng
     
    def change_screen(self, dt):
        self.root.current = 'loginscreen' 
  
    def signup(self):
        signupEmail = self.strng.get_screen('signupscreen').ids.signup_email.text
        signupPassword = self.strng.get_screen('signupscreen').ids.signup_password.text
        signupUsername = self.strng.get_screen('signupscreen').ids.signup_username.text
        if signupEmail.split() == [] or signupPassword.split() == [] or signupUsername.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_username_dialog)
            self.dialog = MDDialog(title = 'Invalid Input',text = 'Please Enter a valid Input',size_hint = (0.7,0.2),buttons = [cancel_btn_username_dialogue])
            self.dialog.open()
        if len(signupUsername.split())>1:
            cancel_btn_username_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_username_dialog)
            self.dialog = MDDialog(title = 'Invalid Username',text = 'Please enter username without space',size_hint = (0.7,0.2),buttons = [cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            print(signupEmail,signupPassword)
            signup_info = str({f'\"{signupEmail}\":{{"Password":\"{signupPassword}\","Username":\"{signupUsername}\"}}'})
            signup_info = signup_info.replace(".","-")
            signup_info = signup_info.replace("\'","")
            to_database = json.loads(signup_info)
            print((to_database))
            requests.patch(url = self.url,json = to_database)
            self.strng.get_screen('loginscreen').manager.current = 'loginscreen'
    auth = 'AIzaSyCe3jNDTo1E8GTDbZjpaRdh42lQkVsB4Cs'

    def login(self):
        loginEmail = self.strng.get_screen('loginscreen').ids.login_email.text
        loginPassword = self.strng.get_screen('loginscreen').ids.login_password.text

        self.login_check = False
        supported_loginEmail = loginEmail.replace('.','-')
        supported_loginPassword = loginPassword.replace('.','-')
        request  = requests.get(self.url+'?auth='+self.auth)
        data = request.json()
        emails= set()
        for key,value in data.items():
            emails.add(key)
        if supported_loginEmail in emails and supported_loginPassword == data[supported_loginEmail]['Password']:
            self.username = data[supported_loginEmail]['Username']
            self.login_check=True
            self.strng.get_screen('mainscreen').manager.current = 'mainscreen'
            
            
        else:
            self.strng.get_screen('loginscreen').manager.current = 'loginscreen'
            self.dialog = MDDialog(text = 'Invalid Username and password',size_hint = (0.7,0.2))
            self.dialog.open()
         
          
    
    def logout(self):
        if self.interval:
            self.interval.cancel()
            self.interval = None

        print("Logged out successfully!")
        self.strng.get_screen('loginscreen').manager.current = 'loginscreen'
    
    def start_interval(self):
        if not self.interval:
            self.interval = Clock.schedule_interval(self.helperFunction, 3)
            
    def helperFunction(self,dt):
       self.water_data();
    

    def water_data(self):
        auth_token = 'AIzaSyCe3jNDTo1E8GTDbZjpaRdh42lQkVsB4Cs'
        response = requests.get(self.url, auth_token)
        data = response.json()

        object_detection_data = data.get('object_detection', {}) 

        object_names = [info['className'] for obj_id, info in object_detection_data.items()]
        object_names2 = [info['distance'] for obj_id, info in object_detection_data.items()]

        if object_names:
            latest_classname = object_names[-1]
            latest_classname2 = object_names2[-1]
            formatted_number = "{:.2f}".format(latest_classname2)
            self.strng.get_screen('mainscreen').ids.data_label.text = f"Object is : {latest_classname}"
            self.strng.get_screen('mainscreen').ids.data_label2.text = f"Distance is : {formatted_number}"
            text = f"{formatted_number} meter away , there is {latest_classname}"
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        else:
            self.strng.get_screen('mainscreen').ids.data_label.text = f"No object"





         
SmartWalkStickApp().run()