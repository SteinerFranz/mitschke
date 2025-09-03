"""
Einfache Verwendungsbeispiele für das Browser-Testing-Tool.
Simple usage examples for the browser testing tool.
"""

from browser_tester import BrowserTester
import time


def simple_search_example():
    """Einfaches Beispiel für eine Google-Suche."""
    print("=== Einfaches Such-Beispiel ===")
    
    # Browser-Tester initialisieren (headless für automatische Tests)
    tester = BrowserTester(headless=True, timeout=15)
    
    try:
        # Browser starten
        print("• Browser wird gestartet...")
        tester.setup_browser()
        
        # Zur Google-Suchseite navigieren
        print("• Navigation zu Google...")
        tester.navigate_to("https://www.google.com")
        
        # Cookies akzeptieren (falls Dialog erscheint)
        try:
            tester.click_element("id", "L2AGLb")
            time.sleep(1)
        except:
            print("  (Kein Cookie-Dialog gefunden)")
        
        # Suchtext eingeben
        search_term = "Python Selenium WebDriver"
        print(f"• Suche nach: '{search_term}'")
        tester.input_text("name", "q", search_term)
        
        # Such-Button klicken
        print("• Such-Button wird geklickt...")
        tester.click_element("name", "btnK")
        
        # Warten auf Suchergebnisse
        time.sleep(3)
        
        # Ergebnis validieren
        title = tester.get_page_title()
        print(f"• Seitentitel: '{title}'")
        
        if search_term.lower() in title.lower():
            print("✓ Suche erfolgreich!")
        else:
            print("? Suchergebnisse geladen (Titel-Validierung nicht eindeutig)")
        
        # Screenshot erstellen
        tester.take_screenshot("google_search_result.png")
        print("• Screenshot gespeichert: google_search_result.png")
        
    except Exception as e:
        print(f"✗ Fehler beim Such-Test: {e}")
        return False
    
    finally:
        # Browser schließen
        tester.close_browser()
        print("• Browser geschlossen")
    
    return True


def simple_form_example():
    """Einfaches Beispiel für Formular-Tests."""
    print("\n=== Einfaches Formular-Beispiel ===")
    
    tester = BrowserTester(headless=True)
    
    try:
        print("• Browser wird gestartet...")
        tester.setup_browser()
        
        # Zur Test-Formular-Seite navigieren
        print("• Navigation zur Formular-Testseite...")
        tester.navigate_to("https://httpbin.org/forms/post")
        
        # Formularfelder ausfüllen
        print("• Formularfelder werden ausgefüllt...")
        tester.input_text("name", "custname", "Test Benutzer")
        tester.input_text("name", "custtel", "0123-456789")
        tester.input_text("name", "custemail", "test@beispiel.de")
        
        # Dropdown-Auswahl
        print("• Dropdown-Option wird ausgewählt...")
        tester.select_dropdown_option("name", "size", option_value="medium")
        
        # Screenshot vor dem Absenden
        tester.take_screenshot("form_before_submit.png")
        print("• Screenshot vor Absendung gespeichert")
        
        # Formular absenden
        print("• Formular wird abgesendet...")
        tester.submit_form()
        
        # Warten auf Antwort
        time.sleep(2)
        
        # Erfolgsmeldung prüfen
        current_url = tester.driver.current_url
        print(f"• Aktuelle URL: {current_url}")
        
        if "/post" in current_url:
            print("✓ Formular erfolgreich abgesendet!")
        else:
            print("? Formular-Übertragung abgeschlossen")
        
        # Screenshot nach dem Absenden
        tester.take_screenshot("form_after_submit.png")
        print("• Screenshot nach Absendung gespeichert")
        
    except Exception as e:
        print(f"✗ Fehler beim Formular-Test: {e}")
        return False
    
    finally:
        tester.close_browser()
        print("• Browser geschlossen")
    
    return True


def interactive_demo():
    """Interaktive Demo mit sichtbarem Browser."""
    print("\n=== Interaktive Demo (sichtbarer Browser) ===")
    print("Hinweis: Diese Demo öffnet einen sichtbaren Browser")
    
    # Browser im sichtbaren Modus starten
    tester = BrowserTester(headless=False, timeout=20)
    
    try:
        print("• Browser wird sichtbar gestartet...")
        tester.setup_browser()
        
        # Zur DuckDuckGo navigieren (datenschutzfreundliche Suchmaschine)
        print("• Navigation zu DuckDuckGo...")
        tester.navigate_to("https://duckduckgo.com")
        
        # Kurz warten, damit der Benutzer sehen kann
        print("• Warte 3 Sekunden...")
        time.sleep(3)
        
        # Suche durchführen
        search_term = "Browser Automatisierung"
        print(f"• Suche nach: '{search_term}'")
        tester.input_text("name", "q", search_term)
        
        # Warten, damit der Benutzer die Eingabe sehen kann
        time.sleep(2)
        
        # Such-Button klicken
        print("• Such-Button wird geklickt...")
        tester.click_element("id", "search_button_homepage")
        
        # Auf Ergebnisse warten
        print("• Warte auf Suchergebnisse...")
        time.sleep(5)
        
        # Screenshot der Ergebnisse
        tester.take_screenshot("duckduckgo_results.png")
        print("• Screenshot gespeichert: duckduckgo_results.png")
        
        print("✓ Interaktive Demo abgeschlossen!")
        print("  Der Browser bleibt noch 5 Sekunden offen...")
        time.sleep(5)
        
    except Exception as e:
        print(f"✗ Fehler in der interaktiven Demo: {e}")
        return False
    
    finally:
        tester.close_browser()
        print("• Browser geschlossen")
    
    return True


def main():
    """Hauptfunktion - führt alle Beispiele aus."""
    print("Browser Input Automation Testing - Verwendungsbeispiele")
    print("=" * 60)
    print("Dieses Programm demonstriert automatisierte Browser-Tests")
    print()
    
    # Sammle Testergebnisse
    results = []
    
    # Führe alle Beispiele aus
    examples = [
        ("Einfaches Such-Beispiel", simple_search_example),
        ("Einfaches Formular-Beispiel", simple_form_example),
        ("Interaktive Demo", interactive_demo)
    ]
    
    for name, example_func in examples:
        try:
            print(f"\n{'='*20} {name} {'='*20}")
            result = example_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Beispiel '{name}' fehlgeschlagen: {e}")
            results.append((name, False))
    
    # Ergebnisse zusammenfassen
    print(f"\n{'='*20} ZUSAMMENFASSUNG {'='*20}")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ ERFOLGREICH" if result else "✗ FEHLGESCHLAGEN"
        print(f"{name}: {status}")
    
    print(f"\nGesamt: {passed}/{total} Beispiele erfolgreich")
    success_rate = (passed / total) * 100
    print(f"Erfolgsrate: {success_rate:.1f}%")
    
    if passed == total:
        print("\n🎉 Alle Beispiele erfolgreich ausgeführt!")
        print("Das Browser-Testing-Tool ist funktionsfähig!")
    else:
        print(f"\n⚠️  {total - passed} Beispiel(e) fehlgeschlagen")
        print("Überprüfen Sie die Internetverbindung und Browser-Installation")


if __name__ == "__main__":
    main()