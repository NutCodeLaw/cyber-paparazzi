"""
Telegram Notifier Module - Allied HQ Monday 08:00 AM BKK Synchronized Fast-Bite
Follows ALLIED_HQ_TELEGRAM_NOTIFICATION_SPEC.md:
- Exclusive room: -1003712039650
- Strict <= 1,200 char summary (hard guard 3,500)
- Never fires during local tests unless --telegram or FORCE_TELEGRAM is explicitly passed
"""
import html
import json
import os
import sys
import urllib.request
from typing import Any, Dict

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_TARGET_MAX = 1200


def _truncate(text: str, max_len: int) -> str:
    clean = " ".join(str(text or "").split())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 3].rstrip() + "..."


def build_telegram_message(payload: Dict[str, Any]) -> str:
    """Build ultra-compact Monday morning Cyber Paparazzi Telegram fast-bite (<= 1,200 chars)."""
    banner = payload.get("episode_banner", {})
    season_ep = html.escape(banner.get("season_ep", "SEASON 2026"))
    ep_title = html.escape(_truncate(banner.get("episode_title", "Tech & AI Spy Briefing"), 85))
    heat = banner.get("heat_score", 80)
    date_th = html.escape(payload.get("date_formatted", payload.get("date", "")))

    # Arms Race Top 1
    arms = sorted(payload.get("ai_arms_race", []), key=lambda x: x.get("power_score", 0), reverse=True)
    leader_line = "-"
    if arms:
        top = arms[0]
        leader_line = f"{top.get('icon', '🏆')} <b>{html.escape(top.get('faction', ''))}</b> ({top.get('power_score', 0)} pts)"

    # 1v1 Showdown Winner
    sd = payload.get("weekly_showdown", {})
    sd_verdict = html.escape(_truncate(sd.get("winner_verdict", "-"), 95))

    # Top 3 Scoops
    scoop_lines = []
    nums = ["1️⃣", "2️⃣", "3️⃣"]
    for idx, sc in enumerate(payload.get("top_scoops", [])[:3]):
        title = html.escape(_truncate(sc.get("headline", ""), 80))
        verdict = html.escape(sc.get("spy_verdict", "INFO"))
        scoop_lines.append(f"{nums[idx]} <b>{title}</b> <code>[{verdict}]</code>")

    # Series highlight
    sagas = payload.get("tech_series_sagas", [])
    saga_line = "-"
    if sagas:
        s0 = sagas[0]
        saga_line = html.escape(_truncate(f"{s0.get('series_title', '')} ({s0.get('episode_badge', '')})", 90))

    msg = (
        f"📸 <b>CYBER PAPARAZZI • จันทร์ 08:00 น.</b>\n"
        f"🎬 <i>{season_ep} | {date_th}</i>\n"
        f"🔥 <b>{ep_title}</b> (Heat: <code>{heat}/100</code>)\n\n"
        f"🧪 <b>Series Update:</b> {saga_line}\n"
        f"🏆 <b>AI Arms Race #1:</b> {leader_line}\n"
        f"⚔️ <b>1v1 Showdown:</b> {sd_verdict}\n\n"
        f"🕵️‍♂️ <b>3 ช็อตเด็ดรอบสัปดาห์:</b>\n"
        + "\n".join(scoop_lines)
        + "\n\n🌐 <b>เปิด Cyber Cockpit &amp; ฟังเสียงสรุป:</b>\nhttps://nutcodelaw.github.io/cyber-paparazzi/"
    )
    if len(msg) > TELEGRAM_TARGET_MAX:
        # Trim gracefully while preserving valid HTML
        msg = (
            f"📸 <b>CYBER PAPARAZZI • {season_ep}</b>\n"
            f"🔥 <b>{ep_title}</b> (Heat: <code>{heat}/100</code>)\n\n"
            + "\n".join(scoop_lines[:3])
            + f"\n\n🏆 <b>#1:</b> {leader_line}\n"
            + "🌐 <b>เปิด Cyber Cockpit:</b>\nhttps://nutcodelaw.github.io/cyber-paparazzi/"
        )
    return msg


def send_telegram_briefing(payload: Dict[str, Any]) -> bool:
    """Dispatch concise briefing strictly in CI or when --telegram / FORCE_TELEGRAM is passed."""
    is_ci = os.environ.get("GITHUB_ACTIONS") == "true"
    force_tg = os.environ.get("FORCE_TELEGRAM", "").lower() in ("true", "1", "yes") or "--telegram" in sys.argv
    if not is_ci and not force_tg:
        print("[Notifier] Local mode: Telegram paused (auto-fires in GitHub Actions Mon 08:00 BKK).")
        return False

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN).strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID).strip() or "-1003712039650"
    if not bot_token:
        print("[Notifier] TELEGRAM_BOT_TOKEN missing; skipping dispatch.")
        return False

    text = build_telegram_message(payload)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    req_data = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            ok = bool(res.get("ok", False))
            print(f"[Notifier] Telegram dispatch -> {ok} (chars={len(text)})")
            return ok
    except Exception as exc:
        print(f"[Notifier] Telegram dispatch failed: {exc}")
        return False
