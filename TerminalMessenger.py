import os, subprocess, sys, hashlib, threading, time, base64
from datetime import datetime

def prepare_libs():
    libs = {"requests": "requests", "rich": "rich", "cryptography": "cryptography", "pyrebase4": "pyrebase4"}
    for lib, imp in libs.items():
        try: __import__(imp.replace("pyrebase4", "pyrebase"))
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--quiet"])

prepare_libs()

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.panel import Panel
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pyrebase import pyrebase

console = Console(force_terminal=True)
SALT_VAL = b"Rhyme_99_X_Secret"

k1 = "AIzaSyDR8"
k2 = "VxCGtzRhy"
k3 = "OeLxYXfKCI"
k4 = "JFm8vwaT0us"

firebaseConfig = {
    "apiKey": k1 + k2 + k3 + k4,
    "authDomain": "terminal-messenger-f1fed.firebaseapp.com",
    "databaseURL": "https://terminal-messenger-f1fed-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "terminal-messenger-f1fed",
    "storageBucket": "terminal-messenger-f1fed.firebasestorage.app",
    "messagingSenderId": "868555403769",
    "appId": "1:868555403769:web:b34fc3ade488e3b5008d28",
    "measurementId": "G-1PTV82S28P"
}

try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
except:
    sys.exit(1)

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
    console.print(Align.right("[bold dim]by rhyme[/] "))
    if user:
        console.print(Align.center(Panel(f"[bold yellow]ID: {user.upper()}[/]", border_style="bold red", expand=False)))
    console.print("\n")

def chat_screen(room_id, username, target, tk, token):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT_VAL, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(tk.encode()))
    cipher = Fernet(key)
    
    draw_header(username)
    console.print(Align.center(f"[bold red]>>> TUNNELING WITH: {target.upper()} <<<[/]\n"))
    shown_msgs = set()
    stop_event = threading.Event()

    def listen():
        while not stop_event.is_set():
            try:
                data = db.child("messages").child(room_id).get(token).val()
                if data:
                    for m_id in sorted(data.keys()):
                        if m_id not in shown_msgs:
                            m = data[m_id]
                            u_dec = cipher.decrypt(m['u'].encode()).decode()
                            m_dec = cipher.decrypt(m['m'].encode()).decode()
                            if u_dec != username: sys.stdout.write('\a'); sys.stdout.flush()
                            color = "red" if u_dec != username else "green"
                            console.print(f"[bold cyan][{m['t']}][/] [bold {color}]{u_dec.upper() if u_dec != username else 'YOU'}:[/] [bold white]{m_dec}[/]")
                            shown_msgs.add(m_id)
            except: pass
            time.sleep(1.5)

    threading.Thread(target=listen, daemon=True).start()
    while not stop_event.is_set():
        try:
            msg = input().strip()
            if not msg: continue
            if msg.lower() == 'q': stop_event.set(); break
            sys.stdout.write("\033[A\033[K")
            db.child("messages").child(room_id).push({
                "u": cipher.encrypt(username.encode()).decode(),
                "m": cipher.encrypt(msg.encode()).decode(),
                "t": datetime.now().strftime("%H:%M")
            }, token)
        except: break

def main():
    try:
        user_auth = auth.sign_in_anonymous()
        token = user_auth['idToken']
        while True:
            draw_header()
            console.print(Align.center(Panel("[bold white]Type “token” to connect[/]", border_style="bold yellow", expand=False)))
            if Prompt.ask("\n[bold cyan]>>>[/]").strip().lower() != "token": continue
            
            curr_u = None
            while not curr_u:
                draw_header()
                u = Prompt.ask("[bold white]USERNAME[/]").lower().strip()
                p = Prompt.ask("[bold white]PASSWORD[/]", password=True).strip()
                u_id = hashlib.sha256((u + "R_S").encode()).hexdigest()[:12]
                p_hash = hashlib.sha256((p + "R_P").encode()).hexdigest()
                
                res = db.child("users").child(u_id).get(token).val()
                if not res:
                    db.child("users").child(u_id).set({"pass": p_hash}, token)
                    curr_u = u
                elif res.get('pass') == p_hash: curr_u = u
                else: 
                    console.print(Align.center("[bold red]WRONG PASS[/]"))
                    time.sleep(1)

            while curr_u:
                draw_header(curr_u)
                menu = Table(box=None, show_header=False)
                menu.add_row("[bold yellow]1.[/]", "[bold white]OPEN TUNNEL[/]")
                menu.add_row("[bold red]Q.[/]", "[bold red]LOGOUT[/]")
                console.print(Align.center(Panel(menu, title="[bold white]MENU[/]", border_style="bold white", expand=False)))
                choice = Prompt.ask("\n[bold white]SELECT[/]").lower().strip()
                
                if choice == "1":
                    target = Prompt.ask("[bold white]TARGET USERNAME[/]").lower().strip()
                    tk = Prompt.ask("[bold white]TUNNEL KEY (T-KEY)[/]", password=True).strip()
                    t_id = hashlib.sha256((target + "R_S").encode()).hexdigest()[:12]
                    r_id = f"CH_{sorted([u_id, t_id])[0]}_{sorted([u_id, t_id])[1]}"
                    chat_screen(r_id, curr_u, target, tk, token)
                elif choice == "q": break
    except Exception as e:
        console.print(f"[bold red]HATA: {e}[/]")

if __name__ == "__main__":
    main()
    except KeyboardInterrupt:
        console.print("\n[bold red]>>> EXITING...[/]")
        sys.exit(0)
