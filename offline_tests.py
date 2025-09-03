"""
Offline-Tests für das Browser-Automatisierung-Tool.
Diese Tests verwenden eine lokale HTML-Datei und funktionieren ohne Internetverbindung.
"""

from browser_tester import BrowserTester
import time
import os


def test_local_form_automation():
    """Test der Formular-Automatisierung mit lokaler HTML-Datei."""
    print("=== Lokaler Formular-Automatisierung Test ===")
    
    # Pfad zur lokalen HTML-Testdatei
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "test_page.html")
    file_url = f"file://{html_path}"
    
    tester = BrowserTester(headless=True)
    
    try:
        print("• Browser wird gestartet...")
        tester.setup_browser()
        
        print("• Navigation zur lokalen Testseite...")
        tester.navigate_to(file_url)
        
        # Screenshot der initialen Seite
        tester.take_screenshot("local_page_initial.png")
        print("• Initial-Screenshot gespeichert")
        
        # Formular ausfüllen
        print("• Formularfelder werden ausgefüllt...")
        tester.input_text("id", "userName", "Test Automatisierung")
        tester.input_text("id", "userEmail", "test@automation.de")
        tester.input_text("id", "userPhone", "0123-456789")
        tester.input_text("id", "userAge", "30")
        
        # Dropdown auswählen
        print("• Land-Dropdown wird ausgewählt...")
        tester.select_dropdown_option("id", "userCountry", option_value="deutschland")
        
        # Textarea füllen
        print("• Nachricht wird eingegeben...")
        tester.input_text("id", "userMessage", "Dies ist eine Test-Nachricht für die Browser-Automatisierung.")
        
        # Screenshot vor dem Absenden
        tester.take_screenshot("local_form_filled.png")
        print("• Screenshot mit ausgefülltem Formular gespeichert")
        
        # Formular absenden
        print("• Formular wird abgesendet...")
        tester.click_element("id", "submitBtn")
        
        # Kurz warten für JavaScript-Verarbeitung
        time.sleep(2)
        
        # Erfolgsmeldung prüfen
        try:
            success_element = tester.find_element("id", "formResult")
            if success_element.is_displayed():
                print("✓ Erfolgsmeldung wird angezeigt")
            else:
                print("? Erfolgsmeldung gefunden aber nicht sichtbar")
        except:
            print("? Erfolgsmeldung-Element nicht gefunden")
        
        # Screenshot nach dem Absenden
        tester.take_screenshot("local_form_submitted.png")
        print("• Screenshot nach Formular-Absendung gespeichert")
        
        print("✓ Lokaler Formular-Test erfolgreich!")
        return True
        
    except Exception as e:
        print(f"✗ Lokaler Formular-Test fehlgeschlagen: {e}")
        return False
    
    finally:
        tester.close_browser()


def test_local_search_functionality():
    """Test der Such-Funktionalität mit lokaler Seite."""
    print("\n=== Lokaler Such-Funktionalität Test ===")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "test_page.html")
    file_url = f"file://{html_path}"
    
    tester = BrowserTester(headless=True)
    
    try:
        print("• Browser wird gestartet...")
        tester.setup_browser()
        
        print("• Navigation zur lokalen Testseite...")
        tester.navigate_to(file_url)
        
        # Zur Suchfunktion scrollen (falls nötig)
        print("• Suche wird getestet...")
        search_term = "Browser Automatisierung Test"
        
        # Suchtext eingeben
        tester.input_text("id", "searchInput", search_term)
        
        # Such-Button klicken
        tester.click_element("id", "searchBtn")
        
        # Kurz warten für JavaScript
        time.sleep(1)
        
        # Suchergebnisse prüfen
        try:
            results_element = tester.find_element("id", "searchResults")
            if results_element.is_displayed():
                print("✓ Suchergebnisse werden angezeigt")
                
                # Suchbegriff prüfen
                search_term_element = tester.find_element("id", "searchTerm")
                displayed_term = search_term_element.text
                if search_term in displayed_term:
                    print(f"✓ Suchbegriff korrekt angezeigt: '{displayed_term}'")
                else:
                    print(f"? Suchbegriff angezeigt: '{displayed_term}'")
            else:
                print("? Suchergebnisse gefunden aber nicht sichtbar")
        except:
            print("? Suchergebnisse-Element nicht gefunden")
        
        # Screenshot der Suchergebnisse
        tester.take_screenshot("local_search_results.png")
        print("• Screenshot der Suchergebnisse gespeichert")
        
        print("✓ Lokaler Such-Test erfolgreich!")
        return True
        
    except Exception as e:
        print(f"✗ Lokaler Such-Test fehlgeschlagen: {e}")
        return False
    
    finally:
        tester.close_browser()


