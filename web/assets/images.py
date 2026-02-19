"""
Forkast Visual Assets
SVG images and icons encoded for Streamlit rendering
"""
import base64

# --- Forkast Logo SVG ---
LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100">
  <defs>
    <linearGradient id="brandGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FF6B35"/>
      <stop offset="100%" style="stop-color:#F7931E"/>
    </linearGradient>
  </defs>
  <circle cx="45" cy="50" r="38" fill="url(#brandGrad)"/>
  <path d="M30 35 L30 65 M30 35 L55 35 M30 48 L50 48" stroke="white" stroke-width="5" stroke-linecap="round" fill="none"/>
  <circle cx="52" cy="58" r="4" fill="white"/>
  <text x="100" y="62" font-family="Arial,sans-serif" font-size="38" font-weight="bold" fill="#2D3436">fork</text>
  <text x="215" y="62" font-family="Arial,sans-serif" font-size="38" font-weight="bold" fill="#FF6B35">ast</text>
  <text x="100" y="82" font-family="Arial,sans-serif" font-size="12" fill="#636e72" letter-spacing="3">PREDICTION-FIRST AI</text>
</svg>'''

# --- Sidebar Logo (compact) ---
SIDEBAR_LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 55">
  <defs>
    <linearGradient id="sGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FF6B35"/>
      <stop offset="100%" style="stop-color:#F7931E"/>
    </linearGradient>
  </defs>
  <circle cx="24" cy="27" r="21" fill="url(#sGrad)"/>
  <path d="M16 18 L16 36 M16 18 L30 18 M16 26 L28 26" stroke="white" stroke-width="3" stroke-linecap="round" fill="none"/>
  <circle cx="28" cy="32" r="2.5" fill="white"/>
  <text x="54" y="34" font-family="Arial,sans-serif" font-size="22" font-weight="bold" fill="#2D3436">fork</text>
  <text x="120" y="34" font-family="Arial,sans-serif" font-size="22" font-weight="bold" fill="#FF6B35">ast</text>
  <text x="54" y="48" font-family="Arial,sans-serif" font-size="8" fill="#636e72" letter-spacing="2">AI RESTAURANT PLATFORM</text>
</svg>'''

# --- Dashboard Hero Banner ---
HERO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 220">
  <defs>
    <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35"/>
      <stop offset="50%" style="stop-color:#F7931E"/>
      <stop offset="100%" style="stop-color:#FF6B35"/>
    </linearGradient>
    <linearGradient id="heroOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:rgba(0,0,0,0)"/>
      <stop offset="100%" style="stop-color:rgba(0,0,0,0.15)"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="220" rx="16" fill="url(#heroBg)"/>
  <rect width="1200" height="220" rx="16" fill="url(#heroOverlay)"/>
  <!-- Decorative circles -->
  <circle cx="1050" cy="40" r="80" fill="rgba(255,255,255,0.08)"/>
  <circle cx="1100" cy="160" r="120" fill="rgba(255,255,255,0.05)"/>
  <circle cx="150" cy="180" r="60" fill="rgba(255,255,255,0.06)"/>
  <!-- Fork icon -->
  <g transform="translate(80,55)">
    <circle cx="50" cy="50" r="45" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <path d="M35 30 L35 70 M35 30 L60 30 M35 45 L55 45" stroke="white" stroke-width="4" stroke-linecap="round" fill="none"/>
    <circle cx="57" cy="58" r="4" fill="white"/>
  </g>
  <!-- Text -->
  <text x="200" y="85" font-family="Arial,sans-serif" font-size="36" font-weight="bold" fill="white">Welcome to Forkast</text>
  <text x="200" y="120" font-family="Arial,sans-serif" font-size="16" fill="rgba(255,255,255,0.9)">Prediction-first AI platform for MENA restaurants</text>
  <text x="200" y="150" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.7)">Forecast demand  |  Reduce waste  |  Optimize operations  |  Grow revenue</text>
</svg>'''

# --- KPI Card backgrounds ---
def kpi_card_svg(icon_path, color="#FF6B35"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60">
  <rect width="60" height="60" rx="12" fill="{color}" opacity="0.12"/>
  <g transform="translate(15,15)" fill="{color}">{icon_path}</g>
</svg>'''

ICON_COVERS = '<path d="M15 3C15 3 22 10 22 17C22 21.4 18.4 25 14 25C9.6 25 6 21.4 6 17C6 10 15 3 15 3Z"/>'
ICON_REVENUE = '<path d="M12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z"/>'
ICON_WASTE = '<path d="M3 6H21M19 6V20C19 21 18 22 17 22H7C6 22 5 21 5 20V6M8 6V4C8 3 9 2 10 2H14C15 2 16 3 16 4V6"/>'
ICON_FORECAST = '<path d="M3 17L9 11L13 15L21 7M21 7H15M21 7V13"/>'
ICON_HEALTH = '<path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z"/>'

# --- Section Header SVGs ---
def section_header_svg(title, subtitle, color="#FF6B35"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 60">
  <rect x="0" y="0" width="6" height="60" rx="3" fill="{color}"/>
  <text x="20" y="28" font-family="Arial,sans-serif" font-size="20" font-weight="bold" fill="#2D3436">{title}</text>
  <text x="20" y="48" font-family="Arial,sans-serif" font-size="12" fill="#636e72">{subtitle}</text>
</svg>'''

# --- Food category icons ---
CATEGORY_ICONS = {
    "appetizer": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#FFF3E0"/><text x="20" y="26" text-anchor="middle" font-size="18">🥗</text></svg>''',
    "main": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#FFF3E0"/><text x="20" y="26" text-anchor="middle" font-size="18">🍖</text></svg>''',
    "dessert": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#FFF3E0"/><text x="20" y="26" text-anchor="middle" font-size="18">🍮</text></svg>''',
    "beverage": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#FFF3E0"/><text x="20" y="26" text-anchor="middle" font-size="18">🍹</text></svg>''',
}

