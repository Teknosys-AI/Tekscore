# Role System Explanation

## Current Database State (After RoleId Swap)

| Role Name | RoleId | Description |
|-----------|--------|-------------|
| **Jscore** | **1** | JScore users (was 5, now 1) |
| Business | 5 | Business/Admin users (was 1, now 5) |
| Manager | 2 | Manager role |
| Analyst | 3 | Analyst role |
| Viewer | 4 | Viewer role |

## User Roles

| Username | RoleId | Role Name | Access Level |
|----------|--------|-----------|-------------|
| JMart | 1 | Jscore | Can access JScore features |
| manager_user, manag, gul_admin, guladmin | 5 | Business | Can access Business admin panel |

## Route Protection System

### 1. `@role_required(role_name)` Decorator
Located in: `blueprints/tasks/tasks.py`

**How it works:**
```python
@role_required("Jscore")  # Checks if user has "Jscore" role
def some_route():
    # This code only runs if user's RoleID matches Jscore role's RoleId
```

**What it checks:**
1. User must be logged in (`session['userId']` exists)
2. Gets `session['RoleID']` (the user's role ID)
3. Queries database for role with `Name="Jscore"` (or whatever role_name is passed)
4. Compares: `session['RoleID']` == `role.RoleId`
5. If match: allows access
6. If no match: redirects to login with "Unauthorized access!" message

### 2. Protected Routes

#### JScore Routes (require "Jscore" role - RoleId=1)
- `@jscore_bp.route('/')` - Main JScore page
- `@jscore_bp.route('/index')` - JScore index page
- **Decorator:** `@role_required("Jscore")`
- **Also checks:** `'agreementuserid'` in session (privacy policy agreement)

#### Business Routes (require "Business" role - RoleId=5)
- `@businessusers_bp.route('/pending_changes')` - View pending plan changes
- `@businessusers_bp.route('/update_plan_status')` - Update plan status
- **Decorator:** `@role_required("Business")`

## Login Flow

### Step 1: User Submits Login Form
- POST to `/login`
- Validates username/password
- Finds user in database

### Step 2: Role Check in Login
```python
if business_role and user.RoleId == business_role.RoleId:  # RoleId == 5
    # Business users: Direct login, no privacy agreement needed
    session['RoleID'] = user.RoleId  # Sets to 5
    redirect to businessusers.pending_changes
else:
    # All other users (including Jscore): Need privacy agreement
    session['temp_RoleID'] = user.RoleId  # Temporarily stores RoleId
    redirect to privacy_policy page
```

### Step 3: Privacy Policy Agreement (for non-Business users)
- User must agree to privacy policy
- POST to `/agree_privacy`
- Sets permanent session:
  ```python
  session['RoleID'] = temp_RoleID  # Sets to user's actual RoleId
  session['agreementuserid'] = temp_user_id
  ```
- Redirects to `jscore.index`

### Step 4: Accessing JScore Index
- `@role_required("Jscore")` decorator runs FIRST
- Checks: `session['RoleID']` == Jscore role's RoleId (which is 1)
- If JMart user (RoleId=1): ✅ Match! Access granted
- If Business user (RoleId=5): ❌ No match! Redirects to login

## Current Issues

### Issue 1: Session Variable Name Mismatch
- Login sets: `session['RoleID']` (capital ID)
- Some code might check: `session['roleId']` or `session['role_id']`
- **Solution:** Always use `session['RoleID']` consistently

### Issue 2: Privacy Agreement Required
- Jscore users MUST agree to privacy policy before accessing JScore routes
- The `jscore.index` route checks: `if 'agreementuserid' not in session`
- If missing, redirects to login

### Issue 3: Role Name vs RoleId Confusion
- Decorator uses role **Name** ("Jscore", "Business")
- But compares against role **RoleId** (1, 5)
- Make sure database has correct Name -> RoleId mapping

## Debugging Login Issues

### Check 1: Is user found?
```python
user = User.query.filter_by(Username=username, Password=hash).first()
if not user:
    # Login fails - wrong credentials
```

### Check 2: Is RoleID set correctly?
After login, check:
- `session['RoleID']` should equal user's RoleId
- For JMart: should be 1
- For Business users: should be 5

### Check 3: Does role exist in database?
```python
jscore_role = Role.query.filter_by(Name="Jscore").first()
if not jscore_role:
    # Role doesn't exist - decorator will fail
```

### Check 4: Does RoleID match?
```python
session['RoleID'] == jscore_role.RoleId  # Should be True for Jscore users
```

## Testing Login

1. **JMart (Jscore user - RoleId=1):**
   - Login → Privacy Policy → Agree → JScore Index ✅

2. **Business user (RoleId=5):**
   - Login → Business Admin Panel ✅
   - Cannot access JScore routes ❌
