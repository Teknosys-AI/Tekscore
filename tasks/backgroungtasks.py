# tasks/quota_tasks.py

from datetime import datetime
from models import db, Quota, User, SubscriptionType

def reset_quota():
    """Reset the quota for prepaid users daily."""
    with db.app.app_context():
        # Fetch all prepaid users and reset their quota
        prepaid_users = (
            db.session.query(Quota)
            .join(User, User.UserId == Quota.UserId)
            .join(SubscriptionType, SubscriptionType.id == User.subscription_type_id)
            .filter(SubscriptionType.subscriptiontype == 'prepaid')
        ).all()

        for quota in prepaid_users:
            quota.UsedQuota = 0
        db.session.commit()
        print(f"Quota reset at {datetime.now()}")
