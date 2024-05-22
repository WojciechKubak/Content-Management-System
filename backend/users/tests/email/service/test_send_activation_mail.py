from tests.factory import UserFactory
from users.email.configuration import mail


def test_send_activation_mail() -> None:
    user = UserFactory()

    with mail.mail.record_messages() as outbox:
        mail.send_activation_mail(user.id, user.email)

        assert "Activate your account" == outbox[0].subject
        assert [user.email] == outbox[0].recipients
        assert 'Click to activate your account' in outbox[0].html
