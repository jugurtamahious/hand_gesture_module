# 🖐️ Hand Gesture Recognition Module

Détection de gestes de la main via webcam avec envoi des entités eHuB sur un panneau LED 128x128.

---

## 📌 Fonctionnalités

-  Détection en temps réel via webcam (Mediapipe)
-  Reconnaissance de gestes : lignes, cercles (extensible)
-  Conversion en grille 128x128
-  Mapping des coordonnées en ID d'entités
-  Envoi des entités actives via UDP (protocole eHuB)
-  Visualisation en local sur grille simulée

---

## 🧰 Prérequis

- Python **3.11** (évite Python 3.14)
- Git
- Une webcam
- Un interpréteur compatible `venv` (environnement virtuel)

---

## 🚀 Installation

### 1. Clone le repo

```bash
git clone https://github.com/jugurtamahious/hand_gesture_module.git

# Guide d'installation et de lancement

## 1. Créer un environnement virtuel

```bash
python -m venv venv
```

## 2. Activer l'environnement virtuel

### Windows :
```bash
venv\Scripts\activate
```

### macOS/Linux :
```bash
source venv/bin/activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 4. Lancer le projet

```bash
python main.py
