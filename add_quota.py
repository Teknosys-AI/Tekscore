#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to add quota for current month for all users with JScore role
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime
from app import app
from models.user_model import User, db
from models.quota_model import Quota
from models.product_model import Product
from models.role_model import Role
from sqlalchemy import text

def add_quota_for_current_month():
    """Add quota for current month for all JScore users"""
    with app.app_context():
        try:
            # Get current month and year
            current_date = datetime.now()
            current_month = current_date.month
            current_year = current_date.year
            
            print("="*70)
            print("ADDING QUOTA FOR CURRENT MONTH")
            print("="*70)
            print(f"Current Month: {current_month}")
            print(f"Current Year: {current_year}")
            print("="*70)
            
            # Get JScore product
            jscore_product = Product.query.filter_by(name='jscore').first()
            if not jscore_product:
                print("[ERROR] JScore product not found in database!")
                return False
            
            print(f"[OK] Found JScore product - ID: {jscore_product.id}")
            
            # Get JScore role (RoleId == 1)
            jscore_role = Role.query.filter_by(Name='Jscore').first()
            if not jscore_role:
                print("[ERROR] JScore role not found in database!")
                return False
            
            print(f"[OK] Found JScore role - ID: {jscore_role.RoleId}")
            
            # Get all users with JScore role
            users = User.query.filter_by(RoleId=jscore_role.RoleId).all()
            
            if not users:
                print("[WARNING] No users with JScore role found!")
                return False
            
            print(f"[OK] Found {len(users)} user(s) with JScore role")
            print("="*70)
            
            added_count = 0
            updated_count = 0
            
            for user in users:
                # Check if quota already exists for this month
                existing_quota = Quota.query.filter_by(
                    UserId=user.UserId,
                    ProductId=jscore_product.id,
                    Month=current_month,
                    Year=current_year
                ).first()
                
                if existing_quota:
                    print(f"[SKIP] User '{user.Username}' (ID: {user.UserId}) already has quota for {current_month}/{current_year}")
                    print(f"       MaxQuota: {existing_quota.MaxQuota}, UsedQuota: {existing_quota.UsedQuota}")
                    updated_count += 1
                else:
                    # Create new quota - default to 100 if user has subscription_type_id
                    max_quota = 100  # Default quota
                    
                    if user.subscription_type_id:
                        # You can customize quota based on subscription type if needed
                        max_quota = 100
                    
                    new_quota = Quota(
                        MaxQuota=max_quota,
                        UsedQuota=0,
                        UserId=user.UserId,
                        ProductId=jscore_product.id,
                        SubscriptionTypeId=user.subscription_type_id,
                        Month=current_month,
                        Year=current_year
                    )
                    
                    db.session.add(new_quota)
                    print(f"[ADD] Added quota for User '{user.Username}' (ID: {user.UserId})")
                    print(f"       MaxQuota: {max_quota}, UsedQuota: 0")
                    added_count += 1
            
            # Commit all changes
            db.session.commit()
            
            print("="*70)
            print(f"[SUCCESS] Quota addition completed!")
            print(f"   - Added: {added_count} new quota(s)")
            print(f"   - Already exists: {updated_count} quota(s)")
            print("="*70)
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print("="*70)
            print("[ERROR] Failed to add quota")
            print("="*70)
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {str(e)}")
            import traceback
            print(f"Full Traceback:\n{traceback.format_exc()}")
            print("="*70)
            return False

if __name__ == "__main__":
    add_quota_for_current_month()
