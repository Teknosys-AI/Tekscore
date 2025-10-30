import time
import logging
import hashlib
import datetime
from models.changeplan_model import ChangePlan
from models.role_model import Role
from models.user_model import User, db
from models.agreement_model import Agreement
from models.usersession_model import UserSession
from ..api_util.api_utils import call_Jscore_api_function
from ..tasks.tasks import role_required
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort, make_response



businessusers_bp = Blueprint("businessusers", __name__, template_folder="templates/businessusers")
logger = logging.getLogger(__name__)



@businessusers_bp.route('/pending_changes')
@role_required("Business")  # 🔥 Role check applied here!
def pending_changes():
    # business_role = Role.query.filter_by(Name="Business").first()
    # print("Business Role ", business_role.RoleId)
    # print("SessionID", session.get('RoleID'))

    # if 'userId' not in session or session.get('RoleID') != (business_role.RoleId):
    #     return redirect(url_for('user.show_login'))  # Redirect if not logged in

    pending_requests = ChangePlan.query.filter_by(status="pending").all()
    if not pending_requests:
        print("No pending requests found in the database.")
    # else: print(pending_requests  )

    return render_template('pending_changes.html', pending_requests=pending_requests)


@businessusers_bp.route('/update_plan_status', methods=['POST'])
@role_required("Business")  # 🔥 Role check applied here!
def update_plan_status():
    if 'userId' not in session:
        return jsonify({"success": False, "message": "Unauthorized access!"}), 403

    data = request.get_json()
    request_id = data.get('request_id')
    new_status = data.get('status')

    if not request_id or not new_status:
        return jsonify({"success": False, "message": "Invalid data!"}), 400

    change_request = ChangePlan.query.get(request_id)

    if not change_request:
        return jsonify({"success": False, "message": "Request not found!"}), 404

    change_request.status = new_status
    db.session.commit()

    return jsonify({"success": True, "message": f"Status updated to {new_status}!"})


