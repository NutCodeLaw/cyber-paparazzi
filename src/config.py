"""
Cyber Paparazzi Configuration Module
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
DATA_DIR = ROOT_DIR / "data"
ARCHIVES_DIR = ROOT_DIR / "archives"
WEB_DIR = ROOT_DIR / "web"

LATEST_MD_PATH = ROOT_DIR / "LATEST.md"
README_MD_PATH = ROOT_DIR / "README.md"
INDEX_HTML_PATH = WEB_DIR / "index.html"
ROOT_INDEX_HTML_PATH = ROOT_DIR / "index.html"

HISTORY_FILE = DATA_DIR / "history.json"
SEEN_URLS_FILE = DATA_DIR / "seen_urls.json"
SAGAS_FILE = DATA_DIR / "sagas.json"
LATEST_JSON_PATH = DATA_DIR / "latest.json"
ARCHIVE_INDEX_PATH = DATA_DIR / "archive_index.json"

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

# API Keys & Telegram Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1003712039650").strip()

# AI Models (Flagship LOW-thinking primary + non-deprecated GA fallbacks)
GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest",
]

# 5 Core Spy Tracks
SPY_TRACKS = {
    "ai_frontier": {
        "id": "ai_frontier",
        "name": "AI Frontier War",
        "name_th": "สมรภูมิ AI มหาอำนาจ",
        "icon": "🤖",
        "color": "#06b6d4",
    },
    "hardware_silicon": {
        "id": "hardware_silicon",
        "name": "Hardware & Silicon",
        "name_th": "ชิปประมวลผล & ฮาร์ดแวร์ล้ำยุค",
        "icon": "🖥️",
        "color": "#f59e0b",
    },
    "software_devtools": {
        "id": "software_devtools",
        "name": "Software, OS & DevTools",
        "name_th": "ซอฟต์แวร์, OS & เครื่องมือนักพัฒนา",
        "icon": "🛠️",
        "color": "#8b5cf6",
    },
    "local_open_ai": {
        "id": "local_open_ai",
        "name": "Open-Weight & Local AI",
        "name_th": "โมเดลเปิดเสรี & Local AI รันในเครื่อง",
        "icon": "🦙",
        "color": "#10b981",
    },
    "deep_tech": {
        "id": "deep_tech",
        "name": "Deep Tech & Wildcards",
        "name_th": "เทคโนโลยีอนาคต หุ่นยนต์ & ควอนตัม",
        "icon": "🧬",
        "color": "#ec4899",
    },
}

# 3-Tier Trusted Spy Network Sources
DIRECT_RSS_FEEDS = [
    # Tier 1: Official AI Labs & Hardware/Software Vendors
    {
        "name": "OpenAI Newsroom",
        "url": "https://openai.com/news/rss.xml",
        "tier": "Tier-1 Official",
        "track_hint": "ai_frontier",
        "limit": 6,
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "tier": "Tier-1 Official",
        "track_hint": "ai_frontier",
        "limit": 6,
    },
    {
        "name": "Google DeepMind Blog",
        "url": "https://blog.google/innovation-and-ai/models-and-research/google-deepmind/rss/",
        "tier": "Tier-1 Official",
        "track_hint": "ai_frontier",
        "limit": 5,
    },
    {
        "name": "NVIDIA Official Blog",
        "url": "https://blogs.nvidia.com/feed/",
        "tier": "Tier-1 Official",
        "track_hint": "hardware_silicon",
        "limit": 6,
    },
    {
        "name": "Microsoft DevBlogs",
        "url": "https://devblogs.microsoft.com/feed/",
        "tier": "Tier-1 Official",
        "track_hint": "software_devtools",
        "limit": 5,
    },
    {
        "name": "Apple Newsroom",
        "url": "https://www.apple.com/newsroom/rss-feed.rss",
        "tier": "Tier-1 Official",
        "track_hint": "hardware_silicon",
        "limit": 5,
    },
    # Tier 2: Tier-1 Global Tech & Hardware Press
    {
        "name": "Ars Technica",
        "url": "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "tier": "Tier-2 Tech Press",
        "track_hint": "software_devtools",
        "limit": 7,
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "tier": "Tier-2 Tech Press",
        "track_hint": "hardware_silicon",
        "limit": 7,
    },
    {
        "name": "Tom's Hardware",
        "url": "https://www.tomshardware.com/feeds/all",
        "tier": "Tier-2 Tech Press",
        "track_hint": "hardware_silicon",
        "limit": 7,
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "tier": "Tier-2 Tech Press",
        "track_hint": "deep_tech",
        "limit": 5,
    },
    {
        "name": "IEEE Spectrum",
        "url": "https://spectrum.ieee.org/feeds/feed.rss",
        "tier": "Tier-2 Tech Press",
        "track_hint": "deep_tech",
        "limit": 5,
    },
    # Tier 3: Developer & Open-Source Pulse
    {
        "name": "GitHub Blog",
        "url": "https://github.blog/feed/",
        "tier": "Tier-3 Dev Pulse",
        "track_hint": "software_devtools",
        "limit": 6,
    },
]

# Domain-pinned & Track-specific Google News RSS Backup Queries
GOOGLE_NEWS_SPY_QUERIES = [
    {
        "name": "Official AI Labs Wiretap (Anthropic/Meta/OpenAI/DeepMind)",
        "query": "site:anthropic.com OR site:ai.meta.com OR site:openai.com OR site:deepmind.google",
        "tier": "Tier-1 Official",
        "track_hint": "ai_frontier",
        "limit": 8,
    },
    {
        "name": "Official Silicon & Chips Wiretap (NVIDIA/AMD/Intel/Qualcomm)",
        "query": "(NVIDIA OR AMD OR Intel OR Apple Silicon OR Qualcomm) (GPU OR NPU OR chip OR processor) launch OR announce",
        "tier": "Tier-2 Tech Press",
        "track_hint": "hardware_silicon",
        "limit": 8,
    },
    {
        "name": "Open-Weight & Local AI Wiretap (Llama/DeepSeek/Qwen/Ollama)",
        "query": "(open-weight OR open source LLM OR DeepSeek OR Qwen OR Llama OR Gemma OR Ollama OR vLLM) release OR benchmark",
        "tier": "Tier-3 Dev Pulse",
        "track_hint": "local_open_ai",
        "limit": 8,
    },
    {
        "name": "DevTools, Agents & OS Launches",
        "query": "(AI coding agent OR IDE OR framework OR Linux OR Windows OR macOS) new release OR developer launch",
        "tier": "Tier-2 Tech Press",
        "track_hint": "software_devtools",
        "limit": 6,
    },
    {
        "name": "Deep Tech & Frontier Breakthroughs",
        "query": "(quantum computing OR humanoid robot OR fusion energy OR AI chip breakthrough) 2026",
        "tier": "Tier-2 Tech Press",
        "track_hint": "deep_tech",
        "limit": 6,
    },
]

HUGGINGFACE_DAILY_PAPERS_API = "https://huggingface.co/api/daily_papers"
