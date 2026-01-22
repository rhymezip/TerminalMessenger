import os, subprocess, sys, base64, hashlib, threading, time
from datetime import datetime

def prepare_libs():
    libs = {"requests": "requests", "rich": "rich", "cryptography": "cryptography"}
    needed = []
    for lib_name, import_name in libs.items():
        try: __import__(import_name)
        except ImportError: needed.append(lib_name)
    if needed:
        flags = ["--break-system-packages"] if os.name != 'nt' else []
        for n in needed:
            subprocess.check_call([sys.executable, "-m", "pip", "install", n, "--quiet"] + flags)

prepare_libs()

import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.panel import Panel
from cryptography.fernet import Fernet

console = Console(force_terminal=True)

def _build_conn():
    _m = "aHR0cHM6Ly90ZXJtaW5hbC1tZXNzZW5nZXItZjFmZWQtZGVmYXVsdC1ydGRiLmV1cm9wZS13ZXN0MS5maXJlYmFzZWRhdGFiYXNlLmFwcA=="
    return base64.b64decode(_m).decode()

DB_URL = _build_conn()
_k = b'YV9zeW00X3A0c3N3MHJkX2ZfcmVhbF9nZWVrc19vbmx5X3JobXk='
cipher = Fernet(base64.urlsafe_b64encode(_k.ljust(32)[:32]))
SALT = "Rhyme_Secret_99!_X"

def enc(data): return cipher.encrypt(data.encode()).decode()
def dec(data):
    try: return cipher.decrypt(data.encode()).decode()
    except: return None
def anonymize(text): return hashlib.sha256((text + SALT).encode()).hexdigest()[:12]
def hash_p(p): return hashlib.sha256((p + SALT).encode()).hexdigest()

LOGO = r"""
[bold red]████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝[/]
"""

def draw_header(user=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Align.center(LOGO))
    if user:
        console.print(f"[bold white]ID: {user.upper()}[/]{' ' * (45 - len(user))}[bold white]by rhymezip[/]")
    else:
        console.print(f"{' ' * 50}[bold white]by rhymezip[/]")
    console.print("\n")

def chat_screen(room_id, username, target):
    draw_header(username)
    console.print(Align.center(Panel(f"[bold white]🔒 TUNNEL: {username.upper()} <-> {target.upper()}\n[italic white](Type 'q' + 'Enter' to exit)[/]", border_style="green", expand=False)))

    shown_msgs = set()
    thread_active = True
    session = requests.Session()

    def listen_msgs():
        while thread_active:
            try:
                res = session.get(f"{DB_URL}/messages/{room_id}.json", timeout=10)
                data = res.json()
                if data:
                    for m_id in sorted(data.keys()):
                        if m_id not in shown_msgs:
                            m = data[m_id]
                            u_real = dec(m.get('u'))
                            if u_real and u_real != username:
                                text = dec(m.get('m'))
                                ts = m.get('t', '--:--')
                                console.print(f"[bold cadet_blue][{ts}][/] [bold orange_red1]{u_real.upper()}:[/] [bold white]{text}[/]")
                                sys.stdout.write('\a')
if os.name == 'nt':
    import winsound
    winsound.Beep(1000, 200)
                                sys.stdout.flush()
                            shown_msgs.add(m_id)
            except: pass
            time.sleep(1)

    threading.Thread(target=listen_msgs, daemon=True).start()

    while True:
        try:
            msg = input().strip()
            if not msg: continue
            sys.stdout.write("\033[A\033[K")
            if msg.lower() == 'q':
                thread_active = False
                break
            ts = datetime.now().strftime("%H:%M")
            console.print(f"[bold cadet_blue][{ts}][/] [bold red]YOU:[/][bold white] {msg}[/]")
            requests.post(f"{DB_URL}/messages/{room_id}.json", json={"u": enc(username), "m": enc(msg), "t": ts}, timeout=5)
        except: break

def main():
    try:
        current_user = None
        while not current_user:
            draw_header()
            u = Prompt.ask(" " * 12 + "👤 [bold white]USERNAME[/]").lower().strip()
            p = Prompt.ask(" " * 12 + "🔐 [bold white]PASSWORD[/]", password=True).strip()
            if not u or not p: continue

            u_id = anonymize(u)
            p_hash = hash_p(p)

            try:
                res = requests.get(f"{DB_URL}/users/{u_id}.json", timeout=10)
                data = res.json()
                if data is None:
                    requests.put(f"{DB_URL}/users/{u_id}.json", json={"pass": p_hash})
                    current_user = u
                elif str(data.get('pass')) == p_hash:
                    current_user = u
                else:
                    console.print(Align.center("[bold red]INVALID PASSWORD![/]"))
                    time.sleep(1)
            except:
                console.print(Align.center("[bold red]CONNECTION ERROR![/]"))
                time.sleep(1)

        while True:
            draw_header(current_user)
            table = Table(show_header=False, border_style="white", box=None)
            table.add_row("[bold yellow][1][/]", "[bold white]START MESSAGING[/]")
            table.add_row("[bold red][Q][/]", "[bold white]LOGOUT[/]")
            console.print(Align.center(table))

            c = Prompt.ask("\n" + " " * 15 + "[bold white]ACTION[/]").lower().strip()
            if not c: continue

            if c == "1":
                target = Prompt.ask(" " * 15 + "👤 [bold white]TARGET USER[/]").lower().strip()
                if target:
                    target_id = anonymize(target)
                    try:
                        check = requests.get(f"{DB_URL}/users/{target_id}.json", timeout=5)
                        if check.json() is None:
                            console.print(Align.center(f"[bold red]USER NOT FOUND: {target.upper()}[/]"))
                            time.sleep(1.5)
                            continue
                        
                        r_id = "CH_" + "_".join(sorted([anonymize(current_user), target_id]))
                        chat_screen(r_id, current_user, target)
                    except:
                        console.print(Align.center("[bold red]NETWORK ERROR![/]"))
                        time.sleep(1)
            elif c == 'q':
                break
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
