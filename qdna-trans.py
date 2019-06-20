
# coding: utf-8

# In[1]:


from googletrans import Translator

def translate(eng_text):
  '''
  Translate from english to vnese
  '''
  language_code = 'vi'
  translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.vi',    ])
  translations = translator.translate(eng_text, dest= language_code)
  
  return translations.text

from flask import Flask , render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qdna123456789@@'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('trans.html')

@socketio.on('message')
def transMessage(msg):
    msgme = msg
    msgbot = translate(msg)
    print('Message: ' + msgme)    
    print('Trans: ' + msgbot)    
    send(msgbot,broadcast=True)

if __name__ == '__main__':
    socketio.run(app)

