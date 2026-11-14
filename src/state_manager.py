"""
State & Multi-Week Series Saga Manager for Cyber Paparazzi
Tracks ISO week guard, seen URLs, historical weekly continuity, and Periodic-Style Tech Series Sagas.
"""
import json
from datetime import datetime
from typing import Any, Dict, List, Set

from src.config import HISTORY_FILE, SAGAS_FILE, SEEN_URLS_FILE
from src.utils import get_now_bangkok

DEFAULT_SEED_SAGAS: List[Dict[str, Any]] = [
    {
        "saga_id": "frontier-elemental-models",
        "series_title": "The Frontier AI Model Race (Google • OpenAI • Anthropic)",
        "vendor": "Multi-Lab Frontier",
        "episode_badge": "ONGOING SAGA",
        "completion_pct": 65,
        "previously_on": "ค่าย AI ยักษ์ใหญ่แข่งกันปล่อยโมเดล Reasoning และ Multimodal รุ่นใหม่แบบรายสัปดาห์",
        "latest_twist": "กำลังจับตารอบอัปเกรดความเร็วและ Agentic Tool Use ล่าสุดจาก Official Blogs",
        "power_up_multiplier": "⚡ Reasoning & Agent Autonomy Escalation",
        "next_episode_rumor": "จับตาการปล่อยรุ่นเรือธงถัดไปและสงครามราคา API",
        "element_roster": [
            {
                "number": "01",
                "symbol": "Gm",
                "name": "Gemini",
                "role_tag": "Multimodal Core",
                "multiplier_badge": "Long Context",
                "status": "UNLOCKED",
            },
            {
                "number": "02",
                "symbol": "Cl",
                "name": "Claude",
                "role_tag": "Coding Precision",
                "multiplier_badge": "Agentic CLI",
                "status": "UNLOCKED",
            },
            {
                "number": "03",
                "symbol": "Gp",
                "name": "GPT / o-Series",
                "role_tag": "Frontier Reasoning",
                "multiplier_badge": "Next Wave",
                "status": "RUMORED",
            },
        ],
    },
    {
        "saga_id": "silicon-titan-war",
        "series_title": "Next-Gen AI Silicon War (NVIDIA • Apple • AMD)",
        "vendor": "Silicon Titans",
        "episode_badge": "ONGOING SAGA",
        "completion_pct": 60,
        "previously_on": "ศึกชิป AI ดุเดือดตั้งแต่ Data Center GPU ไปจนถึงชิป NPU บนโน้ตบุ๊กและเครื่อง Local AI",
        "latest_twist": "สายสืบจับตา Bandwidth หน่วยความจำและประสิทธิภาพต่อวัตต์ (Perf/Watt)",
        "power_up_multiplier": "🔥 High-Bandwidth Memory & Edge NPU",
        "next_episode_rumor": "รุ่นถัดไปของ GPU/Unified Memory สำหรับ Local AI",
        "element_roster": [
            {
                "number": "14",
                "symbol": "Nv",
                "name": "NVIDIA",
                "role_tag": "Data Center King",
                "multiplier_badge": "CUDA Dominance",
                "status": "UNLOCKED",
            },
            {
                "number": "15",
                "symbol": "Ap",
                "name": "Apple Silicon",
                "role_tag": "Unified Memory",
                "multiplier_badge": "Edge Efficiency",
                "status": "UNLOCKED",
            },
            {
                "number": "16",
                "symbol": "Am",
                "name": "AMD ROCm",
                "role_tag": "Challenger",
                "multiplier_badge": "Value/VRAM",
                "status": "RUMORED",
            },
        ],
    },
    {
        "saga_id": "open-weight-uprising",
        "series_title": "Open-Weight & Local AI Rebellion",
        "vendor": "Open-Source Ecosystem",
        "episode_badge": "ONGOING SAGA",
        "completion_pct": 70,
        "previously_on": "โมเดลเปิดเสรีไล่บี้โมเดลปิดแบบหายใจรดต้นคอ รันบนเครื่องส่วนตัวผ่าน Ollama/vLLM ได้แรงขึ้นเรื่อยๆ",
        "latest_twist": "ติดตามโมเดลเปิดและงานวิจัย Hugging Face ประจำสัปดาห์นี้",
        "power_up_multiplier": "🦙 Local GPU & 100% Privacy",
        "next_episode_rumor": "โมเดลขนาดเล็กฉลาดเทียบเท่ารุ่นยักษ์",
        "element_roster": [
            {
                "number": "21",
                "symbol": "Ds",
                "name": "DeepSeek",
                "role_tag": "Reasoning Open",
                "multiplier_badge": "Cost Killer",
                "status": "UNLOCKED",
            },
            {
                "number": "22",
                "symbol": "Qw",
                "name": "Qwen",
                "role_tag": "Multilingual/Code",
                "multiplier_badge": "Edge Champion",
                "status": "UNLOCKED",
            },
            {
                "number": "23",
                "symbol": "Lm",
                "name": "Llama / Gemma",
                "role_tag": "Ecosystem Anchor",
                "multiplier_badge": "Next Drop",
                "status": "RUMORED",
            },
        ],
    },
]


