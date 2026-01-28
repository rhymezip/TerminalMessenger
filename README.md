  # 🛡️ TERMINAL MESSENGER (rhyme Edition)

> **"Speed, Privacy, and the Mathematical Impossibility of Decryption."**

Terminal Messenger is an ultra-secure, OFF-THE-RECORD (OTR), and end-to-end encrypted (E2EE) CLI messaging platform. It is engineered for cyber-security enthusiasts, privacy advocates, and power users who demand military-grade operational security.

Unlike standard secure messengers, this tool is designed to run in a volatile environment (RAM), leaving minimal forensic footprints.

---

  ## 🚀 Key Features

 **🛡️ AES-256-GCM (Galois/Counter Mode):** We have abandoned legacy standards. Every message is sealed with AES-256-GCM, providing not just confidentiality, but Cryptographic Integrity. Any attempt to tamper with the ciphertext (even a single bit flip by a database admin) will cause the decryption to fail instantly, alerting the user.
  
 **🧠 Argon2id (Memory-Hard KDF):** Your passwords and Tunnel Keys are NOT stored as simple hashes. We utilize Argon2id (the winner of the Password Hashing Competition), configured with high memory costs (64MB RAM per hash). This makes GPU-based brute-force attacks mathematically infeasible.
  
 **🕵️ 256-Bit Identity Masking:** Usernames are never stored in plaintext. They are hashed into 64-character (256-bit) SHA-256 strings. This ensures zero collision probability and makes database enumeration impossible without knowing the exact usernames.
  
 **🛡️ Smart Dependency Guard:** To prevent supply-chain attacks and respect system boundaries (especially on Arch/Debian), the script does NOT auto-install packages blindly. Instead, it performs a deep scan and provides the exact safe installation commands for your specific OS (including PEP 668 overrides).
  
 **🔔 Audible Bell & Stealth Mode:** Integrated terminal bell (\a) triggers a discrete hardware "Beep" when a new message arrives, allowing you to keep the terminal minimized while working.
  
 **💻 Cross-Platform:** Fully compatible with Windows, macOS, and Linux.

---

  ## 🛠️ Installation & Setup

**Prerequisites**
You need Python 3.8+. The system relies on the following cryptographic engines:

• pycryptodome (AES-GCM engine)

• argon2-cffi (KDF engine)

• pyrebase4 (Transport layer)

• rich (UI rendering)

### 🪟 Windows

1. Open `PowerShell` or `CMD` in the folder.
2. Install dependencies:
   `pip install pycryptodome argon2-cffi pyrebase4 rich --break-system-packages`
3. Run:
   ```powershell
   python TerminalMessenger.py

### 🍎 macOS

1. Open Terminal (`Cmd + Space` > `Terminal`).
2. Install dependencies:
   `pip3 install pycryptodome argon2-cffi pyrebase4 rich --break-system-packages`
3. *Run:
    ```Bash
    python3 TerminalMessenger.py
    
### 🐧 Linux
For systems with "Externally Managed Environment" (PEP 668) errors:
1. Open Terminal.
2. Recommended Install (System Break Method):
   `pip install -r requirements.txt --break-system-packages`
3.Run:
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
  
  **Authentication:** 
  • Enter Username & Password.
  • Note: Passwords are processed via Argon2id. A lost password is physically unrecoverable.
  
  **The Handshake:** 
  • Enter the target's username.
  • System generates a deterministic Room ID based on SHA-256 sorting.
  
  **Tunnel Opening:**
  • Enter the Tunnel Key (T-Key).
  • WARNING: This key is the seed for the AES-256-GCM engine. It is NEVER sent to the server. Both parties must enter the exact same key.
  
  **Messaging:** 
  • Type and hit Enter.
  • If the "Bell" rings, a packet has been successfully verified and decrypted.
  
  **Exit Strategy:** 
  • Type q and hit Enter to collapse the tunnel and return to the main menu safely.

---

### 🤝 Contributing

Zero-Knowledge Rule: Any code contribution must verify that no key material ever touches the network stack.

   **Reporting Bugs:** If you find a security hole or a connection bug, please open an issue immediately.
   **Feature Requests:** Multi-language support is next on the roadmap.

### Security & Threat Model (Read Carefully):
What is Secure?

• Content: Messages are encrypted with AES-256-GCM. Even if the Firebase database is dumped, the attacker sees only random bytes.
• Integrity: GCM tags prevent message tampering.
• Keys: Your Tunnel Key resides only in your RAM and is cleared upon exit.

---

  ### 📜 License

**MIT License** - Free to use, modify, and distribute.
**Copyright (c) 2026 Ramazanow Rahym**

### 👨‍💻 Developed by rhyme
