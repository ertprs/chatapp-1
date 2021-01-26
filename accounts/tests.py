from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, call
import uuid
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import accounts.views

# Create your tests here.

class ModelsTest(TestCase):

    def test_user_can_register(self):
        username = chiks
        password = chikey12
        password2 = chikey12
        response = self.client.post(
            '/register',
            data={'username': username,
                  'password': password,
                  'password2': password2,
                  })


# class HomePageView(TestCase):
#
#     def test_home_page_template(self):
#         response = self.client.get('/')
#         self.assertTemplateUsed(response, 'home.html')
#
#     def test_content_in_home_page_template(self):
#         response = self.client.get('/')
#         # self.assertContains(response, 'MailApp')
#         # self.assertContains(response, 'Sign Up')
#         # self.assertContains(response, 'Login')
#         self.assertContains(response, 'email')
#
#     def test_message_displays_when_user_tries_to_signup(self):
#         response = self.client.post('/send_login_email', data={'email': 'sonia@example.com'}, follow=True)
#
#         print(response.context['messages'])
#         message = list(response.context['messages'])[0]
#         self.assertEqual(
#             message.message,
#             "Email link sent to sonia@example.com"
#         )
#         self.assertEqual(message.tags, "success")
#
#
#     def test_redirects_to_home_page(self):
#         response = self.client.post('/send_login_email', data={'email': 'chikioffor@gmail.com'})
#         self.assertRedirects(response, '/')
#
#     def test_a_user_can_sign_out_and_get_redirected_to_home_page(self):
#         response = self.client.get('/logout')
#         self.assertRedirects(response, '/')















    # @patch('accounts.views.send_login_email')
    # def test_redirects_to_sent_mail_template(self, mock_send_login_email):
    #     self.client.post('/send_login_email', data={
    #         'email': 'chikioffor@gmail.com'
    #     })
    #
    #     self.assertEqual(mock_send_login_email.called, True)
    #     (subject, body, from_email, to_list), kwargs = mock_send_login_email.call_args
    #     self.assertEqual(subject, 'Your login link to MailApp')
    #     self.assertEqual(from_email, 'noreply@chatapp')
    #     self.assertEqual(to_list, ['chikioffor@gmail.com'])

























