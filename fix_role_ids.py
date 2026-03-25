"""
Script to swap RoleIds: Jscore -> 1, Business -> 5
"""

import pymysql

def swap_role_ids():
    """Swap RoleIds in the database"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='jscore',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            print("Swapping RoleIds...")
            print("Jscore role will become RoleId=1")
            print("Business role will become RoleId=5")
            
            # Disable foreign key checks temporarily
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # First, update users to temporary values
            # Users with RoleId=5 (old Jscore) should become RoleId=1
            cursor.execute("UPDATE `User` SET RoleId = 99 WHERE RoleId = 5")
            # Users with RoleId=1 (old Business) should become RoleId=98
            cursor.execute("UPDATE `User` SET RoleId = 98 WHERE RoleId = 1")
            connection.commit()
            
            # Now update roles to temporary values
            cursor.execute("UPDATE `Role` SET RoleId = 97 WHERE Name = 'Jscore'")
            cursor.execute("UPDATE `Role` SET RoleId = 96 WHERE Name = 'Business'")
            connection.commit()
            
            # Now set roles to final values
            cursor.execute("UPDATE `Role` SET RoleId = 1 WHERE Name = 'Jscore'")
            cursor.execute("UPDATE `Role` SET RoleId = 5 WHERE Name = 'Business'")
            connection.commit()
            
            # Now update users to final values
            cursor.execute("UPDATE `User` SET RoleId = 1 WHERE RoleId = 99")
            cursor.execute("UPDATE `User` SET RoleId = 5 WHERE RoleId = 98")
            connection.commit()
            
            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            connection.commit()
            
            print("\n[SUCCESS] RoleIds swapped!")
            print("\nUpdated roles:")
            cursor.execute("SELECT RoleId, Name FROM `Role` WHERE Name IN ('Jscore', 'Business')")
            roles = cursor.fetchall()
            for role in roles:
                print(f"  - {role[1]}: RoleId={role[0]}")
            
            print("\nUpdated users:")
            cursor.execute("SELECT UserId, Username, RoleId FROM `User`")
            users = cursor.fetchall()
            for user in users:
                print(f"  - {user[1]} (ID:{user[0]}): RoleId={user[2]}")
        
        connection.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    swap_role_ids()
