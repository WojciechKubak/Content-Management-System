from users.extensions import mail_config
from flask import Flask
from typing import Any


def test_send_activation_mail(app: Flask, user_model_data: dict[str, Any]) -> None:
    mail_config.init_app(app)

    with mail_config.mail.record_messages() as outbox:
        email = user_model_data['email']

        mail_config.send_activation_mail(user_model_data['id'], email)

        assert "Activate your account" == outbox[0].subject
        assert [email] == outbox[0].recipients
        assert 'Click to activate your account' in outbox[0].html
