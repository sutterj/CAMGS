from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Composition, NoteObject
from django.forms import ModelForm, RadioSelect


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class CompositionEditForm(ModelForm):
    class Meta:
        model = Composition
        fields = [
            'title', 'composer', 'tempo',
            'base_beat', 'beats_per_bar', 'enharmonic'
        ]


class NoteCreateForm(ModelForm):
    class Meta:
        model = NoteObject
        fields = ['order', 'pitch', 'duration']
        widgets = {
            'pitch': RadioSelect()
        }


class NoteEditForm(ModelForm):
    class Meta:
        model = NoteObject
        fields = ['order', 'pitch', 'duration']
