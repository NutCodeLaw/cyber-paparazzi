"""
Cyber Paparazzi - Main Entrypoint & Weekly Spy Orchestrator
Runs every Monday at 08:00 AM Bangkok Time (or manually via CLI).
"""
import argparse
import sys

from src.ai_analyst import run_spy_analysis
from src.notifier import send_telegram_briefing
from src.reporter import generate_markdown_report, save_all_reports
from src.spy_network import collect_spy_intel
from src.state_manager import (
    append_weekly_history,
    get_current_week_identifier,
    get_recent_history_context,
    get_sagas_context_for_prompt,
    is_current_week_already_reported,
    load_seen_urls,
    save_seen_urls,
    update_sagas,
)
from src.utils import format_thai_full_date, get_iso_date, get_now_bangkok


def main() -> None:
    parser = argparse.ArgumentParser(description="Cyber Paparazzi Weekly IT & AI Spy Engine")
    parser.add_argument("--preview", action="store_true", help="Print Markdown report to stdout without saving")
    parser.add_argument("--force", action="store_true", help="Force regenerate report even if this week ran already")
    parser.add_argument("--dry-run-sources", action="store_true", help="Test Spy Network RSS/API feeds only")
    parser.add_argument("--telegram", action="store_true", help="Explicitly send Telegram briefing locally")
    args = parser.parse_args()

    now = get_now_bangkok()
    thai_date = format_thai_full_date(now)
    iso_date = get_iso_date(now)
    current_week = get_current_week_identifier(now)

    print("=" * 68)
    print("📸 Cyber Paparazzi HQ — Weekly IT & AI Intelligence Engine")
    print(f"📅 {thai_date} | Week: {current_week} | Time: {now.strftime('%H:%M:%S')} BKK")
    print("=" * 68)

    if args.dry_run_sources:
        print("\n[Dry-Run] Testing 3-Tier Spy Network feeds...")
        intel = collect_spy_intel(ignore_seen=True)
        print(f"Stats: {intel['stats']}")
        for fh in intel["feed_health"]:
            mark = "✅" if fh["ok"] and fh["count"] > 0 else ("⚠️ 0 items" if fh["ok"] else f"❌ {fh['error']}")
            print(f"  - {fh['name']}: {fh['count']} ({mark})")
        sys.exit(0)

    # 0. Weekly Schedule Guard
    if not args.force and is_current_week_already_reported():
        print(f"\n[Guard] 🛡️ Week {current_week} has already been published.")
        print("   -> Next scheduled run: Monday 08:00 AM Bangkok (or run with --force).")
        sys.exit(0)

    # 1. Dispatch Spy Network
    print("\n[1/5] 🕵️‍♂️ Dispatching Spy Network across Tier-1 Official, Tech Press & Dev Pulse...")
    seen_urls = load_seen_urls()
    intel_data = collect_spy_intel(seen_urls=seen_urls, ignore_seen=args.force)
    stats = intel_data["stats"]
    print(
        f"   -> {stats['active_feeds']}/{stats['total_feeds']} feeds active | "
        f"{stats['selected_count']} verified signals intercepted"
    )
    if stats["selected_count"] == 0:
        print("❌ No intelligence items fetched. Aborting safely.")
        sys.exit(1)

    # 2. Load Weekly History & Series Sagas
    print("\n[2/5] 🧠 Loading Multi-Week Series Sagas & Continuity Context...")
    history_context = get_recent_history_context(max_weeks=3)
    sagas_context = get_sagas_context_for_prompt()

    # 3. Synthesize Visual Intelligence via Gemini
    print("\n[3/5] 🔬 Synthesizing Visual Dossier & Series Episodes via Gemini...")
    try:
        analysis = run_spy_analysis(intel_data, history_context, sagas_context)
    except Exception as exc:
        print(f"❌ Gemini synthesis failed: {exc}")
        sys.exit(1)

    payload = {
        "week_id": current_week,
        "date": iso_date,
        "date_formatted": thai_date,
        "time": now.strftime("%H:%M น."),
        "intel_stats": stats,
        **analysis,
    }

    # 4. Render Visual Markdown & Cyber Cockpit
    print("\n[4/5] 🎨 Rendering Visual Markdown & Interactive Cyber Cockpit...")
    raw_markdown = generate_markdown_report(payload)

    if args.preview:
        print("\n" + "=" * 68)
        print(raw_markdown)
        print("=" * 68)
        sys.exit(0)

    save_all_reports(payload, raw_markdown)

    # 5. Persist State, Sagas & Notify
    print("\n[5/5] 💾 Persisting Series Memory & Checking Telegram Dispatch...")
    update_sagas(analysis.get("tech_series_sagas", []))
    topics_summary = [
        {"title": sc.get("headline", ""), "track": sc.get("track", "")}
        for sc in analysis.get("top_scoops", [])
    ]
    append_weekly_history(
        current_week,
        iso_date,
        analysis.get("episode_banner", {}).get("episode_title", ""),
        topics_summary,
    )
    used_urls = [sc.get("source_url", "") for sc in analysis.get("top_scoops", [])]
    used_urls.extend(r.get("source_url", "") for r in analysis.get("launch_radar", []))
    save_seen_urls([u for u in used_urls if u])

    send_telegram_briefing(payload)

    print("\n🎉 Cyber Paparazzi Weekly Dossier complete!")
    print("📁 Generated artifacts:")
    print("   - LATEST.md & README.md")
    print(f"   - archives/{iso_date}.md & archives/{iso_date}.json")
    print("   - data/latest.json, data/sagas.json, data/history.json")
    print("   - index.html & web/index.html (Interactive Cyber Cockpit)")


if __name__ == "__main__":
    main()