# --- Forecast confidence visual ---
FORECAST_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="fhBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#fhBg)"/>
  <!-- Chart line decoration -->
  <polyline points="50,80 150,60 250,70 350,40 450,50 550,30 650,45 750,25 850,35 950,20 1050,30 1150,15" stroke="#FF6B35" stroke-width="3" fill="none" opacity="0.6"/>
  <polyline points="50,85 150,70 250,78 350,55 450,62 550,48 650,58 750,42 850,50 950,38 1050,45 1150,30" stroke="#F7931E" stroke-width="2" fill="none" opacity="0.3"/>
  <!-- Dots -->
  <circle cx="350" cy="40" r="4" fill="#FF6B35"/>
  <circle cx="750" cy="25" r="4" fill="#FF6B35"/>
  <circle cx="1050" cy="30" r="4" fill="#FF6B35"/>
  <text x="60" y="40" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Demand Forecast</text>
  <text x="60" y="60" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">AI-powered predictions with confidence intervals</text>
</svg>'''

# --- Inventory health gauge ---
def health_gauge_svg(score):
    color = "#28a745" if score >= 75 else "#ffc107" if score >= 50 else "#dc3545"
    angle = (score / 100) * 180
    import math
    end_x = 50 + 35 * math.cos(math.radians(180 - angle))
    end_y = 55 - 35 * math.sin(math.radians(180 - angle))
    large_arc = 1 if angle > 180 else 0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 65">
  <path d="M15 55 A35 35 0 0 1 85 55" fill="none" stroke="#e9ecef" stroke-width="8" stroke-linecap="round"/>
  <path d="M15 55 A35 35 0 {large_arc} 1 {end_x:.1f} {end_y:.1f}" fill="none" stroke="{color}" stroke-width="8" stroke-linecap="round"/>
  <text x="50" y="52" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="{color}">{score}</text>
  <text x="50" y="63" text-anchor="middle" font-family="Arial,sans-serif" font-size="7" fill="#636e72">HEALTH</text>
</svg>'''

# --- Supplier performance badge ---
def supplier_badge_svg(name, score, tier):
    color = "#28a745" if score >= 90 else "#ffc107" if score >= 80 else "#dc3545"
    tier_color = {"premium": "#FFD700", "standard": "#C0C0C0", "economy": "#CD7F32"}.get(tier, "#C0C0C0")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 80">
  <rect width="200" height="80" rx="10" fill="#f8f9fa" stroke="#dee2e6"/>
  <circle cx="35" cy="40" r="22" fill="{color}" opacity="0.15"/>
  <text x="35" y="46" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" font-weight="bold" fill="{color}">{score}%</text>
  <text x="70" y="30" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="#2D3436">{name}</text>
  <rect x="70" y="38" width="50" height="16" rx="8" fill="{tier_color}" opacity="0.3"/>
  <text x="95" y="50" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#2D3436">{tier.upper()}</text>
  <text x="70" y="72" font-family="Arial,sans-serif" font-size="9" fill="#636e72">Reliability Score</text>
</svg>'''

# --- Alert severity banners ---
ALERT_BANNERS = {
    "critical": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#dc3545" opacity="0.12"/><text x="20" y="27" text-anchor="middle" font-size="20">🚨</text></svg>''',
    "high": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#ffc107" opacity="0.15"/><text x="20" y="27" text-anchor="middle" font-size="20">⚠️</text></svg>''',
    "medium": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#17a2b8" opacity="0.12"/><text x="20" y="27" text-anchor="middle" font-size="20">ℹ️</text></svg>''',
    "low": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#28a745" opacity="0.12"/><text x="20" y="27" text-anchor="middle" font-size="20">✅</text></svg>''',
}

# --- Growth phase illustrations ---
GROWTH_PILOT_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80">
  <rect width="120" height="80" rx="10" fill="#FFF3E0"/>
  <text x="60" y="35" text-anchor="middle" font-size="28">🚀</text>
  <text x="60" y="55" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#FF6B35">PILOT</text>
  <text x="60" y="68" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="#636e72">5-20 kitchens</text>
</svg>'''

GROWTH_SCALE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80">
  <rect width="120" height="80" rx="10" fill="#E8F5E9"/>
  <text x="60" y="35" text-anchor="middle" font-size="28">📈</text>
  <text x="60" y="55" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#28a745">SCALE</text>
  <text x="60" y="68" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="#636e72">50-150 kitchens</text>
</svg>'''

GROWTH_NETWORK_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80">
  <rect width="120" height="80" rx="10" fill="#E3F2FD"/>
  <text x="60" y="35" text-anchor="middle" font-size="28">🌐</text>
  <text x="60" y="55" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#1565C0">NETWORK</text>
  <text x="60" y="68" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="#636e72">300+ kitchens</text>
</svg>'''


# --- Page-specific header SVGs ---
INVENTORY_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="invBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#invBg)"/>
  <rect x="50" y="35" width="40" height="50" rx="4" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <rect x="100" y="25" width="40" height="60" rx="4" fill="none" stroke="rgba(255,107,53,0.5)" stroke-width="2"/>
  <rect x="150" y="45" width="40" height="40" rx="4" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <circle cx="1050" cy="60" r="40" fill="rgba(255,107,53,0.08)"/>
  <circle cx="1100" cy="30" r="25" fill="rgba(255,255,255,0.04)"/>
  <text x="220" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Inventory Management</text>
  <text x="220" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">AI-optimized stock tracking and waste reduction</text>
</svg>'''

PROCUREMENT_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="procBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#procBg)"/>
  <path d="M60 30 L90 30 L100 45 L100 85 L50 85 L50 45 Z" fill="none" stroke="rgba(255,107,53,0.5)" stroke-width="2"/>
  <circle cx="75" cy="30" r="3" fill="#FF6B35"/>
  <line x1="120" y1="50" x2="180" y2="50" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <line x1="120" y1="65" x2="160" y2="65" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <line x1="120" y1="80" x2="170" y2="80" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
  <circle cx="1080" cy="60" r="45" fill="rgba(255,107,53,0.06)"/>
  <text x="220" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Smart Procurement</text>
  <text x="220" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">AI-generated POs with human-in-the-loop approval</text>
</svg>'''

MENU_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="menuBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#menuBg)"/>
  <circle cx="75" cy="55" r="30" fill="none" stroke="rgba(255,107,53,0.4)" stroke-width="2"/>
  <path d="M65 45 L65 65 M65 45 L80 45 M65 53 L77 53" stroke="rgba(255,255,255,0.5)" stroke-width="2" stroke-linecap="round" fill="none"/>
  <circle cx="130" cy="40" r="8" fill="rgba(255,107,53,0.15)"/>
  <circle cx="155" cy="70" r="12" fill="rgba(255,255,255,0.04)"/>
  <circle cx="1060" cy="55" r="35" fill="rgba(255,107,53,0.07)"/>
  <text x="200" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Menu Optimization</text>
  <text x="200" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Engineering matrix, profitability analysis, and AI recommendations</text>
</svg>'''

