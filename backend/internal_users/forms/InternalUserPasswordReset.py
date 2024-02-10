
from .base import PasswordResetForm,ReCaptchaField,ReCaptchaV2Checkbox,InternalUser

class InternalUserPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = InternalUser