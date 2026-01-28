import os, sys, hashlib, threading, time, base64
from datetime import datetime

def check_deps():
    missing = []
    try: import Crypto
    except: missing.append("pycryptodome")
    try: import argon2
    except: missing.append("argon2-cffi")
    try: import pyrebase
    except: missing.append("pyrebase4")
    try: import rich
    except: missing.append("rich")
    
    if missing:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[!] ERROR: MISSING PACKAGES")
        print("-" * 50)
        print(f"Required: {', '.join(missing)}")
        print("\n[FIX]:")
        print("pip install --break-system-packages " + " ".join(missing))
        print("-" * 50)
        sys.exit(1)

check_deps()

from argon2.low_level import hash_secret_raw, Type
from pyrebase import pyrebase
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.panel import Panel

console = Console(force_terminal=True)

k1, k2, k3, k4 = "AIzaSyDR8", "VxCGtzRhy", "OeLxYXfKCI", "JFm8vwaT0us"
firebaseConfig = {
    "apiKey": k1 + k2 + k3 + k4,
    "authDomain": "terminal-messenger-f1fed.firebaseapp.com",
    "databaseURL": "https://terminal-messenger-f1fed-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "terminal-messenger-f1fed",
    "storageBucket": "terminal-messenger-f1fed.firebasestorage.app",
    "messagingSenderId": "868555403769",
    "appId": "1:868555403769:web:b34fc3ade488e3b5008d28"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

class ApocalypseCrypto:
    def __init__(self, tunnel_key):
        self.salt = b"GHOST_ULTRA_SALT_2026_PROTECT_YOUR_MIND"
        self.key = hash_secret_raw(
            secret=tunnel_key.encode(),
            salt=self.salt,
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            type=Type.ID
        )

    def encrypt(self, plain_text):
        from Crypto.Cipher import AES
        from Crypto.Random import get_random_bytes
        nonce = get_random_bytes(12)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
        return base64.b64encode(nonce + tag + ciphertext).decode('utf-8')

    def decrypt(self, encrypted_data):
        try:
            from Crypto.Cipher import AES
            raw = base64.b64decode(encrypted_data)
            nonce, tag, ciphertext = raw[:12], raw[12:28], raw[28:]
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
        except:
            return "[SECURITY_ALERT: UNABLE_TO_DECRYPT]"



def draw_header(user=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = r"""
[bold red]  _______ ______ _____  __  __ _____ _   _          _
 |__   __|  ____|  __ \|  \/  |_   _| \ | |   /\   | |
    | |  | |__  | |__) | \  / | | | |  \| |  /  \  | |
    | |  |  __| |  _  /| |\/| | | | | . ` | / /\ \ | |
    | |  | |____| | \ \| |  | |_| |_| |\  |/ ____ \| |____
    |_|  |______|_|  \_\_|  |_|_____|_| \_/_/    \_\______|[/]
"""
    console.print(Align.center(logo))
    if user:
        console.print(Align.center(Panel(f"[bold yellow]USER: {user.upper()}[/]", border_style="bold red", expand=False)))

def chat_screen(room_id, username, target, tk, token):
    crypto = ApocalypseCrypto(tk)
    draw_header(username)
    console.print(f"[bold red]>>> TUNNEL ACTIVE: {target.upper()} (ARGON2id) <<<[/]\n")
    shown_msgs = set()
    
    def listen():
        while True:
            try:
                data = db.child("messages").child(room_id).get(token).val()
                if data:
                    new_msg_found = False
                    for m_id in sorted(data.keys()):
                        if m_id not in shown_msgs:
                            m = data[m_id]
                            u_dec = crypto.decrypt(m['u'])
                            m_dec = crypto.decrypt(m['m'])
                            color = "red" if u_dec != username else "green"
                            u_disp = u_dec.upper() if u_dec != username else "YOU"
                            console.print(f"[bold cyan][{m['t']}][/] [bold {color}]{u_disp}:[/] [bold white]{m_dec}[/]")
                            shown_msgs.add(m_id)
                            new_msg_found = True
                    
                    if new_msg_found:
                        sys.stdout.write('\a')
                        sys.stdout.flush()
            except: pass
            time.sleep(1.2)

    threading.Thread(target=listen, daemon=True).start()
    
    while True:
        try:
            msg = input().strip()
            if not msg: continue
            if msg.lower() == 'q': break
            sys.stdout.write("\033[A\033[K")
            db.child("messages").child(room_id).push({
                "u": crypto.encrypt(username),
                "m": crypto.encrypt(msg),
                "t": datetime.now().strftime("%H:%M")
            }, token)
        except: break

def main():
    try:
        user_auth = auth.sign_in_anonymous()
        token = user_auth['idToken']
        while True:
            draw_header()
            console.print(Align.center(Panel("[bold white]Type 'token' to connect[/]", border_style="bold yellow", expand=False)))
            try:
                if Prompt.ask("\n[bold cyan]>>>[/]").strip().lower() != "token": continue
            except: break

            curr_u = None
            u_id = ""
            while not curr_u:
                draw_header()
                u = Prompt.ask("[bold white]USERNAME[/]").lower().strip()
                p = Prompt.ask("[bold white]PASSWORD[/]", password=True).strip()
                u_id = hashlib.sha256(u.encode()).hexdigest()
                p_hash = hashlib.sha256((p + "G_SALT_99").encode()).hexdigest()

                res = db.child("users").child(u_id).get(token).val()
                if not res:
                    db.child("users").child(u_id).set({"pass": p_hash}, token)
                    curr_u = u
                elif res.get('pass') == p_hash: curr_u = u
                else:
                    console.print(Align.center("[bold red]INVALID PASSWORD[/]")); time.sleep(1)

            while curr_u:
                draw_header(curr_u)
                menu = Table(box=None, show_header=False)
                menu.add_row("[bold yellow]1.[/]", "[bold white]OPEN TUNNEL[/]")
                menu.add_row("[bold red]Q.[/]", "[bold red]LOGOUT[/]")
                console.print(Align.center(Panel(menu, title="[bold white]MENU[/]", border_style="bold white", expand=False)))
                
                choice = Prompt.ask("\n[bold white]SELECT[/]").lower().strip()
                if choice == "1":
                    target = Prompt.ask("[bold white]TARGET USERNAME[/]").lower().strip()
                    tk = Prompt.ask("[bold white]TUNNEL KEY[/]", password=True).strip()
                    t_id = hashlib.sha256(target.encode()).hexdigest()
                    participants = sorted([u_id, t_id])
                    r_id = hashlib.sha256(f"{participants[0]}_{participants[1]}".encode()).hexdigest()
                    chat_screen(r_id, curr_u, target, tk, token)
                elif choice == "q": break
    except: pass
    finally:
        console.print("\n[bold red]>>> DISCONNECTED.[/]\n")

if __name__ == "__main__":
    main()