LABOR_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="labBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#labBg)"/>
  <circle cx="65" cy="45" r="12" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <circle cx="90" cy="45" r="12" fill="none" stroke="rgba(255,107,53,0.4)" stroke-width="2"/>
  <circle cx="115" cy="45" r="12" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <rect x="45" y="65" width="90" height="20" rx="4" fill="rgba(255,107,53,0.12)"/>
  <circle cx="1070" cy="50" r="30" fill="rgba(255,255,255,0.04)"/>
  <text x="200" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Labor Scheduling</text>
  <text x="200" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Demand-aligned staffing with cost optimization</text>
</svg>'''

SUPPLIERS_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="supBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#supBg)"/>
  <rect x="50" y="30" width="50" height="60" rx="6" fill="none" stroke="rgba(255,107,53,0.4)" stroke-width="2"/>
  <line x1="100" y1="60" x2="140" y2="60" stroke="rgba(255,255,255,0.3)" stroke-width="2" stroke-dasharray="4"/>
  <rect x="140" y="35" width="40" height="50" rx="6" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
  <circle cx="1050" cy="55" r="35" fill="rgba(255,107,53,0.06)"/>
  <text x="220" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Supplier Management</text>
  <text x="220" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Performance monitoring, reliability metrics, and vendor relationships</text>
</svg>'''

ANALYTICS_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="anaBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#anaBg)"/>
  <polyline points="50,85 80,60 110,70 140,40 170,50 200,25" stroke="#FF6B35" stroke-width="3" fill="none" opacity="0.6"/>
  <circle cx="140" cy="40" r="4" fill="#FF6B35"/>
  <circle cx="200" cy="25" r="4" fill="#FF6B35"/>
  <rect x="50" y="88" width="160" height="3" rx="1.5" fill="rgba(255,255,255,0.1)"/>
  <circle cx="1060" cy="55" r="40" fill="rgba(255,107,53,0.06)"/>
  <text x="240" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Analytics &amp; Growth</text>
  <text x="240" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Operations, financial health, and growth trajectory</text>
</svg>'''

ALERTS_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="altBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#altBg)"/>
  <path d="M75 35 L95 75 L55 75 Z" fill="none" stroke="rgba(255,107,53,0.5)" stroke-width="2.5" stroke-linejoin="round"/>
  <line x1="75" y1="50" x2="75" y2="62" stroke="rgba(255,255,255,0.5)" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="75" cy="69" r="2" fill="rgba(255,255,255,0.5)"/>
  <circle cx="130" cy="50" r="6" fill="rgba(255,107,53,0.15)"/>
  <circle cx="150" cy="75" r="4" fill="rgba(255,255,255,0.06)"/>
  <circle cx="1070" cy="55" r="35" fill="rgba(255,107,53,0.06)"/>
  <text x="200" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Operational Alerts</text>
  <text x="200" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">AI-generated alerts with priority levels and recommended actions</text>
</svg>'''

SETTINGS_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="setBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#setBg)"/>
  <circle cx="75" cy="55" r="25" fill="none" stroke="rgba(255,107,53,0.4)" stroke-width="2"/>
  <circle cx="75" cy="55" r="10" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <line x1="75" y1="25" x2="75" y2="35" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <line x1="75" y1="75" x2="75" y2="85" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <line x1="45" y1="55" x2="55" y2="55" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <line x1="95" y1="55" x2="105" y2="55" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <circle cx="1070" cy="55" r="30" fill="rgba(255,107,53,0.06)"/>
  <text x="200" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Settings</text>
  <text x="200" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Platform configuration and restaurant profile</text>
</svg>'''


# --- Registration Page Headers ---
REGISTER_RESTAURANT_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="regRestBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#regRestBg)"/>
  <!-- Building icon -->
  <rect x="55" y="30" width="40" height="55" rx="4" fill="none" stroke="rgba(255,107,53,0.5)" stroke-width="2"/>
  <rect x="62" y="38" width="8" height="8" rx="1" fill="rgba(255,255,255,0.3)"/>
  <rect x="80" y="38" width="8" height="8" rx="1" fill="rgba(255,255,255,0.3)"/>
  <rect x="62" y="54" width="8" height="8" rx="1" fill="rgba(255,255,255,0.3)"/>
  <rect x="80" y="54" width="8" height="8" rx="1" fill="rgba(255,255,255,0.3)"/>
  <rect x="70" y="70" width="10" height="15" rx="1" fill="rgba(255,107,53,0.4)"/>
  <circle cx="1070" cy="55" r="30" fill="rgba(255,107,53,0.06)"/>
  <circle cx="1130" cy="30" r="15" fill="rgba(255,107,53,0.04)"/>
  <text x="200" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Register Restaurant</text>
  <text x="200" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Onboard your restaurant to the Forkast AI platform</text>
</svg>'''

REGISTER_SUPPLIER_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="regSupBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#regSupBg)"/>
  <!-- Connection / supply chain icon -->
  <circle cx="55" cy="55" r="12" fill="none" stroke="rgba(255,107,53,0.5)" stroke-width="2"/>
  <circle cx="95" cy="40" r="10" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <circle cx="95" cy="72" r="10" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <line x1="67" y1="50" x2="85" y2="43" stroke="rgba(255,107,53,0.4)" stroke-width="1.5"/>
  <line x1="67" y1="60" x2="85" y2="68" stroke="rgba(255,107,53,0.4)" stroke-width="1.5"/>
  <circle cx="55" cy="55" r="4" fill="rgba(255,107,53,0.6)"/>
  <circle cx="1070" cy="55" r="30" fill="rgba(255,107,53,0.06)"/>
  <circle cx="1130" cy="30" r="15" fill="rgba(255,107,53,0.04)"/>
  <text x="200" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Register Supplier</text>
  <text x="200" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Join the Forkast supplier network for MENA restaurants</text>
