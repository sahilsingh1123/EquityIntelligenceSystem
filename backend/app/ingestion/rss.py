import re
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
import httpx

from app.core.enums import SourceTrustTier, SourceType
from app.ingestion.base import IngestionSource
from app.models.schemas import DocumentCreate, Source


class RSSNewsIngestSource(IngestionSource):
    def __init__(
        self,
        name: str,
        feed_url: str,
        trust_tier: SourceTrustTier = SourceTrustTier.TIER_3,
        trust_weight: int = 7,
    ):
        self.name = name
        self.feed_url = feed_url
        self.trust_tier = trust_tier
        self.trust_weight = trust_weight

    async def fetch(self) -> list[DocumentCreate]:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.feed_url, headers=headers, timeout=15.0)
                response.raise_for_status()
            except Exception as e:
                print(f"Error fetching RSS feed from {self.feed_url}: {e}")
                return []

        try:
            root = ET.fromstring(response.content)
        except Exception as e:
            print(f"Error parsing RSS XML from {self.feed_url}: {e}")
            return []

        documents: list[DocumentCreate] = []
        for item in root.findall(".//item"):
            title_el = item.find("title")
            link_el = item.find("link")
            pub_date_el = item.find("pubDate")
            desc_el = item.find("description")

            title_text = title_el.text if title_el is not None else ""
            link_text = link_el.text if link_el is not None else ""
            desc_text = desc_el.text if desc_el is not None else ""

            if desc_text:
                desc_text = re.sub(r"<[^>]*>", "", desc_text)

            published_at = datetime.now()
            if pub_date_el is not None and pub_date_el.text:
                try:
                    published_at = parsedate_to_datetime(pub_date_el.text)
                except Exception:
                    pass

            doc = DocumentCreate(
                source=Source(
                    name=self.name,
                    trust_tier=self.trust_tier,
                    trust_weight=self.trust_weight,
                ),
                source_type=SourceType.NEWS,
                url=link_text if link_text else None,
                title=title_text,
                content=desc_text if desc_text else title_text,
                published_at=published_at,
                metadata={},
            )
            documents.append(doc)

        return documents
