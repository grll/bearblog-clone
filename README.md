# Bearblog Clone

A minimalist single-author blog platform inspired by Bear Blog, built with Django.

## Features

- Single-author blog focused on simplicity and speed
- Markdown support for writing posts
- Clean, minimal design with focus on readability
- Django admin interface for content management
- No user registration - admin-only content creation

## Setup

1. Install dependencies with uv:
   ```bash
   uv sync
   ```

2. Run migrations:
   ```bash
   uv run python manage.py migrate
   ```

3. Create superuser (use admin/admin for consistency):
   ```bash
   uv run python manage.py createsuperuser
   ```

4. Run the development server:
   ```bash
   uv run python manage.py runserver
   ```

## Usage

- Access the blog at `/` (homepage shows the latest posts)
- Manage posts at `/admin/` (Django admin interface)
- Admin credentials: admin / admin

## Philosophy

This is a single-author blog platform that prioritizes:
- Minimalism over feature bloat
- Simplicity over complex abstractions
- Fast loading times
- Clean, readable content presentation
- Easy content management through Django admin