</svg>'''

PAYMENT_GATEWAY_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="payBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#payBg)"/>
  <rect x="50" y="30" width="70" height="50" rx="8" fill="none" stroke="rgba(255,107,53,0.5)" stroke-width="2"/>
  <line x1="50" y1="50" x2="120" y2="50" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <rect x="60" y="60" width="25" height="10" rx="3" fill="rgba(255,107,53,0.4)"/>
  <circle cx="110" cy="67" r="4" fill="rgba(255,255,255,0.2)"/>
  <circle cx="1070" cy="55" r="35" fill="rgba(255,107,53,0.06)"/>
  <text x="200" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">Payment Gateway</text>
  <text x="200" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Stripe-powered payments for procurement and supplier transactions</text>
</svg>'''

LOYALTY_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="loyBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="50%" style="stop-color:#16213e"/>
      <stop offset="100%" style="stop-color:#0f3460"/>
    </linearGradient>
    <linearGradient id="loyGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F7931E"/>
      <stop offset="100%" style="stop-color:#FFD700"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="16" fill="url(#loyBg)"/>
  <!-- Decorative -->
  <circle cx="1100" cy="20" r="80" fill="rgba(247,147,30,0.06)"/>
  <circle cx="1050" cy="80" r="50" fill="rgba(255,215,0,0.04)"/>
  <!-- Shield/badge icon -->
  <circle cx="75" cy="55" r="32" fill="url(#loyGold)" opacity="0.15"/>
  <path d="M60 40 L75 32 L90 40 L90 65 C90 72 82 78 75 80 C68 78 60 72 60 65 Z" fill="none" stroke="url(#loyGold)" stroke-width="2.5"/>
  <text x="75" y="62" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" font-weight="bold" fill="#FFD700">&#9733;</text>
  <!-- Text -->
  <text x="125" y="52" font-family="Arial,sans-serif" font-size="26" font-weight="bold" fill="white">Loyalty Program</text>
  <text x="125" y="76" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Earn tier rewards with suppliers through consistent ordering</text>
  <!-- Tier badges -->
  <rect x="680" y="25" width="80" height="28" rx="14" fill="rgba(205,127,50,0.3)" stroke="rgba(205,127,50,0.6)" stroke-width="1"/>
  <text x="720" y="44" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#CD7F32">Bronze</text>
  <rect x="775" y="25" width="75" height="28" rx="14" fill="rgba(192,192,192,0.3)" stroke="rgba(192,192,192,0.6)" stroke-width="1"/>
  <text x="812" y="44" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#C0C0C0">Silver</text>
  <rect x="865" y="25" width="65" height="28" rx="14" fill="rgba(255,215,0,0.3)" stroke="rgba(255,215,0,0.6)" stroke-width="1"/>
  <text x="897" y="44" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#FFD700">Gold</text>
  <rect x="945" y="25" width="90" height="28" rx="14" fill="rgba(229,228,226,0.3)" stroke="rgba(229,228,226,0.6)" stroke-width="1"/>
  <text x="990" y="44" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#E5E4E2">Platinum</text>
  <!-- Fee reduction arrow -->
  <text x="750" y="80" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.4)">15% fee</text>
  <line x1="800" y1="77" x2="900" y2="77" stroke="rgba(40,167,69,0.5)" stroke-width="1.5" stroke-dasharray="4,3"/>
  <polygon points="900,73 910,77 900,81" fill="rgba(40,167,69,0.5)"/>
  <text x="920" y="80" font-family="Arial,sans-serif" font-size="10" fill="#28a745" font-weight="bold">8% fee</text>
</svg>'''

REVENUE_MODEL_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="revBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="50%" style="stop-color:#16213e"/>
      <stop offset="100%" style="stop-color:#0f3460"/>
    </linearGradient>
    <linearGradient id="revAccent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35"/>
      <stop offset="100%" style="stop-color:#F7931E"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="16" fill="url(#revBg)"/>
  <!-- Decorative circles -->
  <circle cx="1100" cy="20" r="80" fill="rgba(255,107,53,0.06)"/>
  <circle cx="1050" cy="80" r="50" fill="rgba(247,147,30,0.05)"/>
  <!-- Revenue icon: stacked coins -->
  <circle cx="75" cy="55" r="32" fill="url(#revAccent)" opacity="0.15"/>
  <ellipse cx="75" cy="65" rx="18" ry="6" fill="none" stroke="#FF6B35" stroke-width="2.5"/>
  <ellipse cx="75" cy="57" rx="18" ry="6" fill="none" stroke="#FF6B35" stroke-width="2.5"/>
  <ellipse cx="75" cy="49" rx="18" ry="6" fill="none" stroke="#F7931E" stroke-width="2.5"/>
  <ellipse cx="75" cy="41" rx="18" ry="6" fill="none" stroke="#F7931E" stroke-width="2.5"/>
  <line x1="57" y1="41" x2="57" y2="65" stroke="#FF6B35" stroke-width="2.5"/>
  <line x1="93" y1="41" x2="93" y2="65" stroke="#FF6B35" stroke-width="2.5"/>
  <!-- Text -->
  <text x="125" y="52" font-family="Arial,sans-serif" font-size="26" font-weight="bold" fill="white">Revenue Model</text>
  <text x="125" y="76" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">Platform revenue from supplier-restaurant transaction fees</text>
  <!-- 15% badge -->
  <rect x="1020" y="35" width="100" height="50" rx="25" fill="url(#revAccent)"/>
  <text x="1070" y="66" text-anchor="middle" font-family="Arial,sans-serif" font-size="20" font-weight="bold" fill="white">15%</text>
  <!-- Flow arrows -->
  <text x="430" y="55" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.4)">SUPPLIER</text>
  <line x1="500" y1="52" x2="550" y2="52" stroke="rgba(255,107,53,0.4)" stroke-width="2" stroke-dasharray="4,4"/>
  <polygon points="550,47 560,52 550,57" fill="rgba(255,107,53,0.4)"/>
  <text x="570" y="55" font-family="Arial,sans-serif" font-size="11" fill="#FF6B35" font-weight="bold">FORKAST</text>
  <line x1="640" y1="52" x2="690" y2="52" stroke="rgba(255,107,53,0.4)" stroke-width="2" stroke-dasharray="4,4"/>
  <polygon points="690,47 700,52 690,57" fill="rgba(255,107,53,0.4)"/>
  <text x="710" y="55" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.4)">RESTAURANT</text>
  <text x="520" y="78" font-family="Arial,sans-serif" font-size="9" fill="rgba(255,255,255,0.3)">85% payout</text>
  <text x="650" y="78" font-family="Arial,sans-serif" font-size="9" fill="rgba(255,255,255,0.3)">115% charged</text>
</svg>'''

