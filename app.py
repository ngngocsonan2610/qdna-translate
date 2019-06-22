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

from flask import Flask , render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200))
    mess_class = db.Column(db.String(10))
    
    def __init__(self, id, text,mess_class):
      self.id = id
      self.text = text
      self.mess_class = mess_class
    
db.create_all()
db.session.commit()

db.engine.execute(" DELETE FROM chat ")
    
@app.route('/')
def index():
    chats = Chat.query.all()
    return render_template('trans.html', chats = chats)



@app.route('/add', methods = ['POST'])
def add():    
    msg = request.form['nameMes'] 
    print(msg)    
    msgbot = translate(msg)
    print(msgbot)

    chat = Chat(text= msg , mess_class = 'me')
    db.session.add(chat)
    db.session.commit()
    
    trans = Chat(text= msgbot , mess_class = 'bot')
    db.session.add(trans)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
    


    
