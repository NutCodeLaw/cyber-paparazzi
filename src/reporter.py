"""
Reporter Module - Visual-First Markdown & Cyber-Intelligence Cockpit Generator
Enforces Zero Plain-Text Walls: Mermaid series trees, emoji stat bars, Periodic Element tiles,
1v1 Tug-of-War Showdown, Dual-Mode Switcher, Web Audio Synth FX, and Thai Voice Briefing.
"""
import html
import json
from pathlib import Path
from typing import Any, Dict, List

from src.config import (
    ARCHIVE_INDEX_PATH,
    ARCHIVES_DIR,
    INDEX_HTML_PATH,
    LATEST_JSON_PATH,
    LATEST_MD_PATH,
    README_MD_PATH,
    ROOT_INDEX_HTML_PATH,
    SPY_TRACKS,
)
from src.utils import get_iso_date, make_emoji_bar, safe_mermaid_label


def generate_markdown_report(payload: Dict[str, Any]) -> str:
    """Generate a visual-first, zero-wall-of-text Markdown intelligence dossier."""
    date_th = payload.get("date_formatted", payload.get("date", ""))
    time_str = payload.get("time", "08:00 น.")
    week_id = payload.get("week_id", "")
    banner = payload.get("episode_banner", {})
    heat_score = banner.get("heat_score", 80)
    heat_bar = make_emoji_bar(heat_score, "🔥", "▫️", 6)

    lines: List[str] = [
        f"# 📸 Cyber Paparazzi — {banner.get('season_ep', 'WEEKLY DOSSIER')}",
        f"## 🎬 {banner.get('episode_title', 'Tech & AI Spy Briefing')}",
        f"📅 **{date_th}** (`{week_id}`) • ⏰ อัปเดตเวลา **{time_str}** • 🌡️ **Tech Heat:** {heat_bar} **{heat_score}/100** (`{banner.get('heat_label', 'HIGH VOLTAGE')}`)",
        "",
        f"> **📡 Wiretap Verdict:** {banner.get('heat_rationale', '')}",
        "",
        "---",
        "",
        "## 🧪 Periodic Table of Tech Series (ซีรีส์เทคโนโลยีต่อเนื่องข้ามสัปดาห์)",
        "",
    ]

    for saga in payload.get("tech_series_sagas", []):
        comp = saga.get("completion_pct", 50)
        comp_bar = make_emoji_bar(comp, "🟩", "⬜", 5)
        lines.append(f"### 📺 {saga.get('series_title', '')} — `{saga.get('episode_badge', 'ONGOING')}`")
        lines.append(
            f"**ค่าย:** {saga.get('vendor', '-')} • **Team Combo:** {comp_bar} `{comp}%` • "
            f"**Power-Up:** `{saga.get('power_up_multiplier', '-')}`"
        )
        lines.append("")
        # Mermaid progression tree for this series
        roster = saga.get("element_roster", [])
        if roster:
            lines.append("```mermaid")
            lines.append("flowchart LR")
            node_ids = []
            for i, el in enumerate(roster):
                nid = f"E{i}"
                node_ids.append(nid)
                sym = safe_mermaid_label(el.get("symbol", "AI"), 6)
                nm = safe_mermaid_label(el.get("name", "Model"), 22)
                st = el.get("status", "UNLOCKED")
                badge = "🔥 NEW" if st == "NEW" else ("🔒 NEXT" if st == "RUMORED" else "✅")
                lines.append(f'    {nid}["{badge} [{sym}] {nm}"]')
            if len(node_ids) > 1:
                lines.append("    " + " --> ".join(node_ids))
            lines.append("```")
            lines.append("")
            lines.append("| # | ธาตุ | ชื่อรุ่น / ชิป | บทบาท | Multiplier | สถานะ |")
            lines.append("|:---:|:---:|:---|:---|:---|:---:|")
            for el in roster:
                st = el.get("status", "UNLOCKED")
                st_icon = "🔥 **NEW**" if st == "NEW" else ("🔒 RUMORED" if st == "RUMORED" else "🟢 UNLOCKED")
                lines.append(
                    f"| `{el.get('number', '01')}` | **{el.get('symbol', 'Ai')}** | {el.get('name', '-')} | "
                    f"{el.get('role_tag', '-')} | `{el.get('multiplier_badge', '-')}` | {st_icon} |"
                )
            lines.append("")

        lines.append("> [!NOTE]")
        lines.append(f"> ⏪ **Previously On:** {saga.get('previously_on', '-')}")
        lines.append(f"> ⚡ **This Week's Twist:** {saga.get('latest_twist', '-')}")
        lines.append(f"> 🔮 **Next Episode Teaser:** {saga.get('next_episode_rumor', '-')}")
        lines.append("")

    # 1v1 Weekly Spec Showdown
    sd = payload.get("weekly_showdown", {})
    fl = sd.get("fighter_left", {})
    fr = sd.get("fighter_right", {})
    lines.extend([
        "---",
        "",
        f"## ⚔️ 1v1 Weekly Spec Showdown: {sd.get('title', 'ศึกมวยคู่เอก')}",
        "",
        f"| 🥊 {fl.get('avatar_emoji', '🤖')} {fl.get('name', 'Left')} (`{fl.get('vendor', '-')}`) | 📊 ยกตัดสิน (Tug-of-War) | {fr.get('avatar_emoji', '⚡')} {fr.get('name', 'Right')} (`{fr.get('vendor', '-')}`) 🥊 |",
        "|:---|:---:|:---|",
        f"| **Score:** `{fl.get('total_score', 80)}/100` • *ท่าไม้ตาย:* {fl.get('special_move', '-')} | **ภาพรวม** | **Score:** `{fr.get('total_score', 80)}/100` • *ท่าไม้ตาย:* {fr.get('special_move', '-')} |",
    ])
    for r in sd.get("rounds", []):
        lp = r.get("left_pct", 50)
        rp = r.get("right_pct", 50)
        bar = make_emoji_bar(lp, "🟦", "🟪", 6)
        lines.append(f"| **{lp}%** | {r.get('metric_name', '-')} <br> {bar} <br> *{r.get('round_note', '')}* | **{rp}%** |")

    lines.extend([
        "",
        f"> **🏆 คำตัดสินผู้ชนะสัปดาห์นี้:** {sd.get('winner_verdict', '-')}",
        "",
        "---",
        "",
        "## 🏆 AI Arms Race Power Board (ตารางพลัง 6 มหาอำนาจ)",
        "",
        "| ค่าย / กองกำลัง | พลังสัปดาห์นี้ (Power Meter) | เปลี่ยนแปลง | สถานะ | ท่าเด็ดประจำสัปดาห์ |",
        "|:---|:---|:---:|:---:|:---|",
    ])
    for row in payload.get("ai_arms_race", []):
        p_score = row.get("power_score", 80)
        p_bar = make_emoji_bar(p_score, "🟦", "⬜", 5)
        delta = int(row.get("weekly_delta", 0))
        delta_str = f"🟢 ▲+{delta}" if delta > 0 else (f"🔴 ▼{delta}" if delta < 0 else "⚪ 0")
        lines.append(
            f"| {row.get('icon', '🛰️')} **{row.get('faction', '-')}** | {p_bar} **{p_score}** | {delta_str} | "
            f"`{row.get('stance_badge', 'ACTIVE')}` | {row.get('signature_move', '-')} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 📸 Top Paparazzi Scoops (ครบ 5 สายข่าวหลัก)",
        "",
    ])
    for idx, sc in enumerate(payload.get("top_scoops", []), 1):
        tr = SPY_TRACKS.get(sc.get("track", "ai_frontier"), SPY_TRACKS["ai_frontier"])
        chips = " ".join(f"`{c}`" for c in sc.get("spec_chips", []))
        hype_b = make_emoji_bar(sc.get("hype_score", 70), "🔥", "▫️", 5)
        imp_b = make_emoji_bar(sc.get("real_impact_score", 70), "💎", "▫️", 5)
        lines.extend([
            f"### {idx}. {tr['icon']} {sc.get('headline', '')} — `{sc.get('spy_verdict', 'SOLID UPGRADE')}`",
            f"{chips}",
            "",
            f"- **📸 โหมดปาปารัสซี่:** {sc.get('paparazzi_hook', '')}",
            f"- **⚙️ โหมดสเปกวิศวกร:** {sc.get('engineer_spec_summary', '')}",
            f"- **📊 มาตรวัด:** Hype {hype_b} `{sc.get('hype_score', 0)}%` | Real Impact {imp_b} `{sc.get('real_impact_score', 0)}%`",
            f"- **🔗 แหล่งข่าวทางการ:** [{sc.get('source_name', 'Source')}]({sc.get('source_url', '#')})",
            "",
        ])

    ac = payload.get("action_compass", {})
    lines.extend([
        "---",
        "",
        "## 🎯 Action Decision Compass (เข็มทิศฟันธงสัปดาห์นี้)",
        "",
        "| 🚀 Switch / Try Now (ลองเลยคุ้ม) | ⏳ Wait Next Episode (รอดูก่อน) | 🛡️ Skip Hype Trap (ข้ามได้ข้าม) |",
        "|:---|:---|:---|",
    ])
    sw = ac.get("switch_now", [])
    wt = ac.get("wait_next_ep", [])
    sk = ac.get("skip_hype_trap", [])
    max_rows = max(len(sw), len(wt), len(sk), 1)
    for i in range(max_rows):
        c1 = f"**{sw[i]['item']}** — {sw[i]['reason']}" if i < len(sw) else "-"
        c2 = f"**{wt[i]['item']}** — {wt[i]['reason']}" if i < len(wt) else "-"
        c3 = f"**{sk[i]['item']}** — {sk[i]['reason']}" if i < len(sk) else "-"
        lines.append(f"| {c1} | {c2} | {c3} |")

    lines.extend([
        "",
        "---",
        "",
        "## 🚀 Hardware & Software Launch Radar (ตารางของใหม่เปิดตัวสัปดาห์นี้)",
        "",
        "| ชื่อรุ่น / ซอฟต์แวร์ | หมวดหมู่ | ค่าย | จุดเด่นสเปก | สถานะ | ลิงก์ |",
        "|:---|:---:|:---|:---|:---:|:---:|",
    ])
    for item in payload.get("launch_radar", []):
        lines.append(
            f"| **{item.get('name', '-')}** | `{item.get('category', '-')}` | {item.get('vendor', '-')} | "
            f"{item.get('killer_spec', '-')} | `{item.get('availability', '-')}` | [Open]({item.get('source_url', '#')}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## ⚡ Quick Wiretaps & 📅 Next Week Watchlist",
        "",
    ])
    for b in payload.get("track_briefs", []):
        tr = SPY_TRACKS.get(b.get("track", "ai_frontier"), SPY_TRACKS["ai_frontier"])
        lines.append(
            f"- {tr['icon']} **`{b.get('tag', '#TECH')}` {b.get('headline', '')}**: "
            f"{b.get('punchline', '')} ([Link]({b.get('source_url', '#')}))"
        )
    lines.append("")
    for w in payload.get("next_week_watchlist", []):
        lines.append(f"- ⏱️ **[{w.get('hype_level', 'HIGH')}] {w.get('window', '')}:** {w.get('event', '')}")

    lines.extend([
        "",
        "---",
        "*จัดทำและตรวจสอบความถูกต้องโดย Cyber Paparazzi Autonomous Spy Pipeline (Allied HQ)*",
    ])
    return "\n".join(lines)


