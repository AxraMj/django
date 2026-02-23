"""
GSoC 2026 - Django Playwright Tests
Converting: tests/view_tests/tests/test_i18n.py
I18nSeleniumTests → I18nPlaywrightTests

Author: AxraMj
Reference: github.com/django/new-features/issues/13
"""
from django.test import override_settings, modify_settings
from django.test.selenium import SeleniumTestCase


class I18nPlaywrightTests(SeleniumTestCase):
    """
    Playwright version of I18nSeleniumTests.

    Original class uses:  self.selenium.get(), find_element(By.ID, ...)
    Playwright uses:      self.page.goto(), self.page.locator("#id")
    """

    available_apps = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "view_tests",
    ]

    @override_settings(LANGUAGE_CODE="de")
    def test_javascript_gettext(self):
        """
        Playwright version of I18nSeleniumTests.test_javascript_gettext

        Original Selenium:
            self.selenium.get(url + "/jsi18n_template/")
            elem = self.selenium.find_element(By.ID, "gettext")
            self.assertEqual(elem.text, "Entfernen")

        Playwright equivalent below:
        """
        # Navigate to page
        # Selenium: self.selenium.get(url)
        # Playwright: self.page.goto(url)
        self.page.goto(self.live_server_url + "/jsi18n_template/")

        # Find elements and check text
        # Selenium: find_element(By.ID, "x").text
        # Playwright: locator("#x").text_content()
        self.assertEqual(
            self.page.locator("#gettext").text_content(),
            "Entfernen",
        )
        self.assertEqual(
            self.page.locator("#ngettext_sing").text_content(),
            "1 Element",
        )
        self.assertEqual(
            self.page.locator("#ngettext_plur").text_content(),
            "455 Elemente",
        )
        self.assertEqual(
            self.page.locator("#ngettext_onnonplural").text_content(),
            "Bild",
        )
        self.assertEqual(
            self.page.locator("#pgettext").text_content(),
            "Kann",
        )
        self.assertEqual(
            self.page.locator("#npgettext_sing").text_content(),
            "1 Resultat",
        )
        self.assertEqual(
            self.page.locator("#npgettext_plur").text_content(),
            "455 Resultate",
        )
        self.assertEqual(
            self.page.locator("#formats").text_content(),
            "DATE_INPUT_FORMATS is an object; DECIMAL_SEPARATOR is a string; "
            "FIRST_DAY_OF_WEEK is a number;",
        )

    @modify_settings(
        INSTALLED_APPS={"append": ["view_tests.app1", "view_tests.app2"]}
    )
    @override_settings(LANGUAGE_CODE="fr")
    def test_multiple_catalogs(self):
        """
        Playwright version of I18nSeleniumTests.test_multiple_catalogs

        Original Selenium:
            self.selenium.get(url + "/jsi18n_multi_catalogs/")
            elem = self.selenium.find_element(By.ID, "app1string")
            self.assertEqual(elem.text, "il faut traduire...")

        Playwright equivalent below:
        """
        self.page.goto(self.live_server_url + "/jsi18n_multi_catalogs/")

        self.assertEqual(
            self.page.locator("#app1string").text_content(),
            "il faut traduire cette chaîne de caractères de app1",
        )
        self.assertEqual(
            self.page.locator("#app2string").text_content(),
            "il faut traduire cette chaîne de caractères de app2",
        )