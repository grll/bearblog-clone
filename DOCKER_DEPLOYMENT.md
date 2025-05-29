# Docker Deployment Guide

Ultra-minimal Docker deployment for your bearblog clone.

## 🚀 Quick Deploy

### 1. Server Setup (Ubuntu/Debian)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Deploy the App
```bash
# Clone your repo
git clone https://github.com/grll/bearblog-clone.git
cd bearblog-clone

# Create environment file
cp .env.example .env
# Edit .env with your domain and secret key

# Create data directory
mkdir -p data

# Build and start
docker-compose up -d --build

# Create superuser
docker-compose exec web uv run python manage.py createsuperuser
```

### 3. Cloudflare Setup
1. Add your domain to Cloudflare
2. Update nameservers at registrar
3. Add DNS records:
   - A record: `@` → your-server-ip
   - A record: `www` → your-server-ip
4. SSL/TLS → **Flexible** (let Cloudflare handle HTTPS)
5. Enable "Always Use HTTPS"

## 📁 Files Created

- `Dockerfile` - Minimal Python container
- `docker-compose.yml` - Nginx + Django services
- `nginx.conf` - Reverse proxy config
- `.env.example` - Environment variables template

## 🔄 Updates

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# Run migrations if needed
docker-compose exec web uv run python manage.py migrate
```

## 📊 Data Persistence

- Database: `./data/db.sqlite3` (SQLite file)
- Media uploads: `./media/` directory
- Static files: Built into container

## 🔧 Maintenance

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop everything
docker-compose down

# Backup database
cp data/db.sqlite3 backup-$(date +%Y%m%d).sqlite3
```

That's it! Your blog runs at `http://your-domain.com` with Cloudflare providing HTTPS and CDN.