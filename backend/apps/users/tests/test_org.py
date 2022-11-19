import json

from rest_framework.reverse import reverse

from users.models import Org, User
from users.tests.factories import OrgFactory, UserFactory
from users.tests.test_users import TestClassWithLogin


class OrgTest(TestClassWithLogin):
    """
    标签相关测试用例
    """
    url = reverse('orgs-list')

    def test_org_list(self):
        """
        标签列表测试用例
        """
        for _ in range(10):
            OrgFactory()
        url = self.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content.__len__(), 11)

    # def test_org_children(self):
    #     """
    #     获取某机构的直属子机构和直属用户测试用例
    #     """
    #     org = OrgFactory()
    #     for _ in range(5):
    #         OrgFactory(parent=org)
    #     for _ in range(5):
    #         UserFactory(org=org)
    #     url = self.url + f'{org.id}/children/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     content = json.loads(response.content)
    #     self.assertEqual(len(content['users']), 5)
    #     self.assertEqual(len(content['orgs']), 5)
