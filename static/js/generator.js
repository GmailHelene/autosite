// HTML Generator JavaScript
let currentTheme = 'landing_page_theme';
let generatedHTML = '';

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeGenerator();
});

function initializeGenerator() {
    // Set up theme selection
    setupThemeSelection();
    
    // Set up auto-update on input changes
    setupAutoUpdate();
    
    // Generate initial preview
    updatePreview();
}

function setupThemeSelection() {
    const themeCards = document.querySelectorAll('.theme-card');
    
    themeCards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove selected class from all cards
            themeCards.forEach(c => c.classList.remove('selected'));
            
            // Add selected class to clicked card
            this.classList.add('selected');
            
            // Update current theme
            currentTheme = this.getAttribute('data-theme');
            document.getElementById('selectedTheme').value = currentTheme;
            
            // Update color picker based on theme
            updateColorForTheme(currentTheme);
            
            // Update preview
            updatePreview();
        });
    });
}

function updateColorForTheme(theme) {
    const colorInput = document.getElementById('primaryColor');
    const themeColors = {
        'landing_page_theme': '#4facfe',
        'massively_blog_theme': '#212931',
        'modern_business_theme': '#667eea',
        'creative_portfolio_theme': '#ff6b6b'
    };
    
    if (themeColors[theme]) {
        colorInput.value = themeColors[theme];
    }
}

function setupAutoUpdate() {
    const inputs = [
        'siteTitle',
        'siteDescription', 
        'authorName',
        'contactEmail',
        'heroHeading',
        'heroSubheading',
        'primaryColor'
    ];
    
    inputs.forEach(inputId => {
        const element = document.getElementById(inputId);
        if (element) {
            if (element.type === 'color') {
                element.addEventListener('change', debounce(updatePreview, 500));
            } else {
                element.addEventListener('input', debounce(updatePreview, 1000));
            }
        }
    });
}