API_MANAGEMENT_HEADER_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120">
  <defs>
    <linearGradient id="apiBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="120" rx="12" fill="url(#apiBg)"/>
  <circle cx="65" cy="45" r="15" fill="none" stroke="rgba(255,107,53,0.5)" stroke-width="2"/>
  <circle cx="65" cy="45" r="5" fill="rgba(255,107,53,0.6)"/>
  <line x1="80" y1="45" x2="110" y2="35" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <line x1="80" y1="45" x2="110" y2="55" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <line x1="80" y1="45" x2="110" y2="75" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <circle cx="115" cy="35" r="6" fill="rgba(255,255,255,0.15)"/>
  <circle cx="115" cy="55" r="6" fill="rgba(255,255,255,0.15)"/>
  <circle cx="115" cy="75" r="6" fill="rgba(255,255,255,0.1)"/>
  <circle cx="1070" cy="55" r="35" fill="rgba(255,107,53,0.06)"/>
  <text x="200" y="50" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="white">API Management</text>
  <text x="200" y="75" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.6)">POS integration, API keys, and endpoint documentation</text>
</svg>'''


# --- Decorative separator SVG ---
def decorative_divider_svg(color="#FF6B35"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 20">
  <line x1="0" y1="10" x2="350" y2="10" stroke="{color}" stroke-width="1" opacity="0.3"/>
  <circle cx="370" cy="10" r="4" fill="{color}" opacity="0.4"/>
  <circle cx="400" cy="10" r="6" fill="{color}" opacity="0.6"/>
  <circle cx="430" cy="10" r="4" fill="{color}" opacity="0.4"/>
  <line x1="450" y1="10" x2="800" y2="10" stroke="{color}" stroke-width="1" opacity="0.3"/>
</svg>'''


