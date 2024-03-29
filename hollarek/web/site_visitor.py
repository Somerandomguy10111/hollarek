from __future__ import annotations
from bs4 import BeautifulSoup
from func_timeout import func_timeout, FunctionTimedOut
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import trafilatura
import logging

from .mail_addresses import get_mail_addresses_in_text

# ---------------------------------------------------------

class SiteVisitor:
    max_site_loading_time = 10

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        prefs = {
            "download.default_directory": "/dev/null",
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        self.engine = webdriver.Chrome(options=chrome_options)
        self.is_busy = False


    def fetch_site_html(self, url: str) -> str:
        self.is_busy = True

        def get_website_html():
            self.engine.get(url)
            return self.engine.page_source

        content = func_timeout(timeout=SiteVisitor.max_site_loading_time, func=get_website_html)
        self.is_busy = False
        return content


    def get_mail_addresses(self, url : str) -> list[str]:
        return get_mail_addresses_in_text(text=self.get_html(url=url))


    def get_text(self, url: str, use_driver : bool = False) -> str:
        if use_driver:
            page_source = self.get_html(url=url)
            soup = BeautifulSoup(page_source, 'html.parser')
            site_text = ' '.join(element for element in soup.stripped_strings)
        else:
            def get_website_text():
                downloaded = trafilatura.fetch_url(url)
                return trafilatura.extract(downloaded)
            site_text = func_timeout(timeout=SiteVisitor.max_site_loading_time, func=get_website_text)
        return site_text


    def get_html(self, url: str) -> str:
        try:
            result = self.fetch_site_html(url)

        except FunctionTimedOut:
            logging.warning(f'Failed to retrieve text from website {url} due to timeout after {SiteVisitor.max_site_loading_time} seconds')
            result = ''

        return result

