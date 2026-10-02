import os
import json
import feedparser
import requests

# Environment variables mapping to GitHub Secrets
FEEDS_JSON = os.environ.get("CANVAS_FEEDS")
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")
STATE_FILE = "processed_ids.json"

def main():
    if not FEEDS_JSON or not NTFY_TOPIC:
        print("Error: Missing environment variables (CANVAS_FEEDS or NTFY_TOPIC).")
        return

    # Parse the JSON containing the courses and their RSS feeds
    try:
        courses = json.loads(FEEDS_JSON)
    except json.JSONDecodeError:
        print("Error: The CANVAS_FEEDS secret is not a valid JSON format.")
        return

    # Load announcement history to manage state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            processed_ids = json.load(file)
    else:
        processed_ids = []

    new_announcements_count = 0

    # Iterate over each course in the JSON dictionary
    for course_name, rss_url in courses.items():
        print(f"Checking: {course_name}...")
        feed = feedparser.parse(rss_url)
        
        # Iterate in reverse to notify older announcements first
        for entry in reversed(feed.entries):
            announcement_id = entry.id
            
            if announcement_id not in processed_ids:
                title = entry.title
                link = entry.link
                
                # Format the push notification
                headers = {
                    "Title": f"{course_name}",
                    "Click": link,
                    "Tags": "blue_book,bell"
                }
                
                # Send the notification via ntfy.sh
                requests.post(
                    f"https://ntfy.sh/{NTFY_TOPIC}", 
                    data=title.encode('utf-8'), 
                    headers=headers
                )
                
                # Add ID to the processed list to avoid duplicate notifications
                processed_ids.append(announcement_id)
                new_announcements_count += 1

    # Save the updated state if new announcements were found
    if new_announcements_count > 0:
        # Using indent=2 makes the JSON readable in the GitHub repository
        with open(STATE_FILE, "w") as file:
            json.dump(processed_ids, file, indent=2)
        print(f"Successfully notified {new_announcements_count} new announcements.")
    else:
        print("No new announcements found for any course.")

if __name__ == "__main__":
    main()