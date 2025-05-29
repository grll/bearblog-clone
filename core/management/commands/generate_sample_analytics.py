from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from core.models import PageView, Post, DailyAnalytics


class Command(BaseCommand):
    help = "Generate sample analytics data for testing"

    def handle(self, *args, **options):
        self.stdout.write("Generating sample analytics data...")

        # Get all published posts
        posts = list(Post.objects.filter(published=True))
        if not posts:
            self.stdout.write(
                self.style.WARNING(
                    "No published posts found. Creating sample data without posts."
                )
            )

        # Paths to simulate
        paths = ["/", "/blog/", "/about/"]
        if posts:
            paths.extend([f"/blog/{post.slug}/" for post in posts])

        # Generate data for the last 7 days
        end_date = timezone.now()

        # Clear ALL existing data for clean sample
        PageView.objects.all().delete()
        DailyAnalytics.objects.all().delete()

        # Generate page views for each day
        for day_offset in range(7):
            current_date = end_date - timedelta(days=day_offset)

            # Match the exact pattern from the screenshot
            # Working backwards from today (2025-05-29)
            if day_offset == 6:  # 2025-05-23
                num_visitors = 0
            elif day_offset == 5:  # 2025-05-24
                num_visitors = 0
            elif day_offset == 4:  # 2025-05-25
                num_visitors = 0
            elif day_offset == 3:  # 2025-05-26
                num_visitors = random.randint(65, 75)  # ~70
            elif day_offset == 2:  # 2025-05-27
                num_visitors = random.randint(140, 150)  # ~145
            elif day_offset == 1:  # 2025-05-28
                num_visitors = random.randint(355, 365)  # ~360
            else:  # day_offset == 0, Today 2025-05-29
                num_visitors = random.randint(60, 70)  # ~65

            unique_ips = []
            unique_sessions = []

            # Generate page views for this day
            for _ in range(num_visitors):
                # Generate unique IP
                ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
                unique_ips.append(ip)

                # Generate session key
                session_key = f"session_{random.randint(1000, 9999)}"
                unique_sessions.append(session_key)

                # Each visitor views 1-3 pages
                num_page_views = random.randint(1, 3)

                for _ in range(num_page_views):
                    # Random timestamp within the day
                    hour = random.randint(0, 23)
                    minute = random.randint(0, 59)
                    view_time = current_date.replace(
                        hour=hour, minute=minute, second=0, microsecond=0
                    )

                    # Select random path
                    path = random.choice(paths)

                    # Determine if this is a post
                    post = None
                    if path.startswith("/blog/") and path != "/blog/" and posts:
                        # Try to match with a post
                        slug = path.strip("/").split("/")[-1]
                        matching_posts = [p for p in posts if p.slug == slug]
                        if matching_posts:
                            post = matching_posts[0]

                    # Create page view
                    PageView.objects.create(
                        post=post,
                        path=path,
                        ip_address=ip,
                        user_agent="Mozilla/5.0 (Sample Analytics Generator)",
                        referrer="https://google.com" if random.random() > 0.5 else "",
                        timestamp=view_time,
                        session_key=session_key,
                    )

            # Aggregate analytics for this day
            if num_visitors > 0:
                # Count unique reads (views on posts)
                post_views = (
                    PageView.objects.filter(
                        timestamp__date=current_date.date(), post__isnull=False
                    )
                    .values("session_key", "ip_address")
                    .distinct()
                    .count()
                )

                DailyAnalytics.objects.create(
                    date=current_date.date(),
                    unique_visitors=len(set(unique_ips)),
                    unique_reads=post_views,
                    total_views=PageView.objects.filter(
                        timestamp__date=current_date.date()
                    ).count(),
                )

        self.stdout.write(
            self.style.SUCCESS("Sample analytics data generated successfully!")
        )
