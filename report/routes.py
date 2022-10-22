from flask import Blueprint, render_template

from access import group_required

blueprint_report = Blueprint('blueprint_report', __name__, template_folder='templates')


@blueprint_report.route('/')
@group_required
def start_report():
    return render_template('report_result.html')
