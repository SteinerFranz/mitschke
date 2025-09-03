# Browser Input Automation Testing Program

Ein umfassendes Python-Programm zur automatisierten Testung von Browsereingaben und -interaktionen.

## Beschreibung

Dieses Programm erfüllt die Anforderung, ein Tool in einer beliebigen Programmiersprache zu erstellen, das Browsereingaben automatisiert testen kann. Es verwendet Python mit Selenium WebDriver für die Browser-Automatisierung und bietet eine vollständige Test-Framework-Lösung.

## Features

### Grundfunktionen
- **Browser-Setup**: Automatische Browser-Initialisierung (Chrome, Firefox)
- **Navigation**: URL-Navigation und Seitenmanagement
- **Element-Interaktion**: Klicken, Texteingabe, Dropdown-Auswahl
- **Formular-Handling**: Automatisches Ausfüllen und Absenden von Formularen
- **Warteschleifen**: Intelligente Wartezeiten für Element-Verfügbarkeit
- **Screenshot-Funktionalität**: Automatische Bildschirmfotos für Dokumentation

### Erweiterte Funktionen
- **Strukturierte Formulardaten**: JSON-basierte Formularkonfiguration
- **Test-Sequenzen**: Vorkonfigurierte Test-Abläufe
- **Validierung**: Automatische Erfolgs-/Fehlerprüfung
- **Error-Handling**: Robuste Fehlerbehandlung
- **Logging**: Umfangreiche Protokollierung aller Aktionen

## Installation

### Voraussetzungen
- Python 3.7 oder höher
- Google Chrome Browser (für Chrome WebDriver)

### Setup
```bash
# Repository klonen
git clone <repository-url>
cd mitschke

# Abhängigkeiten installieren
pip install -r requirements.txt
```

## Verwendung

### Grundlegende Verwendung

```python
from browser_tester import BrowserTester

# Browser-Tester initialisieren
tester = BrowserTester(headless=True)  # headless=False für sichtbaren Browser

try:
    # Browser starten
    tester.setup_browser()
    
    # Zur Webseite navigieren
    tester.navigate_to("https://example.com")
    
    # Text eingeben
    tester.input_text("id", "username", "mein_benutzername")
    tester.input_text("id", "password", "mein_passwort")
    
    # Button klicken
    tester.click_element("id", "login_button")
    
    # Dropdown-Auswahl
    tester.select_dropdown_option("name", "country", option_text="Deutschland")
    
    # Formular absenden
    tester.submit_form()
    
    # Screenshot erstellen
    tester.take_screenshot("test_result.png")
    
finally:
    # Browser schließen
    tester.close_browser()
```

### Beispiel-Tests ausführen

```bash
# Grundlegende Tests
python browser_tester.py

# Beispiel-Tests
python test_examples.py

# Erweiterte Beispiele
python advanced_examples.py
```

## Test-Szenarien

### 1. Formular-Tests (`test_examples.py`)
- Texteingabe-Felder testen
- Dropdown-Menüs validieren
- Formular-Übertragung prüfen
- Eingabevalidierung

### 2. Such-Funktionalität (`test_examples.py`)
- Sucheingaben automatisieren
- Ergebnisse validieren
- Navigation testen

### 3. Erweiterte Tests (`advanced_examples.py`)
- JSON-konfigurierte Formulare
- Strukturierte Test-Sequenzen
- Automatische Validierung
- Fehlerbehandlung

## API-Referenz

### BrowserTester Klasse

#### Initialisierung
```python
BrowserTester(browser="chrome", headless=False, timeout=10)
```

#### Hauptmethoden
- `setup_browser()`: Browser initialisieren
- `navigate_to(url)`: Zu URL navigieren
- `find_element(locator_type, locator_value)`: Element finden
- `input_text(locator_type, locator_value, text)`: Text eingeben
- `click_element(locator_type, locator_value)`: Element klicken
- `select_dropdown_option(locator_type, locator_value, option_text)`: Dropdown-Option wählen
- `submit_form()`: Formular absenden
- `take_screenshot(filename)`: Screenshot erstellen
- `close_browser()`: Browser schließen

#### Locator-Typen
- `"id"`: Element-ID
- `"name"`: Name-Attribut
- `"class"`: CSS-Klasse
- `"xpath"`: XPath-Ausdruck
- `"css"`: CSS-Selektor
- `"tag"`: HTML-Tag-Name

### AdvancedBrowserTester Klasse

Erweitert BrowserTester mit zusätzlichen Funktionen:
- `fill_form_from_data(form_data)`: Formular aus JSON-Daten füllen
- `validate_form_submission(success_indicators)`: Übertragung validieren
- `run_test_sequence(test_config)`: Test-Sequenz ausführen

## Konfiguration

### Browser-Einstellungen
```python
# Headless-Modus (unsichtbar)
tester = BrowserTester(headless=True)

# Sichtbarer Browser
tester = BrowserTester(headless=False)

# Angepasste Timeout-Zeit
tester = BrowserTester(timeout=20)
```

### Test-Konfiguration (JSON)
```python
test_config = {
    'setup': {
        'url': 'https://example.com',
        'wait_time': 2
    },
    'steps': [
        {
            'type': 'input',
            'description': 'Username eingeben',
            'locator_type': 'id',
            'locator_value': 'username',
            'value': 'testuser'
        },
        {
            'type': 'click',
            'description': 'Login-Button klicken',
            'locator_type': 'id',
            'locator_value': 'login_btn'
        }
    ]
}
```

## Fehlerbehebung

### Häufige Probleme

1. **ChromeDriver nicht gefunden**
   - Lösung: `webdriver-manager` installiert ChromeDriver automatisch

2. **Element nicht gefunden**
   - Lösung: Timeout erhöhen oder andere Locator-Strategie verwenden

3. **Browser startet nicht**
   - Lösung: Headless-Modus verwenden oder Browser-Pfad prüfen

### Logging aktivieren
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Beispiele

### Einfacher Google-Suche Test
```python
from browser_tester import BrowserTester

tester = BrowserTester()
tester.setup_browser()

try:
    tester.navigate_to("https://www.google.com")
    tester.input_text("name", "q", "Python Selenium")
    tester.click_element("name", "btnK")
    
    # Warten auf Ergebnisse
    time.sleep(2)
    
    # Validierung
    title = tester.get_page_title()
    assert "Python Selenium" in title
    
    print("✓ Google-Suche erfolgreich")
    
finally:
    tester.close_browser()
```

### Formulardaten-Test
```python
form_data = {
    'name': {
        'locator_type': 'id',
        'locator_value': 'user_name',
        'value': 'Max Mustermann',
        'action': 'input'
    },
    'email': {
        'locator_type': 'name',
        'locator_value': 'user_email',
        'value': 'max@example.com',
        'action': 'input'
    }
}

tester = AdvancedBrowserTester()
tester.setup_browser()
tester.navigate_to("https://example.com/form")
tester.fill_form_from_data(form_data)
tester.submit_form()
```

## Mitwirkung

Beiträge sind willkommen! Bitte:
1. Fork erstellen
2. Feature-Branch erstellen (`git checkout -b feature/neue-funktion`)
3. Änderungen committen (`git commit -am 'Neue Funktion hinzufügen'`)
4. Branch pushen (`git push origin feature/neue-funktion`)
5. Pull Request erstellen

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## Autor

Browser Testing Framework - Ein automatisiertes Testing-Tool für Browsereingaben