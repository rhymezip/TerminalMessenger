import os, sys, hashlib, threading, time, base64, requests
from datetime import datetime

_v1 = "Vis"; _v2 = "ibi"; _v3 = "lit"; _v4 = "y_o"; _v5 = "ff"
_logic_a = [_v1, _v2]; _logic_b = [_v3 + "y"]

def _get_core_tail():
    return f"_{'o'}{'f'}{'f'}"

def check_deps():
    missing = []
    try: import Crypto
    except: missing.append("pycryptodome")
    try: import rich
    except: missing.append("rich")
    try: import requests
    except: missing.append("requests")
    if missing:
        print(f"[!] MISSING: {', '.join(missing)} | RUN: pip install {' '.join(missing)}")
        sys.exit(1)

check_deps()

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.panel import Panel

console = Console(force_terminal=True)
SERVER_URL = "https://rhymezip-terminal-backend.hf.space"

class ApocalypseCrypto:
    def __init__(self, tk):
        self.salt = b"GHOST_ULTRA_SALT_2026_PROTECT_YOUR_MIND"
        self.key = hashlib.pbkdf2_hmac('sha256', tk.encode(), self.salt, 100000)

    def encrypt(self, plain_text):
        from Crypto.Cipher import AES
        cipher = AES.new(self.key, AES.MODE_CFB)
        return base64.b64encode(cipher.iv + cipher.encrypt(plain_text.encode('utf-8'))).decode('utf-8')

    def decrypt(self, encrypted_data):
        try:
            from Crypto.Cipher import AES
            raw = base64.b64decode(encrypted_data)
            cipher = AES.new(self.key, AES.MODE_CFB, iv=raw[:16])
            return cipher.decrypt(raw[16:]).decode('utf-8')
        except: 
            return None

def draw_header(user=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = r"""
 [bold red] _______ ______ _____  __  __ _____ _   _          _ 
 |__   __|  ____|  __ \|  \/  |_   _| \ | |   /\   | |
    | |  | |__  | |__) | \  / | | | |  \| |  /  \  | |
    | |  |  __| |  _  /| |\/| | | | | . ` | / /\ \ | |
    | |  | |____| | \ \| |  | |_| |_| |\  |/ ____ \| |____
    |_|  |______|_|  \_\_|  |_|_____|_| \_/_/    \_\______|[/]
                                        [bold white]by rhymezip[/]
"""
    console.print(Align.center(logo))
    if user:
        console.print(Align.center(Panel(f"[bold yellow]USER: {user.upper()}[/]", border_style="bold red", expand=False)))

def listen(room_id, crypto, username, api_key):
    shown_msgs = set()
    while True:
        try:
            res = requests.get(f"{SERVER_URL}/messages?room={room_id}", headers={"X-Api-Key": api_key}, timeout=5)
            if res.status_code == 200:
                data = res.json()
                for m_id in sorted(data.keys(), key=int):
                    m = data[m_id]
                    sig = hashlib.md5(m['m'].encode()).hexdigest()
                    if sig not in shown_msgs:
                        if m['u'].lower() != username.lower():
                            m_dec = crypto.decrypt(m['m'])
                            if m_dec:
                                sys.stdout.write("\r" + " " * 35 + "\r") 
                                console.print(f"[bold cyan][{m['t']}][/] [bold red]{m['u'].upper()}:[/] [bold white]{m_dec}[/]")
                                sys.stdout.write(" >>> ")
                                sys.stdout.flush()
                        shown_msgs.add(sig)
        except: pass
        time.sleep(1.2)

def main():
    try:
        draw_header()
        FINAL_API = f"{''.join(_logic_a)}{_logic_b[0]}{_get_core_tail()}"
        
        if Prompt.ask("\n[bold cyan]Type 'token'[/]").strip().lower() != "token": return

        curr_u = None
        while not curr_u:
            draw_header()
            u = Prompt.ask( "[bold white] USER").lower().strip()
            p = Prompt.ask("[bold white] password", password=True).strip()
            res = requests.post(f"{SERVER_URL}/login", json={"u": u, "p": hashlib.sha256(p.encode()).hexdigest()}, headers={"X-Api-Key": FINAL_API})
            if res.status_code == 200: curr_u = u
            else: console.print("[red]FAIL[/]"); time.sleep(1)

        while curr_u:
            draw_header(curr_u)
            menu = Table(box=None, show_header=False)
            menu.add_row("[bold yellow]1.[/]", "OPEN CHAT"), menu.add_row("[bold red]Q.[/]", "LOGOUT")
            console.print(Align.center(Panel(menu, border_style="white", expand=False)))
            
            choice = Prompt.ask("[bold white] SELECT").lower().strip()
            if choice == "1":
                target = Prompt.ask("[bold white] TARGET").lower().strip()
                tk = Prompt.ask("[bold white] TUNNEL KEY", password=True).strip()
                crypto = ApocalypseCrypto(tk)
                room_id = hashlib.sha256("".join(sorted([curr_u, target])).encode()).hexdigest()
                
                draw_header(curr_u)
                console.print(f"[bold red]>>> TUNNEL ACTIVE: {target.upper()} <<<[/]\n")
                threading.Thread(target=listen, args=(room_id, crypto, curr_u, FINAL_API), daemon=True).start()
                
                while True:
                    msg = input(" >>> ").strip()
                    if not msg: continue
                    if msg.lower() == 'q': break
                    sys.stdout.write("\033[A\033[K")
                    t_now = datetime.now().strftime("%H:%M")
                    console.print(f"[bold cyan][{t_now}][/] [bold green]YOU:[/] [bold white]{msg}[/]")
                    requests.post(f"{SERVER_URL}/send", json={"room": room_id, "u": curr_u, "m": crypto.encrypt(msg), "t": t_now}, headers={"X-Api-Key": FINAL_API})
            else: break
    except KeyboardInterrupt: sys.exit(0)

if __name__ == "__main__":
    main()
