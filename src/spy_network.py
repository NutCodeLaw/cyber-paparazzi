"""
Spy Network Module - Resilient 3-Tier Official & Tier-1 Tech Intelligence Fetcher
"""
import gzip
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Set

from src.config import (
    DIRECT_RSS_FEEDS,
    GOOGLE_NEWS_SPY_QUERIES,
    HUGGINGFACE_DAILY_PAPERS_API,
)
from src.utils import parse_pub_date, strip_html_tags

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/atom+xml, application/xml, application/json, text/xml;q=0.9, */*;q=0.8",
}


def _strip_ns(tag: str) -> str:
    """Strip XML namespace prefix from tag name."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _find_child_text(element: ET.Element, target_names: List[str]) -> str:
    """Find text of first matching child tag regardless of XML namespace."""
    for child in element:
        local = _strip_ns(child.tag).lower()
        if local in target_names:
            text = "".join(child.itertext()).strip()
            if text:
                return text
    return ""


def _extract_atom_link(entry: ET.Element) -> str:
    """Extract href or text link from an Atom <entry> or RSS <item>."""
    fallback = ""
    for child in entry:
        if _strip_ns(child.tag).lower() == "link":
            href = child.attrib.get("href", "").strip()
            rel = child.attrib.get("rel", "alternate").strip().lower()
            if href and rel == "alternate":
                return href
            if href and not fallback:
                fallback = href
            if child.text and child.text.strip():
                return child.text.strip()
    return fallback


def fetch_direct_rss(feed_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch and normalize RSS 2.0 or Atom feed."""
    name = feed_cfg["name"]
    url = feed_cfg["url"]
    tier = feed_cfg["tier"]
    track_hint = feed_cfg["track_hint"]
    limit = int(feed_cfg.get("limit", 6))
    articles: List[Dict[str, Any]] = []

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml_bytes = resp.read()
        if xml_bytes[:2] == b"\x1f\x8b":
            xml_bytes = gzip.decompress(xml_bytes)

        root = ET.fromstring(xml_bytes)
        entries = [
            el for el in root.iter()
            if _strip_ns(el.tag).lower() in ("item", "entry")
        ]

        for entry in entries[:limit]:
            title = _find_child_text(entry, ["title"])
            link = _extract_atom_link(entry)
            pub_raw = _find_child_text(entry, ["pubdate", "published", "updated", "date"])
            desc_raw = _find_child_text(entry, ["description", "summary", "content"])
            snippet = strip_html_tags(desc_raw, max_len=220)

            if title and link.startswith(("http://", "https://")):
                articles.append({
                    "title": re.sub(r"\s+", " ", title).strip(),
                    "url": link.strip(),
                    "source": name,
                    "tier": tier,
                    "track_hint": track_hint,
                    "pub_date": pub_raw,
                    "summary_snippet": snippet,
                })

        return {"name": name, "ok": True, "count": len(articles), "articles": articles, "error": ""}
    except Exception as exc:
        return {"name": name, "ok": False, "count": 0, "articles": [], "error": str(exc)}


def fetch_google_news_rss(query_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch resilient domain-pinned or topic-pinned news via Google News RSS."""
    name = query_cfg["name"]
    query = query_cfg["query"]
    tier = query_cfg["tier"]
    track_hint = query_cfg["track_hint"]
    limit = int(query_cfg.get("limit", 8))
    articles: List[Dict[str, Any]] = []

    try:
        encoded_q = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml_bytes = resp.read()
        if xml_bytes[:2] == b"\x1f\x8b":
            xml_bytes = gzip.decompress(xml_bytes)

        root = ET.fromstring(xml_bytes)
        items = root.findall(".//item")

        for item in items[:limit]:
            raw_title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub_raw = (item.findtext("pubDate") or "").strip()
            source_el = item.find("source")
            source_name = source_el.text.strip() if source_el is not None and source_el.text else name
            clean_title = raw_title.rsplit(" - ", 1)[0].strip() if " - " in raw_title else raw_title

            if clean_title and link.startswith(("http://", "https://")):
                articles.append({
                    "title": clean_title,
                    "url": link,
                    "source": source_name,
                    "tier": tier,
                    "track_hint": track_hint,
                    "pub_date": pub_raw,
                    "summary_snippet": "",
                })

        return {"name": name, "ok": True, "count": len(articles), "articles": articles, "error": ""}
    except Exception as exc:
        return {"name": name, "ok": False, "count": 0, "articles": [], "error": str(exc)}


def fetch_huggingface_papers(limit: int = 6) -> Dict[str, Any]:
    """Fetch top trending AI research papers & open models from Hugging Face Daily Papers API."""
    name = "Hugging Face Daily Papers"
    articles: List[Dict[str, Any]] = []
    try:
        req = urllib.request.Request(HUGGINGFACE_DAILY_PAPERS_API, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if isinstance(data, list):
            for row in data[:limit]:
                paper = row.get("paper", {}) if isinstance(row, dict) else {}
                paper_id = paper.get("id", "")
                title = (paper.get("title") or row.get("title") or "").strip()
                summary = strip_html_tags(paper.get("summary") or "", max_len=220)
                upvotes = paper.get("upvotes", 0)
                pub_raw = row.get("publishedAt") or paper.get("publishedAt") or ""

                if title and paper_id:
                    articles.append({
                        "title": f"{title} ({upvotes} upvotes)",
                        "url": f"https://huggingface.co/papers/{paper_id}",
                        "source": "Hugging Face Papers",
                        "tier": "Tier-3 Dev Pulse",
                        "track_hint": "local_open_ai",
                        "pub_date": pub_raw,
                        "summary_snippet": summary,
                    })

        return {"name": name, "ok": True, "count": len(articles), "articles": articles, "error": ""}
    except Exception as exc:
        return {"name": name, "ok": False, "count": 0, "articles": [], "error": str(exc)}


def collect_spy_intel(
    seen_urls: Set[str] | None = None,
    lookback_days: int = 10,
    ignore_seen: bool = False,
) -> Dict[str, Any]:
    """
    Dispatch Spy Agents concurrently across Tier 1-3 feeds,
    filter to the recent weekly window, and deduplicate.
    """
    seen_urls = seen_urls or set()
    now_utc = datetime.now(timezone.utc)
    cutoff_dt = now_utc - timedelta(days=lookback_days)

    raw_results: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch_direct_rss, cfg) for cfg in DIRECT_RSS_FEEDS]
        futures.extend(executor.submit(fetch_google_news_rss, q) for q in GOOGLE_NEWS_SPY_QUERIES)
        futures.append(executor.submit(fetch_huggingface_papers, 6))

        for fut in as_completed(futures):
            raw_results.append(fut.result())

    candidate_articles: List[Dict[str, Any]] = []
    feed_health: List[Dict[str, Any]] = []
    for res in raw_results:
        feed_health.append({
            "name": res["name"],
            "ok": res["ok"],
            "count": res["count"],
            "error": res["error"],
        })
        candidate_articles.extend(res["articles"])

    # Deduplicate and filter by lookback window
    seen_local_urls: Set[str] = set()
    seen_local_titles: Set[str] = set()
    recent_pool: List[Dict[str, Any]] = []
    fresh_unseen: List[Dict[str, Any]] = []

    for art in candidate_articles:
        url = art["url"]
        norm_title = re.sub(r"[^a-z0-9]+", " ", art["title"].lower()).strip()
        if not url or url in seen_local_urls or norm_title in seen_local_titles:
            continue

        parsed_dt = parse_pub_date(art.get("pub_date", ""))
        if parsed_dt is not None and parsed_dt < cutoff_dt:
            continue

        seen_local_urls.add(url)
        seen_local_titles.add(norm_title)
        recent_pool.append(art)

        if ignore_seen or url not in seen_urls:
            fresh_unseen.append(art)

    # Graceful fallback if repeated same-day runs exhaust unseen pool
    selected = fresh_unseen if len(fresh_unseen) >= 12 else recent_pool

    items_by_track: Dict[str, List[Dict[str, Any]]] = {
        "ai_frontier": [],
        "hardware_silicon": [],
        "software_devtools": [],
        "local_open_ai": [],
        "deep_tech": [],
    }
    for art in selected:
        track = art.get("track_hint", "ai_frontier")
        items_by_track.setdefault(track, []).append(art)

    ok_feeds = sum(1 for f in feed_health if f["ok"] and f["count"] > 0)
    return {
        "all_items": selected,
        "items_by_track": items_by_track,
        "feed_health": sorted(feed_health, key=lambda x: x["name"]),
        "stats": {
            "total_feeds": len(feed_health),
            "active_feeds": ok_feeds,
            "raw_candidates": len(candidate_articles),
            "recent_deduped": len(recent_pool),
            "selected_count": len(selected),
        },
    }


if __name__ == "__main__":
    intel = collect_spy_intel(ignore_seen=True)
    print(f"Stats: {intel['stats']}")
    for fh in intel["feed_health"]:
        status = "OK" if fh["ok"] else f"ERR ({fh['error']})"
        print(f" - {fh['name']}: {fh['count']} items [{status}]")
    print("\nSample intercepted headlines:")
    for item in intel["all_items"][:8]:
        print(f" [{item['tier']} | {item['track_hint']}] {item['source']}: {item['title']}")
