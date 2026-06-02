  # 🛡️ TERMINAL MESSENGER

> **"Speed, Privacy, and the Mathematical Impossibility of Decryption."**

Terminal Messenger is an ultra-secure, OFF-THE-RECORD (OTR), and end-to-end encrypted (E2EE) CLI messaging platform. It is engineered for cyber-security enthusiasts, privacy advocates, and power users who demand military-grade operational security.

Unlike standard secure messengers, this tool is designed to run in a volatile environment (RAM), leaving minimal forensic footprints.

---

  ## 🚀 Key Features

**🛡️ AES-256-CFB (Advanced Cipher Block)**: Every message is sealed with AES-256 using a dynamic Initialization Vector (IV). This means even if you send the same word twice, the ciphertext will look completely different every time, making pattern analysis impossible.

**🧠 PBKDF2 with Custom Salt**: We utilize PBKDF2 (Password-Based Key Derivation Function 2) with a high iteration count and a hardcoded unique salt. This process transforms your Tunnel Key into a 256-bit cryptographic engine, making brute-force attacks against your messages mathematically infeasible.

**🕵️ 256-Bit Identity Masking**: Usernames are never stored in plaintext. They are hashed into SHA-256 strings. This ensures zero collision probability and makes database enumeration impossible without knowing the exact usernames.

**🛡️ Smart Dependency Guard**: To prevent supply-chain attacks and respect system boundaries, the script performs a deep scan of your environment and provides the exact safe installation commands for your specific OS.

**🤫 Silent Ghost Mode**: Decryption failures (due to wrong keys or old data) are handled silently. The system will never leak information about whether a packet was valid or not to an unauthorized observer.

 **🔔 Audible Bell & Stealth Mode:** Integrated terminal bell (\a) triggers a discrete hardware "Beep" when a new message arrives, allowing you to keep the terminal minimized while working.
 
 **💻 Cross-Platform:** Fully compatible with Windows, macOS, and Linux.

---

  ## 🛠️ Installation & Setup
**Prerequisites**
You need Python 3.8+. The system relies on the following cryptographic engines:

• **pycryptodome** `(AES-GCM engine)`

• **requests** `(Transport Layer)`

• **rich** `(UI rendering)`

### 🪟 Windows

1. Open `PowerShell` or `CMD` in the folder.
2. Install dependencies: `pip install -r requirements.txt --break-system-packages`
3. Run:
   ```powershell
   python TerminalMessenger.py

### 🍎 macOS

1. Open Terminal (`Cmd + Space` > `Terminal`).
2. Install dependencies: `pip install -r requirements.txt --break-system-packages`
3. Run:
    ```Bash
    python3 TerminalMessenger.py
    
### 🐧 Linux
For systems with "Externally Managed Environment" (PEP 668) errors:
1. Open Terminal.
2. Recommended Install (System Break Method): `pip install -r requirements.txt --break-system-packages`
3. Run:
    ```Bash
    python3 TerminalMessenger.py

---
    
  ### 🔔 Notification Sound Setup
If you don't hear a "beep" when a new message arrives:
 
  **Windows (Terminal):** Settings > Defaults > Advanced > Bell notification style -> Set to "Audible".
    
  **macOS (Terminal):** Terminal Settings > Profiles > Advanced > Check "Audible bell".
  
  **Linux:** Check Terminal Preferences > "Terminal Bell".
  
  **Note:** The notification sound only triggers when the terminal is in the background (preventing annoyance while you are actively typing).

---

  ### 🎨 User Interface (Custom UI)
**Entity	Color	Style**

**YOU**	🟢 Green	Bold	Indicates your own outgoing messages.

**PARTNER**	🔴 Red	Bold	Indicates incoming messages from your contact.

**TIMESTAMPS**	🔵  Cyan	Bold	Shows exactly when the message hit the tunnel.

**MESSAGES**	⚪ White	Bold	The decrypted, clear-text message content.

**STATUS**🟡 Encryption mode (Argon2id status).

---

  ### 📖 How to Use
  **⚠️ CRITICAL:** SERVER SETUP FIRST Before running the script, you must deploy your own backend (Firebase or a custom server).
  
  • Deploy your backend and get your Server URL.
  
  • Open `TerminalMessenger.py` and find the `SERVER_URL = "HERE UR URL"` line.
  
  • Paste your URL inside the quotes.
  
  • IMPORTANT: Both you and the person you are talking to MUST use the same `SERVER_URL`. If you are on different servers, you will never see each other's messages.
  
  **Authentication:** 
  
  • Enter Username & Password.
  
  • Note: Passwords are processed via SHA-256. A lost password is physically unrecoverable.
  
  **The Handshake:** 
  
  • Enter the target's username.
  
  • System generates a deterministic Room ID based on SHA-256 sorting of both parties.
  
  **Tunnel Opening:**
  
  • Enter the Tunnel Key (T-Key).
  
  • WARNING: This key is the seed for the AES-256 engine. It is NEVER sent to the server. Both parties must enter the exact same key to see each other's messages.
  
  **Messaging:** 
  
  • Type and hit Enter.
  
  • If the "Bell" rings, a packet has been successfully verified and decrypted.
  
  **Exit Strategy:** 
  
  • Type `q` and hit Enter to collapse the tunnel and return to the main menu safely. Press `Ctrl+C` for an emergency exit.

---

### 🤝 Contributing
Zero-Knowledge Rule: Any code contribution must verify that no key material ever touches the network stack.
   
   **Reporting Bugs:** If you find a security hole or a connection bug, please open an issue immediately.
   
   **Feature Requests:** Multi-language support is next on the roadmap.

### Security & Threat Model (Read Carefully):
What is Secure?

• Content:Messages are encrypted with AES-256. Even if the server is compromised, the attacker sees only random Base64 noise.

• Integrity: Dynamic IV prevents replay attacks and pattern recogniti

• Keys: Your Tunnel Key resides only in your RAM and is cleared upon exit.

• Zero-Knowledge: No keys, salts, or plaintext data ever touch the network stack.

---

  ### 📜 License
**MIT License** - Free to use, modify, and distribute.
**Copyright (c) 2026 Ramazanow Rahym**

### 👨‍💻 Developed by rhyme
