import requests
import threading
import time
from datetime import datetime
import os

from config import LOGIN, PASSWORD

class GetData:

    URL = 'http://127.0.0.1:8000'
    TOKEN = ''
    CONTACTS = []
    USER_INFO = ''

    def create_thread(self, thread_function, args=(), daemon_state=True, start=True):
        new_thread = threading.Thread(target=thread_function, args=args)
        new_thread.daemon = daemon_state
        new_thread.name = thread_function.__name__
        if start:
            new_thread.start()
        return new_thread

    def get_token(self, login, password):
        json = {
            "user_form": {
                "email": login,
                "password": password
                }
            }
        token = eval(requests.post(f'{self.URL}/login', json=json).text)["auth_token"]
        
        return token

    def get_user_info(self):
        json = {
            'token' : self.TOKEN
            }
        self.USER_INFO = requests.get(f'{self.URL}/user/', params=json).json()

    def check_contacts(self):
        json = {
            'token' : self.TOKEN
            }
        contacts_data = eval(requests.get(f'{self.URL}/user/contact', params=json).text)['contacts']
        for contact in contacts_data:
            self.CONTACTS.append(contact)

    def send_message(self, contact_id, message="test"):
        while True:
            message = input()
            json = {
                "message": {
                    "token": self.TOKEN,
                    "contact_id": contact_id,
                    "message": message
                    }
                }
            message = requests.post(f'{self.URL}/user/contact/message', json=json)
            # if message.status_code == 200:
                # print("Message was sent!")

    def look_messages(self, contact_id):
        json = {
            'contact_id' : contact_id,
            'token' : self.TOKEN
            }
        for contact in self.CONTACTS:
            if int(contact["contact_id"]) == int(contact_id):
                friend_login = contact["friend_login"]
                print(f'Чат c {friend_login}:')
        last = datetime.now()
        while True:
            messages = requests.get(f'{self.URL}/user/contact/message', params=json).json()["messages"]
            date_time = datetime.strptime(messages[-1]["created_at"], '%Y-%m-%d %H:%M:%S.%f')
            if date_time > last and not self.USER_INFO["id"] == messages[-1]["sender"]:
                print (messages[-1]["msg"])
                last = date_time

            time.sleep(0.2)
      
        


    def main(self):
        if requests.get(self.URL).status_code == 200:

            self.TOKEN = self.get_token(LOGIN, PASSWORD)
            self.check_contacts()
            self.get_user_info()
            
            print("Выберете чат: ")
            for contact in self.CONTACTS:
                print(f'{contact["contact_id"]} - {contact["friend_login"]}')
            contact_id = input()
            os.system('cls')
      
            
            self.create_thread(self.send_message, (contact_id))
            self.create_thread(self.look_messages, (contact_id))

            while True:
                time.sleep(10)


     


if __name__ == "__main__":
    # GetData().main()
    print(GetData().get_token(LOGIN, PASSWORD))