from flask import Flask, render_template, request, jsonify
from modules.email import analyze_email
from modules.phone import analyze_phone
from modules.username import analyze_username
from modules.domain import analyze_domain
from modules.ip import analyze_ip

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/investigate")
def investigate():
    data = request.get_json(silent=True) or {}
    target = (data.get("target") or "").strip()
    target_type = (data.get("type") or "auto").lower()

    if not target:
        return jsonify({"error": "Enter a target."}), 400

    try:
        if target_type == "email":
            result = analyze_email(target)
        elif target_type == "phone":
            result = analyze_phone(target)
        elif target_type == "username":
            result = analyze_username(target)
        elif target_type == "domain":
            result = analyze_domain(target)
        elif target_type == "ip":
            result = analyze_ip(target)
        else:
            # Conservative auto-detection.
            if "@" in target:
                result = analyze_email(target)
            elif target.replace(".", "").isdigit() and target.count(".") == 3:
                result = analyze_ip(target)
            elif target.startswith("+") or target.replace(" ", "").isdigit():
                result = analyze_phone(target)
            elif "." in target:
                result = analyze_domain(target)
            else:
                result = analyze_username(target)

        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

@app.get("/api/health")
def health():
    return jsonify({"status": "online", "service": "KevinoSINT"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
