"""
Offline Browser Testing - Version ohne automatischen ChromeDriver Download.
Diese Version versucht einen bereits installierten ChromeDriver zu verwenden.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os
import subprocess


class OfflineBrowserTester:
    """
    Browser-Tester der ohne Internet-Verbindung funktioniert.
    Verwendet bereits installierte Browser und WebDriver.
    """
    
    def __init__(self, headless=True, timeout=10):
        """
        Initialize the offline browser tester.
        
        Args:
            headless (bool): Run browser in headless mode
            timeout (int): Default timeout for operations in seconds
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def find_chrome_binary(self):
        """Finde Chrome Binary."""
        possible_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/opt/google/chrome/chrome",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try to find via which command
        try:
            result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        try:
            result = subprocess.run(['which', 'chromium-browser'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def setup_browser_manual(self):
        """Setup browser ohne automatischen WebDriver Download."""
        try:
            # Chrome Optionen konfigurieren
            options = webdriver.ChromeOptions()
            
            if self.headless:
                options.add_argument("--headless")
            
            # Weitere Chrome-Argumente für bessere Kompatibilität
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            
            # Chrome Binary finden
            chrome_binary = self.find_chrome_binary()
            if chrome_binary:
                options.binary_location = chrome_binary
                self.logger.info(f"Chrome Binary gefunden: {chrome_binary}")
            
            # Versuche ChromeDriver in verschiedenen Pfaden zu finden
            chromedriver_paths = [
                "/usr/bin/chromedriver",
                "/usr/local/bin/chromedriver",
                "/snap/bin/chromium.chromedriver",
                "./chromedriver",
                "chromedriver"
            ]
            
            service = None
            for driver_path in chromedriver_paths:
                if os.path.exists(driver_path):
                    service = Service(driver_path)
                    self.logger.info(f"ChromeDriver gefunden: {driver_path}")
                    break
            
            # Browser ohne Service versuchen (falls ChromeDriver im PATH ist)
            if service:
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                self.logger.info("Versuche ChromeDriver aus PATH...")
                self.driver = webdriver.Chrome(options=options)
            
            self.wait = WebDriverWait(self.driver, self.timeout)
            self.logger.info("Browser erfolgreich initialisiert (offline-Modus)")
            
        except Exception as e:
            self.logger.error(f"Offline-Browser-Setup fehlgeschlagen: {str(e)}")
            raise
    
    def find_element(self, locator_type, locator_value):
        """Find an element on the page."""
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
        except (TimeoutException, Exception):
            self.logger.error(f"Element not found: {locator_type}='{locator_value}'")
            raise
    
    def navigate_to(self, url):
        """Navigate to a specific URL."""
        try:
            self.driver.get(url)
            self.logger.info(f"Navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise
    
    def input_text(self, locator_type, locator_value, text, clear_first=True):
        """Input text into a text field."""
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
        """Click on an element."""
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
        """Select an option from a dropdown."""
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
    
    def take_screenshot(self, filename):
        """Take a screenshot of the current page."""
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved as: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def get_page_title(self):
        """Get the current page title."""
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


def demo_offline_testing():
    """Demo der offline Browser-Tests."""
    print("=== Offline Browser Testing Demo ===")
    
    # Pfad zur lokalen HTML-Testdatei
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "test_page.html")
    
    if not os.path.exists(html_path):
        print(f"✗ Test-HTML-Datei nicht gefunden: {html_path}")
        return False
    
    file_url = f"file://{html_path}"
    print(f"• Test-Seite: {file_url}")
    
    tester = OfflineBrowserTester(headless=True)
    
    try:
        print("• Browser wird gestartet (offline-Modus)...")
        tester.setup_browser_manual()
        
        print("• Navigation zur lokalen Testseite...")
        tester.navigate_to(file_url)
        
        # Seitentitel prüfen
        title = tester.get_page_title()
        print(f"• Seitentitel: '{title}'")
        
        # Screenshot der initialen Seite
        tester.take_screenshot("offline_demo_initial.png")
        print("• Initial-Screenshot erstellt")
        
        # Formular ausfüllen
        print("• Formular wird ausgefüllt...")
        tester.input_text("id", "userName", "Offline Test User")
        tester.input_text("id", "userEmail", "offline@test.de")
        tester.input_text("id", "userPhone", "0987-654321")
        tester.select_dropdown_option("id", "userCountry", option_value="schweiz")
        
        # Screenshot mit ausgefülltem Formular
        tester.take_screenshot("offline_demo_filled.png")
        print("• Screenshot mit ausgefülltem Formular erstellt")
        
        # Suchfunktion testen
        print("• Suchfunktion wird getestet...")
        tester.input_text("id", "searchInput", "Offline Browser Test")
        tester.click_element("id", "searchBtn")
        
        time.sleep(1)
        
        # Final Screenshot
        tester.take_screenshot("offline_demo_final.png")
        print("• Final-Screenshot erstellt")
        
        print("✓ Offline Browser Testing Demo erfolgreich!")
        return True
        
    except Exception as e:
        print(f"✗ Offline Demo fehlgeschlagen: {e}")
        print("Mögliche Lösungen:")
        print("  • Stellen Sie sicher, dass Chrome/Chromium installiert ist")
        print("  • Installieren Sie ChromeDriver: apt-get install chromium-chromedriver")
        print("  • Oder verwenden Sie: pip install chromedriver-autoinstaller")
        return False
    
    finally:
        tester.close_browser()


def check_browser_availability():
    """Prüfe verfügbare Browser und WebDriver."""
    print("=== Browser-Verfügbarkeit prüfen ===")
    
    tester = OfflineBrowserTester()
    
    # Chrome Binary prüfen
    chrome_binary = tester.find_chrome_binary()
    if chrome_binary:
        print(f"✓ Chrome gefunden: {chrome_binary}")
    else:
        print("✗ Chrome nicht gefunden")
    
    # ChromeDriver prüfen
    chromedriver_paths = [
        "/usr/bin/chromedriver",
        "/usr/local/bin/chromedriver", 
        "/snap/bin/chromium.chromedriver"
    ]
    
    chromedriver_found = False
    for path in chromedriver_paths:
        if os.path.exists(path):
            print(f"✓ ChromeDriver gefunden: {path}")
            chromedriver_found = True
            break
    
    if not chromedriver_found:
        print("✗ ChromeDriver nicht in Standard-Pfaden gefunden")
        
        # Versuche aus PATH
        try:
            result = subprocess.run(['which', 'chromedriver'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ ChromeDriver in PATH: {result.stdout.strip()}")
                chromedriver_found = True
        except:
            pass
    
    if not chromedriver_found:
        print("! ChromeDriver-Installation erforderlich")
        print("  Installationsoptionen:")
        print("  • Ubuntu/Debian: sudo apt-get install chromium-chromedriver")
        print("  • Manual: Download von https://chromedriver.chromium.org/")
        print("  • Python: pip install chromedriver-autoinstaller")
    
    return chrome_binary is not None and chromedriver_found


if __name__ == "__main__":
    print("Offline Browser Testing Tool")
    print("=" * 40)
    
    # Browser-Verfügbarkeit prüfen
    if check_browser_availability():
        print("\n✓ Browser-Umgebung scheint verfügbar zu sein")
        
        # Demo ausführen
        success = demo_offline_testing()
        
        if success:
            print("\n🎉 Offline Browser Testing funktioniert!")
        else:
            print("\n❌ Offline Testing fehlgeschlagen")
            exit(1)
    else:
        print("\n❌ Browser-Umgebung nicht vollständig verfügbar")
        print("Bitte installieren Sie Chrome/Chromium und ChromeDriver")
        exit(1)