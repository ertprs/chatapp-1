from django import forms

from .models import ChatMessage


class ChatMessageForm(forms.models.ModelForm):

    class Meta:
        model = ChatMessage
        fields = ['text',]
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'chat...',
                'class': 'form-control input-lg',
            }),
        }


# class PreferencesForm(forms.Form):
#     username = forms.CharField(max_length=20, required=False)
#     email = forms.EmailField(required=False)
#     bio = forms.CharField(max_length=50, required=False)