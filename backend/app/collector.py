import feedparser, httpx
from datetime import datetime, timezone
from .sources import RSS_SOURCES, KEY_TERMS
from .classifier import classify, make_id

async def fetch_rss_source(source):
    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        response = await client.get(source["url"])
        response.raise_for_status()
    feed = feedparser.parse(response.text)
    items = []
    for e in feed.entries[:30]:
        title = (e.get("title") or "").strip()
        url = (e.get("link") or "").strip()
        summary = (e.get("summary") or e.get("description") or "").strip()
        text = f"{title} {summary}".lower()
        if not any(term in text for term in KEY_TERMS):
            continue
        published = e.get("published_parsed") or e.get("updated_parsed")
        if published:
            dt = datetime(*published[:6], tzinfo=timezone.utc)
        else:
            dt = datetime.now(timezone.utc)
        banks, topics, score, impact = classify(title, summary)
        items.append({
            "id": make_id(url),
            "title": title,
            "source": source["name"],
            "url": url,
            "published_at": dt.isoformat(),
            "summary": summary[:800],
            "bank_tags": banks,
            "topic_tags": topics,
            "relevance_score": round(score, 3),
            "impact_level": impact
        })
    return items

async def collect_news():
    all_items = {}
    for source in RSS_SOURCES:
        try:
            for item in await fetch_rss_source(source):
                all_items[item["id"]] = item
        except Exception as exc:
            print(f"Source failed: {source['name']} | {exc}")
    return sorted(all_items.values(), key=lambda x: (x["relevance_score"], x["published_at"]), reverse=True)[:80]
