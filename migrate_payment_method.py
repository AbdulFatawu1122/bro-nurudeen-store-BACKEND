import psycopg2
import os

# Connect to the external database URL
DATABASE_URL = "postgresql://bro_nurudeen_backend_db_web:BMLLF1YFPhhyQALoezorrzzWQWsiLE1W@dpg-d7mfsh1o3t8c73e5l1q0-a.oregon-postgres.render.com/bro_nurudeen_db"

def run_migration():
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()

        print("Creating enum type 'paymentmethodenum' if it does not exist...")
        cursor.execute("""
            DO $$ BEGIN
                CREATE TYPE paymentmethodenum AS ENUM ('mobile_money', 'paid_cash');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)

        print("Adding 'payed_using' column to 'sales' table...")
        cursor.execute("""
            ALTER TABLE sales ADD COLUMN IF NOT EXISTS payed_using paymentmethodenum;
        """)

        print("Adding 'payed_using' column to 'saleshist' table...")
        cursor.execute("""
            ALTER TABLE saleshist ADD COLUMN IF NOT EXISTS payed_using paymentmethodenum;
        """)

        print("Migration completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    run_migration()
