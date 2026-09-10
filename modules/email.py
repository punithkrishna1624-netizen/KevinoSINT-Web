import re
import socket

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def analyze_email(email):
    valid = bool(EMAIL_RE.match(email))
    domain = email.split("@", 1)[1].lower() if "@" in email else ""

    mx = []
    if domain:
        try:
            import dns.resolver
            answers = dns.resolver.resolve(domain, "MX")
            mx = sorted([str(a.exchange).rstrip(".") for a in answers])
        except Exception:
            pass

    return {
        "type": "email",
        "target": email,
        "summary": "Public email/domain intelligence",
        "findings": [
            {"label": "Syntax", "value": "Valid" if valid else "Invalid", "status": "good" if valid else "bad"},
            {"label": "Domain", "value": domain or "—", "status": "info"},
            {"label": "MX records", "value": ", ".join(mx) if mx else "Not resolved", "status": "good" if mx else "warn"},
        ],
        "notice": "This module does not reveal private account ownership, passwords, or residential addresses."
    }
