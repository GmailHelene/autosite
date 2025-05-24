from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = "hemmelig_nokkel_for_html_generator"

# Tema-konfigurasjon
THEMES = {
    'landing_page_theme': {
        'name': 'Landing Page',
        'description': 'Kraftfull landingsside for bedrifter og tjenester',
        'colors': {
            'primary': '#4facfe',
            'secondary': '#00f2fe',
            'text': '#333',
            'background': '#ffffff'
        }
    },
    'massively_blog_theme': {
        'name': 'Massively Blog',
        'description': 'Elegant blog-design inspirert av HTML5 UP',
        'colors': {
            'primary': '#212931',
            'secondary': '#ff6b6b',
            'text': '#ffffff',
            'background': '#1e252d'
        }
    },
    'modern_business_theme': {
        'name': 'Moderne Business',
        'description': 'Profesjonell og ren design for bedrifter',
        'colors': {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'text': '#333',
            'background': '#ffffff'
        }
    },
    'creative_portfolio_theme': {
        'name': 'Kreativ Portfolio',
        'description': 'Fargerik design for kreative fagfolk',
        'colors': {
            'primary': '#ff6b6b',
            'secondary': '#4ecdc4',
            'text': '#2c3e50',
            'background': '#ffffff'
        } 
    },
    "prologue_theme": {
        "name": "Prologue (HTML5 UP)",
        "description": "Portfolio/profil-tema fra HTML5 UP",
        "html5up": True,
        "folder": "tema6-html5up-prologue"
    },
    "parallelism_theme": {
        "name": "Parallelism (HTML5 UP)",
        "description": "Moderne portefølje med parallakse-effekt",
        "html5up": True,
        "folder": "tema5-html5up-parallelism"
    }
}

# Standard innhold
DEFAULT_MENU_ITEMS = [
    {'text': 'Hjem', 'url': '#hjem'},
    {'text': 'Tjenester', 'url': '#tjenester'},
    {'text': 'Om oss', 'url': '#om'},
    {'text': 'Kontakt', 'url': '#kontakt'}
]

DEFAULT_SERVICES = [
    {
        'title': 'Rask Utvikling',
        'description': 'Leverer prosjekter med lynets hastighet, uten å kompromisse med kvaliteten.'
    },
    {
        'title': 'Moderne Design', 
        'description': 'Estetisk tiltalende og brukervennlige grensesnitt som engasjerer dine besøkende.'
    },
    {
        'title': 'Skalerbare Løsninger',
        'description': 'Bygger plattformer som vokser med dine behov og fremtidige krav.'
    }
]

@app.route('/')
def index():
    """Hovedside med HTML generator interface"""
    return render_template('generator.html', themes=THEMES)

