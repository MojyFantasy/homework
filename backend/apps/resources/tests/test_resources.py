import json

from rest_framework.reverse import reverse

from resources.models import Resource, ResourceLimit
from resources.tests.factories import ResourceFactory
from users.models import User
from users.tests.factories import UserFactory
from users.tests.test_users import TestClassWithSuperUserLogin, \
    TestClassWithNormalUserLogin


class ResourceTestWithSuperUser(TestClassWithSuperUserLogin):
    """
    资源相关测试用例
    """
    url = reverse('resources-list')

    def test_resources_list(self):
        """
        测试资源列表展示
        """
        url = self.url
        for _ in range(10):
            ResourceFactory()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 10)

    def test_resource_create(self):
        """
        测试超级用户新增资源
        """
        url = self.url
        response = self.client.post(url, data={
            'title': '测试主题', 'content': '测试内容'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['title'], '测试主题')
        self.assertEqual(content['content'], '测试内容')
        self.assertEqual(content['creator']['id'], self.superuser.id)
        self.assertEqual(content['modifier']['id'], self.superuser.id)

    def test_resources_detail(self):
        """
        测试资源详情展示
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.superuser,
            modifier=self.superuser)
        url = self.url
        response = self.client.get(f'{url}{resource.id}/', format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['title'], '123')
        self.assertEqual(content['content'], '123123123')

    def test_resources_update(self):
        """
        测试资源修改信息(超级用户创建)
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.superuser,
            modifier=self.superuser)
        url = self.url
        response = self.client.patch(f'{url}{resource.id}/', data={
            'content': '456456'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['title'], '123')
        self.assertEqual(content['content'], '456456')

    def test_resources_update_1(self):
        """
        测试资源修改信息(普通用户创建)
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.test_user,
            modifier=self.test_user)
        url = self.url
        response = self.client.patch(f'{url}{resource.id}/', data={
            'content': '456456'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['title'], '123')
        self.assertEqual(content['content'], '456456')

    def test_resources_delete(self):
        """
        测试删除资源(超级用户创建)
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.superuser,
            modifier=self.superuser)
        url = self.url
        response = self.client.delete(f'{url}{resource.id}/')
        self.assertEqual(response.status_code, 204)
        resource = Resource.objects.get(id=resource.id)
        self.assertEqual(resource.is_deleted, True)

    def test_resources_delete_1(self):
        """
        测试删除资源(普通用户创建)
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.test_user,
            modifier=self.test_user)
        url = self.url
        response = self.client.delete(f'{url}{resource.id}/')
        self.assertEqual(response.status_code, 204)
        resource = Resource.objects.get(id=resource.id)
        self.assertEqual(resource.is_deleted, True)


class ResourceTestWithNormalUser(TestClassWithNormalUserLogin):
    """
    资源相关测试用例（普通用户登录）
    """
    url = reverse('resources-list')

    def test_resources_list(self):
        """
        测试资源列表展示
        """
        url = self.url
        for _ in range(10):
            ResourceFactory()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['count'], 10)

    def test_resource_create(self):
        """
        测试新增资源
        """
        url = self.url
        response = self.client.post(url, data={
            'title': '测试主题', 'content': '测试内容'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['title'], '测试主题')
        self.assertEqual(content['content'], '测试内容')
        self.assertEqual(content['creator']['id'], self.test_user.id)
        self.assertEqual(content['modifier']['id'], self.test_user.id)

    def test_resources_detail(self):
        """
        测试资源详情展示
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.superuser,
            modifier=self.superuser)
        url = self.url
        response = self.client.get(f'{url}{resource.id}/', format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['title'], '123')
        self.assertEqual(content['content'], '123123123')

    def test_resources_update(self):
        """
        测试资源修改信息(超级用户创建)
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.superuser,
            modifier=self.superuser)
        url = self.url

        # 可查看其他用户创建的资源
        response = self.client.get(f'{url}{resource.id}/', format='json')
        self.assertEqual(response.status_code, 200)

        # 无权限修改其他用户创建的资源
        response = self.client.patch(f'{url}{resource.id}/', data={
            'content': '456456'
        }, format='json')

        self.assertEqual(response.status_code, 403)

    def test_resources_update_1(self):
        """
        测试资源修改信息(普通用户创建)
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.test_user,
            modifier=self.test_user)
        url = self.url
        response = self.client.patch(f'{url}{resource.id}/', data={
            'content': '456456'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['title'], '123')
        self.assertEqual(content['content'], '456456')

    def test_resources_delete(self):
        """
        测试删除资源(超级用户创建)
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.superuser,
            modifier=self.superuser)
        url = self.url

        # 无权限修改其他用户创建的资源
        response = self.client.delete(f'{url}{resource.id}/')
        self.assertEqual(response.status_code, 403)

    def test_resources_delete_1(self):
        """
        测试删除资源(普通用户创建)
        """
        resource = Resource.objects.create(
            title='123', content='123123123', creator=self.test_user,
            modifier=self.test_user)
        url = self.url
        response = self.client.delete(f'{url}{resource.id}/')
        self.assertEqual(response.status_code, 204)
        resource = Resource.objects.get(id=resource.id)
        self.assertEqual(resource.is_deleted, True)

    def test_resources_create_limit(self):
        """
        测试有资源配额的情况下创建资源
        """
        url = self.url

        ResourceLimit.objects.create(
            user=self.test_user, is_limited=True, max_limit=5,
            creator=self.superuser, modifier=self.superuser)

        response = self.client.post(url, data={
            'title': '测试主题', 'content': '测试内容'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['title'], '测试主题')
        self.assertEqual(content['content'], '测试内容')
        self.assertEqual(content['creator']['id'], self.test_user.id)
        self.assertEqual(content['modifier']['id'], self.test_user.id)

    def test_resources_create_limit_2(self):
        """
        测试有资源配额且超配额的情况下创建资源
        """
        url = self.url

        ResourceLimit.objects.create(
            user=self.test_user, is_limited=True, max_limit=5,
            creator=self.superuser, modifier=self.superuser)
        for _ in range(5):
            ResourceFactory(creator=self.test_user)

        response = self.client.post(url, data={
            'title': '测试主题', 'content': '测试内容'
        }, format='json')
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(content['result'], 'error')
        self.assertEqual(content['msg'], '您的资源已达到配额数（5），无法创建。')