// Debounce function to prevent too many API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function updatePreview() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const previewFrame = document.getElementById('previewFrame');
    
    // Show loading spinner
    if (loadingSpinner) {
        loadingSpinner.style.display = 'block';
    }
    
    // Collect form data
    const formData = {
        site_title: getValue('siteTitle'),
        site_description: getValue('siteDescription'),
        author_name: getValue('authorName'),
        contact_email: getValue('contactEmail'),
        hero_heading: getValue('heroHeading'),
        hero_subheading: getValue('heroSubheading'),
        theme_choice: currentTheme,
        primary_color: getValue('primaryColor')
    };
    
    // Make API request to Flask backend
    fetch('/preview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner
        if (loadingSpinner) {
            loadingSpinner.style.display = 'none';
        }
        
        if (data.success) {
            // Store generated HTML
            generatedHTML = data.html;
            
            // Update preview frame
            const blob = new Blob([data.html], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            previewFrame.src = url;
            
            // Clean up old blob URL
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        } else {
            console.error('Preview generation failed:', data.error);
            showAlert('Kunne ikke generere forhåndsvisning: ' + data.error, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (loadingSpinner) {
            loadingSpinner.style.display = 'none';
        }
        showAlert('Nettverksfeil ved generering av forhåndsvisning', 'danger');
    });
}

function downloadHTML() {
    if (!generatedHTML) {
        showAlert('Generer først en forhåndsvisning før nedlasting', 'info');
        return;
    }
    
    const formData = {
        site_title: getValue('siteTitle'),
        site_description: getValue('siteDescription'),
        author_name: getValue('authorName'),
        contact_email: getValue('contactEmail'),
        hero_heading: getValue('heroHeading'),
        hero_subheading: getValue('heroSubheading'),
        theme_choice: currentTheme,
        primary_color: getValue('primaryColor')
    };
    
    // Create download link
    const title = getValue('siteTitle') || 'nettside';
    const filename = title.toLowerCase()
        .replace(/[æøå]/g, match => ({ 'æ': 'ae', 'ø': 'o', 'å': 'a' }[match]))
        .replace(/[^a-z0-9]/g, '-')
        .replace(/-+/g, '-') + '.html';
    
    const blob = new Blob([generatedHTML], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Clean up
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    
    showAlert('HTML-fil lastet ned: ' + filename, 'success');
}

function viewCode() {
    if (!generatedHTML) {
        showAlert('Generer først en forhåndsvisning før kodevisning', 'info');
        return;
    }
    
    const newWindow = window.open('', '_blank', 'width=1000,height=700');
    const safeHTML = generatedHTML.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    
    newWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Generert HTML-kode</title>
            <style>
                body {
                    font-family: 'Courier New', monospace;
                    margin: 0;
                    background: #1e1e1e;
                    color: #fff;
                }
                .header {
                    background: #333;
                    padding: 20px;
                    border-bottom: 3px solid #4facfe;
                    position: sticky;
                    top: 0;
                    z-index: 100;
                }
                .header h2 {
                    margin: 0 0 10px 0;
                    color: #4facfe;
                }
                .button-group {
                    display: flex;
                    gap: 10px;
                    margin-top: 15px;
                }
                button {
                    background: #4facfe;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: background 0.3s;
                }
                button:hover {
                    background: #3d8bfe;
                }
                .copy-btn {
                    background: #28a745;
                }
                .copy-btn:hover {
                    background: #218838;
                }
                pre {
                    background: #2d2d2d;
                    padding: 20px;
                    margin: 20px;
                    border-radius: 8px;
                    overflow-x: auto;
                    border-left: 4px solid #4facfe;
                    font-size: 14px;
                    line-height: 1.4;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
                .stats {
                    background: #495057;
                    padding: 15px 20px;
                    margin: 20px;
                    border-radius: 5px;
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 20px;
                }
                .stat {
                    text-align: center;
                }
                .stat-number {
                    font-size: 24px;
                    font-weight: bold;
                    color: #4facfe;
                }
                .stat-label {
                    font-size: 12px;
                    color: #ccc;
                    text-transform: uppercase;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📄 Generert HTML-kode</h2>
                <p>Tema: <strong>${getThemeName(currentTheme)}</strong></p>
                <div class="button-group">
                    <button class="copy-btn" onclick="copyCode()">📋 Kopier hele koden</button>
                    <button onclick="downloadCodeFile()">💾 Last ned som fil</button>
                    <button onclick="window.close()">❌ Lukk vindu</button>
                </div>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">${generatedHTML.length}</div>
                    <div class="stat-label">Tegn totalt</div>
                </div>
                <div class="stat">
                    <div class="stat-number">${generatedHTML.split('\\n').length}</div>
                    <div class="stat-label">Linjer</div>
                </div>
                <div class="stat">
                    <div class="stat-number">${Math.round(generatedHTML.length / 1024)}KB</div>
                    <div class="stat-label">Fil størrelse</div>
                </div>
                <div class="stat">
                    <div class="stat-number">${currentTheme}</div>
                    <div class="stat-label">Tema ID</div>
                </div>
            </div>
            
            <pre id="codeContent">${safeHTML}</pre>
            
            <script>
                function copyCode() {
                    const code = \`${generatedHTML.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`;
                    navigator.clipboard.writeText(code).then(() => {
                        alert('✅ Hele koden er kopiert til utklippstavlen!');
                    }).catch(err => {
                        alert('❌ Kunne ikke kopiere koden automatisk. Prøv å markere teksten og kopiere manuelt.');
                    });
                }
                
                function downloadCodeFile() {
                    const code = \`${generatedHTML.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`;
                    const blob = new Blob([code], { type: 'text/html;charset=utf-8' });
                    const url = URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = '${getValue('siteTitle').toLowerCase().replace(/[^a-z0-9]/g, '-')}.html';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    URL.revokeObjectURL(url);
                }
            </script>
        </body>
        </html>
    `);
}

function copyCode() {
    if (!generatedHTML) {
        showAlert('Generer først en forhåndsvisning før kopiering', 'info');
        return;
    }
    
    navigator.clipboard.writeText(generatedHTML).then(() => {
        showAlert('HTML-koden er kopiert til utklippstavlen!', 'success');
    }).catch(err => {
        console.error('Kunne ikke kopiere:', err);
        showAlert('Kunne ikke kopiere koden automatisk', 'danger');
    });
}

function getValue(elementId) {
    const element = document.getElementById(elementId);
    return element ? element.value : '';
}

function getThemeName(themeId) {
    const themeNames = {
        'landing_page_theme': 'Landing Page',
        'massively_blog_theme': 'Massively Blog',
        'modern_business_theme': 'Moderne Business',
        'creative_portfolio_theme': 'Kreativ Portfolio'
    };
    return themeNames[themeId] || themeId;
}

function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    // Insert at top of form section
    const formSection = document.querySelector('.form-section');
    if (formSection) {
        formSection.insertBefore(alert, formSection.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

// Export functions for global access
window.updatePreview = updatePreview;
window.downloadHTML = downloadHTML;
window.viewCode = viewCode;
window.copyCode = copyCode;