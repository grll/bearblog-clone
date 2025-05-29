# Single-Author Blog Specifications

This document captures all the information needed to reproduce a single-author blog platform inspired by Bear Blog.

## Overview
This is a minimalist single-author blog platform that focuses on simplicity, fast loading times, and content creation through Django admin.

---

## Homepage (/)

### Header
- Blog title (customizable in Django admin)
- Simple navigation menu (Home, Blog, About - configurable)
- Clean, minimal design

### Main Content
1. **Welcome Section**: Custom homepage content (markdown-based)
2. **Recent Posts**: Latest blog posts with title, date, and excerpt
3. **About Section**: Brief author bio or blog description

### Value Proposition
- "A minimalist blog focused on words and content"
- "No bloat, no trackers, just pure content"

### Key Features
- Looks great on any device
- Tiny, optimized pages
- No trackers, ads, or unnecessary scripts
- Django admin for easy content management
- Markdown support for writing
- RSS feed
- Clean, readable design

### Footer
- RSS feed link
- "Powered by Bear ʕ•ᴥ•ʔ" (optional)
- Contact/social links (configurable)

### Design Notes
- Extremely minimal design
- Clean typography
- Blue links (#0066cc style)
- White background
- Black text
- Focus on readability

---

## Blog Structure

### Homepage Structure
- **Header**:
  - Blog title (configurable in Django admin)
  - Navigation menu (Home, Blog, About - configurable)
- **Main Content**:
  - Custom homepage content (markdown-based, editable in admin)
  - Recent posts section (latest 5-10 posts)
  - About section (brief bio or description)
- **Footer**:
  - RSS feed link
  - Optional "Powered by Bear ʕ•ᴥ•ʔ" link
  - Contact/social links (configurable)

### Individual Post Page (/posts/slug/)
- Post title (h1)
- Publication date
- Post content (markdown rendered)
- Same header/footer as homepage
- Previous/next post navigation

### Blog Archive Page (/blog/)
- List of all posts with:
  - Date
  - Post title (clickable)
  - Brief excerpt
- Simple pagination
- Search functionality (optional)

### URL Structure
- Homepage: /
- Individual posts: /posts/post-slug/
- Blog archive: /blog/
- RSS feed: /feed/
- Django admin: /admin/

---

## Content Management

### Django Admin Interface
- Standard Django admin for content management
- Admin credentials: admin / admin
- Models managed through admin:
  - Blog posts (title, slug, content, published date, status)
  - Pages (About, custom pages)
  - Site configuration (blog title, description, footer links)

### Post Management
- Create/edit posts through Django admin
- Markdown content support
- Draft/published status
- SEO-friendly URL slugs
- Publication date control

### Site Configuration
- Blog title and tagline
- Homepage content
- About page content
- Footer links and text
- All configurable through admin interface

---

## Theme & Styling System

### Minimal Design
- Clean, readable typography
- No CSS framework bloat
- Focus on content readability
- Responsive design for all devices

### Default Styling
- Blue links (#0066cc)
- White background
- Black text
- Minimal spacing and clean layout
- System fonts for fast loading

### CSS Classes for Customization
**Page-specific:**
- `.home` - Homepage
- `.post` - Individual posts
- `.page` - Custom pages
- `.blog` - Blog archive page

**Elements:**
- `.blog-title` - Main blog title
- `.blog-posts` - Post list
- `nav` - Navigation header
- `.post-content` - Post content area
- `.post-meta` - Post date/metadata

---

## Technical Features

### Core Features
- Markdown support for content
- RSS feed generation
- SEO-friendly URLs
- Fast page loading
- No unnecessary JavaScript
- Responsive design

### Technical Stack
- Django 5.2.1+ with Python 3.12+
- SQLite database (simple deployment)
- Markdown processing
- Pillow for image handling

### Performance
- Minimal HTML output
- No external dependencies on frontend
- Fast server-side rendering
- Clean, semantic markup

---

## Philosophy & Values

### Core Principles
- Privacy-first (no trackers, ads, unnecessary scripts)
- Minimal and fast
- Focus on content over features
- Simple content management
- Open source

### Design Philosophy
- "No-nonsense" approach
- Focus on words and content
- Accessibility and readability
- Device-agnostic design
- Against feature bloat
- Admin-driven content management

---