def _load_json(path, default):
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _save_json(path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_current_week_identifier(dt: datetime | None = None) -> str:
    """Return Year-Week string e.g. '2026-W46'."""
    if dt is None:
        dt = get_now_bangkok()
    year, week_num, _ = dt.isocalendar()
    return f"{year}-W{week_num:02d}"


def load_history() -> List[Dict[str, Any]]:
    data = _load_json(HISTORY_FILE, [])
    return data if isinstance(data, list) else []


def is_current_week_already_reported() -> bool:
    current_week = get_current_week_identifier()
    return any(entry.get("week_id") == current_week for entry in load_history())


def append_weekly_history(week_id: str, date_str: str, episode_title: str, topics: List[Dict[str, Any]]) -> None:
    history = [h for h in load_history() if h.get("week_id") != week_id]
    history.append({
        "week_id": week_id,
        "date": date_str,
        "episode_title": episode_title,
        "topics": topics,
        "updated_at": get_now_bangkok().isoformat(),
    })
    _save_json(HISTORY_FILE, history[-30:])


def get_recent_history_context(max_weeks: int = 3) -> str:
    history = load_history()
    if not history:
        return "ยังไม่มีประวัติการออกอากาศสัปดาห์ก่อนหน้า (Episode 1 — Season Premiere)"
    blocks = []
    for entry in history[-max_weeks:]:
        w_id = entry.get("week_id", "")
        d_str = entry.get("date", "")
        ep_title = entry.get("episode_title", "")
        topic_lines = [f"  - {t.get('title', '')}" for t in entry.get("topics", []) if isinstance(t, dict)]
        blocks.append(f"[{w_id} | {d_str}] {ep_title}\n" + "\n".join(topic_lines))
    return "\n\n".join(blocks)


def load_seen_urls() -> Set[str]:
    data = _load_json(SEEN_URLS_FILE, [])
    return set(data) if isinstance(data, list) else set()


def save_seen_urls(new_urls: List[str]) -> None:
    existing = _load_json(SEEN_URLS_FILE, [])
    if not isinstance(existing, list):
        existing = []
    seen_set = set(existing)
    merged = list(existing)
    for url in new_urls:
        if url and url not in seen_set:
            merged.append(url)
            seen_set.add(url)
    _save_json(SEEN_URLS_FILE, merged[-500:])


def load_sagas() -> List[Dict[str, Any]]:
    data = _load_json(SAGAS_FILE, None)
    if isinstance(data, list) and data:
        return data
    _save_json(SAGAS_FILE, DEFAULT_SEED_SAGAS)
    return DEFAULT_SEED_SAGAS


def get_sagas_context_for_prompt() -> str:
    sagas = load_sagas()
    return json.dumps(sagas, ensure_ascii=False, indent=2)


def update_sagas(updated_sagas: List[Dict[str, Any]]) -> None:
    if isinstance(updated_sagas, list) and updated_sagas:
        _save_json(SAGAS_FILE, updated_sagas[:5])
