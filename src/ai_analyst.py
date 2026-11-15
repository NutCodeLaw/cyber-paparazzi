"""
AI Spy Director & Analyst Module
Synthesizes intercepted official & Tier-1 tech intelligence into a visual, series-driven Strict JSON Dossier.
"""
import json
import re
from typing import Any, Dict, List

from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY, GEMINI_MODELS, SPY_TRACKS
from src.utils import format_thai_full_date, get_now_bangkok


def _format_intel_pool(intel_data: Dict[str, Any]) -> str:
    """Format intercepted articles grouped by track so all domains (AI, HW, SW, Local, DeepTech) get fair coverage."""
    items_by_track = intel_data.get("items_by_track", {})
    sections = []
    for track_id, meta in SPY_TRACKS.items():
        articles = items_by_track.get(track_id, [])[:10]
        if not articles:
            continue
        lines = [f"### {meta['icon']} TRACK [{track_id}] — {meta['name']} ({meta['name_th']})"]
        for idx, art in enumerate(articles, 1):
            snippet = f" | Note: {art['summary_snippet']}" if art.get("summary_snippet") else ""
            lines.append(
                f"{idx}. [{art['tier']} | {art['source']}] {art['title']}\n"
                f"   URL: {art['url']}{snippet}"
            )
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def build_spy_prompt(
    intel_data: Dict[str, Any],
    history_context: str,
    sagas_context: str,
) -> str:
    """Build the Chief Cyber Paparazzi Director prompt."""
    now = get_now_bangkok()
    thai_date = format_thai_full_date(now)
    iso_year, iso_week, _ = now.isocalendar()
    intel_block = _format_intel_pool(intel_data)

    return f"""คุณคือ "Chief Cyber Paparazzi Director" สายสืบข่าวกรองวงการเทคโนโลยีและ AI ระดับโลก
ภารกิจประจำสัปดาห์ที่ {iso_week}/{iso_year} ({thai_date}):
สังเคราะห์ข่าวกรองที่สายสืบดักจับมาจาก Official Blogs, สื่อเทค Tier-1 และ Hugging Face ให้กลายเป็น **"Cyber-Intelligence Spy Dossier สไตล์ซีรีส์สุดมันส์"**

กฎเหล็ก 5 ข้อ (ห้ามฝ่าฝืน):
1. **ห้ามนำเสนอเป็นกำแพงตัวหนังสือ (Zero Plain-Text Walls)**: ทุกข้อความต้องสั้น คม สนุก อ่านจบเร็ว และเน้นตัวเลข/Multiplier/Chips
2. **ยึดข้อเท็จจริงจากข่าวที่ดักจับได้จริงเท่านั้น (100% Grounded)**: ห้ามกุข่าวที่ไม่มีในรายการ และ `source_url` ทุกจุดต้องคัดลอก URL จริงจากรายการด้านล่างแบบตรงตัว
3. **ครบทุกด้าน Hardware + Software + AI + Local AI + Deep Tech**: ต้องกระจาย `top_scoops` และ `launch_radar` ให้ครอบคลุมทั้ง 5 Spy Tracks (`ai_frontier`, `hardware_silicon`, `software_devtools`, `local_open_ai`, `deep_tech`)
4. **เล่าเรื่องแบบ Series / Periodic Table Saga**: เชื่อมโยงพัฒนาการเข้ากับ `Active Sagas` ด้านล่างเหมือนดูซีรีส์ (มี Previously On, จุดหักมุมสัปดาห์นี้, การ์ดธาตุ/รุ่น `element_roster` เช่น `UNLOCKED`, `NEW`, `RUMORED` ตามข้อเท็จจริงของสัปดาห์นี้)
5. **ตอบกลับเป็น Strict JSON ที่ถูกต้องเท่านั้น** (ห้ามใส่ markdown fence หรือข้อความอื่นนอก JSON)

---
[ประวัติรอบสัปดาห์ที่ผ่านมา]
{history_context}

---
[Active Tech Series & Periodic Roster ปัจจุบัน (อัปเดตต่อยอดจากสถานะนี้)]
{sagas_context}

---
[แฟ้มข่าวกรองที่สายสืบดักจับได้จริงในรอบสัปดาห์นี้]
{intel_block}

---
โครงสร้าง JSON ที่ต้องส่งกลับ (ใช้คีย์ภาษาอังกฤษตามสเปกนี้เป๊ะ และเขียนเนื้อหาเป็นภาษาไทยที่อ่านสนุกปนศัพท์เทคนิค):
{{
  "episode_banner": {{
    "season_ep": "SEASON {iso_year} • EP.{iso_week:02d}",
    "episode_title": "ชื่อตอนสุดเท่ประจำสัปดาห์ (ไทยปนอังกฤษสั้นๆ 1 บรรทัด)",
    "heat_score": 85,
    "heat_label": "HIGH VOLTAGE หรือ CODE RED หรือ STEADY PULSE",
    "heat_rationale": "สรุปอุณหภูมิการแข่งขันวงการเทคสัปดาห์นี้ 1 ประโยคสั้นๆ",
    "wiretap_ticker": [
      "BREAKING WIRE 1 สั้นๆ ไม่เกิน 90 ตัวอักษร",
      "BREAKING WIRE 2 สั้นๆ",
      "BREAKING WIRE 3 สั้นๆ"
    ]
  }},
  "tech_series_sagas": [
    {{
      "saga_id": "id เดิมหรือใหม่แบบ slug",
      "series_title": "ชื่อซีรีส์ (เช่น The Frontier AI Race หรือ Silicon Titan War)",
      "vendor": "ค่ายหรือกลุ่มค่าย",
      "episode_badge": "EP.X • ชื่อป้ายสถานะสั้นๆ เช่น NEW DROP หรือ ESCALATION",
      "completion_pct": 75,
      "previously_on": "ความเดิมตอนที่แล้ว 1 ประโยคสั้น",
      "latest_twist": "จุดหักมุมสัปดาห์นี้จากข่าวจริง 1 ประโยคสั้น",
      "power_up_multiplier": "สรุปความแรง/ก้าวกระโดด เช่น ⚡ +Speed / 🧠 Agentic Upgrade",
      "next_episode_rumor": "จับตาตอนต่อไป 1 ประโยคสั้น",
      "element_roster": [
        {{
          "number": "01",
          "symbol": "ตัวอักษรย่อ 2 ตัว เช่น Gm, Nv, Ds",
          "name": "ชื่อโมเดล/ชิป/เทคโนโลยีจริง",
          "role_tag": "บทบาทสั้น 2-3 คำ",
          "multiplier_badge": "จุดเด่นสั้นๆ เช่น 2M Ctx",
          "status": "UNLOCKED หรือ NEW หรือ RUMORED"
        }}
      ]
    }}
  ],
  "weekly_showdown": {{
    "title": "ชื่อศึกมวยคู่เอกสัปดาห์นี้ (เช่น Open-Weight vs Closed Frontier หรือ GPU Battle)",
    "fighter_left": {{
      "name": "ชื่อผู้ท้าชิงฝั่งซ้าย (อิงข่าวจริง)",
      "vendor": "ค่าย",
      "avatar_emoji": "🤖",
      "total_score": 88,
      "special_move": "ท่าไม้ตาย 1 วลี"
    }},
    "fighter_right": {{
      "name": "ชื่อผู้ท้าชิงฝั่งขวา (อิงข่าวจริง)",
      "vendor": "ค่าย",
      "avatar_emoji": "⚡",
      "total_score": 84,
      "special_move": "ท่าไม้ตาย 1 วลี"
    }},
    "winner_verdict": "คำตัดสินสั้นๆ 1 ประโยค ว่าใครได้เปรียบสัปดาห์นี้และเพราะอะไร",
    "rounds": [
      {{
        "metric_name": "ยกที่ 1: ประสิทธิภาพ & ความฉลาด (Performance)",
        "left_pct": 55,
        "right_pct": 45,
        "round_note": "เหตุผลสั้น 1 วลี"
      }},
      {{
        "metric_name": "ยกที่ 2: ความคุ้มค่า & ต้นทุน (Value / Cost)",
        "left_pct": 48,
        "right_pct": 52,
        "round_note": "เหตุผลสั้น 1 วลี"
      }},
      {{
        "metric_name": "ยกที่ 3: อิทธิพลต่อระบบนิเวศ (Ecosystem Impact)",
        "left_pct": 54,
        "right_pct": 46,
        "round_note": "เหตุผลสั้น 1 วลี"
      }}
    ]
  }},
  "ai_arms_race": [
    {{
      "faction": "OpenAI",
      "icon": "🟢",
      "power_score": 88,
      "weekly_delta": 3,
      "stance_badge": "SURGING หรือ DEFENDING หรือ STRIKING หรือ STEALTH",
      "signature_move": "ความเคลื่อนไหวเด่นสัปดาห์นี้สั้นๆ 1 วลี"
    }},
    {{
      "faction": "Google DeepMind",
      "icon": "🔵",
      "power_score": 89,
      "weekly_delta": 5,
      "stance_badge": "SURGING",
      "signature_move": "..."
    }},
    {{
      "faction": "Anthropic",
      "icon": "🟠",
      "power_score": 86,
      "weekly_delta": 2,
      "stance_badge": "STRIKING",
      "signature_move": "..."
    }},
    {{
      "faction": "Meta & Open-Weight",
      "icon": "🦙",
      "power_score": 82,
      "weekly_delta": 4,
      "stance_badge": "SURGING",
      "signature_move": "..."
    }},
    {{
      "faction": "NVIDIA & Silicon",
      "icon": "⚡",
      "power_score": 92,
      "weekly_delta": 2,
      "stance_badge": "DOMINATING",
      "signature_move": "..."
    }},
    {{
      "faction": "xAI & DeepSeek",
      "icon": "🟣",
      "power_score": 80,
      "weekly_delta": 1,
      "stance_badge": "CHALLENGING",
      "signature_move": "..."
    }}
  ],
  "top_scoops": [
    {{
      "track": "หนึ่งใน 5 ค่า: ai_frontier, hardware_silicon, software_devtools, local_open_ai, deep_tech (ขอ 6 ข่าวให้ครบทั้ง 5 track!)",
      "headline": "พาดหัวข่าวสุดจี๊ด ภาษาไทยปนอังกฤษ",
      "paparazzi_hook": "โหมดปาปารัสซี่: เล่าแบบมันส์ๆ แซ่บๆ เห็นภาพการชิงไหวชิงพริบ (2 ประโยคกระชับ)",
      "engineer_spec_summary": "โหมดวิศวกร: สรุปสเปก สถาปัตยกรรม ผลกระทบเชิงเทคนิค/ต้นทุน/การใช้งานจริง (2 ประโยคกระชับ)",
      "spec_chips": ["⚡ สเปก/จุดเด่น 1", "💰 ราคา/สิทธิ์ใช้ 2", "🎯 ผลกระทบ 3"],
      "hype_score": 82,
      "real_impact_score": 86,
      "spy_verdict": "GAME CHANGER หรือ SOLID UPGRADE หรือ OVERHYPED หรือ WATCHLIST",
      "source_name": "ชื่อสื่อต้นทาง",
      "source_url": "URL จริงจากรายการด้านบน"
    }}
  ],
  "action_compass": {{
    "switch_now": [
      {{"item": "เครื่องมือ/โมเดล/ฮาร์ดแวร์ที่ควรลองทันที", "reason": "เหตุผลสั้น 1 ประโยค"}}
    ],
    "wait_next_ep": [
      {{"item": "สิ่งที่ควรรอดูก่อน", "reason": "เหตุผลสั้น 1 ประโยค"}}
    ],
    "skip_hype_trap": [
      {{"item": "กระแสที่อาจเป็น Hype เกินจริงหรือยังไม่คุ้ม", "reason": "เหตุผลสั้น 1 ประโยค"}}
    ]
  }},
  "launch_radar": [
    {{
      "name": "ชื่อผลิตภัณฑ์/โมเดล/ชิป/ซอฟต์แวร์เปิดตัวใหม่",
      "category": "AI Model หรือ Hardware หรือ Software",
      "vendor": "ผู้ผลิต",
      "killer_spec": "ทีเด็ด 1 วลี",
      "availability": "สถานะ เช่น Open-Weight / API / Pre-order / Beta",
      "source_url": "URL จริงจากรายการ"
    }}
  ],
  "track_briefs": [
    {{
      "track": "หนึ่งใน 5 ค่า track",
      "tag": "#TAGสั้นๆ",
      "headline": "พาดหัวสั้น",
      "punchline": "สรุป 1 บรรทัดแบบคมกริบ",
      "source_url": "URL จริงจากรายการ"
    }}
  ],
  "next_week_watchlist": [
    {{
      "window": "ช่วงเวลา เช่น สัปดาห์หน้า / ปลายเดือน",
      "event": "สิ่งที่จะเกิดขึ้นหรือต้องจับตา",
      "hype_level": "HIGH หรือ MEDIUM"
    }}
  ],
  "audio_script_th": "สคริปต์วิทยุสายลับ Cyber Paparazzi ความยาว ~150-220 คำ ภาษาไทยล้วน (อ่านออกเสียงเป็นธรรมชาติ ไม่มีอีโมจิ ไม่มีสัญลักษณ์พิเศษ) เปิดรายการด้วย สวัสดีเช้าวันจันทร์ครับ นี่คือคลื่นลับ Cyber Paparazzi สรุปข่าว IT และ AI รอบสัปดาห์..."
}}"""