HTML_SHELL_TEMPLATE = r"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <script>
    try {
      const saved = localStorage.getItem("color-scheme");
      document.querySelector('meta[name="color-scheme"]').content = saved || "dark";
    } catch (e) {}
  </script>
  <title>__PAGE_TITLE__</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Noto+Sans+Thai:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      color-scheme: light dark;
      --bg-canvas: light-dark(#f1f5f9, #060913);
      --bg-surface: light-dark(#ffffff, #0e1628);
      --bg-elevated: light-dark(#e2e8f0, #16213a);
      --bg-glass: light-dark(rgba(255, 255, 255, 0.9), rgba(14, 22, 40, 0.88));
      --text-primary: light-dark(#0f172a, #f1f5f9);
      --text-secondary: light-dark(#475569, #94a3b8);
      --border-subtle: light-dark(#cbd5e1, #243352);
      --accent-cyan: light-dark(#0284c7, #00f5d4);
      --accent-gold: light-dark(#d97706, #ffb703);
      --accent-pink: light-dark(#db2777, #ff4d8d);
      --accent-green: light-dark(#059669, #10b981);
      --accent-purple: light-dark(#7c3aed, #a78bfa);
      --shadow-card: light-dark(0 8px 24px rgba(15, 23, 42, 0.08), 0 10px 30px rgba(0, 0, 0, 0.45));
      --font-display: 'Chakra Petch', 'Noto Sans Thai', sans-serif;
      --font-body: 'Noto Sans Thai', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }
    :root:has(> head > meta[name="color-scheme"][content="dark"]) {
      color-scheme: dark;
    }
    :root:has(> head > meta[name="color-scheme"][content="light"]) {
      color-scheme: light;
    }

    *, *::before, *::after { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: var(--font-body);
      background: var(--bg-canvas);
      color: var(--text-primary);
      line-height: 1.55;
      background-image:
        radial-gradient(circle at 12% 8%, color-mix(in srgb, var(--accent-cyan) 12%, transparent), transparent 36%),
        radial-gradient(circle at 88% 12%, color-mix(in srgb, var(--accent-pink) 10%, transparent), transparent 34%);
    }

    /* Accessibility Utilities */
    .visually-hidden:where(:not(:focus-within, :active)) {
      position: absolute !important;
      clip-path: inset(50%) !important;
      overflow: hidden !important;
      width: 1px !important;
      height: 1px !important;
      margin: -1px !important;
      padding: 0 !important;
      border: 0 !important;
      white-space: nowrap !important;
    }
    .skip-link:focus {
      position: fixed;
      top: 12px;
      left: 12px;
      z-index: 9999;
      padding: 10px 16px;
      background: var(--accent-cyan);
      color: #060913;
      font-weight: 800;
      border-radius: 8px;
      text-decoration: none;
    }
    :where(a:any-link, button, select, input):focus-visible {
      outline: 3px solid var(--accent-cyan);
      outline-offset: 3px;
    }

    /* Camera Flash FX on Scoop Snap / Mode Toggle */
    .camera-flash {
      position: fixed;
      inset: 0;
      background: rgba(255, 255, 255, 0.22);
      pointer-events: none;
      opacity: 0;
      z-index: 9000;
      transition: opacity 0.28s ease-out;
    }
    .camera-flash.active { opacity: 1; transition: none; }

    /* Wiretap Ticker */
    .wiretap-bar {
      background: light-dark(#0f172a, #03060d);
      color: #00f5d4;
      border-bottom: 1px solid var(--border-subtle);
      overflow: hidden;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      padding: 7px 0;
      display: flex;
      align-items: center;
    }
    .wiretap-badge {
      background: #ff4d8d;
      color: #ffffff;
      font-weight: 800;
      padding: 2px 10px;
      margin-inline: 12px;
      border-radius: 4px;
      flex: none;
      letter-spacing: 0.05em;
      z-index: 2;
    }
    .wiretap-track {
      flex: 1;
      min-width: 0;
      overflow: hidden;
    }
    .wiretap-scroll {
      display: flex;
      gap: 48px;
      width: max-content;
      white-space: nowrap;
      animation: ticker-move 34s linear infinite;
    }
    .wiretap-bar:hover .wiretap-scroll { animation-play-state: paused; }
    @keyframes ticker-move {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }

    .container {
      max-width: 1320px;
      margin: 0 auto;
      padding: 20px 18px 60px;
    }

    /* Header Command Deck */
    .command-header {
      background: var(--bg-glass);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 20px 22px;
      box-shadow: var(--shadow-card);
      backdrop-filter: blur(10px);
      margin-bottom: 22px;
    }
    .header-top {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
    }
    .brand-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--accent-cyan);
      background: color-mix(in srgb, var(--accent-cyan) 14%, transparent);
      border: 1px solid color-mix(in srgb, var(--accent-cyan) 40%, transparent);
      padding: 4px 10px;
      border-radius: 999px;
      margin-bottom: 8px;
    }
    h1 {
      margin: 0 0 6px;
      font-family: var(--font-display);
      font-size: clamp(1.55rem, 3vw, 2.25rem);
      font-weight: 700;
      line-height: 1.2;
      letter-spacing: -0.01em;
    }
    .meta-sub {
      color: var(--text-secondary);
      font-size: 0.9rem;
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
    }

    /* Control Deck */
    .controls-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-top: 16px;
      padding-top: 14px;
      border-top: 1px dashed var(--border-subtle);
    }
    .btn {
      appearance: none;
      border: 1px solid var(--border-subtle);
      background: var(--bg-elevated);
      color: var(--text-primary);
      font-family: var(--font-body);
      font-weight: 700;
      font-size: 0.85rem;
      padding: 8px 14px;
      min-block-size: 38px;
      border-radius: 10px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: transform 0.14s ease, border-color 0.14s ease, background 0.14s ease;
    }
    .btn:hover { transform: translateY(-1px); border-color: var(--accent-cyan); }
    .btn[aria-pressed="true"], .btn.active-mode {
      background: var(--accent-cyan);
      color: #060913;
      border-color: var(--accent-cyan);
    }
    .btn-pink[aria-pressed="true"] {
      background: var(--accent-pink);
      color: #ffffff;
      border-color: var(--accent-pink);
    }
    .btn-gold {
      background: color-mix(in srgb, var(--accent-gold) 18%, var(--bg-elevated));
      border-color: color-mix(in srgb, var(--accent-gold) 55%, transparent);
    }
    .select-box, .search-input {
      background: var(--bg-elevated);
      color: var(--text-primary);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 8px 12px;
      min-block-size: 38px;
      max-width: 100%;
      font-family: var(--font-body);
      font-size: 0.86rem;
    }
    .header-actions {
      display: flex;
      flex-direction: column;
      gap: 8px;
      align-items: flex-end;
      max-width: 100%;
      min-width: 0;
    }
    @media (max-width: 640px) {
      .header-actions { align-items: stretch; width: 100%; }
      .select-box { width: 100%; }
    }
    .mode-pill-group {
      display: inline-flex;
      flex-wrap: wrap;
      max-width: 100%;
      background: var(--bg-canvas);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 3px;
      gap: 4px;
    }

    /* Section Headings */
    h2.section-title {
      font-family: var(--font-display);
      font-size: 1.32rem;
      font-weight: 700;
      margin: 28px 0 14px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    h2.section-title::after {
      content: "";
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, var(--border-subtle), transparent);
    }

    /* Top Radar Grid: Heat Gauge + AI Arms Race */
    .radar-grid {
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 18px;
    }
    @media (max-width: 920px) {
      .radar-grid { grid-template-columns: 1fr; }
    }
    .card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 18px;
      box-shadow: var(--shadow-card);
      min-width: 0;
    }
    .gauge-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      justify-content: center;
    }
    .gauge-svg { width: 220px; height: 125px; }
    .gauge-needle {
      transform-origin: 100px 95px;
      transition: transform 0.8s cubic-bezier(0.22, 1, 0.36, 1);
    }
    .heat-number {
      font-family: var(--font-mono);
      font-size: 2.3rem;
      font-weight: 800;
      line-height: 1;
      margin-top: -6px;
    }
    .heat-badge {
      font-family: var(--font-mono);
      font-size: 0.78rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 999px;
      margin: 8px 0;
    }

    /* AI Arms Race */
    .arms-list {
      display: grid;
      gap: 11px;
    }
    .arms-row {
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 10px 14px;
    }
    .arms-row-head {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
      font-size: 0.92rem;
    }
    .arms-bar-track {
      height: 9px;
      border-radius: 999px;
      background: var(--bg-canvas);
      overflow: hidden;
      margin-bottom: 5px;
    }
    .arms-bar-fill {
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
      transition: width 0.6s ease;
    }
    .delta-up { color: var(--accent-green); font-family: var(--font-mono); font-weight: 700; }
    .delta-down { color: var(--accent-pink); font-family: var(--font-mono); font-weight: 700; }
    .delta-flat { color: var(--text-secondary); font-family: var(--font-mono); font-weight: 700; }

    /* Periodic Table of Tech Series */
    .saga-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 360px), 1fr));
      gap: 18px;
    }
    .saga-card {
      position: relative;
      overflow: hidden;
      border-top: 3px solid var(--accent-cyan);
    }
    .saga-head {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
      margin-bottom: 10px;
    }
    .ep-pill {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 6px;
      background: color-mix(in srgb, var(--accent-gold) 18%, transparent);
      color: var(--accent-gold);
      border: 1px solid color-mix(in srgb, var(--accent-gold) 45%, transparent);
      max-width: 100%;
      word-break: break-word;
    }
    .combo-bar-wrap {
      margin: 8px 0 14px;
    }
    .combo-label {
      display: flex;
      justify-content: space-between;
      font-size: 0.78rem;
      font-family: var(--font-mono);
      color: var(--text-secondary);
      margin-bottom: 4px;
    }
    .combo-track {
      height: 8px;
      border-radius: 999px;
      background: var(--bg-canvas);
      overflow: hidden;
    }
    .combo-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan));
    }

    /* Periodic Element Tiles */
    .element-roster {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(112px, 1fr));
      gap: 10px;
      margin: 12px 0 14px;
    }
    .el-tile {
      background: var(--bg-elevated);
      border: 1.5px solid var(--border-subtle);
      border-radius: 12px;
      padding: 10px 9px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 112px;
      transition: transform 0.15s ease;
    }
    .el-tile:hover { transform: translateY(-2px); }
    .el-tile.status-NEW {
      border-color: var(--accent-cyan);
      background: color-mix(in srgb, var(--accent-cyan) 11%, var(--bg-elevated));
      box-shadow: 0 0 16px color-mix(in srgb, var(--accent-cyan) 24%, transparent);
    }
    .el-tile.status-UNLOCKED {
      border-color: color-mix(in srgb, var(--accent-green) 60%, var(--border-subtle));
    }
    .el-tile.status-RUMORED {
      border-style: dashed;
      opacity: 0.78;
    }
    .el-top {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-secondary);
    }
    .el-symbol {
      font-family: var(--font-display);
      font-size: 1.65rem;
      font-weight: 800;
      line-height: 1.1;
      margin: 4px 0 2px;
      color: var(--accent-cyan);
    }
    .el-tile.status-NEW .el-symbol { color: var(--accent-gold); }
    .el-name { font-weight: 700; font-size: 0.82rem; line-height: 1.25; }
    .el-role { font-size: 0.72rem; color: var(--text-secondary); margin-top: 2px; }
    .el-mult {
      margin-top: 6px;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 5px;
      background: var(--bg-canvas);
      display: inline-block;
      width: fit-content;
    }
    .saga-timeline {
      display: grid;
      gap: 6px;
      font-size: 0.83rem;
      background: var(--bg-canvas);
      border-radius: 10px;
      padding: 10px 12px;
    }

    /* 1v1 Spec Showdown Arena */
    .showdown-card {
      border: 1.5px solid color-mix(in srgb, var(--accent-pink) 45%, var(--border-subtle));
      background:
        linear-gradient(135deg, color-mix(in srgb, var(--accent-cyan) 7%, var(--bg-surface)), color-mix(in srgb, var(--accent-pink) 7%, var(--bg-surface)));
    }
    .fighters-banner {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      gap: 14px;
      align-items: center;
      margin-bottom: 16px;
    }
    @media (max-width: 720px) {
      .fighters-banner { grid-template-columns: 1fr; text-align: center; }
    }
    .fighter-box {
      background: var(--bg-elevated);
      border-radius: 14px;
      padding: 14px;
      border: 1px solid var(--border-subtle);
    }
    .fighter-box.right { text-align: right; }
    @media (max-width: 720px) {
      .fighter-box.right { text-align: center; }
    }
    .vs-crest {
      font-family: var(--font-display);
      font-size: 1.45rem;
      font-weight: 800;
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-pink));
      color: #060913;
      width: 54px;
      height: 54px;
      border-radius: 999px;
      display: grid;
      place-items: center;
      margin: 0 auto;
      box-shadow: 0 0 20px color-mix(in srgb, var(--accent-pink) 35%, transparent);
    }
    .round-row {
      margin-bottom: 12px;
    }
    .round-meta {
      display: flex;
      justify-content: space-between;
      font-size: 0.84rem;
      font-weight: 700;
      margin-bottom: 4px;
    }
    .tug-track {
      height: 14px;
      border-radius: 999px;
      overflow: hidden;
      display: flex;
      background: var(--bg-canvas);
    }
    .tug-left { background: var(--accent-cyan); transition: width 0.6s ease; }
    .tug-right { background: var(--accent-pink); transition: width 0.6s ease; }
    .verdict-banner {
      margin-top: 14px;
      padding: 10px 14px;
      border-radius: 10px;
      background: color-mix(in srgb, var(--accent-gold) 14%, var(--bg-canvas));
      border-left: 4px solid var(--accent-gold);
      font-size: 0.9rem;
      font-weight: 600;
    }

    /* Filter Bar & 5-Track Scoops */
    .filter-toolbar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }
    .track-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .scoops-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 350px), 1fr));
      gap: 18px;
    }
    .scoop-card {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
    }
    .scoop-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .track-tag {
      font-size: 0.76rem;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 999px;
      border: 1px solid currentColor;
    }
    .verdict-stamp {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
    }
    .verdict-GAME-CHANGER { background: color-mix(in srgb, var(--accent-green) 22%, transparent); color: var(--accent-green); }
    .verdict-SOLID-UPGRADE { background: color-mix(in srgb, var(--accent-cyan) 20%, transparent); color: var(--accent-cyan); }
    .verdict-OVERHYPED { background: color-mix(in srgb, var(--accent-pink) 20%, transparent); color: var(--accent-pink); }
    .verdict-WATCHLIST { background: color-mix(in srgb, var(--accent-gold) 20%, transparent); color: var(--accent-gold); }

    .scoop-title {
      margin: 0;
      font-size: 1.07rem;
      font-weight: 800;
      line-height: 1.38;
    }
    .chips-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .spec-chip {
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 600;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      padding: 3px 8px;
      border-radius: 6px;
    }
    .narrative-box {
      background: var(--bg-canvas);
      border-radius: 10px;
      padding: 11px 13px;
      font-size: 0.89rem;
      border-left: 3px solid var(--accent-cyan);
    }
    .narrative-box.mode-paparazzi { border-left-color: var(--accent-pink); }
    .dual-meters {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      font-size: 0.76rem;
      font-family: var(--font-mono);
    }
    .meter-track {
      height: 7px;
      background: var(--bg-canvas);
      border-radius: 999px;
      overflow: hidden;
      margin-top: 3px;
    }
    .meter-hype { height: 100%; background: var(--accent-gold); }
    .meter-impact { height: 100%; background: var(--accent-green); }
    .source-link {
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent-cyan);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .source-link:hover { text-decoration: underline; }

    /* Action Decision Compass */
    .compass-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }
    .compass-col {
      border-radius: 14px;
      padding: 16px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      box-shadow: var(--shadow-card);
    }
    .compass-col.go { border-top: 4px solid var(--accent-green); }
    .compass-col.wait { border-top: 4px solid var(--accent-gold); }
    .compass-col.skip { border-top: 4px solid var(--accent-pink); }
    .compass-col h3 { margin: 0 0 10px; font-size: 1rem; }
    .compass-item {
      background: var(--bg-elevated);
      border-radius: 10px;
      padding: 10px 12px;
      margin-bottom: 8px;
      font-size: 0.85rem;
    }

    /* Responsive Table (modern-web-guidance pattern) */
    .table-wrapper {
      overflow: auto;
      max-inline-size: 100%;
      max-block-size: min(520px, 75vh);
      container-type: inline-size;
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      background: var(--bg-surface);
      box-shadow: var(--shadow-card);
    }
    .launch-table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 0.87rem;
      --label-1: "Release";
      --label-2: "Category";
      --label-3: "Vendor";
      --label-4: "Killer Spec";
      --label-5: "Status";
      --label-6: "Source";
    }
    .launch-table caption {
      text-align: left;
      padding: 12px 16px;
      font-weight: 700;
      color: var(--text-secondary);
      border-bottom: 1px solid var(--border-subtle);
    }
    .launch-table thead {
      position: sticky;
      inset-block-start: 0;
      z-index: 2;
      background: var(--bg-elevated);
    }
    .launch-table th, .launch-table td {
      padding: 11px 14px;
      text-align: left;
      border-bottom: 1px solid var(--border-subtle);
    }
    .launch-table tbody th {
      position: sticky;
      inset-inline-start: 0;
      background: var(--bg-surface);
      font-weight: 700;
      z-index: 1;
    }
    @container (width < 640px) {
      .launch-table, .launch-table thead, .launch-table tbody, .launch-table tr, .launch-table th, .launch-table td {
        display: block;
      }
      .launch-table thead { display: none; }
      .launch-table tr {
        margin: 12px;
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        overflow: hidden;
      }
      .launch-table tbody th {
        position: sticky;
        inset-block-start: 0;
        background: var(--bg-elevated);
      }
      .launch-table td::before {
        font-weight: 700;
        color: var(--text-secondary);
        margin-right: 6px;
      }
      .launch-table td:nth-child(2)::before { content: var(--label-2) ": "; }
      .launch-table td:nth-child(3)::before { content: var(--label-3) ": "; }
      .launch-table td:nth-child(4)::before { content: var(--label-4) ": "; }
      .launch-table td:nth-child(5)::before { content: var(--label-5) ": "; }
      .launch-table td:nth-child(6)::before { content: var(--label-6) ": "; }
    }

    /* Bottom Dual Grid */
    .bottom-grid {
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 18px;
      margin-top: 10px;
    }
    @media (max-width: 860px) {
      .bottom-grid { grid-template-columns: 1fr; }
    }
    .brief-item {
      display: flex;
      gap: 10px;
      align-items: flex-start;
      padding: 10px 12px;
      background: var(--bg-elevated);
      border-radius: 10px;
      margin-bottom: 8px;
      font-size: 0.86rem;
    }
    .watch-item {
      padding: 10px 12px;
      border-left: 3px solid var(--accent-gold);
      background: var(--bg-elevated);
      border-radius: 0 10px 10px 0;
      margin-bottom: 8px;
      font-size: 0.86rem;
    }

    footer {
      margin-top: 38px;
      text-align: center;
      font-size: 0.82rem;
      color: var(--text-secondary);
      padding-top: 16px;
      border-top: 1px solid var(--border-subtle);
    }

    @media (prefers-reduced-motion: reduce) {
      .wiretap-scroll { animation: none; }
      .gauge-needle, .arms-bar-fill, .tug-left, .tug-right, .btn, .el-tile { transition: none; }
      .camera-flash { display: none; }
    }
  </style>
