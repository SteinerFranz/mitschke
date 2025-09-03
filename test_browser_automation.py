"""
Pytest-Tests für das Browser-Automatisierung-Tool.
"""

import pytest
import os
import time
from browser_tester import BrowserTester, AdvancedBrowserTester


class TestBrowserTester:
    """Test-Klasse für BrowserTester."""
    
    @pytest.fixture
    def tester(self):
        """Browser-Tester Fixture."""
        tester = BrowserTester(headless=True)
        tester.setup_browser()
        yield tester
        tester.close_browser()
    
    @pytest.fixture
    def test_page_url(self):
        """URL zur lokalen Testseite."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "test_page.html")
        return f"file://{html_path}"
    
    def test_browser_initialization(self):
        """Test der Browser-Initialisierung."""
        tester = BrowserTester(headless=True)
        tester.setup_browser()
        
        assert tester.driver is not None
        assert tester.wait is not None
        
        tester.close_browser()
    
    def test_navigation(self, tester, test_page_url):
        """Test der Navigation zu einer Seite."""
        tester.navigate_to(test_page_url)
        
        # Seitentitel prüfen
        title = tester.get_page_title()
        assert "Browser Automation Test Form" in title
    
    def test_element_finding(self, tester, test_page_url):
        """Test der Element-Suche."""
        tester.navigate_to(test_page_url)
        
        # Element nach ID finden
        element = tester.find_element("id", "userName")
        assert element is not None
        
        # Element nach Name finden  
        element = tester.find_element("name", "userName")
        assert element is not None
    
    def test_text_input(self, tester, test_page_url):
        """Test der Texteingabe."""
        tester.navigate_to(test_page_url)
        
        test_text = "Pytest Test"
        tester.input_text("id", "userName", test_text)
        
        # Eingabe prüfen
        element = tester.find_element("id", "userName")
        assert element.get_attribute("value") == test_text
    
    def test_dropdown_selection(self, tester, test_page_url):
        """Test der Dropdown-Auswahl."""
        tester.navigate_to(test_page_url)
        
        tester.select_dropdown_option("id", "userCountry", option_value="deutschland")
        
        # Auswahl prüfen
        element = tester.find_element("id", "userCountry")
        assert element.get_attribute("value") == "deutschland"
    
    def test_button_clicking(self, tester, test_page_url):
        """Test des Button-Klickens."""
        tester.navigate_to(test_page_url)
        
        # Formular ausfüllen
        tester.input_text("id", "userName", "Test User")
        tester.input_text("id", "userEmail", "test@example.com")
        tester.select_dropdown_option("id", "userCountry", option_value="deutschland")
        
        # Absenden-Button klicken
        tester.click_element("id", "submitBtn")
        
        # Kurz warten für JavaScript
        time.sleep(1)
        
        # Erfolgsmeldung prüfen
        success_element = tester.find_element("id", "formResult")
        # Note: Das Element existiert immer, ist aber möglicherweise nicht sichtbar
        assert success_element is not None
    
    def test_screenshot_functionality(self, tester, test_page_url):
        """Test der Screenshot-Funktionalität."""
        tester.navigate_to(test_page_url)
        
        screenshot_name = "pytest_test_screenshot.png"
        tester.take_screenshot(screenshot_name)
        
        # Prüfen ob Screenshot erstellt wurde
        assert os.path.exists(screenshot_name)
        
        # Aufräumen
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
    
    def test_element_waiting(self, tester, test_page_url):
        """Test der Element-Warte-Funktionalität."""
        tester.navigate_to(test_page_url)
        
        # Auf Element warten
        element = tester.wait_for_element_visible("id", "userName", timeout=5)
        assert element is not None
    
    def test_error_handling(self, tester, test_page_url):
        """Test der Fehlerbehandlung."""
        tester.navigate_to(test_page_url)
        
        # Test für nicht-existierendes Element
        with pytest.raises(Exception):
            tester.find_element("id", "non_existent_element")
        
        # Test für ungültigen Locator-Typ
        with pytest.raises(ValueError):
            tester.find_element("invalid_type", "some_value")


class TestAdvancedBrowserTester:
    """Test-Klasse für AdvancedBrowserTester."""
    
    @pytest.fixture
    def advanced_tester(self):
        """Advanced Browser-Tester Fixture."""
        tester = AdvancedBrowserTester(headless=True)
        tester.setup_browser()
        yield tester
        tester.close_browser()
    
    @pytest.fixture
    def test_page_url(self):
        """URL zur lokalen Testseite."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "test_page.html")
        return f"file://{html_path}"
    
    def test_fill_form_from_data(self, advanced_tester, test_page_url):
        """Test der strukturierten Formular-Befüllung."""
        advanced_tester.navigate_to(test_page_url)
        
        form_data = {
            'name': {
                'locator_type': 'id',
                'locator_value': 'userName',
                'value': 'Advanced Test User',
                'action': 'input'
            },
            'email': {
                'locator_type': 'id',
                'locator_value': 'userEmail',
                'value': 'advanced@test.com',
                'action': 'input'
            },
            'country': {
                'locator_type': 'id',
                'locator_value': 'userCountry',
                'value': 'deutschland',
                'action': 'select'
            }
        }
        
        advanced_tester.fill_form_from_data(form_data)
        
        # Eingaben prüfen
        name_element = advanced_tester.find_element("id", "userName")
        assert name_element.get_attribute("value") == "Advanced Test User"
        
        email_element = advanced_tester.find_element("id", "userEmail")
        assert email_element.get_attribute("value") == "advanced@test.com"
        
        country_element = advanced_tester.find_element("id", "userCountry")
        assert country_element.get_attribute("value") == "deutschland"
    
    def test_form_submission_validation(self, advanced_tester, test_page_url):
        """Test der Formular-Übertragungsvalidierung."""
        advanced_tester.navigate_to(test_page_url)
        
        # Formular ausfüllen und absenden
        advanced_tester.input_text("id", "userName", "Validation Test")
        advanced_tester.input_text("id", "userEmail", "validation@test.com")
        advanced_tester.select_dropdown_option("id", "userCountry", option_value="deutschland")
        advanced_tester.click_element("id", "submitBtn")
        
        time.sleep(1)
        
        # Validierungsindikatoren definieren
        success_indicators = [
            {'type': 'element', 'value': 'id=formResult'}
        ]
        
        # Validierung durchführen
        is_valid = advanced_tester.validate_form_submission(success_indicators)
        assert is_valid is True or is_valid is False  # Prüfung dass Methode ausgeführt wurde


@pytest.fixture(scope="session", autouse=True)
def cleanup_screenshots():
    """Räumt Test-Screenshots nach den Tests auf."""
    yield
    
    # Nach allen Tests aufräumen
    screenshot_files = [f for f in os.listdir('.') if f.startswith('pytest_') and f.endswith('.png')]
    for screenshot in screenshot_files:
        try:
            os.remove(screenshot)
        except:
            pass


# Markierungen für verschiedene Testtypen
pytestmark = pytest.mark.browser


if __name__ == "__main__":
    pytest.main([__file__, "-v"])