import asyncio
import traceback
from apscheduler.schedulers.background import BackgroundScheduler

from app.api.v1.dependencies import pipeline
from app.core.enums import SourceTrustTier
from app.ingestion.rss import RSSNewsIngestSource

# We define the search feeds we want to crawl
FEEDS = [
    {
        "name": "Google News Finance",
        "url": "https://news.google.com/rss/search?q=Nifty+OR+Sensex+OR+Indian+stock+market+when:2h&hl=en-IN&gl=IN&ceid=IN:en",
        "trust_tier": SourceTrustTier.TIER_3,
        "trust_weight": 7,
    },
    {
        "name": "Corporate Updates",
        "url": "https://news.google.com/rss/search?q=NSE+OR+BSE+earnings+OR+dividend+OR+acquisition+when:2h&hl=en-IN&gl=IN&ceid=IN:en",
        "trust_tier": SourceTrustTier.TIER_3,
        "trust_weight": 8,
    },
]

scheduler = BackgroundScheduler()


def run_async_task(coro):
    """Helper to run async functions in a synchronous background job scheduler thread."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    except Exception as e:
        print(f"Error executing async task in thread: {e}")
        traceback.print_exc()
    finally:
        try:
            loop.close()
        except Exception:
            pass


async def poll_rss_feeds_job():
    print("[Scheduler] Running background RSS news polling job...")
    count = 0
    for feed in FEEDS:
        source = RSSNewsIngestSource(
            name=feed["name"],
            feed_url=feed["url"],
            trust_tier=feed["trust_tier"],
            trust_weight=feed["trust_weight"],
        )
        documents = await source.fetch()
        print(f"[Scheduler] Fetched {len(documents)} documents from {feed['name']}.")

        for doc in documents:
            try:
                # Ingest document into our pipeline.
                # The normalizer will deduplicate via checksums, so it's safe to ingest repeatedly.
                pipeline.ingest_document(doc)
                count += 1
            except Exception as e:
                # Log error but don't break the ingestion loop
                print(f"[Scheduler] Error ingesting document '{doc.title}': {e}")

    print(f"[Scheduler] Done. Ingested/processed {count} documents total in this run.")


def start_scheduler():
    # Schedule to poll feeds every 2 hours
    scheduler.add_job(
        lambda: run_async_task(poll_rss_feeds_job()),
        "interval",
        hours=2,
        id="poll_rss_feeds_job",
        replace_existing=True,
    )
    # Also trigger it immediately on boot
    scheduler.add_job(
        lambda: run_async_task(poll_rss_feeds_job()),
        id="poll_rss_feeds_job_initial",
    )
    scheduler.start()
    print("[Scheduler] Started background scheduler successfully.")


def shutdown_scheduler():
    scheduler.shutdown()
    print("[Scheduler] Shutdown background scheduler successfully.")
