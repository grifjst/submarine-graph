import os
import requests
from datetime import datetime, timedelta, timezone
import svgwrite
import random

# === CONFIGURATION ===
GITHUB_USERNAME = "grifjst"
TOKEN = os.getenv("GITHUB_TOKEN")  # Must be set as environment variable before running

COLORS = ['#aceafa', '#a0e8fa', '#93e5fa', '#84e2fa', '#abe6f5']
SQUARE_SIZE = 12
PADDING = 2
COLS = 52
ROWS = 7
WIDTH = COLS * (SQUARE_SIZE + PADDING)
HEIGHT = ROWS * (SQUARE_SIZE + PADDING)
API_URL = "https://api.github.com/graphql"

def fetch_contributions(username, token):
    headers = {"Authorization": f"Bearer {token}"}
    today = datetime.now(timezone.utc).isoformat()
    start_date = (datetime.now(timezone.utc) - timedelta(days=365)).isoformat()
    query = """
    query ($user: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $user) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "user": username,
        "from": start_date,
        "to": today,
    }
    response = requests.post(API_URL, json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code != 200:
        print("GraphQL errors:", response.json().get("errors", "Unknown"))
        raise Exception("GitHub API request failed.")
    weeks = response.json()['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    days = []
    for week in weeks:
        for day in week['contributionDays']:
            days.append(day)
    return days

def color_for_count(count):
    if count == 0:
        return "#caedfa"
    elif count <= 2:
        return COLORS[0]
    elif count <= 4:
        return COLORS[1]
    elif count <= 8:
        return COLORS[2]
    elif count <= 12:
        return COLORS[3]
    else:
        return COLORS[4]

def create_days_colored(days_raw):
    return [{
        "date": d['date'],
        "count": d['contributionCount'],
        "color": color_for_count(d['contributionCount'])
    } for d in days_raw]

def create_svg(days_colored, filename="submarine_graph.svg"):
    dwg = svgwrite.Drawing(filename, size=(f"{WIDTH}px", f"{HEIGHT}px"))
    dwg.attribs['xmlns'] = "http://www.w3.org/2000/svg"

    # Draw contribution squares
    for i, day in enumerate(days_colored):
        col = i // ROWS
        row = i % ROWS
        x = col * (SQUARE_SIZE + PADDING)
        y = row * (SQUARE_SIZE + PADDING)
        dwg.add(dwg.rect(insert=(x, y), size=(SQUARE_SIZE, SQUARE_SIZE), fill=day['color']))

    # Submarine path - random sample of contribution blocks
    path = random.sample(range(len(days_colored)), min(10, len(days_colored)))
    path.sort()

    keyframes = []
    for idx, point in enumerate(path):
        col = point // ROWS
        row = point % ROWS
        x = col * (SQUARE_SIZE + PADDING)
        y = row * (SQUARE_SIZE + PADDING)
        percent = int((idx / (len(path) - 1)) * 100)
        keyframes.append(f"{percent}% {{ transform: translate({x}px, {y}px); }}")

    animation_css = f"""
    @keyframes moveSub {{
        {'\n'.join(keyframes)}
    }}
    #sub {{
        animation: moveSub 23s linear infinite;
        transform-origin: 0 0;
    }}
    .bubble {{
        animation: bubbleRise 1.5s ease-in infinite;
    }}
    @keyframes bubbleRise {{
        0% {{ opacity: 0.6; transform: translate(0, 0); }}
        100% {{ opacity: 0; transform: translate(0, -12px); }}
    }}
    """

    dwg.defs.add(dwg.style(animation_css))

    sub_group = dwg.g(id="sub")

    # Submarine body
    sub_group.add(dwg.ellipse(center=(20, 10), r=(18, 8), fill="#003366"))

    # Propeller
    sub_group.add(dwg.rect(insert=(1, 7), size=(2, 6), fill="#888", rx=1))
    sub_group.add(dwg.circle(center=(2, 10), r=1.5, fill="#aaa"))

    # Tail fins
    sub_group.add(dwg.polygon(points=[(2, 5), (0, 3), (2, 3)], fill="#005599"))
    sub_group.add(dwg.polygon(points=[(2, 15), (0, 17), (2, 17)], fill="#005599"))

    # Periscope
    sub_group.add(dwg.rect(insert=(28, -5), size=(2, 10), fill="#005599"))
    sub_group.add(dwg.rect(insert=(26, -7), size=(6, 2), fill="#005599"))

    # Windows
    sub_group.add(dwg.circle(center=(14, 10), r=2, fill="#66ccff"))
    sub_group.add(dwg.circle(center=(20, 10), r=2, fill="#66ccff"))
    sub_group.add(dwg.circle(center=(26, 10), r=2, fill="#66ccff"))

    # Bubbles
    for i in range(3):
        bubble = dwg.circle(center=(-5 - i * 6, 10), r=2, fill="white", opacity=0.5)
        bubble.update({'class': 'bubble'})
        sub_group.add(bubble)

    dwg.add(sub_group)
    dwg.save()
    print(f"✅ SVG saved as {filename}")

if __name__ == "__main__":
    print(f"Fetching GitHub contributions for {GITHUB_USERNAME}...")
    raw_days = fetch_contributions(GITHUB_USERNAME, TOKEN)
    days_colored = create_days_colored(raw_days)
    create_svg(days_colored)


