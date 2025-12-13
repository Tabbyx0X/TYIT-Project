import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing Supabase Connection...")
print("\n1. Environment Variables:")
print(f"   DATABASE_URL: {os.getenv('DATABASE_URL')[:50]}...")

print("\n2. Testing DNS resolution...")
import socket
try:
    host = "db.oulecxwugqecpbhfqmki.supabase.co"
    ip = socket.gethostbyname(host)
    print(f"   ✅ DNS resolved: {host} -> {ip}")
except Exception as e:
    print(f"   ❌ DNS failed: {e}")
    print("\n🔧 Possible fixes:")
    print("   - Check your internet connection")
    print("   - Try flushing DNS: ipconfig /flushdns")
    print("   - Try using Google DNS (8.8.8.8)")
    print("   - Check if you're behind a firewall/proxy")
    exit(1)

print("\n3. Testing PostgreSQL connection...")
try:
    import psycopg2
    from urllib.parse import urlparse
    
    url = os.getenv('DATABASE_URL')
    parsed = urlparse(url)
    
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password,
        connect_timeout=10
    )
    
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    print(f"   ✅ Connected successfully!")
    print(f"   PostgreSQL version: {version[0][:50]}...")
    
    cursor.close()
    conn.close()
    
    print("\n✅ All tests passed! Ready to initialize database.")
    print("\nRun: python init_supabase_db.py")
    
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    print("\n🔧 Troubleshooting:")
    print("   1. Verify your Supabase password is correct")
    print("   2. Check if your Supabase project is active")
    print("   3. Try resetting your database password in Supabase")
    print("   4. Ensure your IP is not blocked")
