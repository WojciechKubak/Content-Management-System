
from users.settings import REGISTER_TOKEN_LIFESPAN
from flask_mail import Mail, Message
from jinja2 import PackageLoader, Environment
from flask import Flask
from dataclasses import dataclass, field
from jinja2 import Environment
from datetime import datetime
import os


@dataclass
class MailConfig:
    """
    MailConfig Class

    This class provides methods for configuring and sending emails.

    Attributes:
        mail (Mail): An instance of the Flask-Mail class for managing email functionality.
        template_env (Environment): An instance of the Jinja2 Environment class for rendering email templates.
    """
    mail: Mail = field(default=None)
    template_env: Environment = field(
        default=Environment(
            loader=PackageLoader('users.email', 'templates')
            )
        )
    
    def init_app(self, app: Flask) -> None:
        """
        Prepare Mail Configuration

        Configures the MailConfig class with a Flask app.

        Args:
            app (Flask): The Flask app instance.

        Returns:
            None
        """
        self.mail = Mail(app)

    def send_activation_mail(self, id_: int, email: str) -> None:
        """
        Send Activation Mail

        Sends an activation email to the specified email address with an activation link.

        Args:
            id_ (int): The user ID for activation.
            email (str): The email address to which the activation email is sent.

        Returns:
            None
        """
        timestamp = datetime.now().timestamp() * 1000 + REGISTER_TOKEN_LIFESPAN
        activation_url = f'http://localhost:81/users/activate?id={id_}&timestamp={timestamp}'
        template = self.template_env.get_template('activation_mail.html')
        html_body = template.render(activation_url=activation_url)

        message = Message(
            subject='Activate your account',
            sender=os.environ.get('MAIL_USERNAME'),
            recipients=[email],
            html=html_body
        )
        self.mail.send(message)