@app.route('/preview', methods=['POST'])
def preview():
    """Genererer forhåndsvisning av nettsiden (JSON API)"""
    try:
        data = request.get_json()
        theme_choice = data.get('theme_choice', 'landing_page_theme')
        theme = THEMES.get(theme_choice)
        # Sjekk om det er et HTML5 UP-tema
        if theme and theme.get('html5up'):
            folder = theme['folder']
            index_path = os.path.join(app.static_folder, 'themes', folder, 'index.html')
            if not os.path.exists(index_path):
                return jsonify({'success': False, 'error': 'Temaets index.html mangler!'}), 404
            with open(index_path, encoding='utf-8') as f:
                html_content = f.read()
            return jsonify({'success': True, 'html': html_content})
        
        # Hent brukerdata med fallback-verdier
        site_title = data.get('site_title', 'Min Nettside')
        site_description = data.get('site_description', 'Velkommen til min nettside')
        author_name = data.get('author_name', 'Nettside Eier')
        contact_email = data.get('contact_email', 'kontakt@nettside.no')
        primary_color = data.get('primary_color', '#4facfe')
        hero_heading = data.get('hero_heading', 'Velkommen til Fremtiden')
        hero_subheading = data.get('hero_subheading', 'Vi leverer innovative løsninger')
        
        # Bygge template data
        template_data = {
            'site_title': site_title,
            'site_logo_text': site_title,
            'site_description': site_description,
            'author_name': author_name,
            'contact_email': contact_email,
            'theme_choice': theme_choice,
            'primary_color': primary_color,
            'hero_heading': hero_heading,
            'hero_subheading': hero_subheading,
            'menu_items': DEFAULT_MENU_ITEMS,
            'services': DEFAULT_SERVICES,
            'current_year': datetime.now().year,
            'footer_text': f'© {datetime.now().year} {site_title}. Alle rettigheter reservert.'
        }
        
        # Render riktig template basert på tema
        if theme_choice == 'massively_blog_theme':
            html_content = render_template('massively_template.html', **template_data)
        elif theme_choice == 'modern_business_theme':
            html_content = render_template('business_template.html', **template_data)
        elif theme_choice == 'creative_portfolio_theme':
            html_content = render_template('portfolio_template.html', **template_data)
        else:  # landing_page_theme (default)
            html_content = render_template('landing_template.html', **template_data)
            
        return jsonify({'success': True, 'html': html_content})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    """Generer og last ned HTML-fil"""
    try:
        data = request.get_json()
        theme_choice = data.get('theme_choice', 'landing_page_theme')
        theme = THEMES.get(theme_choice)
        # Sjekk om det er et HTML5 UP-tema
        if theme and theme.get('html5up'):
            folder = theme['folder']
            index_path = os.path.join(app.static_folder, 'themes', folder, 'index.html')
            if not os.path.exists(index_path):
                return jsonify({'success': False, 'error': 'Temaets index.html mangler!'}), 404
            with open(index_path, encoding='utf-8') as f:
                html_content = f.read()
            filename = f"{theme['name'].lower().replace(' ', '-')}.html"
            output_dir = os.path.join(app.root_path, 'output')
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return send_from_directory(output_dir, filename, as_attachment=True)
        
        # Samme logikk som preview
        site_title = data.get('site_title', 'Min Nettside')
        site_description = data.get('site_description', 'Velkommen til min nettside')
        author_name = data.get('author_name', 'Nettside Eier')
        contact_email = data.get('contact_email', 'kontakt@nettside.no')
        primary_color = data.get('primary_color', '#4facfe')
        hero_heading = data.get('hero_heading', 'Velkommen til Fremtiden')
        hero_subheading = data.get('hero_subheading', 'Vi leverer innovative løsninger')
        
        template_data = {
            'site_title': site_title,
            'site_logo_text': site_title,
            'site_description': site_description,
            'author_name': author_name,
            'contact_email': contact_email,
            'theme_choice': theme_choice,
            'primary_color': primary_color,
            'hero_heading': hero_heading,
            'hero_subheading': hero_subheading,
            'menu_items': DEFAULT_MENU_ITEMS,
            'services': DEFAULT_SERVICES,
            'current_year': datetime.now().year,
            'footer_text': f'© {datetime.now().year} {site_title}. Alle rettigheter reservert.'
        }
        
        # Render riktig template
        if theme_choice == 'massively_blog_theme':
            html_content = render_template('massively_template.html', **template_data)
        elif theme_choice == 'modern_business_theme':
            html_content = render_template('business_template.html', **template_data)
        elif theme_choice == 'creative_portfolio_theme':
            html_content = render_template('portfolio_template.html', **template_data)
        else:
            html_content = render_template('landing_template.html', **template_data)
        
        # Lag fil og returner
        filename = site_title.lower().replace(' ', '-').replace('æ', 'ae').replace('ø', 'o').replace('å', 'a')
        filename = ''.join(c for c in filename if c.isalnum() or c == '-') + '.html'
        
        # Opprett output mappe hvis den ikke finnes
        output_dir = os.path.join(app.root_path, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Skriv til fil
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return send_from_directory(output_dir, filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/themes')
def get_themes():
    """API endpoint for å hente tilgjengelige temaer"""
    return jsonify(THEMES)

# Legacy routes for testing individual templates
@app.route('/landing')
def landing():
    """Test route for landing page template"""
    return render_template(
        'landing_template.html',
        site_title="Test Landing Page",
        site_description="Dette er en test av landing page template.",
        author_name="Test Forfatter",
        primary_color="#4facfe",
        site_logo_text="TestLogo",
        menu_items=DEFAULT_MENU_ITEMS,
        hero_heading="Velkommen til Test",
        hero_subheading="Dette er en test-underoverskrift",
        services=DEFAULT_SERVICES,
        contact_email="test@test.no",
        footer_text="© 2025 Test Landing Page. Alle rettigheter reservert.",
        current_year=datetime.now().year
    )

@app.route('/business')
def business():
    """Test route for business template"""
    return render_template(
        'business_template.html',
        site_title="Test Bedrift AS",
        site_description="Din partner for vekst og utvikling.",
        author_name="Test Forfatter",
        primary_color="#667eea",
        site_logo_text="TestBedrift",
        menu_items=DEFAULT_MENU_ITEMS,
        contact_email="kontakt@testbedrift.no",
        footer_text="© 2025 Test Bedrift AS. Alle rettigheter reservert.",
        current_year=datetime.now().year
    )

@app.route('/blog')
def blog():
    """Test route for blog template"""
    return render_template(
        'massively_template.html',
        site_title="Test Blog",
        site_description="En fantastisk test-blog",
        author_name="Test Blogger",
        primary_color="#212931",
        site_logo_text="TestBlog",
        menu_items=DEFAULT_MENU_ITEMS,
        contact_email="blog@test.no",
        footer_text="© 2025 Test Blog. Alle rettigheter reservert.",
        current_year=datetime.now().year
    )

@app.route('/portfolio')
def portfolio():
    """Test route for portfolio template"""
    return render_template(
        'portfolio_template.html',
        site_title="Test Portfolio",
        site_description="Kreativ showcase",
        author_name="Test Kunstner",
        primary_color="#ff6b6b",
        site_logo_text="TestPortfolio",
        menu_items=DEFAULT_MENU_ITEMS,
        contact_email="hei@testportfolio.no",
        footer_text="© 2025 Test Portfolio. Alle rettigheter reservert.",
        current_year=datetime.now().year
    )

# Legacy generate route (for compatibility)
@app.route('/generate', methods=['POST'])
def generate():
    """Legacy generate route - videresender til preview"""
    site_name = request.form.get('site_name', 'Mitt nettsted')
    menu_raw = request.form.get('menu_items', 'Hjem,Side 1,Side 2')
    pages_raw = request.form.get('pages', 'Hjem|Velkommen!\nSide 1|Dette er side 1.\nSide 2|Dette er side 2.')
    pages = [line.split('|') for line in pages_raw.splitlines() if '|' in line]
    menu = [item.strip() for item in menu_raw.split(',') if item.strip()]
    theme_choice = request.form.get('theme', 'landing_page_theme')

    # Hvis valgt tema er et HTML5 UP-tema, vis deres index.html direkte
    if theme_choice in ['multiverse', 'dimension']:
        theme_path = os.path.join(app.static_folder, 'themes', theme_choice)
        if not os.path.exists(os.path.join(theme_path, 'index.html')):
            abort(404)
        return send_from_directory(theme_path, 'index.html')

    # Ellers bruk generator
    return render_template(
        'generated.html',
        site_name=site_name,
        menu=menu,
        pages=pages,
        theme_choice=theme_choice
    )

# For å vise bilder, js, css fra temaene:
@app.route('/static/themes/<theme>/<path:filename>')
def theme_static(theme, filename):
    return send_from_directory(f'static/themes/{theme}', filename)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html') if os.path.exists('templates/404.html') else "404 - Side ikke funnet", 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html') if os.path.exists('templates/500.html') else "500 - Intern server feil", 500

if __name__ == '__main__':
    # Opprett nødvendige mapper
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    print("🚀 HTML Generator starter...")
    print("📂 Mapper opprettet: templates, static, output")
    print("🌐 Åpne http://localhost:5000 i nettleseren")
    print("🎨 Tilgjengelige temaer:", len(THEMES))
    
    app.run(debug=True, host='0.0.0.0', port=5000)