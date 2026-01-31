from flask import Blueprint, send_file, request, jsonify
import os
import tarfile
import tempfile
import shutil
import time
import subprocess

backup_api = Blueprint("backup_api", __name__)

BACKUP_PATHS = [
    "/opt/ptp-data",
    "/opt/ptp-config/config.json",
    "/etc/ptp4l.conf",
    "/etc/phc2sys.conf"
]

def restart_services():
    subprocess.call(["systemctl", "restart", "ptp4l"])
    subprocess.call(["systemctl", "restart", "phc2sys"])
    subprocess.call(["systemctl", "restart", "logger.service"])
    subprocess.call(["systemctl", "restart", "alerts.service"])
    subprocess.call(["systemctl", "restart", "dashboard.service"])


@backup_api.route("/export")
def export_backup():
    ts = int(time.time())
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz")
    tmp.close()

    with tarfile.open(tmp.name, "w:gz") as tar:
        for path in BACKUP_PATHS:
            if os.path.exists(path):
                tar.add(path, arcname=os.path.basename(path))

    return send_file(
        tmp.name,
        as_attachment=True,
        download_name=f"ptp-backup-{ts}.tar.gz"
    )


@backup_api.route("/restore", methods=["POST"])
def restore_backup():
    if "file" not in request.files:
        return jsonify({"error": "no_file"}), 400

    uploaded = request.files["file"]

    tmpdir = tempfile.mkdtemp()
    archive_path = os.path.join(tmpdir, "restore.tar.gz")
    uploaded.save(archive_path)

    # Extract to temp
    extract_dir = os.path.join(tmpdir, "extract")
    os.makedirs(extract_dir)

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(extract_dir)
    except Exception:
        shutil.rmtree(tmpdir)
        return jsonify({"error": "invalid_archive"}), 400

    # Validate required files
    required = ["config.json", "ptp4l.conf", "phc2sys.conf"]
    for r in required:
        if not any(r in f for f in os.listdir(extract_dir)):
            shutil.rmtree(tmpdir)
            return jsonify({"error": f"missing_{r}"}), 400

    # Apply restore
    try:
        # Restore config
        cfg_src = os.path.join(extract_dir, "config.json")
        cfg_dst = "/opt/ptp-config/config.json"
        shutil.copy2(cfg_src, cfg_dst)

        # Restore ptp4l
        p4_src = os.path.join(extract_dir, "ptp4l.conf")
        p4_dst = "/etc/ptp4l.conf"
        shutil.copy2(p4_src, p4_dst)

        # Restore phc2sys
        phc_src = os.path.join(extract_dir, "phc2sys.conf")
        phc_dst = "/etc/phc2sys.conf"
        shutil.copy2(phc_src, phc_dst)

        # Restore data directory
        data_src = os.path.join(extract_dir, "ptp-data")
        if os.path.exists(data_src):
            shutil.rmtree("/opt/ptp-data")
            shutil.copytree(data_src, "/opt
