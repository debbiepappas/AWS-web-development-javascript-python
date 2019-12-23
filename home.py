from flask import *
from twilio import twiml
from twilio.rest import Client

from flask import render_template
import os

#Pull in configuration from system environment variables
account_sid = "AC032304da22aa10a434f0adb9724fb75e"
auth_token = "9e3fbe0dc94e66db3f5662633cbc1f3e"

# create an authenticated client that can make requests to Twilio for your
# account.

#client = Client(account='Axxxxx', token'sxxxxxxxx')

#create a flask web app
app = Flask(__name__)

client = Client(account_sid, auth_token)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services/')
def services():
    return render_template('services.html')

@app.route('/projects/')
def projects():
    return render_template('projects.html')

@app.route('/reviews/')
def reviews():
    return render_template('reviews.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/sms-submit/')
def smssubmit():
    return render_template('sms-submit.html')

#@app.route('/test/')
#def test():
    #return render_template('test.html')

#Handling a post request to send text messages.

@app.route('/message', methods=['POST', 'GET'])
def message():
     # Send a text message to the number provided
    if request.method == 'POST':

        message = client.messages.create(to="+12032165526",
                                         from_="12037743717",
                                         body=request.form['sms_message'])

    return render_template('sms-results.html')


if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
                                                                   
