#!/usr/bin/env python3
"""
ADS Pillar - GUI Application
Benutzerfreundliche Oberfläche für das komplette ADS Pillar System
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import json
import os
import threading
from pathlib import Path
import webbrowser
from data_pipeline import DataScraper, PillarPageGenerator, LocationData, DataEnrichment
from niche_research import NicheValidator, KeywordResearch

class ADSPillarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADS Pillar - GUI Dashboard")
        self.root.geometry("1200x800")
        
        # Variables
        self.project_config = {
            'site_name': tk.StringVar(value="Local Places Guide"),
            'domain': tk.StringVar(value="your-domain.com"),
            'city': tk.StringVar(value="Berlin"),
            'category': tk.StringVar(value="Parks"),
            'adsense_id': tk.StringVar(value="ca-pub-XXXXXXXXXXXXXXXX"),
            'ga_id': tk.StringVar(value="GA_MEASUREMENT_ID")
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI"""
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Project Setup
        self.setup_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.setup_tab, text="🚀 Projekt Setup")
        self.create_setup_tab()
        
        # Tab 2: Niche Research
        self.niche_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.niche_tab, text="🔍 Nischen-Analyse")
        self.create_niche_tab()
        
        # Tab 3: Data Collection
        self.data_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.data_tab, text="📊 Daten sammeln")
        self.create_data_tab()
        
        # Tab 4: Page Generation
        self.generate_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.generate_tab, text="🏗️ Seiten generieren")
        self.create_generate_tab()
        
        # Tab 5: Revenue Tracking
        self.revenue_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.revenue_tab, text="💰 Revenue Dashboard")
        self.create_revenue_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Bereit", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_setup_tab(self):
        """Create project setup tab"""
        
        # Main frame
        main_frame = ttk.Frame(self.setup_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Project Configuration
        config_frame = ttk.LabelFrame(main_frame, text="Projekt Konfiguration")
        config_frame.pack(fill="x", pady=(0, 20))
        
        # Config fields
        ttk.Label(config_frame, text="Website Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(config_frame, textvariable=self.project_config['site_name'], width=40).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(config_frame, text="Domain:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(config_frame, textvariable=self.project_config['domain'], width=40).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(config_frame, text="Stadt:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(config_frame, textvariable=self.project_config['city'], width=40).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(config_frame, text="Kategorie:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(config_frame, textvariable=self.project_config['category'], width=40).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(config_frame, text="AdSense ID:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(config_frame, textvariable=self.project_config['adsense_id'], width=40).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(config_frame, text="Google Analytics ID:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(config_frame, textvariable=self.project_config['ga_id'], width=40).grid(row=5, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(button_frame, text="🚀 Vollständiges Setup starten", 
                  command=self.run_full_setup, style="Accent.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="💾 Konfiguration speichern", 
                  command=self.save_config).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="📁 Konfiguration laden", 
                  command=self.load_config).pack(side="left")
        
        # Output area
        self.setup_output = scrolledtext.ScrolledText(main_frame, height=15, width=80)
        self.setup_output.pack(fill="both", expand=True, pady=(20, 0))
        
    def create_niche_tab(self):
        """Create niche research tab"""
        
        main_frame = ttk.Frame(self.niche_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Button(control_frame, text="🔍 Nischen analysieren", 
                  command=self.analyze_niches).pack(side="left", padx=(0, 10))
        ttk.Button(control_frame, text="📊 Keyword Research", 
                  command=self.keyword_research).pack(side="left")
        
        # Results table
        columns = ("Nische", "Score", "Suchvolumen", "Competition", "RPM Potenzial")
        self.niche_tree = ttk.Treeview(main_frame, columns=columns, show="tree headings", height=10)
        
        for col in columns:
            self.niche_tree.heading(col, text=col)
            self.niche_tree.column(col, width=150)
        
        self.niche_tree.pack(fill="both", expand=True)
        
        # Details area
        self.niche_details = scrolledtext.ScrolledText(main_frame, height=8)
        self.niche_details.pack(fill="x", pady=(20, 0))
        
    def create_data_tab(self):
        """Create data collection tab"""
        
        main_frame = ttk.Frame(self.data_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Data source selection
        source_frame = ttk.LabelFrame(main_frame, text="Datenquellen")
        source_frame.pack(fill="x", pady=(0, 20))
        
        self.data_sources = {
            'google_places': tk.BooleanVar(value=True),
            'manual_csv': tk.BooleanVar(value=False),
            'yelp': tk.BooleanVar(value=False),
            'foursquare': tk.BooleanVar(value=False)
        }
        
        ttk.Checkbutton(source_frame, text="Google Places API", 
                       variable=self.data_sources['google_places']).pack(anchor="w", padx=5, pady=2)
        ttk.Checkbutton(source_frame, text="Manuelle CSV", 
                       variable=self.data_sources['manual_csv']).pack(anchor="w", padx=5, pady=2)
        ttk.Checkbutton(source_frame, text="Yelp API (Coming Soon)", 
                       variable=self.data_sources['yelp'], state="disabled").pack(anchor="w", padx=5, pady=2)
        ttk.Checkbutton(source_frame, text="Foursquare API (Coming Soon)", 
                       variable=self.data_sources['foursquare'], state="disabled").pack(anchor="w", padx=5, pady=2)
        
        # API Configuration
        api_frame = ttk.LabelFrame(main_frame, text="API Konfiguration")
        api_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(api_frame, text="Google Places API Key:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.google_api_key = tk.StringVar()
        ttk.Entry(api_frame, textvariable=self.google_api_key, width=50, show="*").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(api_frame, text="Search Query:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.search_query = tk.StringVar(value="parks")
        ttk.Entry(api_frame, textvariable=self.search_query, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Button(control_frame, text="🔄 Daten sammeln", 
                  command=self.collect_data).pack(side="left", padx=(0, 10))
        ttk.Button(control_frame, text="📁 CSV laden", 
                  command=self.load_csv).pack(side="left", padx=(0, 10))
        ttk.Button(control_frame, text="💾 CSV speichern", 
                  command=self.save_csv).pack(side="left")
        
        # Data preview
        self.data_preview = ttk.Treeview(main_frame, height=12)
        self.data_preview.pack(fill="both", expand=True)
        
    def create_generate_tab(self):
        """Create page generation tab"""
        
        main_frame = ttk.Frame(self.generate_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Template selection
        template_frame = ttk.LabelFrame(main_frame, text="Template Auswahl")
        template_frame.pack(fill="x", pady=(0, 20))
        
        self.template_var = tk.StringVar(value="pillar_page_skeleton.html")
        ttk.Radiobutton(template_frame, text="Standard Pillar Page", 
                       variable=self.template_var, value="pillar_page_skeleton.html").pack(anchor="w", padx=5, pady=2)
        ttk.Radiobutton(template_frame, text="Mobile-First Template", 
                       variable=self.template_var, value="mobile_template.html").pack(anchor="w", padx=5, pady=2)
        ttk.Radiobutton(template_frame, text="High-RPM Template", 
                       variable=self.template_var, value="rpm_optimized.html").pack(anchor="w", padx=5, pady=2)
        
        # Generation options
        options_frame = ttk.LabelFrame(main_frame, text="Generierungsoptionen")
        options_frame.pack(fill="x", pady=(0, 20))
        
        self.gen_options = {
            'include_schema': tk.BooleanVar(value=True),
            'include_analytics': tk.BooleanVar(value=True),
            'include_adsense': tk.BooleanVar(value=True),
            'mobile_optimized': tk.BooleanVar(value=True),
            'fast_loading': tk.BooleanVar(value=True)
        }
        
        row = 0
        for key, var in self.gen_options.items():
            text = key.replace('_', ' ').title()
            ttk.Checkbutton(options_frame, text=text, variable=var).grid(row=row//2, column=row%2, sticky="w", padx=5, pady=2)
            row += 1
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Button(control_frame, text="🏗️ Seite generieren", 
                  command=self.generate_page).pack(side="left", padx=(0, 10))
        ttk.Button(control_frame, text="👀 Vorschau öffnen", 
                  command=self.preview_page).pack(side="left", padx=(0, 10))
        ttk.Button(control_frame, text="📤 Upload zu Server", 
                  command=self.upload_page).pack(side="left")
        
        # Generation log
        self.gen_log = scrolledtext.ScrolledText(main_frame, height=15)
        self.gen_log.pack(fill="both", expand=True)
        
    def create_revenue_tab(self):
        """Create revenue tracking tab"""
        
        main_frame = ttk.Frame(self.revenue_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # KPI Dashboard
        kpi_frame = ttk.LabelFrame(main_frame, text="📊 KPI Dashboard")
        kpi_frame.pack(fill="x", pady=(0, 20))
        
        # KPI values (mock data for demo)
        kpis = [
            ("Pageviews (Monat):", "45,230", "↗️ +15%"),
            ("Page RPM:", "€12.45", "↗️ +2.1%"),
            ("AdSense Revenue:", "€563.12", "↗️ +18%"),
            ("Avg. Position:", "23.4", "↗️ -3.2"),
        ]
        
        for i, (label, value, trend) in enumerate(kpis):
            ttk.Label(kpi_frame, text=label).grid(row=i//2, column=(i%2)*3, sticky="w", padx=5, pady=5)
            ttk.Label(kpi_frame, text=value, font=("Arial", 12, "bold")).grid(row=i//2, column=(i%2)*3+1, padx=5, pady=5)
            ttk.Label(kpi_frame, text=trend).grid(row=i//2, column=(i%2)*3+2, padx=5, pady=5)
        
        # Revenue calculator
        calc_frame = ttk.LabelFrame(main_frame, text="💰 Revenue Calculator")
        calc_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(calc_frame, text="Monatliche Pageviews:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.calc_pageviews = tk.IntVar(value=50000)
        ttk.Scale(calc_frame, from_=10000, to=1000000, variable=self.calc_pageviews, 
                 orient="horizontal", length=200).grid(row=0, column=1, padx=5, pady=5)
        self.pv_label = ttk.Label(calc_frame, text="50,000")
        self.pv_label.grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(calc_frame, text="Page RPM (€):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.calc_rpm = tk.DoubleVar(value=12.0)
        ttk.Scale(calc_frame, from_=5.0, to=30.0, variable=self.calc_rpm, 
                 orient="horizontal", length=200).grid(row=1, column=1, padx=5, pady=5)
        self.rpm_label = ttk.Label(calc_frame, text="€12.00")
        self.rpm_label.grid(row=1, column=2, padx=5, pady=5)
        
        self.revenue_label = ttk.Label(calc_frame, text="Geschätzter Umsatz: €600/Monat", 
                                      font=("Arial", 12, "bold"))
        self.revenue_label.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Bind scale updates
        self.calc_pageviews.trace('w', self.update_revenue_calc)
        self.calc_rpm.trace('w', self.update_revenue_calc)
        
        # Analytics integration
        analytics_frame = ttk.LabelFrame(main_frame, text="📈 Analytics Integration")
        analytics_frame.pack(fill="both", expand=True)
        
        ttk.Button(analytics_frame, text="🔗 Mit Google Analytics verbinden", 
                  command=self.connect_analytics).pack(pady=10)
        ttk.Button(analytics_frame, text="💰 AdSense Dashboard öffnen", 
                  command=self.open_adsense).pack(pady=5)
        
        self.analytics_status = ttk.Label(analytics_frame, text="Status: Nicht verbunden")
        self.analytics_status.pack(pady=10)
        
    def log_message(self, message, widget=None):
        """Log message to specified widget or setup output"""
        if widget is None:
            widget = self.setup_output
        
        widget.insert(tk.END, f"{message}\n")
        widget.see(tk.END)
        self.root.update()
        
    def update_status(self, status):
        """Update status bar"""
        self.status_bar.config(text=status)
        self.root.update()
        
    def run_full_setup(self):
        """Run complete project setup"""
        def setup_thread():
            try:
                self.update_status("Setup läuft...")
                self.log_message("🚀 Starte vollständiges Setup...")
                
                # Create directories
                os.makedirs("data", exist_ok=True)
                os.makedirs("generated", exist_ok=True)
                self.log_message("✅ Verzeichnisse erstellt")
                
                # Save configuration
                config_data = {key: var.get() for key, var in self.project_config.items()}
                with open("project_config.json", "w") as f:
                    json.dump(config_data, f, indent=2)
                self.log_message("✅ Konfiguration gespeichert")
                
                # Run niche analysis
                self.log_message("🔍 Führe Nischen-Analyse durch...")
                validator = NicheValidator()
                recommendations = validator.get_niche_recommendations()
                
                self.log_message(f"✅ {len(recommendations)} Nischen analysiert")
                for rec in recommendations[:3]:
                    self.log_message(f"   • {rec['niche']['name']} (Score: {rec['opportunity_score']})")
                
                # Create sample data
                self.create_sample_data()
                self.log_message("✅ Beispieldaten erstellt")
                
                self.log_message("🎉 Setup erfolgreich abgeschlossen!")
                self.update_status("Setup abgeschlossen")
                
            except Exception as e:
                self.log_message(f"❌ Fehler beim Setup: {str(e)}")
                self.update_status("Setup fehlgeschlagen")
        
        threading.Thread(target=setup_thread, daemon=True).start()
        
    def create_sample_data(self):
        """Create sample data file"""
        sample_data = [
            {
                'id': 1, 'name': 'Tiergarten', 'street': 'Unter den Linden 1',
                'city': self.project_config['city'].get(), 'region': 'Berlin',
                'country': 'Deutschland', 'postcode': '10117',
                'latitude': 52.5144, 'longitude': 13.3501,
                'url': 'https://berlin.de/tiergarten', 'phone': '+49 30 123456',
                'email': '', 'opening_hours': 'Mo-So 06:00-22:00',
                'rating': 4.5, 'review_count': 1250,
                'feature_shade': True, 'feature_benches': True, 'feature_water': True,
                'feature_parking': False, 'feature_toilets': True,
                'feature_wheelchair_accessible': True, 'feature_kids_friendly': True,
                'feature_dogs_allowed': True, 'feature_fee': False,
                'feature_seasonal': False, 'tags': 'park,zentral,tourist'
            }
        ]
        
        df = pd.DataFrame(sample_data)
        df.to_csv("data/sample_data.csv", index=False)
        
    def analyze_niches(self):
        """Analyze available niches"""
        def analyze_thread():
            try:
                self.update_status("Analysiere Nischen...")
                
                validator = NicheValidator()
                recommendations = validator.get_niche_recommendations()
                
                # Clear existing data
                for item in self.niche_tree.get_children():
                    self.niche_tree.delete(item)
                
                # Populate tree
                for rec in recommendations:
                    niche = rec['niche']
                    values = (
                        niche['name'],
                        rec['opportunity_score'],
                        f"{rec['total_estimated_volume']:,}",
                        niche['monetization_potential'],
                        f"€{niche.get('estimated_rpm', '12-20')}"
                    )
                    self.niche_tree.insert("", "end", values=values)
                
                self.update_status("Nischen-Analyse abgeschlossen")
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler bei Nischen-Analyse: {str(e)}")
                self.update_status("Bereit")
        
        threading.Thread(target=analyze_thread, daemon=True).start()
        
    def collect_data(self):
        """Collect data from selected sources"""
        if not self.google_api_key.get() or self.google_api_key.get() == "":
            messagebox.showwarning("API Key fehlt", 
                                 "Bitte Google Places API Key eingeben oder CSV-Datei verwenden.")
            return
            
        def collect_thread():
            try:
                self.update_status("Sammle Daten...")
                
                scraper = DataScraper(delay=1.0)
                places = scraper.scrape_google_places(
                    query=self.search_query.get(),
                    location=self.project_config['city'].get(),
                    api_key=self.google_api_key.get()
                )
                
                if places:
                    # Convert to DataFrame and save
                    df = pd.DataFrame(places)
                    df.to_csv("data/collected_data.csv", index=False)
                    
                    # Update preview
                    self.update_data_preview(df)
                    
                    self.update_status(f"{len(places)} Orte gesammelt")
                    messagebox.showinfo("Erfolg", f"{len(places)} Orte erfolgreich gesammelt!")
                else:
                    messagebox.showwarning("Keine Daten", "Keine Daten gefunden. API Key oder Query prüfen.")
                    self.update_status("Bereit")
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Datensammeln: {str(e)}")
                self.update_status("Bereit")
        
        threading.Thread(target=collect_thread, daemon=True).start()
        
    def update_data_preview(self, df):
        """Update data preview table"""
        # Clear existing columns
        self.data_preview["columns"] = list(df.columns)
        self.data_preview["show"] = "headings"
        
        for col in df.columns:
            self.data_preview.heading(col, text=col)
            self.data_preview.column(col, width=100)
        
        # Clear existing data
        for item in self.data_preview.get_children():
            self.data_preview.delete(item)
        
        # Add new data
        for _, row in df.head(50).iterrows():  # Show first 50 rows
            self.data_preview.insert("", "end", values=list(row))
            
    def generate_page(self):
        """Generate pillar page"""
        def generate_thread():
            try:
                self.update_status("Generiere Seite...")
                self.log_message("🏗️ Starte Seiten-Generierung...", self.gen_log)
                
                # Load data
                if not os.path.exists("data/sample_data.csv"):
                    self.create_sample_data()
                
                df = pd.read_csv("data/sample_data.csv")
                self.log_message(f"✅ {len(df)} Locations geladen", self.gen_log)
                
                # Convert to LocationData objects
                locations = []
                for _, row in df.iterrows():
                    loc = LocationData(
                        id=str(row['id']),
                        name=row['name'],
                        street=row['street'],
                        city=row['city'],
                        region=row.get('region', ''),
                        country=row.get('country', 'Deutschland'),
                        postcode=str(row.get('postcode', '')),
                        latitude=float(row.get('latitude', 0)),
                        longitude=float(row.get('longitude', 0)),
                        url=row.get('url', ''),
                        phone=row.get('phone', ''),
                        email=row.get('email', ''),
                        opening_hours=row.get('opening_hours', ''),
                        rating=float(row.get('rating', 0)),
                        review_count=int(row.get('review_count', 0)),
                        feature_shade=bool(row.get('feature_shade', False)),
                        feature_benches=bool(row.get('feature_benches', False)),
                        feature_water=bool(row.get('feature_water', False)),
                        feature_parking=bool(row.get('feature_parking', False)),
                        feature_toilets=bool(row.get('feature_toilets', False)),
                        feature_wheelchair_accessible=bool(row.get('feature_wheelchair_accessible', False)),
                        feature_kids_friendly=bool(row.get('feature_kids_friendly', False)),
                        feature_dogs_allowed=bool(row.get('feature_dogs_allowed', False)),
                        feature_fee=bool(row.get('feature_fee', True)),
                        feature_seasonal=bool(row.get('feature_seasonal', False)),
                        tags=row.get('tags', '')
                    )
                    locations.append(loc)
                
                # Generate page
                generator = PillarPageGenerator(self.template_var.get())
                output_path = f"generated/{self.project_config['city'].get().lower()}_{self.project_config['category'].get().lower()}.html"
                canonical_url = f"https://{self.project_config['domain'].get()}/{self.project_config['city'].get().lower()}-{self.project_config['category'].get().lower()}"
                
                generator.generate_page(
                    data=locations,
                    city=self.project_config['city'].get(),
                    category=self.project_config['category'].get(),
                    output_path=output_path,
                    canonical_url=canonical_url
                )
                
                self.log_message(f"✅ Seite generiert: {output_path}", self.gen_log)
                self.update_status("Seite erfolgreich generiert")
                
                messagebox.showinfo("Erfolg", f"Seite erfolgreich generiert!\n{output_path}")
                
            except Exception as e:
                self.log_message(f"❌ Fehler: {str(e)}", self.gen_log)
                self.update_status("Generierung fehlgeschlagen")
                messagebox.showerror("Fehler", f"Fehler bei Seiten-Generierung: {str(e)}")
        
        threading.Thread(target=generate_thread, daemon=True).start()
        
    def preview_page(self):
        """Open generated page in browser"""
        output_path = f"generated/{self.project_config['city'].get().lower()}_{self.project_config['category'].get().lower()}.html"
        if os.path.exists(output_path):
            webbrowser.open(f"file://{os.path.abspath(output_path)}")
        else:
            messagebox.showwarning("Datei nicht gefunden", "Bitte zuerst eine Seite generieren.")
            
    def update_revenue_calc(self, *args):
        """Update revenue calculation"""
        pageviews = self.calc_pageviews.get()
        rpm = self.calc_rpm.get()
        revenue = (pageviews * rpm) / 1000
        
        self.pv_label.config(text=f"{pageviews:,}")
        self.rpm_label.config(text=f"€{rpm:.2f}")
        self.revenue_label.config(text=f"Geschätzter Umsatz: €{revenue:,.0f}/Monat")
        
    def save_config(self):
        """Save current configuration"""
        try:
            config_data = {key: var.get() for key, var in self.project_config.items()}
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, "w") as f:
                    json.dump(config_data, f, indent=2)
                messagebox.showinfo("Erfolg", "Konfiguration gespeichert!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
            
    def load_config(self):
        """Load configuration"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, "r") as f:
                    config_data = json.load(f)
                
                for key, var in self.project_config.items():
                    if key in config_data:
                        var.set(config_data[key])
                
                messagebox.showinfo("Erfolg", "Konfiguration geladen!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden: {str(e)}")
            
    def load_csv(self):
        """Load CSV data"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                df = pd.read_csv(filename)
                self.update_data_preview(df)
                messagebox.showinfo("Erfolg", f"CSV geladen: {len(df)} Zeilen")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der CSV: {str(e)}")
                
    def save_csv(self):
        """Save current data as CSV"""
        # Implementation would save current data preview to CSV
        messagebox.showinfo("Info", "CSV-Export wird implementiert...")
        
    def keyword_research(self):
        """Run keyword research"""
        messagebox.showinfo("Info", "Keyword Research wird implementiert...")
        
    def upload_page(self):
        """Upload page to server"""
        messagebox.showinfo("Info", "Server-Upload wird implementiert...")
        
    def connect_analytics(self):
        """Connect to Google Analytics"""
        messagebox.showinfo("Info", "Analytics-Integration wird implementiert...")
        
    def open_adsense(self):
        """Open AdSense dashboard"""
        webbrowser.open("https://www.google.com/adsense")

def main():
    """Run the GUI application"""
    root = tk.Tk()
    app = ADSPillarGUI(root)
    
    # Apply modern styling
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    
    root.mainloop()

if __name__ == "__main__":
    main()
