"""
Script to check the role system and understand routing
"""

import pymysql

def check_role_system():
    """Check roles and users in database"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='jscore',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            print("="*70)
            print("ROLE SYSTEM ANALYSIS")
            print("="*70)
            
            # Get all roles
            print("\n1. ROLES IN DATABASE:")
            print("-" * 70)
            cursor.execute("SELECT RoleId, Name, Description FROM Role ORDER BY RoleId")
            roles = cursor.fetchall()
            for role in roles:
                print(f"   RoleId={role[0]:<3} | Name='{role[1]:<15}' | {role[2]}")
            
            # Get Jscore and Business roles specifically
            print("\n2. KEY ROLES FOR ROUTING:")
            print("-" * 70)
            cursor.execute("SELECT RoleId, Name FROM Role WHERE Name IN ('Jscore', 'Business')")
            key_roles = cursor.fetchall()
            for role in key_roles:
                print(f"   {role[1]:<10} role has RoleId = {role[0]}")
            
            # Get test users
            print("\n3. TEST USERS:")
            print("-" * 70)
            cursor.execute("SELECT UserId, Username, RoleId FROM User WHERE Username IN ('JMart', 'gul_admin', 'manager_user')")
            users = cursor.fetchall()
            for user in users:
                # Get role name for this user
                cursor.execute(f"SELECT Name FROM Role WHERE RoleId = {user[2]}")
                role_name = cursor.fetchone()
                role_name_str = role_name[0] if role_name else "Unknown"
                print(f"   Username='{user[1]:<15}' | RoleId={user[2]} | Role Name='{role_name_str}'")
            
            # Explain routing
            print("\n4. ROUTING LOGIC:")
            print("-" * 70)
            print("   @role_required('Jscore')  -> Requires RoleId = 1 (Jscore role)")
            print("   @role_required('Business') -> Requires RoleId = 5 (Business role)")
            print("\n   Login Flow:")
            print("   - Business users (RoleId=5): Login -> Business Admin Panel")
            print("   - Jscore users (RoleId=1): Login -> Privacy Policy -> JScore Index")
            print("   - Other users: Login -> Privacy Policy -> (may not access JScore)")
            
            # Check JMart specifically
            print("\n5. JMART USER CHECK:")
            print("-" * 70)
            cursor.execute("SELECT UserId, Username, RoleId FROM User WHERE Username = 'JMart'")
            jmart = cursor.fetchone()
            if jmart:
                cursor.execute(f"SELECT Name FROM Role WHERE RoleId = {jmart[2]}")
                jmart_role = cursor.fetchone()
                print(f"   UserId: {jmart[0]}")
                print(f"   Username: {jmart[1]}")
                print(f"   RoleId: {jmart[2]}")
                print(f"   Role Name: {jmart_role[0] if jmart_role else 'Unknown'}")
                print(f"\n   Expected Behavior:")
                if jmart[2] == 1:
                    print("   [OK] RoleId=1 matches 'Jscore' role -> Can access JScore routes")
                    print("   [OK] Login -> Privacy Policy -> JScore Index")
                elif jmart[2] == 5:
                    print("   [WARN] RoleId=5 matches 'Business' role -> Cannot access JScore routes")
                    print("   [WARN] Login -> Business Admin Panel (no JScore access)")
                else:
                    print(f"   [ERROR] RoleId={jmart[2]} doesn't match Jscore(1) or Business(5)")
                    print("   [ERROR] May not be able to access protected routes")
        
        connection.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_role_system()
