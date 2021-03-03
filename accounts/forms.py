from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):

    class Meta:
        #grabbing specific field from the default model
        fields = ('username','email','password1','password2')
        #connect with the default model
        model = get_user_model()

    #an optional function to create a label in field
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'
