import psycopg2
import sys
from dotenv import load_dotenv
import os
load_dotenv()


URL = os.getenv("RENDER_POSTGRESS_DB_URL")

def fix_all(database_url):
    fk_constraints = [
        ("sales",     "sales_admin_id_fkey",        "admin_id",    "admins",    "admin_id"),
        ("sales",     "sales_product_id_fkey",       "product_id",  "products",  "product_id"),
        ("purchases", "purchases_supplier_id_fkey",  "supplier_id", "suppliers", "supplier_id"),
        ("purchases", "purchases_product_id_fkey",   "product_id",  "products",  "product_id"),
        ("purchases", "purchases_admin_id_fkey",     "admin_id",    "admins",    "admin_id"),
    ]

    conn = psycopg2.connect(database_url)
    conn.autocommit = False
    cursor = conn.cursor()
    print("Connected!\n")

    # Fix FK constraints
    print("--- Fixing FK Constraints ---")
    for table, constraint, column, ref_table, ref_column in fk_constraints:
        print(f"Fixing {constraint}...")
        cursor.execute(f"ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {constraint};")
        cursor.execute(f"""
            ALTER TABLE {table}
            ADD CONSTRAINT {constraint}
            FOREIGN KEY ({column})
            REFERENCES {ref_table}({ref_column})
            ON DELETE SET NULL;
        """)
        print(f"  ✅ Done")

    # Fix column types
    print("\n--- Fixing Column Types ---")
    for column in ["customer_name", "customer_number"]:
        print(f"Converting sales.{column} to TEXT...")
        cursor.execute(f"""
            ALTER TABLE sales
            ALTER COLUMN {column} TYPE TEXT USING {column}::TEXT;
        """)
        print(f"  ✅ Done")

    conn.commit()
    print("\nAll changes committed! Verifying...\n")

    # Verify FK constraints
    action_map = {"a": "NO ACTION", "r": "RESTRICT", "c": "CASCADE", "n": "SET NULL", "d": "SET DEFAULT"}
    cursor.execute("""
        SELECT conname, conrelid::regclass, confdeltype
        FROM pg_constraint
        WHERE contype = 'f'
        ORDER BY conrelid::regclass::text, conname;
    """)
    print(f"{'Constraint':<40} {'Table':<15} {'On Delete'}")
    print("-" * 65)
    for row in cursor.fetchall():
        print(f"{row[0]:<40} {str(row[1]):<15} {action_map.get(row[2], row[2])}")

    # Verify column types
    cursor.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'sales'
        AND column_name IN ('customer_name', 'customer_number');
    """)
    print(f"\n{'Column':<20} {'Type'}")
    print("-" * 35)
    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[1]}")

    cursor.close()
    conn.close()
    print("\nAll done!")

fix_all(URL)