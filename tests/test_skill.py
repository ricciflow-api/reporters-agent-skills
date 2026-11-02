import pathlib
import contextlib
import io
import sys
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/reporter-research/scripts"))
import reporters_api
import reporters_client


class SkillTests(unittest.TestCase):
    def test_search_is_one_bounded_request(self):
        with patch.object(reporters_api, "request", return_value={"data": {"items": []}}) as request:
            reporters_api.main(["search-reporters", "--query", "climate", "--limit", "10", "--beat", "technology"])
        request.assert_called_once_with("/reporters/search", method="POST", body={"query": "climate", "limit": 10, "beats": ["technology"]})

    def test_contact_command_requires_explicit_confirmation(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            reporters_api.main(["reveal-reporter", "--id", "123", "--idempotency-key", "one"])
        with patch.object(reporters_api, "request", return_value={"data": {}}) as request:
            reporters_api.main(["reveal-reporter", "--id", "123", "--confirm-contact-reveal", "--idempotency-key", "one"])
        request.assert_called_once_with("/reporters/123/contacts/reveal", method="POST", body={}, confirm_contact_reveal=True, idempotency_key="one")

    def test_article_command_preserves_fixed_page_size(self):
        with patch.object(reporters_api, "request", return_value={"data": {"items": []}}) as request:
            reporters_api.main(["reporter-articles", "--id", "123", "--cursor", "one-page"])
        request.assert_called_once_with("/reporters/123/articles", params={"cursor": "one-page"})

    def test_helpers_reject_unapproved_destinations(self):
        with self.assertRaises(ValueError):
            reporters_client.request("https://evil.example", key="fixture-key")
        with self.assertRaises(ValueError):
            reporters_client.request("/account", key="fixture-key", params={"token": "fixture-key"})


if __name__ == "__main__":
    unittest.main()
