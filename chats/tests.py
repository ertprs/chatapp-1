from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import FriendRequest

# Create your tests here.



class ChatTest(TestCase):

    def test_a_users_friend_request(self):
        User.objects.create_user(username='admin', password='chikey12')
        User.objects.create_user(username='chiks', password='chikey12')
        admin = User.objects.get(pk=1)
        chiks = User.objects.get(pk=2)
        self.assertEqual(admin.username, 'admin')
        self.assertEqual(chiks.username, 'chiks')



        FriendRequest.objects.create(username=admin.username, user=chiks)
        print(chiks.friendrequest_set.all())
        self.assertIn(admin.username, chiks.friendrequest_set.all())