# --- Stat card with icon SVG ---
def stat_card_svg(icon, value, label, color="#FF6B35"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 90">
  <rect width="200" height="90" rx="12" fill="white" stroke="#f0f0f0"/>
  <rect x="12" y="12" width="40" height="40" rx="10" fill="{color}" opacity="0.12"/>
  <text x="32" y="38" text-anchor="middle" font-size="20">{icon}</text>
  <text x="65" y="32" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="#2D3436">{value}</text>
  <text x="65" y="50" font-family="Arial,sans-serif" font-size="9" fill="#636e72" text-transform="uppercase">{label}</text>
</svg>'''


# --- Platform Architecture Hub-and-Spoke Diagram ---
PLATFORM_ARCHITECTURE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500">
  <defs>
    <linearGradient id="archBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f8f9fa"/>
      <stop offset="100%" style="stop-color:#e9ecef"/>
    </linearGradient>
    <linearGradient id="centerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35"/>
      <stop offset="100%" style="stop-color:#F7931E"/>
    </linearGradient>
    <linearGradient id="nodeGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
    <filter id="archShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="rgba(0,0,0,0.1)"/>
    </filter>
    <filter id="nodeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="rgba(0,0,0,0.12)"/>
    </filter>
  </defs>
  <rect width="900" height="500" rx="16" fill="url(#archBg)"/>
  <text x="450" y="40" text-anchor="middle" font-family="Arial,sans-serif" font-size="22" font-weight="bold" fill="#2D3436">Forkast Platform Architecture &amp; Network Effects</text>

  <!-- Connection lines (behind nodes) -->
  <line x1="450" y1="250" x2="200" y2="130" stroke="#FF6B35" stroke-width="2.5" opacity="0.4" stroke-dasharray="8,4"/>
  <line x1="450" y1="250" x2="700" y2="130" stroke="#FF6B35" stroke-width="2.5" opacity="0.4" stroke-dasharray="8,4"/>
  <line x1="450" y1="250" x2="200" y2="380" stroke="#FF6B35" stroke-width="2.5" opacity="0.4" stroke-dasharray="8,4"/>
  <line x1="450" y1="250" x2="700" y2="380" stroke="#FF6B35" stroke-width="2.5" opacity="0.4" stroke-dasharray="8,4"/>
  <line x1="450" y1="250" x2="100" y2="250" stroke="#FF6B35" stroke-width="2.5" opacity="0.4" stroke-dasharray="8,4"/>
  <line x1="450" y1="250" x2="800" y2="250" stroke="#FF6B35" stroke-width="2.5" opacity="0.4" stroke-dasharray="8,4"/>

  <!-- Animated pulse circles on connections -->
  <circle cx="325" cy="190" r="5" fill="#FF6B35" opacity="0.6"/>
  <circle cx="575" cy="190" r="5" fill="#FF6B35" opacity="0.6"/>
  <circle cx="325" cy="315" r="5" fill="#FF6B35" opacity="0.6"/>
  <circle cx="575" cy="315" r="5" fill="#FF6B35" opacity="0.6"/>
  <circle cx="275" cy="250" r="5" fill="#FF6B35" opacity="0.6"/>
  <circle cx="625" cy="250" r="5" fill="#FF6B35" opacity="0.6"/>

  <!-- Center hub - Forkast Platform -->
  <circle cx="450" cy="250" r="80" fill="url(#centerGrad)" filter="url(#archShadow)"/>
  <circle cx="450" cy="250" r="75" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
  <text x="450" y="235" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="bold" fill="white">Forkast</text>
  <text x="450" y="255" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="bold" fill="white">Platform</text>
  <text x="450" y="275" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="rgba(255,255,255,0.8)">AI Engine</text>

  <!-- Node: Restaurants (top-left) -->
  <g filter="url(#nodeShadow)">
    <circle cx="200" cy="130" r="55" fill="url(#nodeGrad1)"/>
    <text x="200" y="120" text-anchor="middle" font-size="24">🏪</text>
    <text x="200" y="145" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Restaurants</text>
    <text x="200" y="160" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="rgba(255,255,255,0.6)">Core Users</text>
  </g>

  <!-- Node: Suppliers (top-right) -->
  <g filter="url(#nodeShadow)">
    <circle cx="700" cy="130" r="55" fill="url(#nodeGrad1)"/>
    <text x="700" y="120" text-anchor="middle" font-size="24">🏭</text>
    <text x="700" y="145" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Suppliers</text>
    <text x="700" y="160" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="rgba(255,255,255,0.6)">Demand Visibility</text>
  </g>

  <!-- Node: Forecasting (left) -->
  <g filter="url(#nodeShadow)">
    <circle cx="100" cy="250" r="50" fill="white" stroke="#FF6B35" stroke-width="2"/>
    <text x="100" y="240" text-anchor="middle" font-size="22">📈</text>
    <text x="100" y="260" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="bold" fill="#2D3436">Forecasting</text>
    <text x="100" y="274" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="#636e72">Demand AI</text>
  </g>

  <!-- Node: Analytics (right) -->
  <g filter="url(#nodeShadow)">
    <circle cx="800" cy="250" r="50" fill="white" stroke="#FF6B35" stroke-width="2"/>
    <text x="800" y="240" text-anchor="middle" font-size="22">📊</text>
    <text x="800" y="260" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="bold" fill="#2D3436">Analytics</text>
    <text x="800" y="274" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="#636e72">Growth Metrics</text>
  </g>

  <!-- Node: Inventory (bottom-left) -->
  <g filter="url(#nodeShadow)">
    <circle cx="200" cy="380" r="55" fill="url(#nodeGrad1)"/>
    <text x="200" y="370" text-anchor="middle" font-size="24">📦</text>
    <text x="200" y="395" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Inventory</text>
    <text x="200" y="410" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="rgba(255,255,255,0.6)">Stock Optimizer</text>
  </g>

  <!-- Node: Operations (bottom-right) -->
  <g filter="url(#nodeShadow)">
    <circle cx="700" cy="380" r="55" fill="url(#nodeGrad1)"/>
    <text x="700" y="370" text-anchor="middle" font-size="24">👥</text>
    <text x="700" y="395" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Operations</text>
    <text x="700" y="410" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" fill="rgba(255,255,255,0.6)">Labor &amp; Menu</text>
  </g>

  <!-- Network Effects box -->
  <rect x="30" y="440" width="840" height="48" rx="10" fill="white" stroke="#e9ecef" stroke-width="1" filter="url(#nodeShadow)"/>
  <rect x="30" y="440" width="6" height="48" rx="3" fill="#FF6B35"/>
  <text x="55" y="460" font-family="Arial,sans-serif" font-size="12" font-weight="bold" fill="#2D3436">Network Effects:</text>
  <text x="55" y="478" font-family="Arial,sans-serif" font-size="10" fill="#636e72">+150K Restaurants  |  +10K Suppliers  |  +150K Enterprise Customers  |  AI Improves With Scale</text>
</svg>'''


# --- Layered Data Flow Architecture Diagram ---
DATA_FLOW_ARCHITECTURE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 460">
  <defs>
    <linearGradient id="dfBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#f8f9fa"/>
      <stop offset="100%" style="stop-color:#e9ecef"/>
    </linearGradient>
    <linearGradient id="layerOrange" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FF6B35"/>
      <stop offset="100%" style="stop-color:#F7931E"/>
    </linearGradient>
    <linearGradient id="layerDark" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
    <linearGradient id="layerGreen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#28a745"/>
      <stop offset="100%" style="stop-color:#20c997"/>
    </linearGradient>
    <linearGradient id="layerBlue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1565C0"/>
      <stop offset="100%" style="stop-color:#42a5f5"/>
    </linearGradient>
    <filter id="dfShadow" x="-5%" y="-5%" width="110%" height="120%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="rgba(0,0,0,0.1)"/>
    </filter>
  </defs>
  <rect width="900" height="460" rx="16" fill="url(#dfBg)"/>
  <text x="450" y="38" text-anchor="middle" font-family="Arial,sans-serif" font-size="20" font-weight="bold" fill="#2D3436">Platform Data Flow Architecture</text>

  <!-- Left: API Layer Labels -->
  <text x="55" y="100" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#636e72" transform="rotate(-90,55,100)">User APIs</text>
  <rect x="30" y="70" width="3" height="70" rx="1.5" fill="#FF6B35" opacity="0.6"/>

  <text x="55" y="210" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#636e72" transform="rotate(-90,55,210)">Process APIs</text>
  <rect x="30" y="180" width="3" height="70" rx="1.5" fill="#28a745" opacity="0.6"/>

  <text x="55" y="320" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#636e72" transform="rotate(-90,55,320)">System APIs</text>
  <rect x="30" y="290" width="3" height="70" rx="1.5" fill="#1565C0" opacity="0.6"/>

  <!-- Layer 1: User Interface Layer -->
  <rect x="80" y="60" width="740" height="85" rx="12" fill="url(#layerOrange)" filter="url(#dfShadow)"/>
  <text x="100" y="88" font-family="Arial,sans-serif" font-size="14" font-weight="bold" fill="white">User Interface Layer</text>
  <text x="100" y="108" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.8)">Dashboard  |  Forecasts  |  Inventory  |  Menu  |  Labor  |  Procurement  |  Analytics</text>

  <!-- Sub-boxes in UI layer -->
  <rect x="100" y="115" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="150" y="130" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Streamlit UI</text>
  <rect x="215" y="115" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="265" y="130" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Charts</text>
  <rect x="330" y="115" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="380" y="130" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">KPI Cards</text>
  <rect x="445" y="115" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="495" y="130" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Alerts</text>
  <rect x="560" y="115" width="120" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="620" y="130" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Currency Engine</text>

  <!-- Arrow down -->
  <polygon points="450,148 440,155 460,155" fill="#636e72" opacity="0.5"/>
  <line x1="450" y1="148" x2="450" y2="168" stroke="#636e72" stroke-width="1.5" opacity="0.4"/>

  <!-- Layer 2: AI & Business Logic Layer -->
  <rect x="80" y="168" width="740" height="85" rx="12" fill="url(#layerGreen)" filter="url(#dfShadow)"/>
  <text x="100" y="196" font-family="Arial,sans-serif" font-size="14" font-weight="bold" fill="white">AI &amp; Business Logic Layer</text>
  <text x="100" y="216" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.8)">Prediction Engine  |  Optimization  |  Insights Generator  |  Alert System</text>

  <rect x="100" y="224" width="120" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="160" y="239" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Forecast Engine</text>
  <rect x="235" y="224" width="120" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="295" y="239" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Inventory Optimizer</text>
  <rect x="370" y="224" width="120" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="430" y="239" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Menu Analyzer</text>
  <rect x="505" y="224" width="120" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="565" y="239" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Labor Planner</text>
  <rect x="640" y="224" width="120" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="700" y="239" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Alert Engine</text>

  <!-- Arrow down -->
  <polygon points="450,256 440,263 460,263" fill="#636e72" opacity="0.5"/>
  <line x1="450" y1="256" x2="450" y2="278" stroke="#636e72" stroke-width="1.5" opacity="0.4"/>

  <!-- Layer 3: Data Layer -->
  <rect x="80" y="278" width="740" height="85" rx="12" fill="url(#layerBlue)" filter="url(#dfShadow)"/>
  <text x="100" y="306" font-family="Arial,sans-serif" font-size="14" font-weight="bold" fill="white">Data &amp; Integration Layer</text>
  <text x="100" y="326" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.8)">Historical Orders  |  Inventory State  |  Supplier Network  |  Menu Catalog  |  Staff Records</text>

  <rect x="100" y="334" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="150" y="349" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Order History</text>
  <rect x="215" y="334" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="265" y="349" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Inventory DB</text>
  <rect x="330" y="334" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="380" y="349" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Supplier Data</text>
  <rect x="445" y="334" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="495" y="349" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Menu Config</text>
  <rect x="560" y="334" width="100" height="22" rx="6" fill="rgba(255,255,255,0.2)"/>
  <text x="610" y="349" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="white">Staff Records</text>

  <!-- Right: Module Gating Table -->
  <rect x="835" y="60" width="3" height="303" rx="1.5" fill="#FF6B35" opacity="0.3"/>

  <!-- Bottom: Infrastructure bar -->
  <rect x="80" y="385" width="740" height="55" rx="12" fill="url(#layerDark)" filter="url(#dfShadow)"/>
  <text x="100" y="408" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="white">Infrastructure</text>
  <text x="100" y="428" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.7)">Cloud Hosting  |  Session State  |  Caching  |  Multi-Currency  |  Multi-Tenant Ready</text>
