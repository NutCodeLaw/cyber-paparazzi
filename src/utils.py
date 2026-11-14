"""
Utility functions for Cyber Paparazzi (Bangkok Timezone, Date Parsing, Visual Bars)
"""
import re
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from typing import Optional

# Thai timezone UTC+7
BANGKOK_TZ = timezone(timedelta(hours=7))

THAI_MONTHS = [
    "",
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม",
]

THAI_WEEKDAYS = [
    "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"
]


def get_now_bangkok() -> datetime:
    """Return current datetime in Asia/Bangkok."""
    return datetime.now(BANGKOK_TZ)


def format_thai_date(dt: Optional[datetime] = None) -> str:
    """Format datetime into Thai date string: '15 พฤศจิกายน 2569'."""
    if dt is None:
        dt = get_now_bangkok()
    thai_year = dt.year + 543
    month_name = THAI_MONTHS[dt.month]
    return f"{dt.day} {month_name} {thai_year}"


def format_thai_full_date(dt: Optional[datetime] = None) -> str:
    """Format datetime with weekday: 'วันอาทิตย์ที่ 15 พฤศจิกายน 2569'."""
    if dt is None:
        dt = get_now_bangkok()
    weekday_name = THAI_WEEKDAYS[dt.weekday()]
    return f"วัน{weekday_name}ที่ {format_thai_date(dt)}"


def get_iso_date(dt: Optional[datetime] = None) -> str:
    """Return ISO format YYYY-MM-DD."""
    if dt is None:
        dt = get_now_bangkok()
    return dt.strftime("%Y-%m-%d")


def parse_pub_date(date_str: str) -> Optional[datetime]:
    """Safely parse RFC-2822 or ISO-8601 publication timestamps into aware UTC datetime."""
    if not date_str:
        return None
    cleaned = date_str.strip()
    try:
        dt = parsedate_to_datetime(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass
    try:
        iso_str = cleaned.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def make_emoji_bar(
    score: int,
    fill_emoji: str = "🟦",
    empty_emoji: str = "⬜",
    length: int = 5,
) -> str:
    """Build compact emoji progress bar for visual Markdown dossiers."""
    clamped = max(0, min(100, int(score)))
    filled = round((clamped / 100.0) * length)
    return (fill_emoji * filled) + (empty_emoji * (length - filled))


def strip_html_tags(text: str, max_len: int = 240) -> str:
    """Clean HTML markup from RSS descriptions into crisp single-line snippet."""
    if not text:
        return ""
    no_tags = re.sub(r"<[^>]+>", " ", text)
    collapsed = re.sub(r"\s+", " ", no_tags).strip()
    if len(collapsed) > max_len:
        return collapsed[: max_len - 3].rstrip() + "..."
    return collapsed


def safe_mermaid_label(text: str, max_len: int = 38) -> str:
    """Sanitize text for safe embedding inside Mermaid node labels."""
    cleaned = re.sub(r'["`\[\]\(\)\n\r<>]', " ", str(text or ""))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) > max_len:
        cleaned = cleaned[: max_len - 3].rstrip() + "..."
    return cleaned or "Node"
