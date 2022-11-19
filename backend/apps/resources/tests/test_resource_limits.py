import json

from rest_framework.reverse import reverse

from resources.models import Resource, ResourceLimit
from resources.tests.factories import ResourceFactory, ResourceLimitFactory
from users.models import User
from users.tests.factories import UserFactory
from users.tests.test_users import TestClassWithSuperUserLogin, \
    TestClassWithNormalUserLogin


class ResourceLimitTestWithSuperUser(TestClassWithSuperUserLogin):
    """
    资源配额相关测试用例
    """
    url = reverse('resource_limits-list')

    def test_resource_limits_list(self):
        """
        测试资源配额列表展示
        """
        url = self.url
        for _ in range(10):
            ResourceLimitFactory()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 10)

    def test_resource_limits_create(self):
        """
        测试超级用户新增资源配额
        """
        url = self.url
        response = self.client.post(url, data={
            'user_id': self.test_user.id, 'is_limited': True, 'max_limit': 5
        }, format='json')
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['max_limit'], 5)
        self.assertEqual(content['user']['id'], self.test_user.id)

    def test_resource_limits_detail(self):
        """
        测试资源配额详情展示
        """
        resource_limit = ResourceLimit.objects.create(
            user=self.test_user, is_limited=True, max_limit=5,
            creator=self.superuser, modifier=self.superuser)
        url = self.url
        response = self.client.get(f'{url}{resource_limit.id}/', format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['max_limit'], 5)
        self.assertEqual(content['user']['id'], self.test_user.id)

    def test_resource_limits_update(self):
        """
        测试资源配额修改信息(超级用户创建)
        """
        resource_limit = ResourceLimit.objects.create(
            user=self.test_user, is_limited=True, max_limit=5,
            creator=self.superuser, modifier=self.superuser)

        url = self.url
        response = self.client.patch(f'{url}{resource_limit.id}/', data={
            'max_limit': '8'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['max_limit'], 8)
        self.assertEqual(content['user']['id'], self.test_user.id)

    def test_resource_limits_delete(self):
        """
        测试删除资源(超级用户创建)
        """
        resource_limit = ResourceLimit.objects.create(
            user=self.test_user, is_limited=True, max_limit=5,
            creator=self.superuser, modifier=self.superuser)

        url = self.url
        response = self.client.delete(f'{url}{resource_limit.id}/')
        self.assertEqual(response.status_code, 204)
        resource_limit = ResourceLimit.objects.get(id=resource_limit.id)
        self.assertEqual(resource_limit.is_deleted, True)


class ResourceTestWithNormalUser(TestClassWithNormalUserLogin):
    """
    资源配额相关测试用例
    """
    url = reverse('resource_limits-list')

    def test_resource_limits_list(self):
        """
        测试资源配额列表展示（普通用户无权访问）
        """
        url = self.url
        for _ in range(10):
            ResourceLimitFactory()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)

    def test_resource_limits_create(self):
        """
        测试超级用户新增资源配额（普通用户无权访问）
        """
        url = self.url
        response = self.client.post(url, data={
            'user_id': self.test_user.id, 'is_limited': True, 'max_limit': 5
        }, format='json')
        self.assertEqual(response.status_code, 403)

    def test_resource_limits_detail(self):
        """
        测试资源配额详情展示（普通用户无权访问）
        """
        resource_limit = ResourceLimit.objects.create(
            user=self.test_user, is_limited=True, max_limit=5,
            creator=self.superuser, modifier=self.superuser)
        url = self.url
        response = self.client.get(f'{url}{resource_limit.id}/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_resource_limits_update(self):
        """
        测试资源配额修改信息(超级用户创建)（普通用户无权访问）
        """
        resource_limit = ResourceLimit.objects.create(
            user=self.test_user, is_limited=True, max_limit=5,
            creator=self.superuser, modifier=self.superuser)

        url = self.url
        response = self.client.patch(f'{url}{resource_limit.id}/', data={
            'max_limit': '8'
        }, format='json')
        self.assertEqual(response.status_code, 403)

    def test_resource_limits_delete(self):
        """
        测试删除资源(超级用户创建)（普通用户无权访问）
        """
        resource_limit = ResourceLimit.objects.create(
            user=self.test_user, is_limited=True, max_limit=5,
            creator=self.superuser, modifier=self.superuser)

        url = self.url
        response = self.client.delete(f'{url}{resource_limit.id}/')
        self.assertEqual(response.status_code, 403)
