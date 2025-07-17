#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
import utils


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method returns correct data"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns correct URL"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
        client = GithubOrgClient("test")
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        test_repos = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_repos

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"

            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")
            mock_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()

from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):
    ...

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {}}, "my_license", False),
        ({"license": {"key": None}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

class GithubOrgClient:
    ...
    @staticmethod
    def has_license(repo, license_key):
        return repo.get("license", {}).get("key") == license_key

# fixtures.py

org_payload = {
    "login": "google",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"id": 1, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 2, "name": "repo2", "license": {"key": "mit"}},
    {"id": 3, "name": "repo3", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]

#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and configure side_effect"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                return Mock(json=lambda: cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return Mock(json=lambda: cls.repos_payload)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns correct repo names"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns only repos with given license"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
