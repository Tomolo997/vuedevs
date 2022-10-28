from ast import Try
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
class EmailAuthBackend(ModelBackend):
    def authenticate(self,request,username,password):
        try:
            user = User.objects.get(email=username)
            success = user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            pass
        return None
    
    def get_user(self,uid):
        try:
            return User.objects.get(pk=uid)
        except:
            return None