## DGM Website Development

#### Complete the following steps to create a website for a small business that will text and email the owner :

* **Note :** *the business in this example is a restoration company that decided not to pay for texting in the future , therefore, the code for 'texting' is disabled ( commented out ).*  

1. Start an Ubuntu EC2 instance. Assign an elastic IP address. Configure the security group to allow for inbound ssh and http traffic. 
2. Log in as root and install python, pip, flask and twilo. Twilio code will be used for texting. 
``` apt-get -y upgrade ```
``` apt-get install -y python3-pip ```
``` pip install Flask twilio ``` 
3. Create directory  *DgmApp* under */var/www/FlaskApps* .
4. Go to [Twilio](https://www.twilio.com) and create a username and password. Once you are logged in create a project, purchase a phone number and copy the account_sid and auth_token to be used in **home.py** below. 
5. In **home.py** add the following code : 
```
from flask import *
from twilio import twiml
from twilio.rest import Client

from flask import render_template
import os

#Pull in configuration from system environment variables
account_sid = "your account sid from twilio"
auth_token = "your auth token from twilio"

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

#Handling a post request to send text messages.

@app.route('/message', methods=['POST', 'GET'])
def message():
     # Send a text message to the number provided
    if request.method == 'POST':

        message = client.messages.create(to="+12013621656",
                                         from_="12037743717",
                                         body=request.form['sms_message'])

    return render_template('sms-results.html')


if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
```                                                                   
6. Run the **home.py** script with the following command : 
  `nohup /usr/bin/python /var/www/FlaskApps/DgmApp/home.py & `. 
  This same command was put in /etc/crontab to start home.py after a server reboot. 
  7. When home.py is started , it will reference **home.html** . All html files are in **template** directory under **DgmApp**. All jpg files are in the **static** directory under **DgmApp**.  **Home.html** will reference the definitions in **home.py**. For example,  to reference the definition 'contact' the following code is used : 
 ``` “{{url_for('contact')}}” ```
 8. The company , Twilio, is used to generate an account sid and a auth token for use in AWS lambda. Twilio will allow you to buy a number which is the 'from' number in the code. This is called a Masked Phone Number. 
This keeps personal numbers private by sending texts and calls through an intermediate Twilio phone number.
9. AWS API Gateway acts as interface from **home.py** to **AWS lambda**. The **AWS lambda** code is as follows : 
``` from __future__ import print_function
from twilio import twiml
from twilio.rest import TwilioRestClient
import json, os

client = TwilioRestClient("accound ID from twilio", "auth token from twilio")


def lambda_handler(event, context):
    print("this is the event passed to lambda_handler: " + json.dumps(event))
    to_number = os.environ['to_number']
    from_number = os.environ['from_number']
    print("This is the To Number : " + to_number + "\nThis is the From Number : " + from_number +
          "\nThis is the Message " + event["message"])
    client.messages.create(to=to_number, from_=from_number, body=event['message'])
    return "message sent"
```
10. The following code in **contact.html** contains code to email the owner. The **url** code is the interface to the  AWS API Gateway which calls  AWS Lambda to email the owner. 
```
<script>
function submitToAPI(e)  {
e.preventDefault();
var URL= " https://0yutj6pm3g.execute-api.us-east-1.amazonaws.com
/dev-mail/mail-us";

var Namere = /[A-Za-z]{1}[A-Za-z]/;
if  (!Namere.test($("#name-input").val()))  {
alert  ("Name can not less than 2 char");
return;
}

var mobilere = /[0-9]{10}/;
if  (!mobilere.test($("#phone-input").val()))  {
alert  ("Please enter valid mobile number");
return;
}

if  ($("#email-input").val()=="")  {
alert  ("Please enter your email id");
return;
} 

var reeamil = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,6})?$/;
if  (!reeamil.test($("#email-input").val()))  {
alert  ("Please enter valid email address");
return;
} 

var name = $("#name-input").val();
var phone = $("#phone-input").val();
var email = $("#email-input").val();
var desc = $("#description-input").val();
var data = {
name : name,
phone : phone,
email : email,
desc : desc
};

$.ajax({
type: "POST",
url : " https://0yutj6pm3g.execute-api.us-east-1.amazonaws.com
/dev-mail/mail-us",
dataType: "json",
crossDomain: "true",
contentType: "application/json; charset=utf-8",
data: JSON.stringify(data),
```
11. The script home.py contains code to connect to the internet using port 80 which is used by AWS Route 53. Check that the **apache2** process is not running. If it is stop the process from running because by default is uses port 80. 
12. The **css** files were added in the
**/var/www/FlaskApps/DgmApp/static/css** directory. 

