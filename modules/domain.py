import socket

def analyze_domain(domain):
    domain = domain.replace("https://", "").replace("http://", "").split("/")[0].strip()
    findings = []
    try:
        ip = socket.gethostbyname(domain)
        findings.append({"label": "IPv4", "value": ip, "status": "good"})
    except socket.gaierror:
        findings.append({"label": "IPv4", "value": "Not resolved", "status": "warn"})

    try:
        import dns.resolver
        for record_type in ["A", "AAAA", "MX", "TXT", "NS"]:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                values = [str(a).rstrip(".") for a in answers]
                findings.append({"label": record_type, "value": ", ".join(values[:8]), "status": "good"})
            except Exception:
                findings.append({"label": record_type, "value": "None / unavailable", "status": "info"})
    except Exception:
        pass

    return {
        "type": "domain",
        "target": domain,
        "summary": "DNS and public domain intelligence",
        "findings": findings,
        "notice": "DNS data is public infrastructure information."
    }
