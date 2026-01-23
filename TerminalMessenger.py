import os, subprocess, sys, base64, hashlib, threading, time, json, re
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
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

console = Console(force_terminal=True)
SALT_VAL = b"Rhyme_99_X_Secret"

def get_db_conn():
    p1 = "aHR0cHM6Ly90ZXJtaW5hbC1tZXNzZW5nZXItZjFmZWQt"
    p2 = "ZGVmYXVsdC1ydGRiLmV1cm9wZS13ZXN0MS5maXJlYmFzZWRhdGFiYXNlLmFwcA=="
    return base64.b64decode(p1 + p2).decode()

DB_URL = get_db_conn()

def draw_header(user=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = r"""
[bold red]████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝[/]
"""
    console.print(Align.center(logo))
    if user:
        console.print(Align.center(Panel(f"[bold yellow]ID: {user.upper()}[/]", border_style="bold red")))
    console.print(Align.right("[bold dim]by rhyme[/]   "))
    console.print("\n")

def is_latin(text): return bool(re.match(r'^[a-zA-Z0-9_]+$', text))
def derive_key(passphrase):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT_VAL, iterations=100000)
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
def anonymize(text): return hashlib.sha256((text + "R_S").encode()).hexdigest()[:12]
def hash_p(p): return hashlib.sha256((p + "R_P").encode()).hexdigest()

def chat_screen(room_id, username, target, tk):
    cipher = Fernet(derive_key(tk))
    draw_header(username)
    console.print(Align.center(f"[bold red]>>> [bold white]TUNNELING WITH: {target.upper()}[/] <<<[/]"))
    console.print(Align.center("[bold dim](Type 'q' to exit chat)[/]\n"))
    shown_msgs = set()
    stop_event = threading.Event()

    def listen():
        while not stop_event.is_set():
            try:
                res = requests.get(f"{DB_URL}/messages/{room_id}.json", timeout=10)
                if res.status_code == 200 and res.json():
                    data = res.json()
                    for m_id in sorted(data.keys()):
                        if m_id not in shown_msgs:
                            m = data[m_id]
                            try:
                                u_dec = cipher.decrypt(m['u'].encode()).decode()
                                m_dec = cipher.decrypt(m['m'].encode()).decode()
                                color = "red" if u_dec != username else "green"
                                tag = u_dec.upper() if u_dec != username else "YOU"
                                console.print(f"[bold cyan][{m['t']}][/] [bold {color}]{tag}:[/] [bold white]{m_dec}[/]")
                                shown_msgs.add(m_id)
                            except: shown_msgs.add(m_id)
            except: pass
            time.sleep(1.5)

    threading.Thread(target=listen, daemon=True).start()
    
    while not stop_event.is_set():
        try:
            msg = input().strip()
            if not msg: continue
            if msg.lower() == 'q': stop_event.set(); break
            
            sys.stdout.write("\033[A\033[K")
            ts = datetime.now().strftime("%H:%M")
            payload = {"u": cipher.encrypt(username.encode()).decode(), "m": cipher.encrypt(msg.encode()).decode(), "t": ts}
            
            # GÖNDERME DENEMESİ
            post_res = requests.post(f"{DB_URL}/messages/{room_id}.json", json=payload, timeout=7)
            
            if post_res.status_code != 200:
                console.print("[bold red][ERROR: MESSAGE NOT SENT - SERVER REJECTED][/]")
        except (requests.exceptions.RequestException, Exception):
            console.print("[bold red][ERROR: CONNECTION LOST - RETRYING...][/]")

def main():
    try:
        while True:
            draw_header()
            v_panel = Panel("[bold white]Type “token” below[/]", border_style="bold yellow", expand=False)
            console.print(Align.center(v_panel))
            if Prompt.ask("\n[bold cyan]>>>[/]").strip().lower() != "token": continue

            current_user = None
            while not current_user:
                draw_header()
                u = Prompt.ask("[bold white]USERNAME[/]").lower().strip()
                if not is_latin(u): continue
                p = Prompt.ask("[bold white]PASSWORD[/]", password=True).strip()
                u_id = anonymize(u); p_hash = hash_p(p)
                
                try:
                    res = requests.get(f"{DB_URL}/users/{u_id}.json", timeout=10)
                    data = res.json()
                    if data is None:
                        console.print(Align.center("[bold green]NEW ENCRYPTED PROFILE CREATED![/]"))
                        requests.put(f"{DB_URL}/users/{u_id}.json", json={"pass": p_hash})
                        current_user = u; time.sleep(1)
                    elif data.get('pass') == p_hash:
                        current_user = u; draw_header(current_user); time.sleep(0.5)
                    else:
                        console.print(Align.center("[bold red]INVALID PASSWORD![/]")); time.sleep(1.5)
                except: console.print(Align.center("[bold red]CONNECTION ERROR![/]")); time.sleep(2)

            while current_user:
                draw_header(current_user)
                menu = Table(box=None, show_header=False)
                menu.add_row("[bold yellow]1.[/]", "[bold white]NEW TUNNEL[/]")
                menu.add_row("[bold red]Q.[/]", "[bold red]LOGOUT[/]")
                console.print(Align.center(Panel(menu, title="[bold white]MENU[/]", border_style="bold white", expand=False)))
                choice = Prompt.ask("\n[bold white]SELECT[/]").lower().strip()
                if choice == "1":
                    target = Prompt.ask("[bold white]TARGET USER[/]").lower().strip()
                    t_id = anonymize(target)
                    try:
                        t_res = requests.get(f"{DB_URL}/users/{t_id}.json", timeout=10)
                        if not t_res.json():
                            console.print(Align.center(f"[bold red]USER NOT FOUND: {target.upper()}[/]")); time.sleep(1.5); continue
                        tk = Prompt.ask("[bold white]TUNNEL KEY[/]", password=True).strip()
                        r_id = f"CH_{sorted([u_id, t_id])[0]}_{sorted([u_id, t_id])[1]}"
                        chat_screen(r_id, current_user, target, tk)
                    except: console.print(Align.center("[bold red]SERVER ERROR![/]")); time.sleep(1.5)
                elif choice == "q": break
    except KeyboardInterrupt: pass
    finally:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print("[bold red]TERMINAL CLOSED SECURELY. BYE![/]")

if __name__ == "__main__":
    main()
