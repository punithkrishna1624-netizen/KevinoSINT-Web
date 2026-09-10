import requests

SITES = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "X": "https://x.com/{}",
}

def analyze_username(username):
    findings = []
    for name, url in SITES.items():
        try:
            r = requests.get(url.format(username), timeout=5, headers={"User-Agent": "KevinoSINT/1.0"})
            exists = r.status_code == 200
            findings.append({
                "label": name,
                "value": "Public page found" if exists else f"HTTP {r.status_code}",
                "status": "good" if exists else "info",
                "url": url.format(username)
            })
        except requests.RequestException:
            findings.append({"label": name, "value": "Check failed", "status": "warn"})
    return {
        "type": "username",
        "target": username,
        "summary": "Public username presence checks",
        "findings": findings,
        "notice": "A username match is not proof that multiple accounts belong to the same person."
    }
