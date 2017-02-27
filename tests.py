from django.test import TestCase, RequestFactory
from awsomeProject.models import Game, UserProfile
from django.contrib.auth.models import User
from awsomeProject.views import registerForAPI, manageUploadedGames


class BasicTest(TestCase):
    def test_basic(self):
        a = 1
        self.assertEqual(a, 1)

class PlayerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jacob', email='jacob@jacob.com', password='top_secret')
        self.userProfile = UserProfile(user=self.user, isDeveloper=False)
        self.userProfile.save()

    def test_player_can_not_register_for_API(self):
        request = self.factory.get('/registerForAPI')
        request.user = self.user
        response = registerForAPI(request)
        self.assertEqual(response.status_code, 404)

    def test_player_can_not_manage_game(self):
        request  = self.factory.get('/myProfile/manageUploadedGames')
        request.user = self.user
        response = manageUploadedGames(request)
        self.assertEqual(response.status_code, 302)
