from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from os import environ

app = Flask(__name__)
app.config.from_object('config.default')
settings = environ.get('FORMIDABLE_SETTINGS_MODULE', None)
if settings:
    app.config.from_object(settings)

mail = Mail(app)


@app.route("/submit", methods=['POST'])
def submit():
    referrer = request.referrer
    next_page = request.form.get('next_page', app.config.get('THANKYOU_PAGE_DEFAULT'))
    originator = request.form.get('email', 'unknown')
    mailtext = render_template('new_submit_mail.txt', form=request.form, referrer=request.referrer)
    message = Message(body=mailtext,
                      subject='New form submission on {} from {}'.format(referrer, originator),
                      sender=app.config.get('MAIL_SENDER'),
                      recipients=app.config.get('MAIL_RECIPIENTS'),
                      reply_to=originator if originator != 'unknown' else None
                      )
    print(app.config)
    mail.send(message)

    return redirect(next_page)


if __name__ == '__main__':
    app.run()