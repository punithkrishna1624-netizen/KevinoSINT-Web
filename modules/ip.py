import ipaddress
import requests

def analyze_ip(ip):
    try:
        obj = ipaddress.ip_address(ip)
        valid = True
    except ValueError:
        valid = False

    findings = [
        {"label": "IP syntax", "value": "Valid" if valid else "Invalid", "status": "good" if valid else "bad"},
    ]

    if valid:
        try:
            r = requests.get(f"https://ipwho.is/{ip}", timeout=6)
            data = r.json()
            if data.get("success"):
                for label, key in [
                    ("Country", "country"),
                    ("Region", "region"),
                    ("City", "city"),
                    ("ISP", "connection"),
                ]:
                    value = data.get(key)
                    if isinstance(value, dict):
                        value = value.get("isp") or value.get("org") or value.get("asn")
                    findings.append({"label": label, "value": value or "Unavailable", "status": "info"})
        except requests.RequestException:
            findings.append({"label": "Geo/ASN lookup", "value": "Unavailable", "status": "warn"})

    return {
        "type": "ip",
        "target": ip,
        "summary": "Approximate IP/network intelligence",
        "findings": findings,
        "notice": "IP geolocation is approximate and should not be treated as a residential address."
    }
