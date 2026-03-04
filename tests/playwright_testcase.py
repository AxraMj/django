"""
GSoC 2026 - Django PlaywrightTestCase Base Class
Author: AxraMj
Reference: github.com/django/new-features/issues/13

This module provides PlaywrightTestCase — a base class for writing
browser-based integration tests using Playwright instead of Selenium.

Usage:
    from tests.playwright_testcase import PlaywrightTestCase

    class MyTests(PlaywrightTestCase):
        def test_something(self):
            self.page.goto(self.live_server_url + "/my-page/")
            self.assertEqual(
                self.page.locator("#title").text_content(),
                "Expected Title"
            )
"""

import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright


class PlaywrightTestCase(StaticLiveServerTestCase):
    """
    Base class for Playwright-based browser tests in Django.

    Replaces SeleniumTestCase with Playwright equivalent.
    Provides self.page for test methods.

    Key differences from SeleniumTestCase:
        Selenium: self.selenium.get(url)
        Playwright: self.page.goto(url)

        Selenium: find_element(By.ID, "x").text
        Playwright: self.page.locator("#x").text_content()
    """

    # Browser to use: chromium, firefox, or webkit
    browser_name = "chromium"

    # Run headless by default (no visible browser window)
    # Set to False to see the browser during tests
    headless = True

    @classmethod
    def setUpClass(cls):
        """
        Start Playwright and launch browser once for all tests in class.
        Same pattern as SeleniumTestCase.setUpClass()
        """
        super().setUpClass()
        cls._playwright = sync_playwright().start()

        # Launch browser based on browser_name setting
        browser_type = getattr(cls._playwright, cls.browser_name)
        cls.browser = browser_type.launch(headless=cls.headless)

    @classmethod
    def tearDownClass(cls):
        """
        Close browser and stop Playwright after all tests complete.
        Same pattern as SeleniumTestCase.tearDownClass()
        """
        cls.browser.close()
        cls._playwright.stop()
        super().tearDownClass()

    def setUp(self):
        """
        Create a fresh browser page for each test.
        This ensures test isolation — each test starts with clean state.
        """
        super().setUp()
        # Create new browser context (like incognito window)
        self.context = self.browser.new_context()
        # Create new page (like a browser tab)
        self.page = self.context.new_page()

    def tearDown(self):
        """
        Close page and context after each test.
        """
        self.page.close()
        self.context.close()
        super().tearDown()