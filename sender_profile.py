"""Per-account sender profile for Uplift email notifications.

Each Drive account stores its own sender identity (name + email) in
~/.uplift-profile.json under an "accounts" key.  App password is stored
securely in macOS Keychain via keyring — never written to disk.

JSON format:
  {
    "accounts": {
      "<account_id>": {"sender_name": "…", "sender_email": "…"},
      ...
    }
  }

Keyring key: ("uplift-email", sender_email) — password is per email
address, so two accounts sharing the same Gmail share one Keychain entry.

Migration: old flat-format file (no "accounts" key) is silently ignored.
User re-runs Setup once per account.
"""

import json
from pathlib import Path
import keyring

PROFILE_PATH      = Path.home() / ".uplift-profile.json"
KEYRING_SERVICE   = "uplift-email"

_OLD_PROFILE_PATH    = Path.home() / ".drive-uploader-profile.json"
_OLD_KEYRING_SERVICE = "drive-uploader-email"

# In-memory password cache keyed by sender_email.
# Populated at setup time (save) and at startup (preload_all).
# Background threads read from here — no Keychain access mid-export.
_pw_cache: dict[str, str] = {}


# ── Internal helpers ──────────────────────────────────────────────────────────

def _read_all() -> dict:
    """Return the full profile dict, or {} on any error / missing file."""
    if not PROFILE_PATH.exists():
        return {}
    try:
        data = json.loads(PROFILE_PATH.read_text())
        if not isinstance(data, dict):
            return {}
        # Old flat format has no "accounts" key — treat as empty
        if "accounts" not in data:
            return {}
        return data
    except (json.JSONDecodeError, OSError):
        return {}


def _write_all(data: dict) -> None:
    PROFILE_PATH.write_text(json.dumps(data, indent=2))


def _migrate_old_keyring(email: str) -> None:
    """One-time: copy password from old service to new, then delete old."""
    try:
        old_pw = keyring.get_password(_OLD_KEYRING_SERVICE, email)
        if old_pw:
            if not keyring.get_password(KEYRING_SERVICE, email):
                keyring.set_password(KEYRING_SERVICE, email, old_pw)
            try:
                keyring.delete_password(_OLD_KEYRING_SERVICE, email)
            except Exception:
                pass
    except Exception:
        pass


# ── Public API ────────────────────────────────────────────────────────────────

def load(account_id: str) -> dict | None:
    """Return {sender_name, sender_email, gmail_app_password} for account, or None.

    Password is served from the in-memory cache when available so background
    threads never trigger a Keychain access (and any macOS prompt) mid-export.
    """
    data = _read_all()
    acct = data.get("accounts", {}).get(account_id)
    if not acct:
        return None
    email = acct.get("sender_email", "")
    if email in _pw_cache:
        pw = _pw_cache[email]
    else:
        pw = keyring.get_password(KEYRING_SERVICE, email) or ""
        if pw:
            _pw_cache[email] = pw
    return {
        "sender_name":       acct.get("sender_name", ""),
        "sender_email":      email,
        "gmail_app_password": pw,
    }


def save(account_id: str, sender_name: str, sender_email: str, app_password: str) -> dict:
    """Write sender identity for account to disk, password to Keychain and cache."""
    data = _read_all()
    if "accounts" not in data:
        data["accounts"] = {}
    data["accounts"][account_id] = {
        "sender_name":  sender_name,
        "sender_email": sender_email,
    }
    _write_all(data)
    try:
        keyring.set_password(KEYRING_SERVICE, sender_email, app_password)
    except Exception:
        try:
            keyring.delete_password(KEYRING_SERVICE, sender_email)
            keyring.set_password(KEYRING_SERVICE, sender_email, app_password)
        except Exception:
            pass
    _pw_cache[sender_email] = app_password
    return {
        "sender_name":       sender_name,
        "sender_email":      sender_email,
        "gmail_app_password": app_password,
    }


def preload_all() -> None:
    """Pre-populate the password cache for every configured sender at startup.

    Call this on the main thread at launch so any macOS Keychain access
    prompt fires while the user is present, not mid-export in the background.
    """
    data = _read_all()
    for acct in data.get("accounts", {}).values():
        email = acct.get("sender_email", "")
        if email and email not in _pw_cache:
            _migrate_old_keyring(email)
            pw = keyring.get_password(KEYRING_SERVICE, email) or ""
            if pw:
                _pw_cache[email] = pw


def clear(account_id: str) -> None:
    """Remove sender profile for account from disk (and Keychain if no other account uses that email)."""
    data = _read_all()
    accounts = data.get("accounts", {})
    removed_email = accounts.pop(account_id, {}).get("sender_email", "")
    data["accounts"] = accounts
    _write_all(data)

    # Only delete the Keychain entry if no other account uses that email
    if removed_email:
        still_used = any(
            a.get("sender_email") == removed_email
            for a in accounts.values()
        )
        if not still_used:
            try:
                keyring.delete_password(KEYRING_SERVICE, removed_email)
            except Exception:
                pass
