# Utiliser une image de base légère
FROM python:3.9-slim

# Installer FFmpeg et nettoyer les caches
RUN apt-get update && apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les fichiers nécessaires
COPY requirements.txt .
COPY main.py .

# Installer les dépendances Python sans cache
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 80
EXPOSE 80

# Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]