</svg>'''


# --- Module Gating Table SVG ---
MODULE_GATING_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 350">
  <defs>
    <filter id="gateShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="rgba(0,0,0,0.08)"/>
    </filter>
  </defs>
  <rect width="700" height="350" rx="16" fill="#f8f9fa" filter="url(#gateShadow)"/>
  <text x="350" y="35" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="#2D3436">Module Access &amp; Gating</text>

  <!-- Table header -->
  <rect x="20" y="50" width="660" height="35" rx="8" fill="#1a1a2e"/>
  <text x="140" y="73" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Module</text>
  <text x="320" y="73" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Starter</text>
  <text x="460" y="73" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Professional</text>
  <text x="600" y="73" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Enterprise</text>

  <!-- Row 1 -->
  <rect x="20" y="90" width="660" height="35" rx="0" fill="white"/>
  <text x="40" y="112" font-family="Arial,sans-serif" font-size="11" fill="#2D3436">📈 Demand Forecasting</text>
  <rect x="295" y="98" width="50" height="20" rx="10" fill="#28a745" opacity="0.15"/>
  <text x="320" y="113" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#28a745">Basic</text>
  <rect x="435" y="98" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="460" y="113" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>
  <rect x="575" y="98" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="600" y="113" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>

  <!-- Row 2 -->
  <rect x="20" y="128" width="660" height="35" rx="0" fill="#f8f9fa"/>
  <text x="40" y="150" font-family="Arial,sans-serif" font-size="11" fill="#2D3436">📦 Inventory Management</text>
  <rect x="295" y="136" width="50" height="20" rx="10" fill="#28a745" opacity="0.15"/>
  <text x="320" y="151" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#28a745">Basic</text>
  <rect x="435" y="136" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="460" y="151" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>
  <rect x="575" y="136" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="600" y="151" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>

  <!-- Row 3 -->
  <rect x="20" y="166" width="660" height="35" rx="0" fill="white"/>
  <text x="40" y="188" font-family="Arial,sans-serif" font-size="11" fill="#2D3436">🛒 Smart Procurement</text>
  <rect x="303" y="174" width="35" height="20" rx="10" fill="#6c757d" opacity="0.15"/>
  <text x="320" y="189" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#6c757d">—</text>
  <rect x="435" y="174" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="460" y="189" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>
  <rect x="575" y="174" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="600" y="189" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>

  <!-- Row 4 -->
  <rect x="20" y="204" width="660" height="35" rx="0" fill="#f8f9fa"/>
  <text x="40" y="226" font-family="Arial,sans-serif" font-size="11" fill="#2D3436">🍽️ Menu Engineering</text>
  <rect x="303" y="212" width="35" height="20" rx="10" fill="#6c757d" opacity="0.15"/>
  <text x="320" y="227" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#6c757d">—</text>
  <rect x="435" y="212" width="50" height="20" rx="10" fill="#28a745" opacity="0.15"/>
  <text x="460" y="227" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#28a745">Basic</text>
  <rect x="575" y="212" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="600" y="227" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>

  <!-- Row 5 -->
  <rect x="20" y="242" width="660" height="35" rx="0" fill="white"/>
  <text x="40" y="264" font-family="Arial,sans-serif" font-size="11" fill="#2D3436">👥 Labor Scheduling</text>
  <rect x="303" y="250" width="35" height="20" rx="10" fill="#6c757d" opacity="0.15"/>
  <text x="320" y="265" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#6c757d">—</text>
  <rect x="435" y="250" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="460" y="265" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>
  <rect x="575" y="250" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="600" y="265" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>

  <!-- Row 6 -->
  <rect x="20" y="280" width="660" height="35" rx="0" fill="#f8f9fa"/>
  <text x="40" y="302" font-family="Arial,sans-serif" font-size="11" fill="#2D3436">📊 Analytics &amp; Growth</text>
  <rect x="295" y="288" width="50" height="20" rx="10" fill="#28a745" opacity="0.15"/>
  <text x="320" y="303" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#28a745">Basic</text>
  <rect x="435" y="288" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="460" y="303" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>
  <rect x="575" y="288" width="50" height="20" rx="10" fill="#FF6B35" opacity="0.15"/>
  <text x="600" y="303" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>

  <!-- Row 7 -->
  <rect x="20" y="318" width="660" height="28" rx="0" fill="white"/>
  <text x="40" y="337" font-family="Arial,sans-serif" font-size="11" fill="#2D3436">🔗 Supplier Network</text>
  <rect x="303" y="324" width="35" height="18" rx="9" fill="#6c757d" opacity="0.15"/>
  <text x="320" y="337" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#6c757d">—</text>
  <rect x="303" y="324" width="35" height="18" rx="9" fill="#6c757d" opacity="0.15"/>
  <text x="460" y="337" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#6c757d">—</text>
  <rect x="575" y="324" width="50" height="18" rx="9" fill="#FF6B35" opacity="0.15"/>
  <text x="600" y="337" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="#FF6B35">Full</text>
</svg>'''


