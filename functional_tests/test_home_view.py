from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class HomepageTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_a_user_can_see_items_on_the_home_page(self):
        # Sonia heard about this new chatapp and decided to check it out
        self.browser.get(self.live_server_url)

        # She sees an inputbox
        inputbox = self.browser.find_element_by_name('email')
        self.assertTrue(inputbox)



    def test_a_user_can_login(self):
        # and she sees an input box with a label asking her to enter her email to login
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_name('email')

        # She decided to sign up
        inputbox.send_keys('sonia@example.com')
        inputbox.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(5)

        # Successfully she sees a success message displayed
        message = self.browser.find_element_by_class_name('message')
        self.assertEqual(message.text, "Email link sent to sonia@example.com")
    #
    #     # Successfully she receives a uid link.
    #     uid = 'abc-d-ef'
    #
    #     # And she decides to log into it
    #
    #     response = self.browser.post(self.live_server_url + f'/login?token={uid}')
    #     self.assertEqual(response.status_code, 302)



        # # She now notices a message saying an email link has been sent
        # info_message = self.browser.find_element_by_css_selector('.email-link')
        #
        # self.assertEqual(info_message.text, "An email link has been sent to sonia@gmail.com")



