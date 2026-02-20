import re
from pathlib import Path

from app.core.config import settings


_filename_re = re.compile(r"[^A-Za-z0-9._-]+")


def ensure_upload_dir() -> None:
    """
    Stellt sicher, dass das Upload-Verzeichnis existiert.
    """
    settings.upload_dir_abs.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Ersetzt problematische Zeichen im Dateinamen.
    """
    name = Path(filename).name
    name = _filename_re.sub("_", name).strip("._")
    return name or "file"


def build_public_url(stored_filename: str) -> str:
    """
    Baut die öffentliche URL für eine gespeicherte Datei.
    """
    prefix = settings.UPLOAD_PUBLIC_PREFIX.rstrip("/")
    return f"{prefix}/{stored_filename}"


def disk_path_from_attachment_value(value: str) -> Path:
    """
    Wandelt eine gespeicherte Attachment-Angabe (URL oder relativer Pfad) in einen Disk-Pfad um.
    """
    v = (value or "").strip()

    if not v:
        return settings.upload_dir_abs

    public_prefix = settings.UPLOAD_PUBLIC_PREFIX.rstrip("/")
    if v.startswith(public_prefix + "/"):
        relative = v[len(public_prefix) + 1 :]
        return (settings.upload_dir_abs / relative).resolve()

    if v.startswith("/"):
        v = v.lstrip("/")

    return (settings.upload_dir_abs.parent / v).resolve()
