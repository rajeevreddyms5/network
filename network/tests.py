from django.test import TestCase, Client
from .models import UserProfile, User, Posts

# Create your tests here.

# create test case for Posts model
class PostsModelTestCase(TestCase):
        
    def setUp(self):
        # create test user and user1
        user0 = User.objects.create_user(username="user0", email="user0@email", password="password0")
        user1 = User.objects.create_user(username="user1", email="user1@email", password="password1")
        user2 = User.objects.create_user(username="user2", email="user2@email", password="password2")

        # test posts made by user
        Posts.objects.create(content="test content by user 1", author = user0)
        Posts.objects.create(content="text content by user 2", author = user1)
        Posts.objects.create(content="test content by user 3", author = user2)

    # test default likes
    def test_likes(self):

        # get post objects
        post0 = Posts.objects.get(content="test content by user 1")
        post1 = Posts.objects.get(content="text content by user 2")
        post2 = Posts.objects.get(content="test content by user 3")

        # test likes
        self.assertEqual(post0.liked.all().count(), 0)
        self.assertEqual(post1.liked.all().count(), 0)
        self.assertEqual(post2.liked.all().count(), 0)

    # tests likes after adding likes
    def test_posts_after_adding_likes(self):

        # get user objects
        user0  = User.objects.get(username="user0")
        user1  = User.objects.get(username="user1")
        user2  = User.objects.get(username="user2")

        # get post objects
        post0 = Posts.objects.get(content="test content by user 1")
        post1 = Posts.objects.get(content="text content by user 2")
        post2 = Posts.objects.get(content="test content by user 3")

        # add likes by the user
        post0.liked.add(user0)
        post1.liked.add(user1)

        # test
        self.assertQuerysetEqual(post0.liked.all(), [user0])
        self.assertQuerysetEqual(post1.liked.all(), [user1])
        self.assertQuerysetEqual(post2.liked.all(), [])
        
    
    # test index view page response
    def test_index(self):
        
            # setup client to make requests
            c = Client()
        
            # send get request to index page and store response
            response = c.get("")
        
            # make sure the status code is 200
            self.assertEqual(response.status_code, 200)
            
            # make sure three posts are returned in the context
            self.assertEqual(response.context['posts'].count(), 3)
    

# create UserProfile Model Test Case
class UserProfileModelTestCase(TestCase):

    def setUp(self):

        # create test user, user1 and user2
        user0 = User.objects.create_user(username="user0", email="user0@email", password="password0")
        user1 = User.objects.create_user(username="user1", email="user1@email", password="password1")
        user2 = User.objects.create_user(username="user2", email="user2@email", password="password2")

        # add followers
        UserProfile.objects.create(user_name=user0, follows=user1)
        UserProfile.objects.create(user_name=user1, follows=user0)
        UserProfile.objects.create(user_name=user1, follows=user2)

    # test user is followed by
    def test_followed_by(self):
        # get user objects
        user0  = User.objects.get(username="user0")
        user1  = User.objects.get(username="user1")
        user2  = User.objects.get(username="user2")

        # test number of users the user is following
        self.assertEqual(user0.following.all().count(), 1)
        self.assertEqual(user1.following.all().count(), 2)
        self.assertEqual(user2.following.all().count(), 0)
        
        # test number of users the user is followed by
        self.assertEqual(user0.followed_by.all().count(), 1)
        self.assertEqual(user1.followed_by.all().count(), 1)
        self.assertEqual(user2.followed_by.all().count(), 1)
    
    # test profile page if the user is not logged in
    def test_profile_view_not_loggedin(self):
         response = self.client.get("/profile/")
         self.assertEqual(response.status_code, 404)
    

   # test profile page if the user is loggedin
    def test_profile_view_loggedin(self):

        # get user objects
        user0  = User.objects.get(username="user0")
        user1  = User.objects.get(username="user1")
        user2  = User.objects.get(username="user2")
        
        # test posts made by user
        Posts.objects.create(content="test content by user 1", author = user0)
        Posts.objects.create(content="text content by user 2", author = user1)
        Posts.objects.create(content="test content by user 3", author = user2)

        # setup client
        c = Client()

        # login the user0
        response = c.post("/login", {
            "username": "user0",
            "password": "password0"
        })
        self.assertEqual(response.status_code, 302)

        # get profile page
        response = c.get("/profile")
        self.assertEqual(response.status_code, 200)

        # test profile page content
        self.assertEqual(response.context['followed_by'], 1)
        self.assertEqual(response.context['following'], 1)
        self.assertEqual(response.context['posts'].count(), 1)
        self.assertEqual(response.context['no_posts'], 1)
        self.assertEqual(len(response.context['users']), 2)
    

    # test following page if the user is not logged in
    def test_following_view_not_loggedin(self):
         response = self.client.get("/profile/")
         self.assertEqual(response.status_code, 404)
        
    
    # test following page if the user is loggedin
    def test_profile_view_loggedin(self):

        # get user objects
        user0  = User.objects.get(username="user0")
        user1  = User.objects.get(username="user1")
        user2  = User.objects.get(username="user2")
        
        # test posts made by user
        Posts.objects.create(content="test content by user 1", author = user0)
        Posts.objects.create(content="text content a by user 2", author = user1)
        Posts.objects.create(content="text content b by user 2", author = user1)
        Posts.objects.create(content="test content by user 3", author = user2)

        # setup client
        c = Client()

        # login the user0
        response = c.post("/login", {
            "username": "user0",
            "password": "password0"
        })
        self.assertEqual(response.status_code, 302)

        # get profile page
        response = c.get("/following")
        self.assertEqual(response.status_code, 200)

        # test profile page content
        self.assertEqual(len(response.context['posts']), 2)
        self.assertEqual(response.context['no_posts'], 2)