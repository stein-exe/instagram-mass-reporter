# Instagram Mass Reporter

> Automate reporting of false, unwanted, and abusive content on Instagram.

A paid tool for users who need to triage abusive or fraudulent content at scale. Runs locally on your machine, exposes a web UI for configuration, and handles the report-submission loop so you don't have to.

- **Repo:** https://github.com/stein-exe/instagram-mass-reporter
- **Support / contact:** [@rejerk](https://t.me/rejerk) on Telegram
- **Community chat:** [@keped](https://t.me/keped) on Telegram

---

## Stats

<p>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=stein-exe.instagram-mass-reporter&left_text=Visitors" alt="Visitors" />
  <img src="https://img.shields.io/github/stars/stein-exe/instagram-mass-reporter?style=for-the-badge&logo=github&logoColor=white" alt="Stars" />
  <img src="https://img.shields.io/github/forks/stein-exe/instagram-mass-reporter?style=for-the-badge&logo=github&logoColor=white" alt="Forks" />
  <img src="https://img.shields.io/github/subscribers/stein-exe/instagram-mass-reporter?style=for-the-badge&logo=github&logoColor=white" alt="Watchers" />
  <img src="https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Telegram-@rejerk-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" />
</p>
<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/flask-%23000.svg?style=flat-square&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/fastapi-005571?style=flat-square&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/requests-3670A0?style=flat-square&logo=python&logoColor=white" alt="Requests" />
  <img src="https://img.shields.io/badge/rich-FFC107?style=flat-square" alt="Rich" />
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=flat-square&logo=telegram&logoColor=white" alt="Telegram" />
  <img src="https://img.shields.io/badge/Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white" alt="Instagram" />
</p>

---

<p align="center">
  <img src="https://i.pinimg.com/736x/d9/12/4e/d9124e0ba3e7179a1833da49dec5546e.jpg" alt="cover" />
</p>

---

## What it does

- Automates submission of Instagram reports against a target account, with a configurable reason and loop count.
- Web UI with a built-in help tab that documents every option, every report reason, and every config knob — open it once and you don't need the README for usage.
- Two backends, picked automatically based on the host:
  - **Flask** for Android environments (Termux, Pydroid)
  - **FastAPI** for desktop environments (Windows, Linux)
- Self-installs its pip dependencies on first run. You don't install Flask, FastAPI, or anything else by hand.

---

## Supported platforms

| Platform | Backend | Notes |
| --- | --- | --- |
| Termux (Android) | Flask | Auto-detected via `PREFIX` containing `com.termux` |
| Pydroid (Android) | Flask | Auto-detected via `PYDROID_PYTHON` or `HOME` containing `pydroid` |
| Windows | FastAPI | |
| Linux (desktop) | FastAPI | |

The loader inspects your environment on startup and downloads the matching backend from the `flask/` or `fastapi/` directory in this repo. No flag to choose — just run it.

---

## Requirements

- **Python 3.11, 3.12, or 3.13.** Other versions are not currently published in the repo and will fail to download.
- **Instagram accounts** — at least one, with valid session credentials (session ID, or username + password). You provide these in the web UI; nothing is hardcoded.
- **Proxies** — optional but strongly recommended for any non-trivial volume.
- **An active subscription.** Contact [@rejerk](https://t.me/rejerk) to get one. You will not be able to run reports without a valid key.
- `git`, `pip`, and outbound HTTPS to `raw.githubusercontent.com` (the loader downloads its payload on first run).

That's it. No Node, no Docker, no system packages.

---

## Installation

```bash
git clone https://github.com/stein-exe/instagram-mass-reporter.git
cd instagram-mass-reporter
python main.py
```

That's the whole install. On first run:

1. The loader checks your environment (Termux / Pydroid / desktop).
2. It installs missing pip packages automatically (`flask` or `fastapi` + `uvicorn` + shared deps, depending on platform).
3. It downloads the matching backend script from this repo and caches it in `files/`.
4. It opens the web UI in your default browser.

Subsequent runs reuse the cached backend for 12 hours before re-checking upstream.

If you want to force a fresh download (e.g. after an upstream update), delete the contents of `files/` and re-run.

---

## Usage

```bash
python main.py
```

Then:

1. The web UI opens automatically. If it doesn't, check the terminal for the local URL (usually `http://127.0.0.1:5000` or similar) and open it manually.
2. Open the **Help** tab in the UI for full documentation on every option — report reasons, target input, loop counts, proxy settings, account pool, etc. The Help tab is the source of truth; this README is the overview.
3. Configure your targets, accounts, and proxies.
4. Start the report loop. Output streams into the web UI and the terminal.

To stop, close the browser tab and press `Ctrl+C` in the terminal.

---

## Configuration

Everything is configured through the web UI — there is no config file to edit by hand. The Help tab in the UI documents every option. The short version:

- **Targets** — single username, or a list from a text file (one username per line).
- **Report reason** — picked from Instagram's official report categories.
- **Loop count** — how many reports to submit per target.
- **Delay** — seconds between reports. Respect this or you'll get rate-limited.
- **Account pool** — the Instagram accounts (session ID or user/pass) used to submit. Rotate them.
- **Proxies** — HTTP/HTTPS or SOCKS5, one per line, paired with the account pool.

---

## Project layout

```
instagram-mass-reporter/
├── main.py              # the loader — run this
├── files/               # cached backend + cache timestamp
│   ├── 3.13_fastapi.py  # or 3.13_android.py, depending on platform
│   └── lastupdate.txt
├── flask/               # Flask backend (Android)
│   └── 3.11.py, 3.12.py, 3.13.py
└── fastapi/             # FastAPI backend (desktop)
    └── 3.11.py, 3.12.py, 3.13.py
```

You never edit the files in `flask/` or `fastapi/`. They're the deployed backends and are pulled by the loader.

---

## Disclaimer

This tool is for **educational purposes and authorized use only.** Automated reporting of accounts you do not own or have no legitimate relationship to may violate Instagram's Terms of Service and, depending on jurisdiction, applicable law. The author is not responsible for misuse.

- Not affiliated with, endorsed by, or connected to Meta or Instagram.
- Use at your own risk. Your accounts may be restricted or banned by Instagram if you abuse this tool.
- Do not use this tool to harass, dox, or coordinate attacks against individuals.