</head>
<body>
  <a href="#main-content" class="skip-link visually-hidden">ข้ามไปยังเนื้อหาหลัก</a>
  <div id="camera-flash" class="camera-flash" aria-hidden="true"></div>
  <div id="live-announcer" class="visually-hidden" aria-live="polite"></div>

  <!-- Live Spy Wiretap Ticker -->
  <div class="wiretap-bar" aria-label="แถบดักฟังข่าวด่วน">
    <span class="wiretap-badge">📡 WIRETAP LIVE</span>
    <div class="wiretap-track">
      <div id="wiretap-scroll" class="wiretap-scroll"></div>
    </div>
  </div>

  <div class="container">
    <header class="command-header">
      <div class="header-top">
        <div>
          <div class="brand-eyebrow" id="season-ep-badge">SEASON 2026 • WEEKLY SPY DOSSIER</div>
          <h1 id="episode-title-h1">__PAGE_TITLE__</h1>
          <div class="meta-sub">
            <span id="date-display">📅 __LAST_UPDATED__</span>
            <span>•</span>
            <span>⏰ Every Monday 08:00 น. (Bangkok)</span>
            <span>•</span>
            <span id="intel-stats-pill">🕵️ Verified Official & Tier-1 Press</span>
          </div>
        </div>

        <div class="header-actions">
          <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center; max-width:100%;">
            <label for="archive-select" class="visually-hidden">เลือกสัปดาห์ย้อนหลัง</label>
            <select id="archive-select" class="select-box" aria-label="เลือกสัปดาห์ย้อนหลัง"></select>
            <button type="button" id="theme-toggle-btn" class="btn" aria-label="สลับโหมดสีหน้าจอ">🌓 <span id="theme-toggle-label">โหมดสว่าง</span></button>
          </div>
        </div>
      </div>

      <div class="controls-row">
        <div class="mode-pill-group" role="group" aria-label="เลือกโหมดการเล่าข่าว">
          <button type="button" id="mode-paparazzi-btn" class="btn btn-pink" aria-pressed="true">📸 โหมดปาปารัสซี่สุดมันส์</button>
          <button type="button" id="mode-engineer-btn" class="btn" aria-pressed="false">⚙️ โหมดสเปกวิศวกร</button>
        </div>

        <button type="button" id="voice-play-btn" class="btn btn-gold" aria-pressed="false">🔊 ฟังวิทยุสายลับ 60 วิ</button>
        <button type="button" id="voice-speed-btn" class="btn" title="ปรับความเร็วเสียง">⏩ 1.1x</button>
        <button type="button" id="sfx-toggle-btn" class="btn" aria-pressed="true">📸 Shutter FX: ON</button>
        <button type="button" id="copy-md-btn" class="btn">📋 Copy Markdown</button>
      </div>
    </header>

    <main id="main-content" tabindex="-1">
      <!-- 1. Tech Heat Speedometer + AI Arms Race -->
      <section aria-labelledby="sec-radar-h">
        <h2 id="sec-radar-h" class="section-title">📡 Tech Heat & AI Arms Race Power Board</h2>
        <div class="radar-grid">
          <div class="card gauge-card">
            <div style="font-size:0.82rem; font-weight:800; color:var(--text-secondary);">🌡️ WEEKLY TECH HEAT INDEX</div>
            <svg class="gauge-svg" viewBox="0 0 200 115" role="img" aria-labelledby="gauge-svg-title">
              <title id="gauge-svg-title">เข็มไมล์วัดความเดือดของวงการเทคโนโลยีและ AI ประจำสัปดาห์</title>
              <path d="M 20 95 A 80 80 0 0 1 180 95" fill="none" stroke="currentColor" opacity="0.16" stroke-width="16" stroke-linecap="round"/>
              <path d="M 20 95 A 80 80 0 0 1 65 38" fill="none" stroke="#10b981" stroke-width="16" stroke-linecap="round"/>
              <path d="M 68 35 A 80 80 0 0 1 132 35" fill="none" stroke="#ffb703" stroke-width="16"/>
              <path d="M 135 38 A 80 80 0 0 1 180 95" fill="none" stroke="#ff4d8d" stroke-width="16" stroke-linecap="round"/>
              <g id="gauge-needle" class="gauge-needle">
                <polygon points="97,95 103,95 100,22" fill="#f8fafc"/>
                <circle cx="100" cy="95" r="7" fill="#00f5d4"/>
              </g>
            </svg>
            <div id="heat-score-val" class="heat-number">85</div>
            <div id="heat-label-pill" class="heat-badge">HIGH VOLTAGE</div>
            <div id="heat-rationale" style="font-size:0.84rem; color:var(--text-secondary);"></div>
          </div>

          <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <strong>🏆 6-Faction AI & Silicon Power Ranking</strong>
              <span style="font-size:0.78rem; color:var(--text-secondary);">Delta เทียบสัปดาห์ก่อน</span>
            </div>
            <div id="arms-race-list" class="arms-list"></div>
          </div>
        </div>
      </section>

      <!-- 2. Periodic Table of Tech Series -->
      <section aria-labelledby="sec-saga-h">
        <h2 id="sec-saga-h" class="section-title">🧪 Periodic Table of Tech Series (ซีรีส์ต่อเนื่องข้ามสัปดาห์)</h2>
        <div id="saga-grid" class="saga-grid"></div>
      </section>

      <!-- 3. 1v1 Spec Showdown -->
      <section aria-labelledby="sec-duel-h">
        <h2 id="sec-duel-h" class="section-title">⚔️ 1v1 Weekly Spec Showdown (ศึกมวยคู่เอกประจำสัปดาห์)</h2>
        <div id="showdown-container" class="card showdown-card"></div>
      </section>

      <!-- 4. 5-Track Paparazzi Scoops -->
      <section aria-labelledby="sec-scoops-h">
        <h2 id="sec-scoops-h" class="section-title">📸 Paparazzi Scoops Vault (แฟ้มข่าวเจาะลึก 5 สาย)</h2>
        <div class="filter-toolbar">
          <nav class="track-pills" aria-label="ตัวกรองสายข่าว 5 หมวด" id="track-filter-nav"></nav>
          <div style="display:flex; align-items:center; gap:8px;">
            <label for="scoop-search" class="visually-hidden">ค้นหาข่าวเทค</label>
            <input id="scoop-search" type="search" class="search-input" placeholder="🔍 ค้นหาชื่อรุ่น, ชิป, ค่าย...">
          </div>
        </div>
        <div id="scoops-grid" class="scoops-grid"></div>
      </section>

      <!-- 5. Action Decision Compass -->
      <section aria-labelledby="sec-compass-h">
        <h2 id="sec-compass-h" class="section-title">🎯 "Switch, Wait, or Skip?" Action Decision Compass</h2>
        <div id="compass-grid" class="compass-grid"></div>
      </section>

      <!-- 6. Hardware & Software Launch Radar Matrix -->
      <section aria-labelledby="sec-launch-h">
        <h2 id="sec-launch-h" class="section-title">🚀 Hardware & Software Launch Radar Matrix</h2>
        <div class="track-pills" id="launch-filter-bar" style="margin-bottom:12px;"></div>
        <div tabindex="0" role="region" aria-labelledby="launch-radar-caption" class="table-wrapper">
          <table class="launch-table">
            <caption id="launch-radar-caption">สรุปรายการโมเดล AI, ชิปฮาร์ดแวร์ และซอฟต์แวร์เปิดตัวใหม่ประจำสัปดาห์</caption>
            <thead>
              <tr>
                <th scope="col">Release</th>
                <th scope="col">Category</th>
                <th scope="col">Vendor</th>
                <th scope="col">Killer Spec</th>
                <th scope="col">Status</th>
                <th scope="col">Source</th>
              </tr>
            </thead>
            <tbody id="launch-table-body"></tbody>
          </table>
        </div>
      </section>

      <!-- 7. Quick Wiretaps & Next Week Watchlist -->
      <div class="bottom-grid">
        <section class="card" aria-labelledby="sec-briefs-h">
          <h2 id="sec-briefs-h" class="section-title" style="margin-top:0;">⚡ 5-Track Quick Wiretaps</h2>
          <div id="briefs-list"></div>
        </section>

        <section class="card" aria-labelledby="sec-watch-h">
          <h2 id="sec-watch-h" class="section-title" style="margin-top:0;">📅 Next Week Watchlist</h2>
          <div id="watchlist-list"></div>
        </section>
      </div>
    </main>

    <footer>
      <strong>Cyber Paparazzi HQ v2.0</strong> • Autonomous Monday 08:00 AM BKK Spy Pipeline •
      Sources: OpenAI, Google AI/DeepMind, NVIDIA, Apple, Microsoft, Ars Technica, The Verge, Tom's Hardware, MIT Tech Review, IEEE Spectrum, Hugging Face, GitHub
    </footer>
  </div>

  <textarea id="raw-markdown-data" class="visually-hidden" aria-hidden="true">__ESCAPED_RAW_MARKDOWN__</textarea>

  <script>
    const INITIAL_DOSSIER = __EMBEDDED_DOSSIER_JSON__;
    const ARCHIVE_INDEX = __ARCHIVE_INDEX_JSON__;
    const TRACK_META = __TRACK_META_JSON__;

    let activeDossier = INITIAL_DOSSIER;
    let currentMode = "paparazzi";
    let activeTrack = "all";
    let activeLaunchCat = "all";
    let searchQuery = "";
    let sfxEnabled = true;
    let isSpeaking = false;
    let voiceRate = 1.1;
    let audioCtx = null;

    function esc(str) {
      return String(str ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }

    function safeUrl(url) {
      const s = String(url || "").trim();
      return (s.startsWith("https://") || s.startsWith("http://")) ? s : "#";
    }

    function announce(msg) {
      const el = document.getElementById("live-announcer");
      if (el) el.textContent = msg;
    }

    /* Web Audio API Synth FX (Zero external files) */
    function playSfx(type = "shutter") {
      if (!sfxEnabled) return;
      try {
        if (!audioCtx) {
          const Ctx = window.AudioContext || window.webkitAudioContext;
          if (!Ctx) return;
          audioCtx = new Ctx();
        }
        if (audioCtx.state === "suspended") audioCtx.resume();

        const now = audioCtx.currentTime;
        if (type === "shutter") {
          // Camera shutter white-noise burst + flash
          const bufferSize = Math.floor(audioCtx.sampleRate * 0.06);
          const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
          const data = buffer.getChannelData(0);
          for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.28));
          }
          const src = audioCtx.createBufferSource();
          src.buffer = buffer;
          const gain = audioCtx.createGain();
          gain.gain.setValueAtTime(0.18, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
          src.connect(gain).connect(audioCtx.destination);
          src.start(now);

          const flash = document.getElementById("camera-flash");
          if (flash) {
            flash.classList.add("active");
            requestAnimationFrame(() => setTimeout(() => flash.classList.remove("active"), 45));
          }
        } else {
          // Radar Sonar Ping
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(880, now);
          osc.frequency.exponentialRampToValueAtTime(1320, now + 0.12);
          gain.gain.setValueAtTime(0.09, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
          osc.connect(gain).connect(audioCtx.destination);
          osc.start(now);
          osc.stop(now + 0.15);
        }
      } catch (e) {}
    }

    function renderDossier(d) {
      activeDossier = d;
      const banner = d.episode_banner || {};

      // Header
      document.getElementById("season-ep-badge").textContent = banner.season_ep || "SEASON 2026 • SPY DOSSIER";
      document.getElementById("episode-title-h1").textContent = banner.episode_title || "Cyber Paparazzi Weekly Dossier";
      document.getElementById("date-display").textContent = `📅 ${d.date_formatted || d.date || ""} (${d.week_id || ""})`;

      const stats = d.intel_stats || {};
      if (stats.active_feeds) {
        document.getElementById("intel-stats-pill").textContent = `🕵️ ${stats.active_feeds}/${stats.total_feeds} Feeds • ${stats.selected_count || 0} Signals`;
      }

      // Wiretap Ticker
      const tickerItems = (banner.wiretap_ticker || []).map(t => `<span>⚡ ${esc(t)}</span>`).join("");
      document.getElementById("wiretap-scroll").innerHTML = tickerItems + tickerItems;

      // Speedometer
      const heat = Math.max(0, Math.min(100, Number(banner.heat_score || 80)));
      const deg = ((heat / 100) * 180) - 90;
      document.getElementById("gauge-needle").style.transform = `rotate(${deg}deg)`;
      const hColor = heat >= 75 ? "#ff4d8d" : (heat >= 50 ? "#ffb703" : "#10b981");
      const scoreEl = document.getElementById("heat-score-val");
      scoreEl.textContent = heat;
      scoreEl.style.color = hColor;
      const pill = document.getElementById("heat-label-pill");
      pill.textContent = banner.heat_label || "HIGH VOLTAGE";
      pill.style.background = `color-mix(in srgb, ${hColor} 20%, transparent)`;
      pill.style.color = hColor;
      document.getElementById("heat-rationale").textContent = banner.heat_rationale || "";

      // AI Arms Race
      const sortedArms = [...(d.ai_arms_race || [])].sort((a, b) => (b.power_score || 0) - (a.power_score || 0));
      document.getElementById("arms-race-list").innerHTML = sortedArms.map((row, idx) => {
        const delta = Number(row.weekly_delta || 0);
        const deltaCls = delta > 0 ? "delta-up" : (delta < 0 ? "delta-down" : "delta-flat");
        const deltaTxt = delta > 0 ? `▲ +${delta}` : (delta < 0 ? `▼ ${delta}` : "• 0");
        return `
          <div class="arms-row">
            <div class="arms-row-head">
              <div><strong>#${idx + 1} ${esc(row.icon)} ${esc(row.faction)}</strong> <span class="spec-chip">${esc(row.stance_badge)}</span></div>
              <div><span class="${deltaCls}">${deltaTxt}</span> &nbsp; <strong>${Number(row.power_score || 0)}</strong>/100</div>
            </div>
            <div class="arms-bar-track"><div class="arms-bar-fill" style="width:${Number(row.power_score || 0)}%"></div></div>
            <div style="font-size:0.8rem; color:var(--text-secondary);">⚡ ${esc(row.signature_move)}</div>
          </div>`;
      }).join("");

      // Periodic Table of Tech Series
      document.getElementById("saga-grid").innerHTML = (d.tech_series_sagas || []).map(saga => {
        const comp = Math.max(0, Math.min(100, Number(saga.completion_pct || 0)));
        const rosterHtml = (saga.element_roster || []).map(el => `
          <div class="el-tile status-${esc(el.status)}">
            <div class="el-top">
              <span>${esc(el.number)}</span>
              <span>${el.status === "NEW" ? "🔥 NEW" : (el.status === "RUMORED" ? "🔒 NEXT" : "🟢")}</span>
            </div>
            <div>
              <div class="el-symbol">${esc(el.symbol)}</div>
              <div class="el-name">${esc(el.name)}</div>
              <div class="el-role">${esc(el.role_tag)}</div>
            </div>
            <span class="el-mult">${esc(el.multiplier_badge)}</span>
          </div>
        `).join("");

        return `
          <article class="card saga-card">
            <div class="saga-head">
              <div>
                <div style="font-size:0.78rem; color:var(--text-secondary); font-weight:700;">${esc(saga.vendor)}</div>
                <h3 style="margin:2px 0 0; font-size:1.08rem;">${esc(saga.series_title)}</h3>
              </div>
              <span class="ep-pill">${esc(saga.episode_badge)}</span>
            </div>
            <div class="combo-bar-wrap">
              <div class="combo-label">
                <span>⚡ ${esc(saga.power_up_multiplier)}</span>
                <span>Roster ${comp}%</span>
              </div>
              <div class="combo-track"><div class="combo-fill" style="width:${comp}%"></div></div>
            </div>
            <div class="element-roster">${rosterHtml}</div>
            <div class="saga-timeline">
              <div><strong>⏪ Previously:</strong> ${esc(saga.previously_on)}</div>
              <div><strong>⚡ This Week:</strong> ${esc(saga.latest_twist)}</div>
              <div><strong>🔮 Next EP:</strong> ${esc(saga.next_episode_rumor)}</div>
            </div>
          </article>`;
      }).join("");

      // 1v1 Spec Showdown
      const sd = d.weekly_showdown || {};
      const fl = sd.fighter_left || {};
      const fr = sd.fighter_right || {};
      const roundsHtml = (sd.rounds || []).map(r => `
        <div class="round-row">
          <div class="round-meta">
            <span style="color:var(--accent-cyan)">${Number(r.left_pct || 50)}%</span>
            <span>${esc(r.metric_name)}</span>
            <span style="color:var(--accent-pink)">${Number(r.right_pct || 50)}%</span>
          </div>
          <div class="tug-track">
            <div class="tug-left" style="width:${Number(r.left_pct || 50)}%"></div>
            <div class="tug-right" style="width:${Number(r.right_pct || 50)}%"></div>
          </div>
          <div style="font-size:0.78rem; color:var(--text-secondary); margin-top:3px; text-align:center;">${esc(r.round_note)}</div>
        </div>
      `).join("");

      document.getElementById("showdown-container").innerHTML = `
        <h3 style="margin:0 0 14px; font-size:1.15rem; text-align:center;">🥊 ${esc(sd.title)}</h3>
        <div class="fighters-banner">
          <div class="fighter-box">
            <div style="font-size:1.6rem;">${esc(fl.avatar_emoji || "🤖")}</div>
            <div style="font-weight:800; font-size:1.05rem;">${esc(fl.name)}</div>
            <div style="font-size:0.8rem; color:var(--text-secondary);">${esc(fl.vendor)} • Score <strong>${Number(fl.total_score || 0)}</strong></div>
            <div class="spec-chip" style="margin-top:6px;">⚡ ${esc(fl.special_move)}</div>
          </div>
          <div class="vs-crest" aria-hidden="true">VS</div>
          <div class="fighter-box right">
            <div style="font-size:1.6rem;">${esc(fr.avatar_emoji || "⚡")}</div>
            <div style="font-weight:800; font-size:1.05rem;">${esc(fr.name)}</div>
            <div style="font-size:0.8rem; color:var(--text-secondary);">${esc(fr.vendor)} • Score <strong>${Number(fr.total_score || 0)}</strong></div>
            <div class="spec-chip" style="margin-top:6px;">⚡ ${esc(fr.special_move)}</div>
          </div>
        </div>
        ${roundsHtml}
        <div class="verdict-banner">🏆 <strong>คำตัดสินสัปดาห์นี้:</strong> ${esc(sd.winner_verdict)}</div>
      `;

      renderTrackButtons();
      renderScoops();
      renderCompass();
      renderLaunchFilters();
      renderLaunchTable();
      renderBottomSections();
    }

    function renderTrackButtons() {
      const scoops = activeDossier.top_scoops || [];
      const counts = {};
      for (const s of scoops) {
        counts[s.track] = (counts[s.track] || 0) + 1;
      }
      const nav = document.getElementById("track-filter-nav");
      const buttons = [
        `<button type="button" class="btn" data-track="all" aria-pressed="${activeTrack === "all"}">🌐 ทั้งหมด (${scoops.length})</button>`
      ];
      for (const [tid, meta] of Object.entries(TRACK_META)) {
        buttons.push(
          `<button type="button" class="btn" data-track="${esc(tid)}" aria-pressed="${activeTrack === tid}">${esc(meta.icon)} ${esc(meta.name)} (${counts[tid] || 0})</button>`
        );
      }
      nav.innerHTML = buttons.join("");
      nav.querySelectorAll("button").forEach(btn => {
        btn.addEventListener("click", () => {
          activeTrack = btn.dataset.track;
          playSfx("radar");
          renderTrackButtons();
          renderScoops();
          announce(`กรองสายข่าว: ${btn.textContent}`);
        });
      });
    }

    function renderScoops() {
      const q = searchQuery.trim().toLowerCase();
      const filtered = (activeDossier.top_scoops || []).filter(sc => {
        if (activeTrack !== "all" && sc.track !== activeTrack) return false;
        if (!q) return true;
        const hay = `${sc.headline} ${sc.paparazzi_hook} ${sc.engineer_spec_summary} ${(sc.spec_chips || []).join(" ")} ${sc.source_name}`.toLowerCase();
        return hay.includes(q);
      });

      const grid = document.getElementById("scoops-grid");
      if (!filtered.length) {
        grid.innerHTML = `<div class="card" style="grid-column:1/-1; text-align:center;">🕵️ ไม่พบข่าวที่ตรงกับเงื่อนไขการค้นหา</div>`;
        return;
      }

      grid.innerHTML = filtered.map(sc => {
        const meta = TRACK_META[sc.track] || { icon: "🛰️", name: "Tech", color: "#00f5d4" };
        const chips = (sc.spec_chips || []).map(c => `<span class="spec-chip">${esc(c)}</span>`).join("");
        const narrative = currentMode === "paparazzi" ? sc.paparazzi_hook : sc.engineer_spec_summary;
        const modeTag = currentMode === "paparazzi" ? "📸 PAPARAZZI LENS" : "⚙️ ENGINEER SPEC";
        const verdictSlug = String(sc.spy_verdict || "SOLID UPGRADE").trim().replace(/\s+/g, "-");
        return `
          <article class="card scoop-card">
            <div>
              <div class="scoop-top">
                <span class="track-tag" style="color:${esc(meta.color)}">${esc(meta.icon)} ${esc(meta.name)}</span>
                <span class="verdict-stamp verdict-${esc(verdictSlug)}">${esc(sc.spy_verdict)}</span>
              </div>
              <h3 class="scoop-title" style="margin-top:10px;">${esc(sc.headline)}</h3>
              <div class="chips-row" style="margin-top:9px;">${chips}</div>
            </div>

            <div class="narrative-box mode-${currentMode}">
              <div style="font-family:var(--font-mono); font-size:0.7rem; font-weight:800; color:var(--text-secondary); margin-bottom:4px;">${modeTag}</div>
              <div>${esc(narrative)}</div>
            </div>

            <div>
              <div class="dual-meters">
                <div>
                  <div>🔥 Hype: ${Number(sc.hype_score || 0)}%</div>
                  <div class="meter-track"><div class="meter-hype" style="width:${Number(sc.hype_score || 0)}%"></div></div>
                </div>
                <div>
                  <div>💎 Real Impact: ${Number(sc.real_impact_score || 0)}%</div>
                  <div class="meter-track"><div class="meter-impact" style="width:${Number(sc.real_impact_score || 0)}%"></div></div>
                </div>
              </div>
              <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                <a class="source-link" href="${safeUrl(sc.source_url)}" target="_blank" rel="noopener noreferrer">🔗 ${esc(sc.source_name)} ↗</a>
              </div>
            </div>
          </article>`;
      }).join("");
    }

    function renderCompass() {
      const ac = activeDossier.action_compass || {};
      const cols = [
        { cls: "go", title: "🚀 Switch / Try Now (ลองเลยคุ้ม)", items: ac.switch_now || [] },
        { cls: "wait", title: "⏳ Wait Next Episode (รอดูก่อน)", items: ac.wait_next_ep || [] },
        { cls: "skip", title: "🛡️ Skip Hype Trap (ข้ามได้ข้าม)", items: ac.skip_hype_trap || [] },
      ];
      document.getElementById("compass-grid").innerHTML = cols.map(c => `
        <div class="compass-col ${c.cls}">
          <h3>${c.title}</h3>
          ${c.items.map(it => `<div class="compass-item"><strong>${esc(it.item)}</strong><br><span style="color:var(--text-secondary)">${esc(it.reason)}</span></div>`).join("") || `<div class="compass-item">-</div>`}
        </div>
      `).join("");
    }

    function renderLaunchFilters() {
      const cats = ["all", "AI Model", "Hardware", "Software"];
      const bar = document.getElementById("launch-filter-bar");
      bar.innerHTML = cats.map(c => `
        <button type="button" class="btn" data-cat="${esc(c)}" aria-pressed="${activeLaunchCat === c}">
          ${c === "all" ? "📦 All Releases" : esc(c)}
        </button>
      `).join("");
      bar.querySelectorAll("button").forEach(btn => {
        btn.addEventListener("click", () => {
          activeLaunchCat = btn.dataset.cat;
          playSfx("radar");
          renderLaunchFilters();
          renderLaunchTable();
        });
      });
    }

    function renderLaunchTable() {
      const rows = (activeDossier.launch_radar || []).filter(r =>
        activeLaunchCat === "all" || (r.category || "").toLowerCase().includes(activeLaunchCat.toLowerCase())
      );
      document.getElementById("launch-table-body").innerHTML = rows.map(r => `
        <tr>
          <th scope="row">${esc(r.name)}</th>
          <td><span class="spec-chip">${esc(r.category)}</span></td>
          <td>${esc(r.vendor)}</td>
          <td>${esc(r.killer_spec)}</td>
          <td><span class="spec-chip">${esc(r.availability)}</span></td>
          <td><a class="source-link" href="${safeUrl(r.source_url)}" target="_blank" rel="noopener noreferrer">Open ↗</a></td>
        </tr>
      `).join("") || `<tr><td colspan="6">ไม่มีรายการในหมวดหมู่นี้</td></tr>`;
    }

    function renderBottomSections() {
      document.getElementById("briefs-list").innerHTML = (activeDossier.track_briefs || []).map(b => {
        const meta = TRACK_META[b.track] || { icon: "⚡" };
        return `
          <div class="brief-item">
            <span aria-hidden="true">${esc(meta.icon)}</span>
            <div>
              <span class="spec-chip">${esc(b.tag)}</span>
              <strong>${esc(b.headline)}</strong> —
              <span style="color:var(--text-secondary)">${esc(b.punchline)}</span>
              <a class="source-link" href="${safeUrl(b.source_url)}" target="_blank" rel="noopener noreferrer">↗</a>
            </div>
          </div>`;
      }).join("");

      document.getElementById("watchlist-list").innerHTML = (activeDossier.next_week_watchlist || []).map(w => `
        <div class="watch-item">
          <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:800; color:var(--accent-gold);">⏱️ ${esc(w.window)} • [${esc(w.hype_level)}]</div>
          <div style="margin-top:2px;">${esc(w.event)}</div>
        </div>
      `).join("");
    }

    /* Archive Selector */
    const INITIAL_MARKDOWN = document.getElementById("raw-markdown-data").value;
    function initArchiveSelect() {
      const sel = document.getElementById("archive-select");
      const list = Array.isArray(ARCHIVE_INDEX) && ARCHIVE_INDEX.length
        ? ARCHIVE_INDEX
        : [{ date: activeDossier.date, week_id: activeDossier.week_id, label: `${activeDossier.week_id} (${activeDossier.date})`, json_path: "data/latest.json" }];

      sel.innerHTML = list.map((item, idx) =>
        `<option value="${esc(item.json_path)}" ${idx === 0 ? "selected" : ""}>🗂️ ${esc(item.label || item.date)}</option>`
      ).join("");

      sel.addEventListener("change", async () => {
        const target = sel.value;
        if (target === "data/latest.json" || sel.selectedIndex === 0) {
          document.getElementById("raw-markdown-data").value = INITIAL_MARKDOWN;
          renderDossier(INITIAL_DOSSIER);
          playSfx("shutter");
          return;
        }
        try {
          const resp = await fetch(target);
          if (!resp.ok) throw new Error("Fetch failed");
          const data = await resp.json();
          try {
            const mdResp = await fetch(target.replace(/\.json$/, ".md"));
            if (mdResp.ok) {
              document.getElementById("raw-markdown-data").value = await mdResp.text();
            }
          } catch (e) {}
          renderDossier(data);
          playSfx("shutter");
        } catch (err) {
          alert("การสลับดูแฟ้มย้อนหลังข้ามไฟล์ต้องเปิดผ่านเว็บ (GitHub Pages หรือ Live Server) ครับ");
          sel.selectedIndex = 0;
        }
      });
    }

    /* Dark Mode Toggle (modern-web-guidance dark-mode-toggle standard) */
    function initThemeToggle() {
      const meta = document.querySelector('meta[name="color-scheme"]');
      const btn = document.getElementById("theme-toggle-btn");
      const label = document.getElementById("theme-toggle-label");

      function getSystemDark() {
        return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      }
      function getEffectiveScheme() {
        const content = meta.content;
        if (content === "dark" || content === "light") return content;
        return getSystemDark() ? "dark" : "light";
      }
      function updateLabel() {
        const eff = getEffectiveScheme();
        label.textContent = eff === "dark" ? "โหมดสว่าง" : "โหมดมืด Cyber";
      }

      btn.addEventListener("click", () => {
        const current = getEffectiveScheme();
        const target = current === "dark" ? "light" : "dark";
        const sys = getSystemDark() ? "dark" : "light";
        try {
          if (target === sys) {
            localStorage.removeItem("color-scheme");
            meta.content = "light dark";
          } else {
            localStorage.setItem("color-scheme", target);
            meta.content = target;
          }
        } catch (e) {
          meta.content = target;
        }
        updateLabel();
        playSfx("radar");
      });

      window.addEventListener("storage", (e) => {
        if (e.key === "color-scheme") {
          meta.content = e.newValue || "light dark";
          updateLabel();
        }
      });
      updateLabel();
    }

    /* Controls Binding */
    function initControls() {
      const pBtn = document.getElementById("mode-paparazzi-btn");
      const eBtn = document.getElementById("mode-engineer-btn");
      pBtn.addEventListener("click", () => {
        currentMode = "paparazzi";
        pBtn.setAttribute("aria-pressed", "true");
        eBtn.setAttribute("aria-pressed", "false");
        playSfx("shutter");
        renderScoops();
        announce("เปลี่ยนเป็นโหมดปาปารัสซี่");
      });
      eBtn.addEventListener("click", () => {
        currentMode = "engineer";
        pBtn.setAttribute("aria-pressed", "false");
        eBtn.setAttribute("aria-pressed", "true");
        playSfx("shutter");
        renderScoops();
        announce("เปลี่ยนเป็นโหมดสเปกวิศวกร");
      });

      document.getElementById("scoop-search").addEventListener("input", (e) => {
        searchQuery = e.target.value;
        renderScoops();
      });

      const sfxBtn = document.getElementById("sfx-toggle-btn");
      sfxBtn.addEventListener("click", () => {
        sfxEnabled = !sfxEnabled;
        sfxBtn.setAttribute("aria-pressed", String(sfxEnabled));
        sfxBtn.textContent = sfxEnabled ? "📸 Shutter FX: ON" : "🔇 Shutter FX: OFF";
        if (sfxEnabled) playSfx("radar");
      });

      document.getElementById("copy-md-btn").addEventListener("click", () => {
        const md = document.getElementById("raw-markdown-data").value;
        navigator.clipboard.writeText(md).then(() => {
          playSfx("shutter");
          announce("คัดลอกรายงาน Markdown แล้ว");
          alert("📋 คัดลอกรายงาน Markdown เรียบร้อยแล้ว!");
        });
      });

      // Thai Voice Spy Briefing
      const voiceBtn = document.getElementById("voice-play-btn");
      const speedBtn = document.getElementById("voice-speed-btn");
      const rates = [1.0, 1.1, 1.25, 1.5];
      let rateIdx = 1;

      speedBtn.addEventListener("click", () => {
        rateIdx = (rateIdx + 1) % rates.length;
        voiceRate = rates[rateIdx];
        speedBtn.textContent = `⏩ ${voiceRate}x`;
      });

      voiceBtn.addEventListener("click", () => {
        if (!("speechSynthesis" in window)) {
          alert("เบราว์เซอร์นี้ไม่รองรับการอ่านออกเสียงภาษาไทย");
          return;
        }
        if (isSpeaking) {
          window.speechSynthesis.cancel();
          isSpeaking = false;
          voiceBtn.setAttribute("aria-pressed", "false");
          voiceBtn.textContent = "🔊 ฟังวิทยุสายลับ 60 วิ";
          return;
        }
        window.speechSynthesis.cancel();
        const utt = new SpeechSynthesisUtterance(activeDossier.audio_script_th || "");
        utt.lang = "th-TH";
        utt.rate = voiceRate;
        utt.onstart = () => {
          isSpeaking = true;
          voiceBtn.setAttribute("aria-pressed", "true");
          voiceBtn.textContent = "⏹️ หยุดเสียงวิทยุสายลับ";
        };
        utt.onend = utt.onerror = () => {
          isSpeaking = false;
          voiceBtn.setAttribute("aria-pressed", "false");
          voiceBtn.textContent = "🔊 ฟังวิทยุสายลับ 60 วิ";
        };
        window.speechSynthesis.speak(utt);
      });
    }

    initThemeToggle();
    initControls();
    initArchiveSelect();
    renderDossier(INITIAL_DOSSIER);
  </script>
