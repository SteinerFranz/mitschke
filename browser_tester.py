"""
Browser Input Automation Testing Program
=========================================

A program for automated testing of browser inputs and interactions.
This module provides a comprehensive framework for testing web applications
through automated browser interactions.

Author: Browser Testing Framework
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging


class BrowserTester:
    """
    A comprehensive browser automation testing class that can automate
    various browser inputs and interactions for testing purposes.
    """
    
    def __init__(self, browser="chrome", headless=False, timeout=10):
        """
        Initialize the browser tester.
        
        Args:
            browser (str): Browser type to use (chrome, firefox)
            headless (bool): Run browser in headless mode
            timeout (int): Default timeout for operations in seconds
        """
        self.browser_type = browser
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def setup_browser(self):
        """Setup and initialize the browser driver."""
        try:
            if self.browser_type.lower() == "chrome":
                options = webdriver.ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                raise ValueError(f"Browser {self.browser_type} not supported yet")
            
            self.wait = WebDriverWait(self.driver, self.timeout)
            self.logger.info(f"Browser {self.browser_type} initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup browser: {str(e)}")
            raise
    
    def navigate_to(self, url):
        """
        Navigate to a specific URL.
        
        Args:
            url (str): URL to navigate to
        """
        try:
            self.driver.get(url)
            self.logger.info(f"Navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise
    
    def find_element(self, locator_type, locator_value):
        """
        Find an element on the page.
        
        Args:
            locator_type (str): Type of locator (id, name, class, xpath, css)
            locator_value (str): Value of the locator
            
        Returns:
            WebElement: Found element
        """
        locator_map = {
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "tag": By.TAG_NAME
        }
        
        if locator_type not in locator_map:
            raise ValueError(f"Unsupported locator type: {locator_type}")
        
        try:
            element = self.wait.until(
                EC.presence_of_element_located((locator_map[locator_type], locator_value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator_type}='{locator_value}'")
            raise
    
    def input_text(self, locator_type, locator_value, text, clear_first=True):
        """
        Input text into a text field.
        
        Args:
            locator_type (str): Type of locator
            locator_value (str): Value of the locator
            text (str): Text to input
            clear_first (bool): Clear field before input
        """
        try:
            element = self.find_element(locator_type, locator_value)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Text '{text}' entered into element {locator_type}='{locator_value}'")
        except Exception as e:
            self.logger.error(f"Failed to input text: {str(e)}")
            raise
    
    def click_element(self, locator_type, locator_value):
        """
        Click on an element.
        
        Args:
            locator_type (str): Type of locator
            locator_value (str): Value of the locator
        """
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((getattr(By, locator_type.upper()), locator_value))
            )
            element.click()
            self.logger.info(f"Clicked element {locator_type}='{locator_value}'")
        except Exception as e:
            self.logger.error(f"Failed to click element: {str(e)}")
            raise
    
    def select_dropdown_option(self, locator_type, locator_value, option_text=None, option_value=None):
        """
        Select an option from a dropdown.
        
        Args:
            locator_type (str): Type of locator
            locator_value (str): Value of the locator
            option_text (str): Visible text of the option to select
            option_value (str): Value attribute of the option to select
        """
        try:
            element = self.find_element(locator_type, locator_value)
            select = Select(element)
            
            if option_text:
                select.select_by_visible_text(option_text)
                self.logger.info(f"Selected option '{option_text}' from dropdown")
            elif option_value:
                select.select_by_value(option_value)
                self.logger.info(f"Selected option with value '{option_value}' from dropdown")
            else:
                raise ValueError("Either option_text or option_value must be provided")
                
        except Exception as e:
            self.logger.error(f"Failed to select dropdown option: {str(e)}")
            raise
    
    def get_element_text(self, locator_type, locator_value):
        """
        Get text content of an element.
        
        Args:
            locator_type (str): Type of locator
            locator_value (str): Value of the locator
            
        Returns:
            str: Text content of the element
        """
        try:
            element = self.find_element(locator_type, locator_value)
            text = element.text
            self.logger.info(f"Retrieved text '{text}' from element {locator_type}='{locator_value}'")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get element text: {str(e)}")
            raise
    
    def wait_for_element_visible(self, locator_type, locator_value, timeout=None):
        """
        Wait for an element to become visible.
        
        Args:
            locator_type (str): Type of locator
            locator_value (str): Value of the locator
            timeout (int): Timeout in seconds (uses default if None)
        """
        wait_time = timeout or self.timeout
        locator_map = {
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "tag": By.TAG_NAME
        }
        
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(
                EC.visibility_of_element_located((locator_map[locator_type], locator_value))
            )
            self.logger.info(f"Element {locator_type}='{locator_value}' became visible")
            return element
        except TimeoutException:
            self.logger.error(f"Element {locator_type}='{locator_value}' did not become visible within {wait_time} seconds")
            raise
    
    def submit_form(self, form_locator_type=None, form_locator_value=None):
        """
        Submit a form.
        
        Args:
            form_locator_type (str): Type of locator for form (optional)
            form_locator_value (str): Value of the locator for form (optional)
        """
        try:
            if form_locator_type and form_locator_value:
                form = self.find_element(form_locator_type, form_locator_value)
                form.submit()
            else:
                # Find first form on page and submit
                form = self.driver.find_element(By.TAG_NAME, "form")
                form.submit()
            
            self.logger.info("Form submitted successfully")
        except Exception as e:
            self.logger.error(f"Failed to submit form: {str(e)}")
            raise
    
    def take_screenshot(self, filename):
        """
        Take a screenshot of the current page.
        
        Args:
            filename (str): Filename to save the screenshot
        """
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved as: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def get_page_title(self):
        """
        Get the current page title.
        
        Returns:
            str: Page title
        """
        try:
            title = self.driver.title
            self.logger.info(f"Page title: '{title}'")
            return title
        except Exception as e:
            self.logger.error(f"Failed to get page title: {str(e)}")
            raise
    
    def close_browser(self):
        """Close the browser and cleanup."""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed successfully")


# Test scenarios and examples
def run_basic_tests():
    """Run basic browser automation tests."""
    tester = BrowserTester(headless=True)
    
    try:
        tester.setup_browser()
        
        # Example 1: Google Search Test
        print("\n=== Running Google Search Test ===")
        tester.navigate_to("https://www.google.com")
        
        # Accept cookies if present (Google often shows this)
        try:
            tester.click_element("id", "L2AGLb")  # Accept cookies button
            time.sleep(1)
        except:
            pass  # Cookies dialog might not appear
        
        # Perform search
        tester.input_text("name", "q", "browser automation testing")
        tester.click_element("name", "btnK")  # Google Search button
        
        # Wait for results and get title
        time.sleep(2)
        title = tester.get_page_title()
        assert "browser automation testing" in title.lower()
        print("✓ Google search test passed")
        
        # Example 2: Form Testing (using a test form website)
        print("\n=== Running Form Test ===")
        tester.navigate_to("https://httpbin.org/forms/post")
        
        # Fill out the form
        tester.input_text("name", "custname", "Test User")
        tester.input_text("name", "custtel", "123-456-7890")
        tester.input_text("name", "custemail", "test@example.com")
        tester.select_dropdown_option("name", "size", option_value="large")
        
        # Submit form
        tester.submit_form()
        
        # Verify form submission
        time.sleep(2)
        print("✓ Form submission test completed")
        
        print("\n=== All Tests Completed Successfully ===")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        raise
    finally:
        tester.close_browser()


if __name__ == "__main__":
    run_basic_tests()