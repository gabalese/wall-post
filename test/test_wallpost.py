import unittest
from src.wallpost import *


class TestSpecs(unittest.TestCase):
    def setUp(self):
        """
        Init data repositories
        """
        self.users = Users()
        # Init command context
        self.command = Command(self.users)

    def test_user_can_post_message_in_own_timeline(self):
        """
        User can publish messages to a personal timeline
        """
        status = self.command.execute("Alice -> I love the weather today")
        alice = self.users.getuser("Alice")

        # Command is valid
        self.assertTrue(status is not None)

        # Last message is saved in user timeline
        self.assertIn("I love the weather today", [message.message for message in alice.getposts()])

        # Last message should be the last timeline element
        self.assertTrue("I love the weather today" == [message.message for message in alice.getposts()][-1])

    def test_user_can_view_other_user_timeline(self):
        """
        User can view other user's timeline
        """
        self.command.execute("Alice -> I love the weather today")
        self.command.execute("Alice -> It's sunny and warm")
        status = self.command.execute("Alice")

        # Command is valid
        self.assertTrue(status is not None)

        # status contains the user timeline, a list of Message objects
        self.assertIsInstance(status, list)

        print status

        # is this Alice's timeline?
        for message in self.command._usertimeline("Alice"):
            self.assertTrue(message.username == "Alice")

    def test_user_can_follow_other_user(self):
        """
        User can subscribe to other people's timeline...
        """
        self.command.execute("Charlie -> Love this place")
        self.command.execute("Alice -> Love this Town!")
        status = self.command.execute("Charlie follows Alice")

        # Command is valid
        self.assertTrue(status is True)

        # Alice is in Charlie's following list
        charlie = self.users.getuser("Charlie")
        charlie_follows = [user.username for user in charlie.getfollowing()]
        self.assertIn("Alice", charlie_follows)

    def test_user_can_view_following_users_timeline(self):
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

        self.command.execute("Charlie wall")
        charlie_wall = self.command._user_wall("Charlie")
        users_in_charlie_wall = set([message.username for message in charlie_wall])
        self.assertTrue({"Charlie", "Bob", "Alice"}.issubset(users_in_charlie_wall))

    def test_timeline_must_be_in_reverse_order(self):
        """
        User's or aggregated wall must be in chronological reverse order
        """
        import time
        self.command.execute("Charlie -> In New York today!")
        time.sleep(0.2)
        self.command.execute("Alice -> Another full day at the office")
        time.sleep(0.5)
        self.command.execute("Charlie -> Love the weather!")
        time.sleep(0.4)
        self.command.execute("Charlie follows Alice")
        time.sleep(0.3)
        self.command.execute("Alice -> I hate my life")
        time.sleep(0.8)
        charlie_wall = self.command.execute("Charlie wall")

        # Each message[n] should be newer than message[n+1]
        for index, message in enumerate(charlie_wall):
            while index+1 > len(charlie_wall):
                self.assertGreaterEqual(charlie_wall[index].timestamp, charlie_wall[index+1].timestamp)


class TestUsers(unittest.TestCase):
    def setUp(self):
        """
        Init data repositories
        """
        self.users = Users()
        # Init command context
        self.command = Command(self.users)

    def test_no_such_user(self):
        """
        The most basic command is <Username>, which returns the <Username> timeline
        What if no such user is present?
        """
        with self.assertRaises(NoSuchUser):
            self.command.execute("Piotr")

    def test_user_follows_no_users(self):
        self.command.execute("Piotr -> Ja liublju tebja")
        status = self.command.execute("Piotr wall")
        self.assertEqual(len(status), 1)

    def test_user_follows_more_than_one_user(self):
        self.command.execute("Nadja -> Its'a good day")
        self.command.execute("Piotr -> Ja liublju tebja, Nadja")
        self.command.execute("Piotr follows Nadja")
        self.command.execute("Olga -> What's up guys?")
        self.command.execute("Piotr -> Tebja todze liubliu!")
        self.command.execute("Piotr follows Olga")
        self.command.execute("Olga -> Are you serious?")

        piotr = self.users.getuser("Piotr")
        self.assertEqual(len(piotr.getfollowing()), 2)

        followed_by_piotr = piotr.getfollowing()
        self.assertIn("Olga", [user.username for user in followed_by_piotr])
        self.assertIn("Nadja", [user.username for user in followed_by_piotr])

        for following in followed_by_piotr:
            self.assertIsNot(None, [(message.message, message.username) for message in following.getposts()])

        self.assertEqual(len(piotr.getposts()), 2)

        status = self.command.execute("Piotr wall")
        self.assertEqual(len(status), 5)

    def test_invalid_user(self):

        with self.assertRaises(NoSuchUser):
            self.command.execute("Piotr")

    def test_invalid_commands(self):

        with self.assertRaises(InvalidCommand):
            self.command.execute("Piotr wall Nestor")

        with self.assertRaises(InvalidCommand):
            self.command.execute("Olga -> Hey")
            self.command.execute("Piotr -> Sdrastvuijte")
            self.command.execute("Nadja -> Sdrastvuijte")
            self.command.execute("Olga follows Piotr Olga Nadja")

    def test_time_intervals_seconds(self):
        import time
        self.command.execute("Alice -> I love the weather today")
        self.command.execute("Bob -> Damn! We lost!")
        self.command.execute("Bob -> Good game though.")
        self.command.execute("Charlie -> I'm in New York today! Anyone wants to have a coffee?")
        self.command.execute("Charlie follows Alice")
        time.sleep(2)
        charlie_wall = self.command.execute("Charlie wall")
        self.assertIn("2 seconds ago", charlie_wall[0])
        charlie_timeline = self.command.execute("Charlie")
        self.assertIn("2 seconds ago", charlie_timeline[0])

    def test_time_intervals_minutes(self):
        charlie = User("Charlie")
        self.users.adduser(charlie)
        message = Message("Charlie", "A-ehm.")
        timestamp_now = datetime.datetime.now().strftime("%s")
        timestamp_two_minutes_ago = int(timestamp_now) - 65
        message.timestamp = timestamp_two_minutes_ago
        charlie.addpost(message)
        charlie_wall = self.command.execute("Charlie")
        self.assertIn("1 minute ago", charlie_wall[0])
