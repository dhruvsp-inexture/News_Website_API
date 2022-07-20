from flask_mail import Message

from app import mail


def send_reset_email(user):
    """function for mailing the user the token to reset password who has requested for it

    Parameters
    ----------
    user: str
        user to whom password reset email will be sent
    """
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender=('No Nonsense News', 'nononsensenews@gmail.com'),
                  recipients=[user.email])
    msg.body = f'''Following is the token to reset your password:
"{token}"
If you didn't send this password reset request then please ignore this mail'''

    mail.send(msg)

    return token
