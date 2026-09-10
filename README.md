# KevinoSINT

A local, ethical OSINT dashboard for authorized/public-source investigations.

## Kali Linux

```bash
sudo apt update
sudo apt install python3 python3-venv git -y

cd KevinoSINT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python3 app.py
```

Open:

http://127.0.0.1:5000

## API

`POST /api/investigate`

Example:

```json
{
  "type": "email",
  "target": "example@example.com"
}
```

Supported types:

- auto
- email
- phone
- username
- domain
- ip

## Branding

The uploaded profile image is stored as:

`static/kevin-avatar.jpeg`

Replace that file with your own logo/avatar if desired.

## Important

Use only public or authorized data sources. Do not use this application to obtain private residential addresses, passwords, OTPs, or unauthorized personal records.
