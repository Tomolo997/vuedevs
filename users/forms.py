from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Developer,Business, Skill, Message , Availability , RoleLevel, RoleType


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class DeveloperForm(ModelForm):
    class Meta:
        model = Developer
        fields = ['name',
                  'city', 'country','hero', 'bio', 'profile_image','timezone',
                  'social_github', 'social_linkedin', 'social_twitter',
                 'social_website']

    def __init__(self, *args, **kwargs):
        super(DeveloperForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'bio':
                field.widget.attrs.update({'class': 'create-developer__input'})
            elif name == 'profile_image':
                field.widget.attrs.update({'class': 'create-developer__input'})
            else: 
                field.widget.attrs.update({'class': 'create-developer__field-textarea'}) 

class AvailabilityForm(ModelForm):
    class Meta:
        model = Availability
        fields = ['available', 'open',
                  'not_available']

    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class RoleTypeForm(ModelForm):
    class Meta:
        model = RoleType
        fields = ['part_time_contract', 'full_time_contract',
                  'full_time_job']

    def __init__(self, *args, **kwargs):
        super(RoleTypeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class RoleLevelForm(ModelForm):
    class Meta:
        model = RoleLevel
        fields = ['junior', 'mid',
                  'senior','principal','c_level']

    def __init__(self, *args, **kwargs):
        super(RoleLevelForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ['bio',
                  'name','profile_image','website']

    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'bio':
                field.widget.attrs.update({'class': 'create-developer__input'})
            elif name == 'profile_image':
                field.widget.attrs.update({'class': 'create-developer__input'})
            else: 
                field.widget.attrs.update({'class': 'create-developer__field-textarea'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'conversations-input'})