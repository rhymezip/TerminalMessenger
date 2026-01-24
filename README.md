  # 🛡️ TERMINAL MESSENGER (rhyme Edition)

> **"Speed, Privacy, and the Power of Terminal."**

Terminal Messenger is a minimalist, ultra-secure, and end-to-end encrypted (E2EE) messaging platform. Built for power users who value privacy, it ensures that your conversations remain invisible to everyone—including database administrators.

---

  ## 🚀 Key Features

 **🛡️ AES-256 Encryption:** Industry-standard Fernet (AES-256) encryption applied locally on your machine.
  
 **🕵️ Identity Masking:** Usernames are transformed into 12-character hex strings using SHA-256 salting, making metadata analysis impossible.
  
 **💾 Cloud Persistence:** Messages are stored in a secure Firebase Realtime Database. They stay there until you decide to change the tunnel.
  
 **🔔 Audible Bell (Notification):** Integrated terminal bell (\a) triggers a "Beep" sound when a new message arrives from your partner.
  
 **🎨 Terminal Aesthetics:** A beautiful, color-coded interface designed with the rich library for maximum readability.
  
 **💻 Cross-Platform:** Fully compatible with Windows, macOS, and Linux.
  
 **⚡ Auto-Dependency Engine:** The script is designed for a seamless "plug-and-play" experience. Upon launch, it automatically detects any missing libraries (such as rich, cryptography, or pyrebase4) and installs them for you. No manual configuration is required.
  
 **🔒 Zero-Knowledge Policy:** No readable logs or data are ever stored on the server side.

---

  ## 🛠️ Setup Instructions by OS

### 🪟 Windows

1. **Download:** Save `TerminalMessenger.py` to a folder.
2. **Open Terminal:** Type `cmd` or `powershell` in the folder's address bar and hit Enter.
3. **Run:** Execute the following command:
   ```powershell
   python TerminalMessenger.py

### 🍎 macOS

1. **Download:** Save TerminalMessenger.py to your device.
2. **Open Terminal:** Press Cmd + Space, type Terminal, and hit Enter.
3. **Navigate:** Go to the file's folder (e.g., cd Downloads).
4. **Run:** Execute the following command:
    Bash
    python3 TerminalMessenger.py
    
### 🐧 Linux

1. **Download:** Save the script to your desired directory.
2. **Open Terminal:** Right-click in the folder and select "Open in Terminal".
3. **Run:** Execute the following command:
    ```Bash

    python3 TerminalMessenger.py

---
    
  ### 🔔 Notification Sound Setup

 If you don't hear a "beep" when a new message arrives, please check your terminal settings:
    **Windows (Terminal):** Settings > Defaults > Advanced > Bell notification style -> Set to "Audible" or "All".
    **macOS (Terminal):** Settings > Profiles > Advanced > Check "Audible bell".
    **Linux:** Open your terminal's Preferences and enable "Terminal Bell". Also, ensure "System Sounds" is unmuted in your OS settings.
    **Note:** The notification sound only triggers when the terminal is in the background (preventing annoyance while you are actively typing).

---
    
  ### 🛠️ What Happens When You Run It?

 When you launch the script:
    **Auto-Dependency Check:** Scans your system for requests, rich, and cryptography libraries.
    **Silent Installation:** If any are missing, it installs them automatically within seconds—no manual setup required.
    **Cryptographic Handshake:** Initializes the AES-256 Fernet engine and establishes a secure, masked connection to the Firebase Realtime Database.
    **UI Rendering:** The custom ASCII logo and the secure login portal are rendered instantly.

---

  ### 🎨 User Interface (Custom UI)
**Entity	Color	Style**
**YOU**	🟢 Green	Bold	Indicates your own outgoing messages.

**PARTNER**	🔴 Red	Bold	Indicates incoming messages from your contact.

**TIMESTAMPS**	🔵 🔵 Cyan	Bold	Shows exactly when the message hit the tunnel.

**MESSAGES**	⚪ White	Bold	The decrypted, clear-text message content.

**TUNNEL INFO**🟡 Yellow	Bold	Displays current encryption status and room ID.

---

  ### 📖 How to Use
  
  **Authentication:** Enter your username and password. Note: Your password is hashed (SHA-256) and cannot be recovered if lost.
  
  **The Handshake:** Type the username of the person you wish to connect with. Both users must be registered on the database.
  
  **Tunnel Opening:** Enter your secret "Tunnel Key". This key is the master cipher for your messages and is NEVER stored online.
  
  **Messaging:** Type your message and hit Enter. You will hear a "Bell" notification when your partner replies.
  
  **Exit Strategy:** Type q and hit Enter to collapse the tunnel and return to the main menu safely.

---

  ### 🗺️ Roadmap & Future Developments

We are constantly working to make Terminal Messenger the most secure CLI chat tool. Here is our path forward:

   **🌍 Multi-Language Support:** We aim to implement a localization system. Contributors are welcome to add Turkish, German, Spanish, and more.

   **🕵️ Metadata & Username Anonymity:** Currently, usernames are masked with SHA-256. While the message content is 100% secure, we are working on a more advanced relay system to further decouple identities from room IDs.

   **📁 Encrypted File Transfer:** Implementation of a system to send small files (base64 encoded) through the same AES-256 encrypted tunnel.

   **🔑 Multi-Factor Authentication (MFA):** Adding a second layer of security via mobile or email codes for the login process.

---

  ### 🤝 Contributing

Terminal Messenger is an open-source project and we love contributions!

   **Reporting Bugs:** If you find a security hole or a connection bug, please open an issue immediately.

   **Feature Requests:** Have a cool idea? Let us know!

   **Code Quality:** We strictly follow the "Zero-Knowledge" policy. Any contribution must ensure that the Tunnel Key never touches the server side.

"The only way to keep a secret is to make sure no one else knows you have one."

### ⚠️ Important (Tunnel Key Sync):

For messages to be decrypted successfully, both users in the tunnel must enter the exact same "Tunnel Key". If the keys do not match, the messages will appear as encrypted (unreadable) junk text. Always share your T-Key through a secure channel before starting a session.

### ⚠️ Security Disclaimer

The system is designed with a "Privacy-First" mindset. The only theoretical weak point is the mapping of usernames via SHA-256 hashes. Apart from this, there are no backdoors. Your messages are protected by military-grade AES-256 encryption, and only those with the Tunnel Key can read them.

---

  ### 📜 License

This project is licensed under the MIT License.
Plaintext

Copyright (c) 2026 Ramazanow Rahym

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

  ### 👨‍💻 Developed by rhyme

"In Code We Trust, In Encryption We Hide."
