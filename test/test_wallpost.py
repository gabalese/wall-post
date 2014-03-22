import unittest
from src.wallpost import *


class TestSpecs(unittest.TestCase):
    def setUp(self):
        """
        Init data repositories
        """
        self.messages = Messages()
        self.users = Users()
        # Init command context
        self.command = Command(self.users, self.messages)

    def test_1_user_can_post_message_in_own_timeline(self):
        """
        User can publish messages to a personal timeline
        """
        status = self.command.execute("Alice -> I love the weather today")
        alice = self.users.getuser("Alice")

        # Command is valid
        self.assertTrue(status is not False)

        # Last message is saved in user timeline
        self.assertIn("I love the weather today", [message.message for message in alice.getposts()])

        # Last message should be the last timeline element
        self.assertTrue("I love the weather today" == [message.message for message in alice.getposts()][-1])

    def test_2_user_can_view_other_user_timeline(self):
        """
        User can view other user's timeline
        """
        self.command.execute("Alice -> I love the weather today")
        status = self.command.execute("Alice")

        # Command is valid
        self.assertTrue(status is not False)

        # status contains the user timeline, a list of Message objects
        self.assertIsInstance(status, list)

        # is this Alice's timeline?
        for message in status:
            self.assertTrue(message.username == "Alice")

    def test_3_user_can_follow_other_user(self):
        """
        User can subscribe to other people's timeline...
        """
        self.command.execute("Charlie -> Love this place")
        self.command.execute("Alice -> Love this Town!")
        status = self.command.execute("Charlie follows Alice")

        # Command is valid
        self.assertTrue(status is not False)

        # Alice is in Charlie's following list
        charlie = self.users.getuser("Charlie")
        charlie_follows = [user.username for user in charlie.getfollowing()]
        self.assertIn("Alice", charlie_follows)

    def test_4_user_can_view_following_users_timeline(self):
        """
        ... and User can view an aggregated list of all subscription
        """
        self.command.execute("Charlie -> This is not good")
        self.command.execute("Alice -> Love this place")
        self.command.execute("Alice -> Having a splendid afternoon")
        self.command.execute("Charlie -> I'm fixing nasty bugs")
        self.command.execute("Bob -> Hey guys, what's up?")
        self.command.execute("Charlie follows Alice")
        self.command.execute("Charlie follows Bob")

        charlie_wall = self.command.execute("Charlie wall")
        for message in charlie_wall:
            print message.username, message.timestamp

    def test_5_timeline_must_be_in_reverse_order(self):
        """
        User's or aggregated wall must be in chronological reverse order
        """
        import time
        self.command.execute("Charlie -> In New York today!")
        time.sleep(1)
        self.command.execute("Alice -> Another full day at the office")
        time.sleep(1)
        self.command.execute("Charlie -> Love the weather!")
        time.sleep(1)
        self.command.execute("Charlie follows Alice")
        time.sleep(1)
        self.command.execute("Alice -> I hate my life")
        time.sleep(1)
        charlie_wall = self.command.execute("Charlie wall")

        # Each message[n] should be newer than message[n+1]
        for index, message in enumerate(charlie_wall):
            while index+1 > len(charlie_wall):
                self.assertGreaterEqual(charlie_wall[index], charlie_wall[index+1])


class TestUsers(unittest.TestCase):
    def setUp(self):
        """
        Init data repositories
        """
        self.messages = Messages()
        self.users = Users()
        # Init command context
        self.command = Command(self.users, self.messages)

    def test_no_such_user(self):
        """
        The most basic command is <Username>, which returns the <Username> timeline
        What if no such user is present?
        """
        with self.assertRaises(NoSuchUser):
            self.command.execute("Piotr")
