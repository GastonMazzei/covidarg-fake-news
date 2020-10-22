from flask import Flask
from flask import render_template
#from flask import request
#from flask import redirect
#from flask import send_file
#from flask import send_from_directory
#from flask import Markup
import os
import sys

app = Flask(__name__,)# template_folder='../templates')

@app.route('/')
def landing():
  message = get_message('message.txt')
  title = get_message('title.txt')
  return render_template('index.html', fake_news=message, upper_desc=title)

def get_message(name):
  print('current folder is ',os.getcwd())
  with open(name,'r') as f:
    text = ''
    for x in f.readlines():
      text += x
  return text

if __name__ == '__main__':
  if len(sys.argv)==2:
    if sys.argv[1]=='dev':
      app.run(host='0.0.0.0')
  else:
    port = int(os.environ['PORT'])
    app.run(app.run(host='0.0.0.0', port=port))

