from django import forms
from .models import *


class RoomForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        # Filter the 'course' queryset based on the 'user'
        self.fields['course'].queryset = Course.objects.filter(user=user)

    topic = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label="Category", to_field_name="name")

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']