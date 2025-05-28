# Bearblog.dev Specifications

This document captures all the information needed to reproduce bearblog.dev.

## Overview
Bearblog is a minimalist blogging platform that focuses on simplicity and fast loading times.

---

## Homepage (https://bearblog.dev/)

### Header
- Logo: "ʕ•ᴥ•ʔ Bear" (clickable, links to homepage)
- Clean, minimal design with no navigation menu on homepage

### Main Content
1. **Primary Tagline**: "A privacy-first, no-nonsense, super-fast blogging platform"
2. **Secondary Tagline**: "No trackers, no javascript, no stylesheets. Just your words."

### Call-to-Action Buttons
- Sign up (/signup/)
- Log in (/accounts/login/)
- Discover (/discover/)

### Value Proposition
- "This is a blogging platform where words matter most."
- "Shun the bloat of the current web, embrace the bear necessities."

### Key Features List
- Looks great on any device
- Tiny (~2.7kb), optimized, and awesome pages
- No trackers, ads, or scripts
- Seconds to sign up
- Connect your custom domain
- Free themes
- RSS & Atom feeds
- Built to last forever* (asterisk links to manifesto)

### Additional Elements
- "View example blog" link (https://herman.bearblog.dev)
- Tagline: "Publish something awesome with your bear hands ᕦʕ •ᴥ•ʔᕤ"

### Footer
- "Built and maintained by Herman" (links to https://herman.bearblog.dev)
- Links: Privacy Policy | Terms of Service | GitHub | Docs | Roadmap

### Design Notes
- Extremely minimal design
- No CSS framework or styling (as stated)
- Clean typography
- Blue links (#0066cc style)
- White background
- Black text
- No images except bear emoticons

---

## Discovery Feed (https://bearblog.dev/discover/)

### Navigation
- Trending (default view)
- Most recent (?newest=true)
- Search (/discover/search/)

### Features
- Language filter option
- Hidden blogs functionality (stored in cookies)
- Blog reporting mechanism

### Post List Display
Each post shows:
- Rank number (#1, #2, etc.)
- Post title (clickable)
- Blog domain (in parentheses, clickable)
- Publication time (e.g., "Published 1 day, 19 hours ago")
- Upvote count with icon

### Ranking Algorithm
```
Score = log10(U) + (S / B * 86,400)
Where:
- U = Upvotes of a post
- S = Seconds since Jan 1st, 2020
- B = Buoyancy modifier (currently at 14)
```

### Additional Elements
- Pagination ("Next »" link)
- RSS feed link
- Footer CTA: "Start your own blog with ʕ•ᴥ•ʔ Bear"

---

## Authentication

### Sign Up Page (https://bearblog.dev/signup/)
**Extremely simple 3-field form:**
1. Blog title (placeholder: "A title for your blog...")
2. Subdomain (placeholder: "Preferred subdomain...") + ".bearblog.dev"
3. Homepage text (textarea, placeholder: "Some homepage text...")
- Note: "Don't worry, you can change all this later"
- Single button: "Create »"
- No email or password required initially

### Login Page (https://bearblog.dev/accounts/login/)
**Standard login form:**
- Email field
- Password field
- "Remember Me" checkbox
- "Sign In »" button
- Links: "Forgot Password?" and "Create an account"

### Authentication Notes
- Ultra-simple signup process (no email/password on initial creation)
- Appears to create blog first, then account setup later
- Focus on reducing friction for new users

---

## Individual Blog Structure

### Example Blog: herman.bearblog.dev

#### Homepage Structure
- **Header**:
  - Blog title (clickable, links to home)
  - Navigation menu (customizable pages like Home, Now, Projects, Blog)
- **Main Content**:
  - Custom homepage content (markdown-based)
  - Recent posts section
  - Popular posts section
- **Footer**:
  - Subscribe options: RSS, Email, Contact
  - "Powered by Bear ʕ•ᴥ•ʔ" link

#### Individual Post Page
- Post title (h1)
- Publication date
- Post content (markdown rendered)
- Upvote button with count (heart icon + number)
- Same header/footer as homepage

#### Archive/Blog List Page (/blog/)
- Search box at top
- Chronological list of all posts with:
  - Date
  - Post title (clickable)
- Tag cloud at bottom (clickable hashtags)
- Supports filtering by tag (?q=tagname)

### URL Structure
- Homepage: username.bearblog.dev
- Individual posts: username.bearblog.dev/post-slug/
- Archive: username.bearblog.dev/blog/
- Custom pages: username.bearblog.dev/pagename/
- RSS feed: username.bearblog.dev/feed/
- Email subscription: username.bearblog.dev/subscribe/

---

## Pricing Model

### Free Tier
- Basic blog functionality
- Subdomain (username.bearblog.dev)
- Basic analytics (past week only)
- All core features
- Must keep "Powered by Bear" footer

### Upgraded/Sponsor Tier
- Custom domains
- In-depth analytics:
  - Readers currently on site
  - Filter by pages
  - Filter by referrers
  - Location of reader
  - Device of reader
  - OS of reader
  - Export all analytics as CSV
- Beta features access
- Can remove "Powered by Bear" footer
- Priority support

### Sponsorship Model
- Based on GitHub Sponsors or similar
- Described as "Sponsorware" approach
- Custom domains locked behind sponsorship
- Helps support server costs and development

---

## Analytics System

### Privacy-First Approach
- No Google Analytics (explicitly refused)
- Tracks only "human-reads" (requires hover or scroll)
- No bot/scraper tracking
- Unique reads per post per reader per day
- CSS-based tracking system

### Basic Analytics
- Number of reads
- Unique visitors
- Past week data only

### Integration Support
- Fathom Analytics (privacy-respecting third-party)
- Custom site ID field for integration

---

## Theme & Styling System

### Pre-built Themes
- Multiple themes available in dashboard
- Can be used as-is or as starting point
- Supports no-class CSS themes

### Custom CSS
- Full CSS customization
- Import external stylesheets (@import)
- Custom fonts support
- Dark mode support (@media prefers-color-scheme)

### CSS Classes
**Page-specific:**
- `.home` - Homepage
- `.post` - Individual posts
- `.page` - Custom pages
- `.blog` - Blog list page
- `.subscribe` - Email subscription page
- `.not-found` - 404 page

**Elements:**
- `.title h1` - Blog title
- `.blog-posts` - Post list UL
- `nav` - Navigation header
- `.highlight, .code` - Code blocks

**Custom Classes:**
- Posts can have custom `class_name` header
- Allows per-post styling

### Dashboard Styling
- Can customize admin dashboard appearance
- Separate from blog styling

---

## Additional Features

### Email Newsletters
- Built-in email subscription system
- Subscribe page at /subscribe/

### RSS/Atom Feeds
- Automatic RSS feed at /feed/
- Atom feed support

### SEO
- Clean URLs
- Semantic HTML
- Fast loading times
- No JavaScript requirement

### Content Features
- Markdown support
- LaTeX mathematical notation
- Code syntax highlighting
- Image hosting (via CDN)
- Custom robots.txt editing

### Blog Management
- Spam control system
- Manual blog approval process
- Email blacklisting
- Tag system with filtering
- Post search functionality
- Custom page creation

### Technical Features
- SQLite database
- No JavaScript on frontend
- ~2.7kb page size
- IPv4 and IPv6 support
- SSL certificates automatic
- Built with Django/Python

---

## Philosophy & Values

### Core Principles
- Privacy-first (no trackers, ads, scripts)
- Minimal and fast
- Built to last forever
- No VC funding
- Independent ownership
- Open source

### Design Philosophy
- "No-nonsense" approach
- Focus on words/content
- Accessibility
- Device-agnostic design
- Against feature bloat

---

## Dashboard & Admin Interface

### Account Dashboard (/dashboard/)
- **Your blogs**: List of user's blogs
- **Account options**:
  - Sign out
  - Customise dashboard
  - Update email address
  - Change password
  - Delete account
- **Upgrade CTA**: "Upgrade to create up to 10 blogs"

### Blog Dashboard Navigation
- **Top bar**: Shows blog subdomain (e.g., "grll.bearblog.dev")
- **Primary nav**: Home, Nav, Posts, Pages, Themes, Emails, Upgrade
- **Secondary nav**: Analytics, Settings, Back to account (ʕ-ᴥ-ʔ)
- **Notice bar**: For non-upgraded blogs: "Your blog is currently hidden from search engines and the discover feed"

### Home Page Editor
- **Buttons**: Publish, View
- **Attributes** (collapsible):
  - title: Blog title
  - favicon: Emoji favicon
- **Content**: Markdown textarea
- **Footer links**: Markdown syntax, Insert media, Media library

### Posts Management
- **Posts list**: Shows date and title
- **Actions**: New post, Edit template
- **Post editor**:
  - Buttons: Back, Publish, Save as draft
  - Attributes (all optional):
    - title: Post title
    - link: URL slug
    - alias: Old URL redirect
    - canonical_url: Canonical URL
    - published_date: YYYY-MM-DD HH:MM
    - is_page: false (for posts)
    - meta_description: SEO description
    - meta_image: Social media image
    - lang: Language code
    - tags: Comma-separated tags
    - make_discoverable: true/false
    - class_name: Custom CSS class
  - Title field
  - Content textarea
  - Footer: Markdown syntax, Insert media, Media, Preview

### Pages Management
- Same as posts but with is_page: true

### Navigation Editor
- Customize blog navigation menu

### Email Subscribers
- List of email subscribers
- Email capture management

### Analytics Dashboard
- **Free tier**: 
  - Past 7 days only
  - Shows unique reads and visitors
  - Simple line graph
- **Upgrade prompt**: Links to upgrade for in-depth analytics

### Settings
- **Basic settings**:
  - Subdomain change
  - Language setting
- **Links to**:
  - Custom domain setup
  - Header and footer directives
  - Advanced settings
  - Export all blog data
  - Delete blog

### Theme Customization
- **Pre-built themes** (29 themes):
  Default, Plain HTML, Writer, Bahunya, Sakura, Sakura Vader, Water, Archie, Bloc, Retro, Hilda, Tex, MSDos, Thoughts, Terminal, Vetro, The Bold Type, Starter, Breeze, 8Bit, Docs, Bento, Split tea, Newspaper, OS, Grid, Typewriter, Low Vision Reader, Delightful
- **Each theme**: Preview and Apply buttons
- **Custom CSS editor**:
  - Full CSS editing with CSS variables
  - CodeMirror option for syntax highlighting
  - Publish and View buttons

### Media Management
- Upload and manage images/files
- Insert into posts/pages

### Upgrade Page
**Pricing**: $5/month or $49/year

**Upgrade benefits**:
- Custom domains
- Show up on Discover feed
- Publish up to 10 sites
- Media and file uploading
- In-depth analytics
- Email subscriber capture
- Add JavaScript to page content
- Add code to head and footer elements
- Remove Bear branding (optional)

**Marketing copy**: 
"Upgrade and keep the tiny internet awesome!"
"We don't make money by selling data, tracking readers, or displaying ads. We do it by creating something great and charging a fee for it."

---
