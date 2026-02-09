import requests
import time
import os
import sys
import argparse
from datetime import datetime

# --- CONFIGURATION ---
SNAPSHOT_PATH = "/tmp/zt_snapshot.txt"
ICON_PATH = "/usr/share/icons/Humanity-Dark/status/22/network-idle.svg"
BASE_URL = "https://api.zerotier.com/api/v1"

def get_relative_time(ls_ms):
    if not ls_ms or ls_ms == 0: return "Never"
    diff = (time.time() * 1000 - ls_ms) / 1000
    if diff < 60: return f"{int(diff)}s"
    if diff < 3600: return f"{int(diff//60)}m"
    if diff < 86400: return f"{int(diff//3600)}h {int((diff%3600)//60)}m"
    return f"{int(diff//86400)}d"

def fetch_data(api_token):
    headers = {"Authorization": f"token {api_token}"}
    output = []
    try:
        networks = requests.get(f"{BASE_URL}/network", headers=headers).json()
        if isinstance(networks, dict) and networks.get('status') == 403:
            return "Error: Invalid API Token"
            
        output.append(f"ZeroTier Status | {datetime.now().strftime('%H:%M:%S')}")
        for nw in networks:
            nw_id = nw['id']
            nw_name = nw.get('config', {}).get('name', 'Unknown')
            output.append(f"\n[ NETWORK: {nw_name} ]")
            output.append(f"{'HOSTNAME':<18} | {'ZT IP':<15} | {'WAN IP':<16} | {'SEEN':<8} | STATUS")
            output.append("-" * 72)
            
            members = requests.get(f"{BASE_URL}/network/{nw_id}/member", headers=headers).json()
            processed = []
            for m in members:
                ls_ms = m.get('lastSeen', 0) or 0
                is_online = (time.time() * 1000 - ls_ms) < 300000 
                processed.append({
                    'name': str(m.get('name') or m.get('nodeId'))[:18],
                    'zt_ip': (m.get('config', {}).get('ipAssignments', []) or ["No IP"])[0],
                    'wan_ip': str(m.get('physicalAddress', '---'))[:16],
                    'seen': get_relative_time(ls_ms),
                    'online': is_online
                })
            for m in sorted(processed, key=lambda x: (not x['online'], x['name'].lower())):
                icon = "🟢" if m['online'] else "🔴"
                output.append(f"{m['name']:<18} | {m['zt_ip']:<15} | {m['wan_ip']:<16} | {m['seen']:<8} | {icon}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: {e}"

def handle_widget(api_token):
    data = fetch_data(api_token)
    with open(SNAPSHOT_PATH, "w") as f:
        f.write(data)
    
    online = data.count("🟢")
    total = data.count("🟢") + data.count("🔴")
    
    script_path = os.path.abspath(__file__)
    
    print(f"<img>{ICON_PATH}</img>")
    print(f"<txt><span fgcolor='#dfdfdf' weight='bold'> {online}/{total}</span></txt>")
    # Pass the token into the click command so the popup knows it too
    print(f"<click>python3 {script_path} --token {api_token} --popup</click>")
    print(f"<tool>Last sync: {datetime.now().strftime('%H:%M:%S')}</tool>")

def handle_popup():
    if not os.path.exists(SNAPSHOT_PATH):
        return
    
    with open(SNAPSHOT_PATH, "r") as f:
        content = f.read()
    
    # Zenity is much more stable with the --font flag on Xubuntu
    cmd = [
        "zenity", "--text-info", 
        "--title=ZeroTier Status", 
        "--width=800", "--height=500", 
        "--ok-label=Close", 
        "--font=Monospace 10", 
        "--no-wrap"
    ]
    
    import subprocess
    env = os.environ.copy()
    env["GTK_THEME"] = "Adwaita:dark"
    
    # This pipes the text directly into the Zenity window
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, env=env, text=True)
    process.communicate(input=content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ZeroTier XFCE Dashboard")
    parser.add_argument("--token", help="ZeroTier API Token")
    parser.add_argument("--widget", action="store_true", help="Run in XFCE Widget mode")
    parser.add_argument("--popup", action="store_true", help="Run in Popup mode")
    
    args = parser.parse_args()

    if args.popup:
        handle_popup()
    elif args.widget:
        if not args.token:
            print("<txt>Missing Token</txt>")
        else:
            handle_widget(args.token)
    else:
        # Terminal Mode
        if not args.token:
            print("Usage: python3 zerotier.py --token YOUR_TOKEN")
        else:
            try:
                while True:
                    os.system('clear')
                    print(fetch_data(args.token))
                    time.sleep(30)
            except KeyboardInterrupt:
                pass

