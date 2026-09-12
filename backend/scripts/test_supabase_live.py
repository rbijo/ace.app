import asyncio
import asyncpg
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


async def main():
    host = "aws-0-ca-central-1.pooler.supabase.com"
    user = "postgres.hpydfcixuvjkecoomhnm"
    password = "Ace@app2026"
    database = "postgres"

    for port in [6543, 5432]:
        try:
            print(f"Connecting to Supabase PostgreSQL at {host}:{port}...")
            conn = await asyncpg.connect(
                user=user,
                password=password,
                database=database,
                host=host,
                port=port,
                ssl=ctx,
                timeout=10
            )
            print("==================================================")
            print(f"🔥 LIVE SUPABASE POSTGRESQL CONNECTED SUCCESS!")
            print("==================================================")
            version = await conn.fetchval("SELECT version();")
            print(f"PostgreSQL Version: {version}")

            # Test creating tables in Supabase PostgreSQL
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS alpha_test_users (
                    id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            print("✔ Verified table creation permissions on Supabase PostgreSQL.")
            await conn.close()
            return
        except Exception as e:
            print(f"Port {port} Connection Result: {e}")


if __name__ == "__main__":
    asyncio.run(main())

