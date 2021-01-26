#from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
#from .models import Tok
User = get_user_model()


class MyBackend(object):

    def authenticate(self, email, uid):
        try:
            user = User.objects.get(uid=uid)
            return user
        except User.DoesNotExist:
            return None
        # except Token.DoesNotExist:
        #     return None

    def get_user(self, email):
        try:
            return User.objects.get(pk=email)
        except User.DoesNotExist:
            return None



