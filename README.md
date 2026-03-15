# AutoFlow Store Agent

Agent IA qui scrape Facebook automatiquement
et envoie le lien Chariow aux prospects 24h/24.

## Déploiement sur Render.com

### Étape 1 — Upload sur GitHub
Crée un repository GitHub "autoflow-agent"
Upload les 3 fichiers : agent.py, requirements.txt, README.md

### Étape 2 — Déployer sur Render
Va sur https://render.com
Clique "New" → "Web Service"
Connecte ton GitHub → sélectionne "autoflow-agent"

### Étape 3 — Configuration Render
- Name : autoflow-agent
- Runtime : Python 3
- Build Command : pip install -r requirements.txt && playwright install chromium
- Start Command : python agent.py

### Étape 4 — Variables d'environnement
Dans Render → Environment Variables, ajoute :
- FB_EMAIL = ton email Facebook
- FB_PASSWORD = ton mot de passe Facebook
- CHARIOW_API_KEY = sk_2whz48u8_b4d6825f0569dc468572d68b60ec0be2

### Étape 5 — Lancer
Clique "Create Web Service"
L'agent démarre et tourne 24h/24 automatiquement

## Ce que l'agent fait

- Entre dans les groupes Facebook entrepreneurs
- Extrait jusqu'à 20 membres par groupe
- Envoie un message privé avec ton lien Chariow
- Enregistre chaque prospect dans ta boutique Chariow
- Recommence toutes les 2 heures automatiquement
- Tourne 24h/24 même si ton ordinateur est éteint
