#!/usr/bin/env python3
"""Project Cerberus · Odin demo server.

Serves the Odin web page and a small JSON API backed by SQLite.
Python 3.9+ standard library only: no packages to install.

    python3 server.py                      # http://127.0.0.1:8080
    HOST=0.0.0.0 PORT=8080 ODIN_DEMO_PASSWORD=change-me python3 server.py

This demo holds invented students only. Never load real student data into a hosted copy.
"""
import base64
import hmac
import json
import os
import re
import sqlite3
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("ODIN_DB", ROOT / "db" / "odin_demo.db"))
SCHEMA = ROOT / "db" / "schema.sql"
SEED = ROOT / "db" / "seed.sql"
INDEX = ROOT / "public" / "index.html"
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8080"))
PASSWORD = os.environ.get("ODIN_DEMO_PASSWORD", "")
MAX_BODY = 2 * 1024 * 1024
WRITE_LOCK = threading.Lock()

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KEY = re.compile(r"^S-\d{3}:(reading|math)$")
SUBJECTS = ("reading", "math")
ROADMAP_TABLES = ("roadmaps", "lessons", "lesson_standards", "lesson_marks")


# ---------- database ----------
def connect():
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def build_database():
    """Create the database from schema.sql and seed.sql (used on first run and on reset)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = DB_PATH.with_suffix(".tmp")
    if tmp.exists():
        tmp.unlink()
    con = sqlite3.connect(tmp)
    con.executescript(SCHEMA.read_text())
    con.executescript(SEED.read_text())
    con.commit()
    con.close()
    os.replace(tmp, DB_PATH)


def restore_roadmaps(con):
    """Put the sample roadmaps and the sample teacher marks back."""
    con.execute("DELETE FROM lesson_marks")
    con.execute("DELETE FROM lessons")
    con.execute("DELETE FROM roadmaps")
    stmts = [ln for ln in SEED.read_text().splitlines()
             if any(ln.startswith(f"INSERT INTO {t} ") for t in ROADMAP_TABLES)]
    con.executescript("\n".join(stmts))


def load_data(con):
    """Assemble the JSON the Odin page expects."""
    one = lambda sql, *a: con.execute(sql, a).fetchone()
    data = {"today": one("SELECT value FROM settings WHERE key='today'")[0]}
    data["standards"] = {s: [{"code": r["code"], "label": r["label"], "rung": r["skill"]}
                             for r in con.execute("SELECT * FROM standards WHERE subject=? ORDER BY position", (s,))]
                         for s in SUBJECTS}
    students = []
    for r in con.execute("SELECT * FROM students ORDER BY code"):
        s = {"code": r["code"], "name": r["name"], "grade": r["grade"]}
        e = one("SELECT * FROM ese_profiles WHERE code=?", r["code"])
        if e:
            c = r["code"]
            s["ese"] = {
                "exceptionality": e["exceptionality"], "review": e["review_date"],
                "areas": [x[0] for x in con.execute("SELECT subject FROM ese_areas WHERE code=? ORDER BY subject DESC", (c,))],
                "services": [x[0] for x in con.execute("SELECT text FROM ese_services WHERE code=? ORDER BY position", (c,))],
                "accommodations": [x[0] for x in con.execute("SELECT text FROM ese_accommodations WHERE code=? ORDER BY position", (c,))],
                "probes": {x["skill"]: {"date": x["probe_date"], "right": x["items_right"], "total": x["items_total"]}
                           for x in con.execute("SELECT * FROM ese_probes WHERE code=?", (c,))},
            }
        students.append(s)
    data["students"] = students
    files = []
    for f in con.execute("SELECT * FROM assessment_files ORDER BY position"):
        d = {"id": f["id"], "source": f["source"], "subject": f["subject"], "name": f["file_name"],
             "date": f["file_date"], "what": f["description"], "active": bool(f["active"])}
        if f["pending"]:
            d["pending"] = True
        if f["imported"]:
            d["imported"] = True
        rows = {}
        if f["source"] == "i-Ready":
            for x in con.execute("SELECT * FROM iready_results WHERE file_id=?", (f["id"],)):
                rows.setdefault(x["code"], {})[x["domain"]] = x["placement"]
        elif f["source"] == "FAST":
            for x in con.execute("SELECT * FROM fast_scores WHERE file_id=?", (f["id"],)):
                rows[x["code"]] = {"ss": x["scale_score"], "level": x["achievement_level"]}
            for x in con.execute("SELECT * FROM fast_categories WHERE file_id=?", (f["id"],)):
                rows[x["code"]][x["skill"]] = x["band"]
        else:
            d["items"] = [{"n": x["item_number"], "code": x["benchmark"], "label": x["label"], "rung": x["skill"]}
                          for x in con.execute("SELECT * FROM pm_items WHERE file_id=? ORDER BY item_number", (f["id"],))]
            for x in con.execute("SELECT * FROM pm_responses WHERE file_id=? ORDER BY code, item_number", (f["id"],)):
                rows.setdefault(x["code"], []).append(x["correct"])
        d["rows"] = rows
        files.append(d)
    data["files"] = files
    roadmap = {}
    for rm in con.execute("SELECT * FROM roadmaps"):
        lessons = []
        for l in con.execute("SELECT * FROM lessons WHERE subject=? ORDER BY position", (rm["subject"],)):
            unit = int(l["unit"]) if l["unit"].isdigit() else l["unit"]
            lessons.append({"id": l["id"], "unit": unit, "unitTitle": l["unit_title"], "date": l["lesson_date"],
                            "title": l["title"], "activity": l["activity"],
                            "standards": [x[0] for x in con.execute(
                                "SELECT code FROM lesson_standards WHERE lesson_id=? ORDER BY position", (l["id"],))]})
        roadmap[rm["subject"]] = {"name": rm["name"], "lessons": lessons}
    for s in SUBJECTS:
        roadmap.setdefault(s, {"name": "No roadmap loaded", "lessons": []})
    data["roadmap"] = roadmap
    marks = con.execute("SELECT * FROM lesson_marks").fetchall()
    data["overrides"] = {m["lesson_id"]: m["status"] for m in marks if m["status"]}
    data["overrideNotes"] = {m["lesson_id"]: m["note"] for m in marks if m["note"]}
    data["approvals"] = {f'{a["code"]}:{a["subject"]}': a["approved_on"] for a in con.execute("SELECT * FROM plan_approvals")}
    return data


# ---------- request validation ----------
class BadRequest(Exception):
    pass


def text(v, name, limit, required=True):
    if v is None or v == "":
        if required:
            raise BadRequest(f"{name} is required")
        return ""
    if not isinstance(v, (str, int)):
        raise BadRequest(f"{name} must be text")
    v = str(v).strip()
    if len(v) > limit:
        raise BadRequest(f"{name} is longer than {limit} characters")
    return v


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def api_lesson(con, body):
    lid = text(body.get("id"), "id", 40)
    status = body.get("status")
    if status not in ("taught", "nottaught", None):
        raise BadRequest("status must be taught, nottaught or null")
    if not con.execute("SELECT 1 FROM lessons WHERE id=?", (lid,)).fetchone():
        raise BadRequest("unknown lesson")
    con.execute("""INSERT INTO lesson_marks (lesson_id, status, note, updated_at) VALUES (?, ?, NULL, ?)
                   ON CONFLICT(lesson_id) DO UPDATE SET status=excluded.status, updated_at=excluded.updated_at""",
                (lid, status, now()))


def api_approval(con, body):
    key = text(body.get("key"), "key", 20)
    if not KEY.match(key):
        raise BadRequest("key must look like S-004:reading")
    code, subject = key.split(":")
    if not con.execute("SELECT 1 FROM students WHERE code=?", (code,)).fetchone():
        raise BadRequest("unknown student")
    date = body.get("date")
    if date is None:
        con.execute("DELETE FROM plan_approvals WHERE code=? AND subject=?", (code, subject))
    else:
        con.execute("INSERT OR REPLACE INTO plan_approvals VALUES (?, ?, ?)", (code, subject, text(date, "date", 40)))


def api_file(con, body):
    fid = text(body.get("id"), "id", 20)
    row = con.execute("SELECT * FROM assessment_files WHERE id=?", (fid,)).fetchone()
    if not row:
        raise BadRequest("unknown file")
    vals = {k: (1 if body[k] else 0) for k in ("active", "pending", "imported") if k in body}
    if not vals:
        raise BadRequest("nothing to change")
    con.execute(f"UPDATE assessment_files SET {', '.join(k + '=?' for k in vals)} WHERE id=?", (*vals.values(), fid))


def api_roadmap(con, body):
    subject = body.get("subject")
    if subject not in SUBJECTS:
        raise BadRequest("subject must be reading or math")
    name = text(body.get("name"), "name", 120)
    lessons = body.get("lessons")
    if not isinstance(lessons, list) or not 0 < len(lessons) <= 500:
        raise BadRequest("lessons must be a list of 1 to 500 lessons")
    clean = []
    for i, l in enumerate(lessons):
        if not isinstance(l, dict):
            raise BadRequest(f"lesson {i + 1} is not an object")
        date = text(l.get("date"), "date", 10)
        if not ISO.match(date):
            raise BadRequest(f"lesson {i + 1}: date must be YYYY-MM-DD")
        stds = l.get("standards")
        if not isinstance(stds, list) or not 0 < len(stds) <= 20:
            raise BadRequest(f"lesson {i + 1}: list 1 to 20 standards")
        clean.append((text(l.get("id"), "id", 40), text(l.get("unit"), "unit", 40), text(l.get("unitTitle"), "unitTitle", 120),
                       date, text(l.get("title"), "title", 200), text(l.get("activity"), "activity", 300, required=False),
                       list(dict.fromkeys(text(c, "standard", 40) for c in stds))))
    ids = [c[0] for c in clean]
    if len(set(ids)) != len(ids):
        raise BadRequest("lesson ids must be unique")
    old = [r[0] for r in con.execute("SELECT id FROM lessons WHERE subject=?", (subject,))]
    con.executemany("DELETE FROM lesson_marks WHERE lesson_id=?", [(x,) for x in old])
    con.execute("DELETE FROM lessons WHERE subject=?", (subject,))
    for lid in ids:
        if con.execute("SELECT 1 FROM lessons WHERE id=?", (lid,)).fetchone():
            raise BadRequest(f"lesson id {lid} is already used by the other subject")
    con.execute("INSERT OR REPLACE INTO roadmaps VALUES (?, ?)", (subject, name))
    for pos, (lid, unit, ut, date, title, act, stds) in enumerate(clean):
        con.execute("INSERT INTO lessons VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (lid, subject, unit, ut, date, title, act, pos))
        con.executemany("INSERT INTO lesson_standards VALUES (?, ?, ?)", [(lid, c, j) for j, c in enumerate(stds)])


POST_ROUTES = {"/api/lesson": api_lesson, "/api/approval": api_approval, "/api/file": api_file, "/api/roadmap": api_roadmap}


# ---------- HTTP ----------
class Handler(BaseHTTPRequestHandler):
    server_version = "Odin"
    sys_version = ""

    def log_message(self, fmt, *args):  # keep logs short; no request bodies
        print(f"{self.log_date_time_string()} {self.command} {self.path.split('?')[0]} {args[1] if len(args) > 1 else ''}")

    def authorized(self):
        if not PASSWORD:
            return True
        h = self.headers.get("Authorization", "")
        if h.startswith("Basic "):
            try:
                _, _, pw = base64.b64decode(h[6:]).decode("utf-8").partition(":")
                return hmac.compare_digest(pw.encode(), PASSWORD.encode())
            except Exception:
                return False
        return False

    def send(self, code, body, ctype="application/json; charset=utf-8"):
        raw = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(raw)

    def gate(self):
        if self.authorized():
            return True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Odin demo", charset="UTF-8"')
        self.send_header("Content-Length", "0")
        self.end_headers()
        return False

    def do_GET(self):
        if not self.gate():
            return
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            return self.send(200, INDEX.read_bytes(), "text/html; charset=utf-8")
        if path == "/api/health":
            return self.send(200, {"ok": True, "app": "Odin", "project": "Project Cerberus"})
        if path == "/api/data":
            con = connect()
            try:
                return self.send(200, load_data(con))
            finally:
                con.close()
        self.send(404, {"error": "not found"})

    def do_POST(self):
        if not self.gate():
            return
        path = self.path.split("?")[0]
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self.send(413, {"error": "request too large"})
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(body, dict):
                raise BadRequest("send a JSON object")
        except (ValueError, BadRequest) as e:
            return self.send(400, {"error": str(e) or "invalid JSON"})
        with WRITE_LOCK:
            if path == "/api/reset":
                build_database()
                return self.send(200, {"ok": True})
            con = connect()
            try:
                if path == "/api/roadmap/restore":
                    restore_roadmaps(con)
                elif path in POST_ROUTES:
                    POST_ROUTES[path](con, body)
                else:
                    return self.send(404, {"error": "not found"})
                con.commit()
                return self.send(200, {"ok": True})
            except BadRequest as e:
                con.rollback()
                return self.send(400, {"error": str(e)})
            finally:
                con.close()


def main():
    if not DB_PATH.exists():
        build_database()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    lock = "on" if PASSWORD else "off (set ODIN_DEMO_PASSWORD to require one)"
    print(f"Odin demo for Project Cerberus on http://{HOST}:{PORT}  ·  password {lock}")
    print("Demo data only: every student is invented.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
