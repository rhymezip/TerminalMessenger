import os
import subprocess
import sys
import base64
import hashlib
import threading
import time
import json
import re
from datetime import datetime

def prepare_libs():
    libs = {
        "requests": "requests",
        "rich": "rich",
        "cryptography": "cryptography",
        "pyrebase4": "pyrebase4"
    }
    needed = []
    for lib_name, import_name in libs.items():
        try:
            __import__(import_name.replace("pyrebase4", "pyrebase"))
            print(f"{lib_name} is already installed")
        except ImportError:
            needed.append(lib_name)
    if needed:
        flags = ["--break-system-packages"] if os.name != 'nt' else []
        for n in needed:
            print(f"Installing {n}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", n, "--quiet"] + flags)
                print(f"{n} installed successfully")
            except Exception as e:
                print(f"Failed to install {n}: {str(e)}")
                sys.exit(1)

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
from pyrebase import pyrebase

console = Console(force_terminal=True)
SALT_VAL = b"Rhyme_99_X_Secret"

firebaseConfig = {
    "apiKey": "AIzaSyDR8VxCGtzRhyOeLxYXfKCIJFm8vwaT0us",
    "authDomain": "terminal-messenger-f1fed.firebaseapp.com",
    "databaseURL": "https://terminal-messenger-f1fed-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "terminal-messenger-f1fed",
    "storageBucket": "terminal-messenger-f1fed.firebasestorage.app",
    "messagingSenderId": "868555403769",
    "appId": "1:868555403769:web:b34fc3ade488e3b5008d28",
    "measurementId": "G-1PTV82S28P"
}

print("Initializing Firebase...")
try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
    print("Firebase initialized successfully")
except Exception as e:
    print(f"Firebase initialization failed: {str(e)}")
    sys.exit(1)

def draw_header(user=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = r"""
[bold red]████████╗███████╗██████╗ ███╗ ███╗██╗███╗ ██╗ █████╗ ██╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗ ██║██╔══██╗██║
   ██║ █████╗ ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
   ██║ ██╔══╝ ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
   ██║ ███████╗██║ ██║██║ ╚═╝ ██║██║██║ ╚████║██║ ██║███████╗
   ╚═╝ ╚══════╝╚═╝ ╚═╝╚═╝ ╚═╝╚═╝╚═╝ ╚═══╝╚═╝ ╚═╝╚══════╝[/]
"""
    console.print(Align.center(logo))
    console.print(Align.right("[bold dim]by rhyme[/] "))
    
    if user:
        console.print(Align.center(Panel(f"[bold yellow]ID: {user.upper()}[/]", border_style="bold red", expand=False)))
    console.print("\n")

def is_latin(text):
    return bool(re.match(r'^[a-zA-Z0-9_]+$', text))

def derive_key(passphrase):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT_VAL, iterations=100000)
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

def anonymize(text):
    return hashlib.sha256((text + "R_S").encode()).hexdigest()[:12]

def hash_p(p):
    return hashlib.sha256((p + "R_P").encode()).hexdigest()

def chat_screen(room_id, username, target, tk, token):
    cipher = Fernet(derive_key(tk))
    draw_header(username)
    console.print(Align.center(f"[bold red]>>> TUNNELING WITH: {target.upper()} <<<[/]"))
    console.print(Align.center("[bold dim](Type 'q' to exit chat)[/]\n"))
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
                            try:
                                u_dec = cipher.decrypt(m['u'].encode()).decode()
                                m_dec = cipher.decrypt(m['m'].encode()).decode()
                                
                                if u_dec != username:
                                    sys.stdout.write('\a')
                                    sys.stdout.flush()
                                
                                color = "red" if u_dec != username else "green"
                                tag = u_dec.upper() if u_dec != username else "YOU"
                                console.print(f"[bold cyan][{m['t']}][/] [bold {color}]{tag}:[/] [bold white]{m_dec}[/]")
                                shown_msgs.add(m_id)
                            except:
                                shown_msgs.add(m_id)
            except Exception as e:
                pass
            time.sleep(1.5)

    threading.Thread(target=listen, daemon=True).start()

    while not stop_event.is_set():
        try:
            msg = input().strip()
            if not msg:
                continue
            if msg.lower() == 'q':
                stop_event.set()
                break

            sys.stdout.write("\033[A\033[K")
            ts = datetime.now().strftime("%H:%M")
            payload = {
                "u": cipher.encrypt(username.encode()).decode(),
                "m": cipher.encrypt(msg.encode()).decode(),
                "t": ts
            }

            db.child("messages").child(room_id).push(payload, token)
        except Exception as e:
            console.print(f"[bold red][ERROR: {str(e)}][/]")

def main():
    try:
        print("Signing in anonymously...")
        user_auth = auth.sign_in_anonymous()
        token = user_auth['idToken']
        console.print("[green]Anonymous sign-in successful[/green]")

        while True:
            draw_header()
            v_panel = Panel("[bold white]Type “token” below[/]", border_style="bold yellow", expand=False)
            console.print(Align.center(v_panel))
            if Prompt.ask("\n[bold cyan]>>>[/]").strip().lower() != "token":
                continue

            current_user = None
            while not current_user:
                draw_header()
                u = Prompt.ask("[bold white]USERNAME[/]").lower().strip()
                if not is_latin(u):
                    continue
                p = Prompt.ask("[bold white]PASSWORD[/]", password=True).strip()
                u_id = anonymize(u)
                p_hash = hash_p(p)

                try:
                    data = db.child("users").child(u_id).get(token).val()
                    if data is None:
                        console.print(Align.center("[bold green]NEW ENCRYPTED PROFILE CREATED![/]"))
                        db.child("users").child(u_id).set({"pass": p_hash}, token)
                        current_user = u
                        time.sleep(1)
                    elif data.get('pass') == p_hash:
                        current_user = u
                        draw_header(current_user)
                        time.sleep(0.5)
                    else:
                        console.print(Align.center("[bold red]INVALID PASSWORD![/]"))
                        time.sleep(1.5)
                except Exception as e:
                    console.print(Align.center(f"[bold red]CONNECTION ERROR: {str(e)}[/]"))
                    time.sleep(2)

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
                        t_data = db.child("users").child(t_id).get(token).val()
                        if not t_data:
                            console.print(Align.center(f"[bold red]USER NOT FOUND: {target.upper()}[/]"))
                            time.sleep(1.5)
                            continue
                        tk = Prompt.ask("[bold white]TUNNEL KEY[/]", password=True).strip()
                        r_id = f"CH_{sorted([u_id, t_id])[0]}_{sorted([u_id, t_id])[1]}"
                        chat_screen(r_id, current_user, target, tk, token)
                    except Exception as e:
                        console.print(Align.center(f"[bold red]SERVER ERROR: {str(e)}[/]"))
                        time.sleep(1.5)
                elif choice == "q":
                    break
    except KeyboardInterrupt:
        pass
    finally:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print("[bold red]TERMINAL CLOSED SECURELY. BYE![/]")

if __name__ == "__main__":
    main()
