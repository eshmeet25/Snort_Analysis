# analyzer.py
from collections import Counter
import re
import json
from email_alert import send_email

def parse_alerts(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_alerts = 0
    priorities = Counter()
    src_ips = Counter()
    alert_msgs = Counter()

    for line in lines:
        if '[**]' in line:
            total_alerts += 1
            msg_match = re.search(r'\[\*\*\] \[(.*?)\] (.*?) \[\*\*\]', line)
            if msg_match:
                alert_msgs[msg_match.group(2)] += 1

        if 'Priority:' in line:
            prio = re.search(r'Priority: (\d+)', line)
            if prio:
                priorities[int(prio.group(1))] += 1

        if '->' in line:
            ip_match = re.match(r'(\d+\.\d+\.\d+\.\d+):', line.strip())
            if ip_match:
                src_ips[ip_match.group(1)] += 1

    return total_alerts, priorities, src_ips, alert_msgs

def print_and_email_summary():
    total, prios, srcs, msgs = parse_alerts("alert.txt")

    summary = f"📊 Snort Alert Summary 📊\n\n"
    summary += f"Total Alerts: {total}\n\n"

    summary += "Alerts by Priority:\n"
    for p in sorted(prios):
        summary += f"  Priority {p}: {prios[p]}\n"

    summary += "\nTop 5 Source IPs:\n"
    for ip, count in srcs.most_common(5):
        summary += f"  {ip}: {count} alerts\n"

    summary += "\nTop 5 Alert Types:\n"
    for msg, count in msgs.most_common(5):
        summary += f"  {msg}: {count} times\n"

    # ✅ Save priority counts to JSON for chart.js
    with open("alerts_data.json", "w") as json_file:
        json.dump(dict(prios), json_file)

    # ✅ Print to console
    print(summary)

    # ✅ Send email if Priority 1 alerts exist
    if prios.get(1, 0) > 0:
        send_email("🚨 Snort High Priority Alert Summary", summary)

if __name__ == "__main__":
    print_and_email_summary()
