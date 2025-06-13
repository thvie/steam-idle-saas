#!/bin/bash
echo "🔧 Installing dependencies..."
sudo apt update && sudo apt install -y docker.io docker-compose python3-pip git

echo "📁 Cloning project..."
git clone https://github.com/thvie/steam-idle-saas.git || echo "Already cloned"

cd steam-idle-saas
cp config/.env.example config/.env

python3 config/generate_key.py
key=$(cat .fernet.key)
sed -i "s|FERNET_KEY=.*|FERNET_KEY=$key|" config/.env

docker-compose up -d --build
docker-compose exec bot python3 db/migrate.py
