from flask import Blueprint, send_file
from backend.storage.excel_export import generate_excel_export

export_api = Blueprint("export_api", __name__)

@export_api.route("/excel", methods=["GET"])
def export_excel():
    excel_data = generate_excel_export()
    return send_file(
        excel_data,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="ptp_export.xlsx"
    )
