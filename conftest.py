import base64
import re
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils import logger
from utils.config import PASSWORD, USERNAME

SCREENSHOT_DIR = Path(__file__).resolve().parent / "reports" / "screenshots"


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="run Chrome without opening a window")
    parser.addoption("--demo", action="store_true", help="pause 1 second after each browser action, for live demos")


def pytest_configure(config):
    logger.setup_logging()
    BasePage.demo_mode = config.getoption("--demo")


def pytest_html_report_title(report):
    report.title = "SauceDemo Automation Report"


def _chrome_service():
    try:
        from webdriver_manager.chrome import ChromeDriverManager

        return Service(ChromeDriverManager().install())
    except Exception:
        return Service()


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    options.add_argument("--disable-features=PasswordLeakDetection")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    drv = webdriver.Chrome(service=_chrome_service(), options=options)
    request.node.driver = drv
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).open()


@pytest.fixture
def inventory_page(login_page, driver):
    login_page.login(USERNAME, PASSWORD)
    page = InventoryPage(driver)
    assert page.is_open(), "Precondition failed: login did not reach the Products page"
    return page


@pytest.fixture
def checkout_info_page(inventory_page):
    inventory_page.add_to_cart("Sauce Labs Backpack")
    page = inventory_page.open_cart().checkout()
    assert page.is_open(), "Precondition failed: Checkout: Your Information did not open"
    return page


@pytest.fixture(autouse=True)
def _log_test(request):
    logger.set_test(request.node.name)
    logger.status("START")
    yield
    logger.set_test("-")


def _screenshot(item, report):
    drv = getattr(item, "driver", None)
    if drv is None:
        return
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SCREENSHOT_DIR / f"{re.sub(r'[^\w.-]', '_', item.name)}_{datetime.now():%Y%m%d_%H%M%S}.png"
    drv.save_screenshot(str(path))
    logger.status(f"screenshot saved: reports/screenshots/{path.name}")
    html = item.config.pluginmanager.getplugin("html")
    if html:
        report.extras = getattr(report, "extras", []) + [html.extras.png(base64.b64encode(path.read_bytes()).decode())]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.when == "call" or (report.when == "setup" and not report.passed):
        if hasattr(report, "wasxfail"):
            result = "XFAIL" if report.skipped else "XPASS"
        else:
            result = report.outcome.upper()
        if report.failed:
            _screenshot(item, report)
        logger.status(result)
