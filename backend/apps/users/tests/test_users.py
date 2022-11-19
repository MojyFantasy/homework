import json

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from users.models import User
from users.tests.factories import UserFactory


def create_a_user(username, password, nickname, email, is_superuser=True):
    """
    创建一个用户
    """
    user = User.objects.create(username=username)
    user.set_password(password)
    user.nickname = nickname
    user.is_superuser = is_superuser
    user.is_active = True
    user.email = email
    user.save()
    return user


class TestClassWithBaseData(TestCase):

    # 添加测试用户
    def setUp(self):
        self.superuser = create_a_user(
            'admin', 'admin', '管理员', 'admin@163.com', is_superuser=True)
        self.test_user = create_a_user(
            'test_user', 'test_user', '测试用户', 'test_user@163.com',
            is_superuser=False)
        self.prepare()

    def prepare(self):
        pass


class TestClassForRegister(APITestCase, TestClassWithBaseData):
    """
    测试注册接口
    """

    url = reverse('users-list')

    def prepare(self):
        pass

    def test_users_register(self):
        """
        测试注册用户
        """
        url = self.url
        response = self.client.post(f'{url}register/', data={
            'email': 'test_user2@163.com', 'nickname': '游客2333',
            'password': '666666'
        })
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email='test_user2@163.com')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.check_password('666666'), True)
        self.assertEqual(user.nickname, '游客2333')

    def test_users_register_error1(self):
        """
        测试注册用户-测试已存在注册邮箱
        """
        url = self.url
        create_a_user(
            'test_user2@163.com', '666666', '游客2', 'test_user2@163.com',
            is_superuser=False)
        response = self.client.post(f'{url}register/', data={
            'email': 'test_user2@163.com', 'nickname': '游客2333',
            'password': '666666'
        })
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(content['result'], 'error')
        self.assertEqual(content['msg'], '该邮箱已被注册！')


class TestClassWithSuperUserLogin(APITestCase, TestClassWithBaseData):
    """
    需要用户登录的测试用例
    """
    def prepare(self):
        username = self.superuser.username
        self.client.post('/api-auth/login/', {'username': username,
                                              'password': 'admin'})
        self.login_user = self.test_user


class TestClassWithNormalUserLogin(APITestCase, TestClassWithBaseData):
    """
    需要用户登录的测试用例
    """
    def prepare(self):
        username = self.test_user.username
        self.client.post('/api-auth/login/', {'username': username,
                                              'password': 'test_user'})
        self.login_user = self.test_user


class UserTestWithSuperUser(TestClassWithSuperUserLogin):
    """
    用户相关测试用例
    """
    url = reverse('users-list')

    def test_users_list(self):
        """
        测试用户列表展示
        """
        url = self.url
        for _ in range(10):
            UserFactory()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 12)

    def test_users_create(self):
        """
        测试超级用户新增用户
        """
        url = self.url
        response = self.client.post(url, data={
            'username': 'test_user2', 'email': 'test_user2@163.com',
            'password': 'test_user2', 'nickname': '测试新增用户',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='test_user2')
        self.assertEqual(user.nickname, '测试新增用户')
        self.assertEqual(user.check_password('test_user2'), True)
        self.assertEqual(user.is_active, True)

    def test_users_detail(self):
        """
        测试用户详情展示
        """
        url = self.url
        user_id = self.superuser.id
        response = self.client.get(f'{url}{user_id}/', format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['username'], 'admin')
        self.assertEqual(content['id'], user_id)

    def test_users_update(self):
        """
        测试用户修改信息
        """
        url = self.url
        user_id = self.test_user.id
        response = self.client.patch(
            f'{url}{user_id}/', data={'nickname': '游客1'}, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['username'], 'test_user')
        self.assertEqual(content['nickname'], '游客1')
        self.assertEqual(content['id'], user_id)

    def test_users_delete(self):
        """
        测试删除用户
        """
        url = self.url
        user_id = self.test_user.id
        response = self.client.delete(f'{url}{user_id}/')
        self.assertEqual(response.status_code, 204)
        user = User.objects.get(id=user_id)
        self.assertEqual(user.is_active, False)


class UserTestWithNormalUser(TestClassWithNormalUserLogin):
    """
    用户相关测试用例（普通用户登录）
    """
    url = reverse('users-list')

    def test_users_list(self):
        """
        测试用户列表展示（普通用户只能看到自己的用户信息）
        """
        url = self.url
        for _ in range(10):
            UserFactory()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 1)

    def test_users_create(self):
        """
        测试超级用户新增用户(普通用户无新增用户权限)
        """
        url = self.url
        response = self.client.post(url, data={
            'username': 'test_user2', 'email': 'test_user2@163.com',
            'password': 'test_user2', 'nickname': '测试新增用户',
        }, format='json')
        self.assertEqual(response.status_code, 403)

    def test_users_detail(self):
        """
        测试用户详情展示
        """
        url = self.url
        user_id = self.test_user.id
        response = self.client.get(f'{url}{user_id}/', format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['username'], 'test_user')
        self.assertEqual(content['id'], user_id)

    def test_users_update(self):
        """
        测试用户修改信息(普通用户无修改权限)
        """
        url = self.url
        user_id = self.test_user.id
        response = self.client.patch(
            f'{url}{user_id}/', data={'nickname': '游客1'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_users_delete(self):
        """
        测试删除用户(普通用户无删除权限)
        """
        url = self.url
        user_id = self.test_user.id
        response = self.client.delete(f'{url}{user_id}/')
        self.assertEqual(response.status_code, 403)
