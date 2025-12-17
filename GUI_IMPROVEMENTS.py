"""
GUI Improvements for Files/gui_app.py

Fügen Sie diese Verbesserungen in die bestehende GUI ein.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import requests


# ===========================================
# 1. VERBESSERUNG: Größere GUI (1400x900)
# ===========================================

# ERSETZEN SIE Zeile 55-63 mit:
def __init__(self, root):
    self.root = root
    self.root.title("ADS Pillar Scraper - Professional Dashboard")

    # Größere GUI: 1400x900 (statt 1200x800)
    width = 1400
    height = 900

    # Center window on screen
    self.root.update_idletasks()
    x = (self.root.winfo_screenwidth() // 2) - (width // 2)
    y = (self.root.winfo_screenheight() // 2) - (height // 2)
    self.root.geometry(f'{width}x{height}+{x}+{y}')

    # Minimum size
    self.root.minsize(1200, 750)

    # Bring window to front
    self.root.lift()
    self.root.attributes('-topmost', True)
    self.root.after_idle(self.root.attributes, '-topmost', False)

    # NEW: Track if config was saved
    self.config_saved = False
    self.config_modified = False

    # ... rest of __init__ ...


# ===========================================
# 2. VERBESSERUNG: Auto-Save beim Tab-Wechsel
# ===========================================

# FÜGEN SIE IN setup_gui() NACH notebook.pack() HINZU:
# self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)


# NEU: Tab Change Handler
def on_tab_changed(self, event):
    """Handle tab change - Auto-save config if modified"""
    current_tab = self.notebook.index(self.notebook.select())

    # Wenn wir vom Setup-Tab weggehen und Config geändert wurde
    if hasattr(self, '_last_tab') and self._last_tab == 0 and current_tab != 0:
        if self.config_modified and not self.config_saved:
            result = messagebox.askyesnocancel(
                "Konfiguration speichern?",
                "Sie haben die Projekt-Konfiguration geändert.\n\n"
                "Möchten Sie die Änderungen speichern, bevor Sie fortfahren?\n\n"
                "Ja = Speichern und fortfahren\n"
                "Nein = Verwerfen und fortfahren\n"
                "Abbrechen = Zurück zum Setup-Tab"
            )

            if result is True:  # Ja - Speichern
                self.save_config()
                self.config_saved = True
            elif result is False:  # Nein - Verwerfen
                self.config_modified = False
            else:  # Abbrechen - Zurück
                self.notebook.select(0)  # Zurück zum Setup-Tab
                return "break"  # Verhindere Tab-Wechsel

    self._last_tab = current_tab


# NEU: Track Config Changes
def track_config_change(self, *args):
    """Track when config is modified"""
    self.config_modified = True
    self.config_saved = False
    # Update Status Bar
    self.status_bar.config(text="⚠️ Konfiguration geändert - Bitte speichern!")


# FÜGEN SIE IN __init__ NACH self.project_config HINZU:
# Track changes on all config variables
for key, var in self.project_config.items():
    var.trace_add('write', self.track_config_change)


# ===========================================
# 3. VERBESSERUNG: API Key Validierung
# ===========================================

def validate_google_api_key(api_key):
    """
    Validate Google Places API Key

    Returns: (is_valid, error_message)
    """
    if not api_key or api_key.strip() == "":
        return False, "API Key ist leer"

    # Check format (Google API keys are usually 39 characters)
    if len(api_key) < 30:
        return False, "API Key ist zu kurz (mindestens 30 Zeichen erwartet)"

    # Check for placeholder
    if "XXXXXXX" in api_key.upper():
        return False, "Bitte ersetzen Sie den Platzhalter mit Ihrem echten API Key"

    # Test API Key with simple request
    try:
        test_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': 'test',
            'key': api_key
        }

        response = requests.get(test_url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 200:
            if data.get('status') == 'REQUEST_DENIED':
                error_msg = data.get('error_message', 'API Key ungültig')
                return False, f"API Key ungültig: {error_msg}"
            elif data.get('status') in ['OK', 'ZERO_RESULTS']:
                return True, "API Key ist gültig!"
            else:
                return False, f"API Status: {data.get('status')}"
        else:
            return False, f"HTTP Fehler: {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "Timeout - Bitte Internetverbindung prüfen"
    except requests.exceptions.RequestException as e:
        return False, f"Netzwerkfehler: {str(e)}"
    except Exception as e:
        return False, f"Fehler: {str(e)}"


# NEU: API Key Validierung Button
def validate_api_key_button(self):
    """Validate the entered API key"""
    api_key = self.google_api_key.get().strip()

    if not api_key:
        messagebox.showwarning(
            "Kein API Key",
            "Bitte geben Sie zuerst einen Google Places API Key ein."
        )
        return

    # Show progress
    self.status_bar.config(text="🔍 Validiere Google Places API Key...")
    self.root.update()

    # Validate
    is_valid, message = validate_google_api_key(api_key)

    if is_valid:
        messagebox.showinfo(
            "✅ API Key gültig",
            f"{message}\n\n"
            "Sie können jetzt Daten von Google Places sammeln."
        )
        self.status_bar.config(text="✅ API Key gültig")
    else:
        messagebox.showerror(
            "❌ API Key ungültig",
            f"{message}\n\n"
            "Bitte prüfen Sie:\n"
            "1. Haben Sie die Google Places API aktiviert?\n"
            "2. Ist der API Key korrekt kopiert?\n"
            "3. Gibt es Einschränkungen für den Key?\n\n"
            "Google Cloud Console:\n"
            "https://console.cloud.google.com/apis/credentials"
        )
        self.status_bar.config(text="❌ API Key ungültig")


# ===========================================
# 4. VERBESSERUNG: Explizite API Benennung
# ===========================================

# ERSETZEN SIE Zeilen 248-250 mit:
def create_data_tab(self):
    # ... existing code ...

    # API Configuration (IMPROVED)
    api_frame = ttk.LabelFrame(main_frame, text="🔑 Google Places API Konfiguration")
    api_frame.pack(fill="x", pady=(0, 20))

    # Header
    header_label = ttk.Label(
        api_frame,
        text="Google Places API Key (erforderlich für Live-Scraping)",
        font=('TkDefaultFont', 10, 'bold')
    )
    header_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=(5, 2))

    # Info text
    info_label = ttk.Label(
        api_frame,
        text="Erstellen Sie einen API Key unter: https://console.cloud.google.com/apis/credentials",
        foreground="blue",
        cursor="hand2"
    )
    info_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 10))
    info_label.bind("<Button-1>", lambda e: webbrowser.open("https://console.cloud.google.com/apis/credentials"))

    # API Key Entry
    ttk.Label(api_frame, text="API Key:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    self.google_api_key = tk.StringVar()

    api_entry = ttk.Entry(api_frame, textvariable=self.google_api_key, width=50, show="*")
    api_entry.grid(row=2, column=1, padx=5, pady=5)

    # Show/Hide Button
    show_button = ttk.Button(
        api_frame,
        text="👁️",
        width=3,
        command=lambda: self.toggle_api_visibility(api_entry)
    )
    show_button.grid(row=2, column=2, padx=5, pady=5)

    # Validate Button
    validate_button = ttk.Button(
        api_frame,
        text="✓ Validieren",
        command=self.validate_api_key_button,
        style="Accent.TButton"
    )
    validate_button.grid(row=2, column=3, padx=5, pady=5)

    # ... rest of create_data_tab ...


def toggle_api_visibility(self, entry_widget):
    """Toggle API key visibility"""
    if entry_widget.cget('show') == '*':
        entry_widget.config(show='')
    else:
        entry_widget.config(show='*')


# ===========================================
# 5. VERBESSERUNG: Bessere Styles + Tab Binding
# ===========================================

# ERWEITERN SIE setup_gui() mit:
def setup_gui(self):
    """Setup the main GUI"""

    # Configure styles
    style = ttk.Style()

    # Modern button style
    style.configure(
        "Accent.TButton",
        font=('TkDefaultFont', 10, 'bold'),
        padding=10
    )

    # Tab style
    style.configure(
        "TNotebook.Tab",
        padding=[20, 10],
        font=('TkDefaultFont', 10)
    )

    # Create notebook for tabs
    self.notebook = ttk.Notebook(self.root)
    self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # NEU: Bind tab change event (für Auto-Save)
    self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    # ... rest of setup_gui ...


# ===========================================
# 6. VERBESSERUNG: Save Config Updates
# ===========================================

def save_config(self):
    """Save project configuration"""
    config = {
        'site_name': self.project_config['site_name'].get(),
        'domain': self.project_config['domain'].get(),
        'city': self.project_config['city'].get(),
        'category': self.project_config['category'].get(),
        'adsense_id': self.project_config['adsense_id'].get(),
        'ga_id': self.project_config['ga_id'].get()
    }

    try:
        with open('project_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Mark as saved
        self.config_saved = True
        self.config_modified = False

        messagebox.showinfo(
            "✅ Gespeichert",
            "Projekt-Konfiguration wurde gespeichert!\n\n"
            f"Datei: project_config.json"
        )
        self.status_bar.config(text="✅ Konfiguration gespeichert")

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")


# ===========================================
# INTEGRATION ANLEITUNG
# ===========================================

"""
So integrieren Sie diese Verbesserungen:

1. Öffnen Sie Files/gui_app.py

2. ERSETZEN SIE die __init__ Methode (Zeile 52-100)
   mit der verbesserten Version oben (Punkt 1)

3. FÜGEN SIE DIE NEUEN METHODEN HINZU:
   - on_tab_changed()
   - track_config_change()
   - validate_google_api_key()
   - validate_api_key_button()
   - toggle_api_visibility()

4. ERSETZEN SIE create_data_tab() API-Sektion (Zeilen 248-250)
   mit der verbesserten Version (Punkt 4)

5. ERWEITERN SIE setup_gui() mit Styles und Tab Binding (Punkt 5):
   - Style-Konfiguration hinzufügen
   - Tab change event binding hinzufügen

6. AKTUALISIEREN SIE save_config() (Punkt 6)

7. FÜGEN SIE requests HINZU zu den Imports oben:
   import requests

8. TESTEN SIE die GUI:
   python Files/gui_app.py
"""