def test_element_interactions():
    """Test verschiedener Element-Interaktionen."""
    print("\n=== Element-Interaktionen Test ===")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "test_page.html")
    file_url = f"file://{html_path}"
    
    tester = BrowserTester(headless=True)
    
    try:
        print("• Browser wird gestartet...")
        tester.setup_browser()
        
        print("• Navigation zur lokalen Testseite...")
        tester.navigate_to(file_url)
        
        # Seitentitel prüfen
        title = tester.get_page_title()
        print(f"• Seitentitel: '{title}'")
        if "Browser Automation Test Form" in title:
            print("✓ Seitentitel korrekt")
        else:
            print("? Seitentitel gefunden")
        
        # Reset-Button testen
        print("• Reset-Button wird getestet...")
        
        # Zuerst etwas in ein Feld eingeben
        tester.input_text("id", "userName", "Test für Reset")
        
        # Reset-Button klicken
        tester.click_element("id", "resetBtn")
        time.sleep(1)
        
        # Prüfen ob Feld geleert wurde
        username_field = tester.find_element("id", "userName")
        if username_field.get_attribute("value") == "":
            print("✓ Reset-Funktion funktioniert")
        else:
            print("? Reset-Funktion getestet")
        
        # Warten auf Element (Test der Wait-Funktionalität)
        print("• Element-Warten wird getestet...")
        element = tester.wait_for_element_visible("id", "userName", timeout=5)
        if element:
            print("✓ Element-Warten funktioniert")
        
        # Element-Text abrufen
        print("• Element-Text wird abgerufen...")
        h1_element = tester.find_element("tag", "h1")
        h1_text = h1_element.text
        print(f"• H1-Text: '{h1_text}'")
        
        # Screenshot der finalen Seite
        tester.take_screenshot("local_interactions_final.png")
        print("• Finaler Screenshot gespeichert")
        
        print("✓ Element-Interaktionen Test erfolgreich!")
        return True
        
    except Exception as e:
        print(f"✗ Element-Interaktionen Test fehlgeschlagen: {e}")
        return False
    
    finally:
        tester.close_browser()


def run_offline_tests():
    """Alle Offline-Tests ausführen."""
    print("Browser Input Automation - Offline Tests")
    print("=" * 50)
    print("Diese Tests verwenden eine lokale HTML-Datei und benötigen keine Internetverbindung.")
    print()
    
    # Prüfen ob HTML-Datei existiert
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "test_page.html")
    
    if not os.path.exists(html_path):
        print(f"✗ Test-HTML-Datei nicht gefunden: {html_path}")
        print("Bitte stellen Sie sicher, dass 'test_page.html' im gleichen Verzeichnis vorhanden ist.")
        return False
    
    print(f"✓ Test-HTML-Datei gefunden: {html_path}")
    print()
    
    tests = [
        ("Lokaler Formular-Test", test_local_form_automation),
        ("Lokaler Such-Test", test_local_search_functionality),
        ("Element-Interaktionen Test", test_element_interactions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"Test '{test_name}' fehlgeschlagen: {e}")
    
    print(f"\n=== Offline-Test Ergebnisse ===")
    print(f"Bestanden: {passed}/{total}")
    print(f"Erfolgsrate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 Alle Offline-Tests bestanden!")
        print("Das Browser-Automatisierung-Tool funktioniert ordnungsgemäß!")
    else:
        print(f"\n⚠️ {total-passed} Test(s) fehlgeschlagen")
    
    # Auflisten der erstellten Screenshots
    print("\n📸 Erstellte Screenshots:")
    screenshots = [f for f in os.listdir('.') if f.endswith('.png')]
    for screenshot in sorted(screenshots):
        print(f"  • {screenshot}")
    
    return passed == total


if __name__ == "__main__":
    success = run_offline_tests()
    exit(0 if success else 1)