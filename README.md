# Project Cerberus · Odin demo server

A hostable demo of **Odin**, the Secure Student Analyzer for Project Cerberus. Teacher actions are saved to a SQLite database, so everyone who opens the demo sees the same state: lesson marks on the roadmap, approved plans, imported files and uploaded roadmaps.

**Every student in this database is invented.** This copy is for showing the idea to the school. Never load real student data into a hosted demo; the real Odin runs offline on the Project Cerberus server.

## What's inside

| Path | What it is |
| --- | --- |
| `server.py` | The backend. Python 3.9 or newer, standard library only, nothing to install |
| `public/index.html` | The Odin web page; it loads its data from the server |
| `db/odin_demo.db` | The demo database, ready to use |
| `db/schema.sql`, `db/seed.sql` | The same database as plain SQL, to rebuild it or load it elsewhere |
| `data_export/*.csv` | One CSV per table, for a look in Excel |
| `Dockerfile` | For hosts that run containers |

## Run it on your own computer

```
python3 server.py
```

Open http://127.0.0.1:8080.

## Host it on a server

On a Linux server or VPS with Python 3:

```
HOST=0.0.0.0 PORT=8080 ODIN_DEMO_PASSWORD=pick-a-password python3 server.py
```

- `ODIN_DEMO_PASSWORD` turns on a browser password prompt. Any user name works; only the password is checked. Leave it unset only on a private network.
- Put HTTPS in front before sharing a link. With Caddy installed, one command does it: `caddy reverse-proxy --from demo.yourdomain.org --to localhost:8080`.

With Docker:

```
docker build -t odin-demo .
docker run -d -p 8080:8080 -e ODIN_DEMO_PASSWORD=pick-a-password -v odin-data:/app/data --name odin-demo odin-demo
```

The `odin-data` volume keeps the database between restarts. Hosts that run a Dockerfile and set `PORT` themselves also work.

## Settings

| Variable | Default | Meaning |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Address to listen on. Use `0.0.0.0` to accept outside connections |
| `PORT` | `8080` | Port |
| `ODIN_DEMO_PASSWORD` | not set | Password for the demo |
| `ODIN_DB` | `db/odin_demo.db` | Database file. Built from `schema.sql` and `seed.sql` if missing |

## Resetting the demo

On the **Imports** tab, **Reset demo data** (click twice) puts everything back to the starting demo for all viewers. On the **Roadmap** tab, **Restore sample roadmap** resets only the roadmaps and lesson marks. You can also delete the database file and restart; it rebuilds from the SQL files.

## API

| Method and path | Does |
| --- | --- |
| `GET /api/health` | Health check |
| `GET /api/data` | Everything the page needs, assembled from the database |
| `POST /api/lesson` `{"id": "R2.2", "status": "taught" or "nottaught" or null}` | Marks a lesson; null returns it to the roadmap date |
| `POST /api/approval` `{"key": "S-004:reading", "date": "Oct 9, 2026" or null}` | Approves or un-approves a plan |
| `POST /api/file` `{"id": "pm2", "active": true, "imported": true}` | Imports or switches a test file on or off |
| `POST /api/roadmap` `{"subject": "reading", "name": "...", "lessons": [...]}` | Replaces a subject's roadmap |
| `POST /api/roadmap/restore` | Restores the sample roadmaps and marks |
| `POST /api/reset` | Rebuilds the whole database from the seed |

## Notes

- The demo calendar is frozen at October 9, 2026 (the `today` row in `settings`), so pacing and "taught so far" always look the same.
- Scoring, grade-level conversion, priorities, standards mastery and IEP goal drafts run in the page from the database rows, exactly as in the online demo.
- The page loads its fonts from Google Fonts. The offline build on Project Cerberus would bundle them instead.