</body>
</html>
"""


def _safe_json_for_script(obj: Any) -> str:
    """Serialize JSON safely for inline <script> embedding."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def build_cyber_cockpit_html(
    payload: Dict[str, Any],
    raw_markdown: str,
    archive_index: List[Dict[str, Any]],
) -> str:
    """Hydrate HTML shell using token replacement (immune to CSS/JS brace collisions)."""
    banner = payload.get("episode_banner", {})
    page_title = f"Cyber Paparazzi — {banner.get('episode_title', 'Weekly Tech & AI Dossier')}"
    last_updated = payload.get("date_formatted", payload.get("date", ""))

    return (
        HTML_SHELL_TEMPLATE
        .replace("__PAGE_TITLE__", html.escape(page_title))
        .replace("__LAST_UPDATED__", html.escape(last_updated))
        .replace("__ESCAPED_RAW_MARKDOWN__", html.escape(raw_markdown))
        .replace("__EMBEDDED_DOSSIER_JSON__", _safe_json_for_script(payload))
        .replace("__ARCHIVE_INDEX_JSON__", _safe_json_for_script(archive_index))
        .replace("__TRACK_META_JSON__", _safe_json_for_script(SPY_TRACKS))
    )


def _update_archive_index(payload: Dict[str, Any], iso_date: str) -> List[Dict[str, Any]]:
    """Maintain rolling archive index JSON for multi-week browser switching."""
    existing: List[Dict[str, Any]] = []
    if ARCHIVE_INDEX_PATH.exists():
        try:
            with open(ARCHIVE_INDEX_PATH, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    existing = loaded
        except Exception:
            existing = []

    banner = payload.get("episode_banner", {})
    week_id = payload.get("week_id", "")
    entry = {
        "date": iso_date,
        "week_id": week_id,
        "label": f"{week_id} ({iso_date}) — {banner.get('season_ep', '')}",
        "json_path": f"archives/{iso_date}.json",
        "md_path": f"archives/{iso_date}.md",
    }
    filtered = [e for e in existing if e.get("date") != iso_date]
    updated = [entry] + filtered
    updated = updated[:24]

    ARCHIVE_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ARCHIVE_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(updated, f, ensure_ascii=False, indent=2)
    return updated


def save_all_reports(payload: Dict[str, Any], raw_markdown: str) -> None:
    """Write LATEST.md, archives/*.md & *.json, README.md, data/*.json, web/index.html, and index.html."""
    iso_date = payload.get("date", get_iso_date())
    ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 1. Markdown reports
    with open(LATEST_MD_PATH, "w", encoding="utf-8") as f:
        f.write(raw_markdown)

    with open(ARCHIVES_DIR / f"{iso_date}.md", "w", encoding="utf-8") as f:
        f.write(raw_markdown)

    # 2. Machine-readable JSON snapshots
    with open(LATEST_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    with open(ARCHIVES_DIR / f"{iso_date}.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    archive_index = _update_archive_index(payload, iso_date)

    # 3. Visual README.md with embedded latest dossier
    readme_content = f"""# 📸🕵️‍♂️ Cyber Paparazzi HQ (`cyber-paparazzi`)

> **Autonomous Weekly IT, AI, Hardware & Frontier Tech Spy Engine**  
> ส่งสายลับดักรอข่าว Official Labs & Tier-1 Tech Press ทั่วโลก รายงานเป็น **Series + Visual Dossier** ทุกเช้าวันจันทร์ เวลา 08:00 น.

[![Weekly Spy Dispatch](https://img.shields.io/badge/Schedule-Monday%2008%3A00%20BKK-00f5d4?style=for-the-badge)](./.github/workflows/weekly_spy.yml)
[![Powered By Gemini](https://img.shields.io/badge/AI-Gemini%20Flash%20Series-3b82f6?style=for-the-badge)](https://ai.google.dev/)
[![Allied HQ](https://img.shields.io/badge/Allied%20HQ-v2.0%20Synchronized-ff4d8d?style=for-the-badge)](./project_manifest.json)

---

## 🎯 5 สายลับเฝ้าระวังหลัก (The 5 Spy Tracks)

| Track | ขอบเขตที่สายสืบดักรอ | แหล่งข่าวหลัก |
|:---:|:---|:---|
| 🤖 **AI Frontier War** | โมเดลใหม่ Agents, Reasoning, ราคา API | OpenAI, Google AI/DeepMind, Anthropic |
| 🖥️ **Hardware & Silicon** | GPU, NPU, ชิปประมวลผล, โน้ตบุ๊ก, อุปกรณ์ล้ำยุค | NVIDIA, Apple, AMD, Tom's Hardware |
| 🛠️ **Software, OS & DevTools** | IDE, Frameworks, Cloud, OS Updates | Microsoft AI, GitHub Blog, Ars Technica, The Verge |
| 🦙 **Open-Weight & Local AI** | โมเดลเปิดเสรี, Ollama/vLLM, Quantization | Hugging Face Daily Papers, Meta AI, Open-Weight Wire |
| 🧬 **Deep Tech & Wildcards** | Robotics, Quantum, Energy, Bio-AI | MIT Technology Review, IEEE Spectrum |

---

## 📖 แฟ้มข่าวกรองประจำสัปดาห์ล่าสุด (Latest Weekly Spy Dossier)
👉 **อ่านไฟล์แยก:** [`LATEST.md`](./LATEST.md) • **เปิดหน้าเว็บ Interactive:** [`index.html`](./index.html)

<!-- PAPARAZZI_REPORT_START -->
{raw_markdown}
<!-- PAPARAZZI_REPORT_END -->

---

## 💻 การรันและทดสอบในเครื่อง (Local Setup)

```bash
pip install -r requirements.txt
cp .env.example .env  # ใส่ GEMINI_API_KEY

# ทดสอบดึงข่าวจากเครือข่ายสายสืบโดยไม่เรียก AI
python main.py --dry-run-sources

# สั่งวิเคราะห์และสร้างแฟ้มสัปดาห์นี้ใหม่ทันที (ไม่ยิง Telegram)
python main.py --force
```
"""
    with open(README_MD_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 4. Build interactive Cyber Cockpit HTML
    cockpit_html = build_cyber_cockpit_html(payload, raw_markdown, archive_index)
    INDEX_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(cockpit_html)

    with open(ROOT_INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(cockpit_html)