def extract_json_from_response(text: str) -> Dict[str, Any]:
    """Strip markdown fences if present and parse JSON reliably."""
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)
    try:
        return json.loads(cleaned)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Unable to extract valid JSON from Gemini output")


def _clamp(val: Any, low: int = 0, high: int = 100, default: int = 50) -> int:
    try:
        return max(low, min(high, int(float(val))))
    except (TypeError, ValueError):
        return default


def _resolve_real_url(candidate_url: str, fallback_pool: List[Dict[str, Any]], idx: int = 0) -> str:
    """Guarantee every URL belongs to a verified fetched article."""
    valid_urls = {a["url"] for a in fallback_pool if a.get("url")}
    if isinstance(candidate_url, str) and candidate_url.strip() in valid_urls:
        return candidate_url.strip()
    if isinstance(candidate_url, str) and candidate_url.strip().startswith(("http://", "https://")):
        # Check domain match if Google/RSS link slightly differed, else pick real pool URL
        for v in valid_urls:
            if candidate_url.strip() in v or v in candidate_url.strip():
                return v
    if fallback_pool:
        return fallback_pool[idx % len(fallback_pool)]["url"]
    return "https://news.google.com"


def sanitize_analysis(raw: Dict[str, Any], intel_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate types, clamp scores, balance tug-of-war rounds, and verify source URLs."""
    pool = intel_data.get("all_items", [])
    valid_tracks = set(SPY_TRACKS.keys())
    track_order = list(SPY_TRACKS.keys())

    # 1. Episode Banner
    banner = raw.get("episode_banner") or {}
    episode_banner = {
        "season_ep": str(banner.get("season_ep") or "SEASON 2026 • WEEKLY DISPATCH"),
        "episode_title": str(banner.get("episode_title") or "สงคราม AI & เทคโนโลยีประจำสัปดาห์"),
        "heat_score": _clamp(banner.get("heat_score"), 0, 100, 82),
        "heat_label": str(banner.get("heat_label") or "HIGH VOLTAGE"),
        "heat_rationale": str(banner.get("heat_rationale") or "การแข่งขันโมเดล AI และชิปประมวลผลเร่งตัวต่อเนื่อง"),
        "wiretap_ticker": [str(x) for x in (banner.get("wiretap_ticker") or []) if x][:5],
    }
    if not episode_banner["wiretap_ticker"]:
        episode_banner["wiretap_ticker"] = [a["title"] for a in pool[:3]]

    # 2. Tech Series Sagas
    sagas_out = []
    for s in (raw.get("tech_series_sagas") or [])[:4]:
        if not isinstance(s, dict):
            continue
        roster = []
        for idx, el in enumerate((s.get("element_roster") or [])[:6], 1):
            if not isinstance(el, dict):
                continue
            status = str(el.get("status") or "UNLOCKED").upper()
            if status not in ("UNLOCKED", "NEW", "RUMORED"):
                status = "UNLOCKED"
            roster.append({
                "number": str(el.get("number") or f"{idx:02d}")[:4],
                "symbol": str(el.get("symbol") or "Ai")[:3],
                "name": str(el.get("name") or "Model"),
                "role_tag": str(el.get("role_tag") or "Core Unit"),
                "multiplier_badge": str(el.get("multiplier_badge") or "Active"),
                "status": status,
            })
        sagas_out.append({
            "saga_id": str(s.get("saga_id") or f"saga-{len(sagas_out)+1}"),
            "series_title": str(s.get("series_title") or "Tech Evolution Saga"),
            "vendor": str(s.get("vendor") or "Industry"),
            "episode_badge": str(s.get("episode_badge") or "ONGOING"),
            "completion_pct": _clamp(s.get("completion_pct"), 0, 100, 70),
            "previously_on": str(s.get("previously_on") or "-"),
            "latest_twist": str(s.get("latest_twist") or "-"),
            "power_up_multiplier": str(s.get("power_up_multiplier") or "⚡ Next-Gen Upgrade"),
            "next_episode_rumor": str(s.get("next_episode_rumor") or "ติดตามตอนต่อไปสัปดาห์หน้า"),
            "element_roster": roster,
        })

    # 3. 1v1 Weekly Showdown
    sd = raw.get("weekly_showdown") or {}
    fl = sd.get("fighter_left") or {}
    fr = sd.get("fighter_right") or {}
    rounds_out = []
    for r in (sd.get("rounds") or [])[:3]:
        if not isinstance(r, dict):
            continue
        lp = _clamp(r.get("left_pct"), 10, 90, 50)
        rp = 100 - lp
        rounds_out.append({
            "metric_name": str(r.get("metric_name") or "Head-to-Head Metric"),
            "left_pct": lp,
            "right_pct": rp,
            "round_note": str(r.get("round_note") or "-"),
        })
    weekly_showdown = {
        "title": str(sd.get("title") or "ศึกมวยคู่เอกประจำสัปดาห์"),
        "fighter_left": {
            "name": str(fl.get("name") or "Contender A"),
            "vendor": str(fl.get("vendor") or "Lab A"),
            "avatar_emoji": str(fl.get("avatar_emoji") or "🤖"),
            "total_score": _clamp(fl.get("total_score"), 0, 100, 86),
            "special_move": str(fl.get("special_move") or "Frontier Speed"),
        },
        "fighter_right": {
            "name": str(fr.get("name") or "Contender B"),
            "vendor": str(fr.get("vendor") or "Lab B"),
            "avatar_emoji": str(fr.get("avatar_emoji") or "⚡"),
            "total_score": _clamp(fr.get("total_score"), 0, 100, 84),
            "special_move": str(fr.get("special_move") or "Open Ecosystem"),
        },
        "winner_verdict": str(sd.get("winner_verdict") or "สูสีดุเดือด ต้องวัดกันที่การใช้งานจริง"),
        "rounds": rounds_out,
    }

    # 4. AI Arms Race
    arms_out = []
    for row in (raw.get("ai_arms_race") or [])[:6]:
        if not isinstance(row, dict):
            continue
        try:
            delta = max(-25, min(25, int(float(row.get("weekly_delta", 0)))))
        except (TypeError, ValueError):
            delta = 0
        arms_out.append({
            "faction": str(row.get("faction") or "Tech Lab"),
            "icon": str(row.get("icon") or "🛰️"),
            "power_score": _clamp(row.get("power_score"), 0, 100, 80),
            "weekly_delta": delta,
            "stance_badge": str(row.get("stance_badge") or "ACTIVE").upper(),
            "signature_move": str(row.get("signature_move") or "-"),
        })

    # 5. Top Scoops
    scoops_out = []
    for idx, sc in enumerate(raw.get("top_scoops") or []):
        if not isinstance(sc, dict):
            continue
        track = str(sc.get("track") or "").strip()
        if track not in valid_tracks:
            track = track_order[idx % len(track_order)]
        verdict = str(sc.get("spy_verdict") or "SOLID UPGRADE").upper()
        if verdict not in ("GAME CHANGER", "SOLID UPGRADE", "OVERHYPED", "WATCHLIST"):
            verdict = "SOLID UPGRADE"
        chips = [str(c) for c in (sc.get("spec_chips") or []) if c][:4]
        if not chips:
            chips = [SPY_TRACKS[track]["name"]]
        scoops_out.append({
            "track": track,
            "headline": str(sc.get("headline") or "Tech Intelligence Scoop"),
            "paparazzi_hook": str(sc.get("paparazzi_hook") or ""),
            "engineer_spec_summary": str(sc.get("engineer_spec_summary") or ""),
            "spec_chips": chips,
            "hype_score": _clamp(sc.get("hype_score"), 0, 100, 75),
            "real_impact_score": _clamp(sc.get("real_impact_score"), 0, 100, 75),
            "spy_verdict": verdict,
            "source_name": str(sc.get("source_name") or "Verified Tech Wire"),
            "source_url": _resolve_real_url(sc.get("source_url", ""), pool, idx),
        })

    # 6. Action Compass
    ac = raw.get("action_compass") or {}
    def _clean_ac_list(items):
        out = []
        for it in (items or [])[:3]:
            if isinstance(it, dict):
                out.append({"item": str(it.get("item") or "-"), "reason": str(it.get("reason") or "-")})
        return out

    action_compass = {
        "switch_now": _clean_ac_list(ac.get("switch_now")),
        "wait_next_ep": _clean_ac_list(ac.get("wait_next_ep")),
        "skip_hype_trap": _clean_ac_list(ac.get("skip_hype_trap")),
    }

    # 7. Launch Radar
    radar_out = []
    for idx, r in enumerate((raw.get("launch_radar") or [])[:10]):
        if not isinstance(r, dict):
            continue
        radar_out.append({
            "name": str(r.get("name") or "Release"),
            "category": str(r.get("category") or "Software"),
            "vendor": str(r.get("vendor") or "-"),
            "killer_spec": str(r.get("killer_spec") or "-"),
            "availability": str(r.get("availability") or "Announced"),
            "source_url": _resolve_real_url(r.get("source_url", ""), pool, idx + 3),
        })

    # 8. Track Briefs
    briefs_out = []
    for idx, b in enumerate((raw.get("track_briefs") or [])[:12]):
        if not isinstance(b, dict):
            continue
        track = str(b.get("track") or "").strip()
        if track not in valid_tracks:
            track = track_order[idx % len(track_order)]
        briefs_out.append({
            "track": track,
            "tag": str(b.get("tag") or "#TECH"),
            "headline": str(b.get("headline") or "-"),
            "punchline": str(b.get("punchline") or "-"),
            "source_url": _resolve_real_url(b.get("source_url", ""), pool, idx + 5),
        })

    # 9. Watchlist
    watchlist_out = []
    for w in (raw.get("next_week_watchlist") or [])[:5]:
        if isinstance(w, dict):
            watchlist_out.append({
                "window": str(w.get("window") or "สัปดาห์หน้า"),
                "event": str(w.get("event") or "-"),
                "hype_level": str(w.get("hype_level") or "HIGH").upper(),
            })

    audio_script = str(
        raw.get("audio_script_th")
        or f"สวัสดีเช้าวันจันทร์ครับ นี่คือคลื่นลับ Cyber Paparazzi สรุปข่าว IT และ AI ประจำสัปดาห์ {episode_banner['episode_title']}"
    ).strip()

    return {
        "episode_banner": episode_banner,
        "tech_series_sagas": sagas_out,
        "weekly_showdown": weekly_showdown,
        "ai_arms_race": arms_out,
        "top_scoops": scoops_out,
        "action_compass": action_compass,
        "launch_radar": radar_out,
        "track_briefs": briefs_out,
        "next_week_watchlist": watchlist_out,
        "audio_script_th": audio_script,
    }


def run_spy_analysis(
    intel_data: Dict[str, Any],
    history_context: str,
    sagas_context: str,
) -> Dict[str, Any]:
    """Run Gemini Spy Director analysis with automatic model fallback."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing. Please configure .env or GitHub Secrets.")

    prompt = build_spy_prompt(intel_data, history_context, sagas_context)
    client = genai.Client(api_key=GEMINI_API_KEY)

    last_error = None
    for model_name in GEMINI_MODELS:
        try:
            print(f"[SpyAnalyst] Intercepting & analyzing via {model_name}...")
            cfg_kwargs: Dict[str, Any] = {
                "response_mime_type": "application/json",
                "temperature": 0.6,
            }
            if "lite" not in model_name:
                cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_level="LOW")
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(**cfg_kwargs),
                )
            except Exception:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )

            um = getattr(response, "usage_metadata", None)
            if um:
                print(
                    f"[SpyAnalyst] Tokens -> prompt={getattr(um, 'prompt_token_count', 0)} "
                    f"out={getattr(um, 'candidates_token_count', 0)} "
                    f"think={getattr(um, 'thoughts_token_count', 0) or 0}"
                )
            raw_text = response.text or ""
            parsed = extract_json_from_response(raw_text)
            validated = sanitize_analysis(parsed, intel_data)
            print(f"[SpyAnalyst] Dossier synthesized cleanly using {model_name}.")
            return validated
        except Exception as exc:
            print(f"[SpyAnalyst] Model {model_name} fallback triggered: {exc}")
            last_error = exc
            continue

    raise RuntimeError(f"All Gemini models failed: {last_error}")
