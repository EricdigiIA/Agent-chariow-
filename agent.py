import os
import time
import random
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright

# ============================================
# CONFIGURATION AUTOFLOW STORE AGENT
# ============================================

CHARIOW_API_KEY = os.environ.get("CHARIOW_API_KEY", "sk_2whz48u8_b4d6825f0569dc468572d68b60ec0be2")
CHARIOW_PRODUCT_LINK = "https://sftwjfub.mychariow.shop/prd_jndo6h"
CHARIOW_API_URL = "https://chariow.dev/api/v1"

# Tes identifiants Facebook — mets dans variables environnement Render
FB_EMAIL = os.environ.get("FB_EMAIL", "")
FB_PASSWORD = os.environ.get("FB_PASSWORD", "")

# Groupes Facebook à cibler
GROUPES_FACEBOOK = [
    "https://www.facebook.com/groups/entrepreneursafrique",
    "https://www.facebook.com/groups/marketingdigitalafrique",
    "https://www.facebook.com/groups/businessafrique",
]

# Message à envoyer à chaque prospect
MESSAGE = f"""Bonjour 👋

Tu veux automatiser ta prospection sur Facebook
et recevoir des clients sans effort ?

Ce système répond à ta place en quelques secondes
et dirige tes prospects vers WhatsApp 24h/24.

Prêt à installer en 30 minutes.
Zéro compétence technique requise.

👉 {CHARIOW_PRODUCT_LINK}"""

# Headers API Chariow
HEADERS_CHARIOW = {
    "Authorization": f"Bearer {CHARIOW_API_KEY}",
    "Content-Type": "application/json"
}

# ============================================
# CONNEXION CHARIOW
# ============================================

def enregistrer_prospect(nom, source, profil_url):
    """Enregistre le prospect dans Chariow"""
    try:
        data = {
            "name": nom,
            "source": source,
            "profile_url": profil_url,
            "product_link": CHARIOW_PRODUCT_LINK,
            "date": datetime.now().isoformat()
        }
        response = requests.post(
            f"{CHARIOW_API_URL}/contacts",
            headers=HEADERS_CHARIOW,
            json=data,
            timeout=10
        )
        print(f"✅ Prospect enregistré Chariow: {nom}")
    except Exception as e:
        print(f"⚠️ Erreur Chariow: {e}")

# ============================================
# CONNEXION FACEBOOK
# ============================================

def connecter_facebook(page):
    """Se connecte à Facebook automatiquement"""
    try:
        print("🔐 Connexion Facebook en cours...")
        page.goto("https://www.facebook.com/login")
        time.sleep(random.uniform(2, 4))

        page.fill("#email", FB_EMAIL)
        time.sleep(random.uniform(1, 2))
        page.fill("#pass", FB_PASSWORD)
        time.sleep(random.uniform(1, 2))
        page.click("[name='login']")
        time.sleep(random.uniform(4, 6))

        if "facebook.com" in page.url and "login" not in page.url:
            print("✅ Connexion Facebook réussie")
            return True
        else:
            print("❌ Echec connexion Facebook")
            return False
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False

# ============================================
# SCRAPING MEMBRES GROUPES
# ============================================

def scraper_groupe(page, groupe_url):
    """Scrape les membres d'un groupe Facebook"""
    membres = []
    try:
        print(f"📘 Scraping: {groupe_url}")
        page.goto(f"{groupe_url}/members")
        time.sleep(random.uniform(3, 5))

        # Scroll pour charger les membres
        for i in range(5):
            page.keyboard.press("End")
            time.sleep(random.uniform(2, 3))

        # Extraire les profils
        profils = page.query_selector_all("a[href*='facebook.com/']")

        for profil in profils[:20]:
            try:
                nom = profil.inner_text().strip()
                url = profil.get_attribute("href")
                if nom and url and len(nom) > 2 and "groups" not in url:
                    membres.append({
                        "nom": nom,
                        "url": url,
                        "source": "Facebook"
                    })
            except:
                continue

        print(f"✅ {len(membres)} membres trouvés")
        return membres

    except Exception as e:
        print(f"❌ Erreur scraping: {e}")
        return []

# ============================================
# ENVOI MESSAGES FACEBOOK
# ============================================

def envoyer_message(page, profil):
    """Envoie un message privé Facebook"""
    try:
        page.goto(profil["url"])
        time.sleep(random.uniform(2, 4))

        # Chercher bouton Message
        bouton = page.query_selector("[aria-label*='Message'], a[href*='messages']")
        if bouton:
            bouton.click()
            time.sleep(random.uniform(2, 3))

            # Taper le message naturellement
            page.keyboard.type(MESSAGE, delay=random.randint(30, 80))
            time.sleep(random.uniform(1, 2))
            page.keyboard.press("Enter")
            time.sleep(random.uniform(2, 3))

            print(f"📤 Message envoyé à {profil['nom']}")

            # Enregistrer dans Chariow
            enregistrer_prospect(
                nom=profil["nom"],
                source=profil["source"],
                profil_url=profil["url"]
            )
            return True
        else:
            print(f"⚠️ Bouton message non trouvé: {profil['nom']}")
            return False

    except Exception as e:
        print(f"❌ Erreur envoi: {e}")
        return False

# ============================================
# BOUCLE PRINCIPALE AGENT
# ============================================

def lancer_agent():
    """Lance l'agent principal en boucle infinie"""
    print("=" * 50)
    print("🤖 AUTOFLOW STORE AGENT — DÉMARRAGE")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Produit: {CHARIOW_PRODUCT_LINK}")
    print("=" * 50)

    if not FB_EMAIL or not FB_PASSWORD:
        print("❌ ERREUR: Configure FB_EMAIL et FB_PASSWORD")
        print("   Dans Render → Environment Variables")
        return

    cycle = 0

    while True:
        cycle += 1
        print(f"\n🔄 CYCLE {cycle} — {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 40)

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720}
            )
            page = context.new_page()

            # Connexion Facebook
            connecte = connecter_facebook(page)

            if connecte:
                tous_membres = []

                # Scraper chaque groupe
                for groupe in GROUPES_FACEBOOK:
                    membres = scraper_groupe(page, groupe)
                    tous_membres.extend(membres)
                    time.sleep(random.uniform(5, 10))

                print(f"\n📊 Total prospects trouvés: {len(tous_membres)}")
                print("-" * 40)

                # Envoyer messages
                envoyes = 0
                for membre in tous_membres:
                    succes = envoyer_message(page, membre)
                    if succes:
                        envoyes += 1
                    # Délai naturel anti-ban
                    time.sleep(random.uniform(45, 90))

                    # Max 15 messages par cycle
                    if envoyes >= 15:
                        break

                print(f"\n✅ {envoyes} messages envoyés ce cycle")

            browser.close()

        print(f"⏳ Prochain cycle dans 2 heures...")
        print("=" * 50)

        # Attendre 2 heures
        time.sleep(7200)

if __name__ == "__main__":
    lancer_agent()
