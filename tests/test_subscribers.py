import os, uuid
import mysql.connector as mysql

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "prog8850_db")
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASS = os.getenv("DB_PASS", "app_password")

def get_conn():
    return mysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, database=DB_NAME)

def test_crud_subscriber():
    email = f"student_{uuid.uuid4().hex[:8]}@example.com"
    full_name = "Test Student"
    status = "active"
    conn = get_conn(); cur = conn.cursor()

    # CREATE
    cur.execute("INSERT INTO subscribers (email, full_name, status) VALUES (%s, %s, %s)", (email, full_name, status))
    conn.commit(); assert cur.rowcount == 1

    # READ
    cur.execute("SELECT id, email, full_name, status FROM subscribers WHERE email=%s", (email,))
    sub_id, r_email, r_name, r_status = cur.fetchone()
    assert r_email == email and r_name == full_name and r_status == status

    # UPDATE
    cur.execute("UPDATE subscribers SET full_name=%s, status=%s WHERE id=%s", ("Updated Name", "inactive", sub_id))
    conn.commit(); assert cur.rowcount == 1

    # READ again
    cur.execute("SELECT full_name, status FROM subscribers WHERE id=%s", (sub_id,))
    assert cur.fetchone() == ("Updated Name", "inactive")

    # DELETE
    cur.execute("DELETE FROM subscribers WHERE id=%s", (sub_id,))
    conn.commit(); assert cur.rowcount == 1

    # Ensure deleted
    cur.execute("SELECT COUNT(*) FROM subscribers WHERE id=%s", (sub_id,))
    assert cur.fetchone()[0] == 0

    cur.close(); conn.close()
