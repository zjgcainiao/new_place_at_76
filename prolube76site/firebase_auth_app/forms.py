from django import forms
from firebase_auth_app.models import FirebaseUser

class FirebaseUserCreationForm(forms.ModelForm):

    class Meta:
        model = FirebaseUser
        fields = [
            'firebase_user_display_name',
            'firebase_user_email',
            'firebase_user_phone_number',
            'firebase_user_photo_url',
            'firebase_user_password',
        ]