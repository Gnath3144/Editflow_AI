"""
Script to update Day 01 YouTube video visibilities from PRIVATE to UNLISTED.
Preserves all titles, descriptions, categories, tags, and languages intact.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.authentication import AuthManager
from core.channel_manager import ChannelManager

TARGET_CHANNEL_ID = "UClHA7HX1h5eWwgfVjt8wb5A"
VIDEO_IDS = [
    "zP0kOyucuMA",  # Lesson 01
    "x-7RglvLPVw",  # Lesson 02
    "v0Ce7IYYCvU",  # Lesson 03
    "bUsxJjJW0uY",  # Lesson 04
    "ThBJnBpSjkI",  # Lesson 05
    "EjkFaIYaU60",  # Lesson 06
]


def main():
    print("=" * 65)
    print("🔄 UPDATING DAY 01 VIDEO VISIBILITY: PRIVATE -> UNLISTED")
    print("=" * 65)

    auth = AuthManager()
    service = auth.get_youtube_service()
    if not service:
        print("❌ Error: Unable to build YouTube API service.")
        sys.exit(1)

    cm = ChannelManager(service, expected_channel_id=TARGET_CHANNEL_ID)
    ok, info, msg = cm.fetch_primary_channel()
    if not ok or not info:
        print(f"❌ Security Block: {msg}")
        sys.exit(1)

    print(f"✅ Verified Channel: {info.channel_title} ({info.channel_id})\n")

    results = []

    for idx, vid in enumerate(VIDEO_IDS, start=1):
        print(f"[{idx}/6] Fetching metadata for video ID: {vid}...")
        res = service.videos().list(part="snippet,status", id=vid).execute()
        items = res.get("items", [])
        if not items:
            print(f"  ❌ Video {vid} not found on YouTube.")
            results.append({"id": vid, "title": "Not Found", "status": "NOT_FOUND"})
            continue

        item = items[0]
        snippet = item.get("snippet", {})
        status = item.get("status", {})
        title = snippet.get("title", "")
        old_privacy = status.get("privacyStatus", "")

        print(f"  Title: {title}")
        print(f"  Current Privacy: {old_privacy.upper()}")

        if old_privacy.lower() == "unlisted":
            print("  ℹ️ Video is already UNLISTED. Skipping update.")
            results.append({"id": vid, "title": title, "status": "UNLISTED"})
            continue

        # Prepare update body preserving all fields
        update_body = {
            "id": vid,
            "snippet": {
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "tags": snippet.get("tags", []),
                "categoryId": snippet.get("categoryId", "27"),
                "defaultLanguage": snippet.get("defaultLanguage", "en"),
                "defaultAudioLanguage": snippet.get("defaultAudioLanguage", "en")
            },
            "status": {
                "privacyStatus": "unlisted",
                "selfDeclaredMadeForKids": status.get("selfDeclaredMadeForKids", False),
                "embeddable": status.get("embeddable", True),
                "license": status.get("license", "youtube")
            }
        }

        print("  Updating privacyStatus to 'unlisted'...")
        update_res = service.videos().update(part="snippet,status", body=update_body).execute()
        new_privacy = update_res.get("status", {}).get("privacyStatus", "")

        if new_privacy.lower() == "unlisted":
            print(f"  ✅ Successfully updated to UNLISTED!\n")
            results.append({"id": vid, "title": title, "status": "UNLISTED"})
        else:
            print(f"  ⚠️ Warning: Updated privacy is {new_privacy}\n")
            results.append({"id": vid, "title": title, "status": new_privacy})

    print("=" * 65)
    print("📊 VERIFICATION SUMMARY:")
    all_unlisted = True
    for r in results:
        status_icon = "✅" if r["status"].lower() == "unlisted" else "❌"
        print(f"  {status_icon} [{r['id']}] {r['title'][:45]}... ➔ {r['status'].upper()}")
        if r["status"].lower() != "unlisted":
            all_unlisted = False

    print("=" * 65)
    if all_unlisted:
        print("🎉 ALL 6 VIDEOS ARE NOW VERIFIED UNLISTED ON YOUTUBE!")
    else:
        print("⚠️ Some videos could not be set to UNLISTED.")


if __name__ == "__main__":
    main()
