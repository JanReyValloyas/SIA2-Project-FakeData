# SIA2 - Utilities Dashboard (Option 3B)

A comprehensive Python-based desktop utility dashboard application developed using **CustomTkinter**, **SQLite**, and **Faker**. This project is built as part of the Systems Integration and Architecture 2 (SIA2) laboratory requirements.

---

## 🚀 Features & Modules

### 1. 🔐 User Authentication
* Secure user registration and login system.
* Implements **salted PBKDF2/SHA-256** password hashing (`auth.py`) for enhanced credential security.
* Modern card-based UI design with show/hide password toggles.

### 2. 📊 3B.3 Fake Data Generation
* Generates randomized, realistic mock user profiles containing 12 unique data fields (Name, Address, Birthdate, Mobile Number, Email, Username, Job Title, Company, City, Country, Blood Type, and Website).
* Interactive search filtering across names, jobs, cities, and companies.
* Data management utilities: Delete selected rows, clear all records, and copy individual records directly to the clipboard.
* Data export support for both **CSV** and **JSON** file formats.

### 3. 🔗 3B.1 URL Shortener
* Shortens long URLs into clean, manageable custom links.
* **Custom Alias Support:** Option to define a personalized short code or generate a random secure string.
* Click/Testing analytics tracker to monitor how many times a shortened URL has been tested.
* Built-in browser redirection tool (`webbrowser`) for live link testing and a copy-to-clipboard utility.

### 4. 💬 3B.2 Messaging Utility (SMS & Email)
* **SMS Module:** Send, simulate receiving, and reply to mobile text messages.
* **Email Module:** Send and simulate receiving email messages with dedicated logs stored safely in the database.
* Tabbed sub-interfaces maintaining real-time action logs via structured SQLite tables.

---

## 🛠️ Tech Stack & Requirements

* **Language:** Python 3.x
* **GUI Framework:** `customtkinter`
* **Database:** SQLite3 (`app_data.db`)
* **Libraries:** `faker`, `hashlib`, `os`, `json`, `csv`, `tkinter`

---

## 📦 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
   cd YOUR_REPOSITORY_NAME
