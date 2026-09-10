
# KevinoSINT — Website Deployment

This is the web version of KevinoSINT. It includes your supplied branding image.

## Option 1 — Render

1. Create a GitHub repository.
2. Upload the contents of this folder.
3. On Render, create a new Web Service from the repository.
4. Build command:
   pip install -r requirements.txt
5. Start command:
   gunicorn app:app
6. Deploy.

Render will provide a public HTTPS website URL.

## Option 2 — Any Python host

Use Python 3.11+ and run:

    pip install -r requirements.txt
    gunicorn app:app

For local testing:

    python3 app.py

Then visit:

    http://127.0.0.1:5000

## API

POST /api/investigate

JSON:
{
  "type": "email",
  "target": "example@example.com"
}

Supported target types:
auto, email, phone, username, domain, ip

## Branding

Your supplied image is:

static/kevin-avatar.jpeg

Replace that image with a different logo/avatar whenever you want.

## Production note

For a public deployment, add authentication, rate limiting, server-side logging controls, API-key secrets through environment variables, and terms/privacy notices before exposing investigation endpoints publicly.

Use only public or authorized OSINT sources. Do not use the site to obtain private residential addresses, passwords, OTPs, or unauthorized personal records.
