# Phase Echo

**Rynex Technologies · Cryptography · Insane**

An archival signing service has left behind a public key, a set of signed audit records, and an encrypted vault capsule. Recover the original archive flag.

The package includes `output.txt`, a captured service export, and `challenge.py`, the reference implementation of the service format. No network access or external service is needed.

## Your task

Recover the signing key material needed to authenticate and open the vault capsule. The flag format is `RTCTF{...}`. This is an offline practice challenge; there is no submission platform.

## Files

- `output.txt` — public key, audit records, and sealed capsule.
- `challenge.py` — curve, signature, and envelope implementation.
- `requirements.txt` — Python dependencies.

## Run

Python 3.11+ is recommended.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 challenge.py
```

The script prints format and curve information; the captured instance is in `output.txt`.

## Safety

All data is fictional and local. The challenge performs no network requests, file traversal, persistence, or destructive operations. Do not use recovered material outside this practice exercise.
