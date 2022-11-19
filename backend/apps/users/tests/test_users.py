import json

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from users.models import User, Org


def create_a_user(username, password, nickname, org):
    """
    创建一个用户
    """
    user = User.objects.create(username=username)
    user.set_password(password)
    user.nickname = nickname
    user.is_superuser = True
    user.is_active = True
    user.org = org
    user.save()
    return user


def create_a_org(name, parent=None):
    """
    创建一个组织机构
    :param name: 机构名称
    :param parent: 父级机构
    """
    org = Org()
    org.name = name
    if parent:
        org.parent = parent
    org.save()
    return org


class TestClassWithBaseData(TestCase):

    # 添加测试用户
    def setUp(self):
        self.org = create_a_org(name='测试机构')
        self.test_user = create_a_user('test_user', '666666', '测试用户',
                                       self.org)
        self.second_test_user = create_a_user('second_test_user', '777777', '第二个用户', self.org)
        self.prepare()

    def prepare(self):
        pass


class TestClassWithLogin(APITestCase, TestClassWithBaseData):
    """
    需要用户登录的测试用例
    """
    def prepare(self):
        username = self.test_user.username
        self.client.post('/api-auth/login/', {'username': username,
                                              'password': '666666'})
        self.login_user = self.test_user


class UserTest(TestClassWithLogin):
    """
    用户相关测试用例
    """
    url = reverse('users-list')

    def test_users_list(self):
        """
        测试用户列表展示
        """
        url = self.url
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 2)

    def test_change_password(self):
        """
        测试修改密码接口
        :return:
        """
        url = self.url + 'change_password/'
        response = self.client.post(url, {'old_password': '666666',
                                          'new_password': '777777'})
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(id=self.test_user.id)
        self.assertTrue(user.check_password('777777'))

    def test_i_am(self):
        url = self.url + 'iam/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['id'], self.test_user.id)
