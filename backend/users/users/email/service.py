from flask import Flask
from flask_mail import Mail, Message
from jinja2 import PackageLoader, Environment
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MailService:
    """
    MailConfig Class

    This class provides methods for configuring and sending emails.

    Attributes:
        mail (Mail): An instance of the Flask-Mail class for managing email functionality.
        template_env (Environment): An instance of the Jinja2 Environment class for rendering email templates.
    """
    register_token_lifespan_secs: str
    mail_username: str
    base_url: str
    template_module: str
    
    def __post_init__(self):
        self.mail = Mail()
        self.template_env = Environment(loader=PackageLoader(self.template_module))
    
    def init_app(self, app: Flask) -> None:
        """
        Prepare Mail Configuration

        Configures the MailConfig class with a Flask app.

        Args:
            app (Flask): The Flask app instance.

        Returns:
            None
        """
        self.mail.init_app(app)

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
        timestamp = datetime.now().timestamp() * 1000 + self.register_token_lifespan_secs
        activation_url = f'{self.base_url}/activate?id={id_}&timestamp={timestamp}'
        template = self.template_env.get_template('activation_mail.html')
        html_body = template.render(activation_url=activation_url)

        message = Message(
            subject='Activate your account',
            sender=self.mail_username,
            recipients=[email],
            html=html_body
        )
        self.mail.send(message)
