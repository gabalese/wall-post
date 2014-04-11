import unittest
from src.client import Client, Users, Message, NoSuchUser


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(Users())

    def test_client_instances(self):
        self.client.post("Piotr", "Sdrastvujte")
        self.assertIsInstance(self.client.get_user_timeline("Piotr")[0], Message)

    def test_user_can_post(self):
        self.client.post("Piotr", "Hello world!")
        self.assertEquals(self.client.get_user_timeline("Piotr")[0].message, "Hello world!")


class TestUserPosts(unittest.TestCase):
    def setUp(self):
        self.client = Client(Users())
        self.client.post("Piotr", "Hello there")
        self.client.post("Piotr", "What's up?")
        self.client.post("Olga", "Lovely morning")

    def test_user_can_follow(self):
        self.client.follow("Piotr", "Olga")
        piotr = self.client.get_user_profile("Piotr")
        self.assertEquals(piotr.getfollowing()[0].username, "Olga")

    def test_user_can_view_other_walls(self):
        olga_wall = self.client.get_user_wall("Olga")
        self.assertEqual(len(olga_wall), 1)

    def test_user_cannot_see_uncreated_user_wall(self):
        with self.assertRaises(NoSuchUser):
            self.client.get_user_timeline("Nadja")


if __name__ == '__main__':
    unittest.main()
