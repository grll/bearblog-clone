from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import PageView, DailyAnalytics


class Command(BaseCommand):
    help = "Aggregate daily analytics from page views"

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            help="Specific date to aggregate (YYYY-MM-DD format)",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=1,
            help="Number of days to aggregate (default: 1)",
        )

    def handle(self, *args, **options):
        if options["date"]:
            # Aggregate specific date
            date = datetime.strptime(options["date"], "%Y-%m-%d").date()
            self.aggregate_date(date)
        else:
            # Aggregate last N days
            days = options["days"]
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=days)

            current_date = start_date
            while current_date <= end_date:
                self.aggregate_date(current_date)
                current_date += timedelta(days=1)

    def aggregate_date(self, date):
        """Aggregate analytics for a specific date."""
        self.stdout.write(f"Aggregating analytics for {date}...")

        # Get page views for the date
        start_datetime = timezone.make_aware(
            datetime.combine(date, datetime.min.time())
        )
        end_datetime = timezone.make_aware(datetime.combine(date, datetime.max.time()))

        page_views = PageView.objects.filter(
            timestamp__gte=start_datetime, timestamp__lte=end_datetime
        )

        # Calculate unique visitors (by IP)
        unique_visitors = page_views.values("ip_address").distinct().count()

        # Calculate unique reads (unique session/IP combinations on posts)
        post_views = page_views.filter(post__isnull=False)
        unique_reads = post_views.values("session_key", "ip_address").distinct().count()

        # Total page views
        total_views = page_views.count()

        # Create or update daily analytics
        analytics, created = DailyAnalytics.objects.update_or_create(
            date=date,
            defaults={
                "unique_visitors": unique_visitors,
                "unique_reads": unique_reads,
                "total_views": total_views,
            },
        )

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} analytics for {date}: "
                f"{unique_visitors} visitors, {unique_reads} reads, {total_views} views"
            )
        )
