from django.test import TestCase,Client
from bs4 import BeautifulSoup
from .models import Post
from django.db import models

# Create your tests here.



class TestView(TestCase): #Test 무조건 포함

    # 함수 시작에서 test 무조건 포함

    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        response = self.client.get('/blog/', follow=True)
        # response 결과가 정상적으로 보이는지 test
        self.assertEqual(response.status_code, 200)

        # beautifulsoup 적용
        soup = BeautifulSoup(response.content, 'html.parser')

        #title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog') #title 안에 있는 글자 -> .text -> 통과

        #navbar가 정상적으로 보이는지
        # navbar - soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About me', navbar.text)

        #post가 정상적으로 보이는지
        #1. 맨 처음에는 Post가 없음(db에)
        self.assertEqual(Post.objects.count(),0)
        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        #2. Post가 추가
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.")
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.")
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        def test_post_detail(self):
            post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.")
            self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

            response = self.client.get('/blog/1/', follow=True) # '/blog/1/'
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')

            #navbar
            navbar = soup.nav
            self.assertIn('Blog', navbar.text)
            self.assertIn('About Me', navbar.text)

            self.assertIn(post_001.title, soup.title.text)
            main_area = soup.find('div', id='main-area')
            post_area = main_area('div', id='post-area')
            self.assertIn(post_001.title, post_area.text)
            self.assertIn(post_001.content, post_area.text)

