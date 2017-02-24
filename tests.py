from django.test import TestCase
from awsomeProject.models import Game
from django.contrib.auth.models import User


class BasicTest(TestCase):
    def test_basic(self):
        a = 1
        self.assertEqual(a, 1)

class PlayerTest(TestCase):
    def test_fail(self):
        pass
