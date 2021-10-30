from flask import Flask, request, session, render_template
from twilio.twiml.messaging_response import MessagingResponse
import os, time

from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("./key.json")
initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # Start our TwiML response
    resp = MessagingResponse()
    body = request.values.get('Body', None)

    if 'question_id' in session and session['question_id'] is not None:
        q = session['question_id']
        if q == 1:
            session['feedback'] = body
            session['question_id'] = None
            resp.message('Thank you')
        if q == 0:
            resp.message('What feedback would you like to send to ' + body + '?')
            session['professor'] = body
        if session['question_id'] is not None: session['question_id'] += 1
        # store data
        doc_id = request.values.get('From')
        msg_id = db.collection('feedback-data').document(doc_id).collection('messages').document()
        timestamp = time.time()
        msg_id.set({ 'question_id': q, 'body': body, 'timestamp': timestamp })
    else:
        # Start survey
        session['question_id'] = 0
        resp.message('Hi! Who would you like to give feedback to today?')

    return str(resp)

@app.route("/dashboard", methods=['GET'])
def dashboard():
    allItems = []
    for n in ['+13479331820', '+18452826490']:
        for d in list(db.collection(u'feedback-data').document(n).collection(u'messages').stream()):
            data = d.to_dict()
            data['id'] = n
            allItems.append(data)
    return render_template('dashboard.html', items = allItems)  

if __name__ == "__main__":
    app.run(debug=True)
