from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from os import environ


app = Flask(__name__)
app.config.from_object('config.default')
settings = environ.get('FORMIDABLE_SETTINGS_MODULE', None)
if settings:
    app.config.from_object(settings)
    if not app.config.get('SPAM_PAGE_DEFAULT'):
        app.config['SPAM_PAGE_DEFAULT'] = app.config.get('THANKYOU_PAGE_DEFAULT')

mail = Mail(app)


@app.route("/submit", methods=['POST'])
def submit():
    if app.config.get('GOTCHA_FIELD') and request.form.get(app.config.get('GOTCHA_FIELD')):
        next_page = request.form.get('next_page', app.config.get('SPAM_PAGE_DEFAULT'))
        return redirect(next_page)

    referrer = request.referrer
    originator = request.form.get('email', 'unknown')
    mailtext = render_template('new_submit_mail.txt', form=request.form, referrer=request.referrer)
    message = Message(body=mailtext,
                      subject='New form submission on {} from {}'.format(referrer, originator),
                      sender=app.config.get('MAIL_SENDER'),
                      recipients=app.config.get('MAIL_RECIPIENTS'),
                      reply_to=originator if originator != 'unknown' else None
                      )
    if not app.config.get('DEBUG'):
        mail.send(message)

    next_page = request.form.get('next_page', app.config.get('THANKYOU_PAGE_DEFAULT'))
    return redirect(next_page)


if __name__ == '__main__':
    app.run()
