from flask_mail import Message

from app import celery_app
from database.models import Category, User, user_datastore
from celery_context import taskContext
from mailer import mail

# @app.route()
@celery_app.task(base=taskContext)
def helloWorld():
    print('this is the first test task')
    return 'hello world'

@celery_app.task(base=taskContext)
def add(a, b):
    x = a
    y = b
    return x + y

@celery_app.task(base=taskContext)
def fetch_X_category(x):
    cate = Category.query.filter_by(id=x).first()
    if not cate:
        return 'No category found by that id'
    print(cate.description)
    return cate.name


@celery_app.task(base=taskContext)
def monthly_mail_demo():  # this is a demo task for sending mail to all users monthly, not following the problem statement's conditions
    users = User.query.all()
    for user in users:
        email_user = user.email
        email_subject = f"Hello, user: {user.id}! This is a monthly mail from us."
        email_body = f"hello {user.email},/n this is a test mail, kindly check the attached html/n/n regards/n admin"
        cate = Category.get_all()
        email_html = "<html><body>"
        for category in cate:
            if user_datastore.has_role(user, 'admin'):
                email_html += f"<h1>Category: {category.name}</h1>"
                email_html += f"<p>Description: {category.description}</p>"
                email_html += f"<p>Status: {category.status}</p>"
                email_html += f"<p>Created at: {category.created_at}</p>"
                email_html += f"<p>Created by: {category.created_by}</p>"
                email_html += f"<p>User's email: {user.email}</p>"
            else:
                email_html += f"<h1>No categories found</h1>"
        email_html += "</body></html>"

        msg = Message(subject=email_subject, recipients=[email_user], )
        msg.html = email_html
        msg.body = email_body
        # msg.attachments = ['']
        msg.sender = 'admin@grocerystore.com'
        mail.send(msg)

        return 'Mail sent successfully'