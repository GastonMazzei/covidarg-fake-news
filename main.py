from flask import Flask
from flask import render_template
#from flask import request
#from flask import redirect
#from flask import send_file
#from flask import send_from_directory
#from flask import Markup
import os

app = Flask(__name__,)# template_folder='../templates')

@app.route('/')
def landing():
  return render_template('index.html')



if __name__ == '__main__':
  port = int(os.environ['PORT'])
  app.run(app.run(host='0.0.0.0', port=port))

