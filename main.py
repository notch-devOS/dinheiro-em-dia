import os
import time
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.properties import ObjectProperty
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Transaction

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///dinheiro_em_dia.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class SplashScreen(Screen):
    def on_enter(self):
        # Mudar para a tela de login após 3 segundos
        App.get_running_app().root.current = 'login'

class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def do_login(self):
        session = Session()
        user = session.query(User).filter_by(username=self.username.text, password=self.password.text).first()
        if user:
            App.get_running_app().root.current = 'dashboard'
        else:
            print("Credenciais inválidas.")
        session.close()

class RegisterScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def do_register(self):
        session = Session()
        new_user = User(username=self.username.text, password=self.password.text)
        session.add(new_user)
        session.commit()
        session.close()
        App.get_running_app().root.current = 'login'

class DashboardScreen(Screen):
    def on_enter(self):
        self.update_dashboard()

    def update_dashboard(self):
        # Aqui você pode atualizar o dashboard com informações de despesas e receitas
        pass

class MainApp(App):
    def build(self):
        self.title = "Dinheiro em Dia"
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    MainApp().run()