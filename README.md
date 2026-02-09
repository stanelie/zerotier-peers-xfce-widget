ZeroTier XFCE Dashboard

A lightweight, "NeoRouter-style" status monitor for XFCE/Xubuntu. It provides an at-a-glance connection count on your taskbar and an instant, detailed network map when clicked.
Features

    Live Taskbar Stats: Shows Online / Total members directly in your panel.

    Instant Detailed Popup: Click the widget to see Hostnames, Zerotier IPs, WAN IPs, and "Last Seen" times.

    Dark Mode Support: Uses a forced GTK dark theme for a sleek look.

    Zero-Latency UI: Uses data caching so the window pops up the millisecond you click it.

    Privacy-Focused: API tokens are passed via command line, not stored in the script.

🛠 Installation
1. Prerequisites

Ensure you have the necessary dependencies installed:
Bash

sudo apt update
sudo apt install python3-requests yad zenity

2. Download the Script

Save the zerotier.py script to your home directory (e.g., /home/yourusername/zerotier.py).

Make it executable:
Bash

chmod +x ~/zerotier.py

3. Add to XFCE Panel

    Right-click your XFCE Panel -> Panel -> Add New Items.

    Select Generic Monitor (Genmon).

    Right-click the new (empty) widget on your panel -> Properties.

    Enter the following:

        Command: python3 /home/YOUR_USER/zerotier.py --token YOUR_API_TOKEN --widget

        Label: (Uncheck this)

        Period (s): 30

        Font: (Leave as default)

🔑 How to get an API Token

    Log into [suspicious link removed].

    Go to Account Settings.

    Scroll down to API Access Tokens.

    Generate a new token and copy it into the command above.

🚀 Usage

    In the Panel: Displays 🟢 Online / Total.

    OnClick: Opens a dark-themed table showing all network members.

    In Terminal: You can also run it as a standalone dashboard by running: python3 zerotier.py --token YOUR_TOKEN

Troubleshooting Tip:

If the widget looks "crashed" (no icon), run the command in your terminal manually to see if your API token is correct. If the panel stops responding to clicks, restart it with xfce4-panel -r.
