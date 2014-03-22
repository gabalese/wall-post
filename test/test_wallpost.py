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

    def test_user_can_post_message_in_own_timeline(self):
        """
        User can publish messages to a personal timeline
        """
        status = self.command.execute("Alice -> I love the weather today")
        alice = self.users.getuser("Alice")

        # Command is valid
        self.assertTrue(status)

        # Last message is saved in user timeline
        self.assertIn("I love the weather today", alice.getPosts())

        # Last message should be the last timeline element
        self.assertTrue("I love the weather today" == alice.getPosts()[-1])

    def test_user_can_view_other_user_timeline(self):
        """
        User can view other user's timeline
        """
        status = self.command.execute("Alice")

        # Command is valid
        self.assertTrue(status)

        # status contains the user timeline, a list of Message objects
        self.assertIsInstance(status, list)

        # is this Alice's timeline?
        for message in status:
            self.assertTrue(message.username == "Alice")

    def test_user_can_follow_other_user(self):
        """
        User can subscribe to other people's timeline...
        """
        status = self.command.execute("Charlie follows Alice")

        # Command is valid
        self.assertTrue(status)

        # Alice is in Charlie's following list
        charlie = self.users.getuser("Charlie")
        self.assertIn("Alice", charlie.getFollowing())

    def test_user_can_view_following_users_timeline(self):
        """
        ... and User can view an aggregated list of all subscription
        """
        status = self.command.execute("Charlie wall")

        # Command is valid
        self.assertTrue(status)

        # Status contains the aggregated user timeline, a list of Message
        self.assertIsInstance(status, list)

        # Each status Message can be Charlie's or Alice's
        for message in status:
            self.assertTrue(message.username == ("Charlie" or "Alice"))

    def test_timeline_must_be_in_reverse_order(self):
        """
        User's or aggregated wall must be in chronological reverse order
        """
        self.command.execute("Charlie -> In New York today!")
        self.command.execute("Alice -> Another full day at the office")
        self.command.execute("Charlie -> Love the weather!")
        self.command.execute("Charlie follows Alice")
        self.command.execute("Alice -> I hate my life")

        charlie_wall = self.command.execute("Charlie wall")

        # Each message[n] should be newer than message[n+1]
        for index, message in enumerate(charlie_wall):
            while index + 1 != len(charlie_wall):  # Avoid IndexError Exception
                self.assertGreater(charlie_wall[index].timestamp, charlie_wall[index + 1].timestamp)


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
        self.assertRaises(NoSuchUser, self.command.execute("Piotr"))