# --- Network Effects Diagram ---
NETWORK_EFFECTS_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380">
  <defs>
    <linearGradient id="neBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
    <filter id="neShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="rgba(0,0,0,0.2)"/>
    </filter>
  </defs>
  <rect width="900" height="380" rx="16" fill="url(#neBg)"/>
  <text x="450" y="40" text-anchor="middle" font-family="Arial,sans-serif" font-size="20" font-weight="bold" fill="white">Network Effects &amp; Data Flywheel</text>
  <text x="450" y="62" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="rgba(255,255,255,0.6)">How Forkast compounds value with every new restaurant</text>

  <!-- Circular flywheel arrows -->
  <circle cx="250" cy="210" r="100" fill="none" stroke="rgba(255,107,53,0.2)" stroke-width="3" stroke-dasharray="12,6"/>

  <!-- Flywheel nodes -->
  <g filter="url(#neShadow)">
    <circle cx="250" cy="110" r="35" fill="#FF6B35"/>
    <text x="250" y="105" text-anchor="middle" font-size="18">🏪</text>
    <text x="250" y="125" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="bold" fill="white">More Users</text>
  </g>

  <g filter="url(#neShadow)">
    <circle cx="350" cy="210" r="35" fill="#28a745"/>
    <text x="350" y="205" text-anchor="middle" font-size="18">📊</text>
    <text x="350" y="225" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="bold" fill="white">More Data</text>
  </g>

  <g filter="url(#neShadow)">
    <circle cx="250" cy="310" r="35" fill="#1565C0"/>
    <text x="250" y="305" text-anchor="middle" font-size="18">🧠</text>
    <text x="250" y="325" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="bold" fill="white">Better AI</text>
  </g>

  <g filter="url(#neShadow)">
    <circle cx="150" cy="210" r="35" fill="#F7931E"/>
    <text x="150" y="205" text-anchor="middle" font-size="18">💰</text>
    <text x="150" y="225" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="bold" fill="white">More Value</text>
  </g>

  <!-- Flywheel arrows -->
  <path d="M280 125 Q320 150 340 180" fill="none" stroke="#FF6B35" stroke-width="2.5" marker-end="url(#arrowOrange)"/>
  <path d="M340 240 Q320 280 275 300" fill="none" stroke="#28a745" stroke-width="2.5"/>
  <path d="M220 300 Q180 280 160 245" fill="none" stroke="#1565C0" stroke-width="2.5"/>
  <path d="M160 180 Q170 150 225 125" fill="none" stroke="#F7931E" stroke-width="2.5"/>

  <!-- Arrow triangles -->
  <polygon points="338,178 330,185 342,186" fill="#FF6B35"/>
  <polygon points="277,298 282,308 272,306" fill="#28a745"/>
  <polygon points="162,247 154,240 158,252" fill="#1565C0"/>
  <polygon points="223,127 228,118 218,122" fill="#F7931E"/>

  <!-- Right side: Network effect cards -->
  <rect x="440" y="85" width="430" height="75" rx="12" fill="rgba(255,255,255,0.08)" stroke="rgba(255,107,53,0.3)" stroke-width="1.5"/>
  <rect x="440" y="85" width="5" height="75" rx="2.5" fill="#FF6B35"/>
  <text x="465" y="108" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="white">Direct Network Effects</text>
  <text x="465" y="128" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.7)">More restaurants = richer demand data = better forecasts</text>
  <text x="465" y="148" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.7)">for all users across cuisine types and regions</text>

  <rect x="440" y="175" width="430" height="75" rx="12" fill="rgba(255,255,255,0.08)" stroke="rgba(40,167,69,0.3)" stroke-width="1.5"/>
  <rect x="440" y="175" width="5" height="75" rx="2.5" fill="#28a745"/>
  <text x="465" y="198" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="white">Cross-Side Network Effects</text>
  <text x="465" y="218" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.7)">More restaurants = more supplier demand visibility</text>
  <text x="465" y="238" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.7)">= better fill rates and pricing for the whole network</text>

  <rect x="440" y="265" width="430" height="75" rx="12" fill="rgba(255,255,255,0.08)" stroke="rgba(21,101,192,0.3)" stroke-width="1.5"/>
  <rect x="440" y="265" width="5" height="75" rx="2.5" fill="#1565C0"/>
  <text x="465" y="288" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="white">Data Moat Effects</text>
  <text x="465" y="308" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.7)">Aggregate insights improve with scale: cuisine patterns,</text>
  <text x="465" y="328" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.7)">seasonal trends, event impacts, supplier reliability scores</text>

  <!-- Metrics bar at bottom -->
  <rect x="30" y="352" width="840" height="20" rx="4" fill="rgba(255,255,255,0.05)"/>
  <text x="450" y="366" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="rgba(255,255,255,0.5)">Target: 150K+ Restaurants  |  10K+ Suppliers  |  150K+ Enterprise Customers  |  AI Accuracy Compounds With Scale</text>
</svg>'''


def svg_to_html(svg_string, width="100%"):
    """Convert SVG string to displayable HTML"""
    b64 = base64.b64encode(svg_string.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" style="width:{width};">'


def render_svg(svg_string, width="100%"):
    """Render SVG directly in Streamlit"""
    b64 = base64.b64encode(svg_string.encode()).decode()
    return f'<div style="text-align:center;"><img src="data:image/svg+xml;base64,{b64}" style="width:{width};max-width:100%;"></div>'
