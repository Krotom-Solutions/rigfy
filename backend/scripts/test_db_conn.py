import asyncio, asyncpg
from urllib.parse import quote_plus

async def main():
    print("Testando conexao Supabase...")
    try:
        conn = await asyncpg.connect(
            host='aws-1-sa-east-1.pooler.supabase.com',
            port=5432,
            user='postgres.zoxzmbsuzycskzdfdspk',
            password='#@Rigfy2026#@',
            database='postgres',
            ssl='require',
            timeout=15,
        )
        version = await conn.fetchval('SELECT version()')
        tables = await conn.fetchval(
            "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'"
        )
        print(f'OK - PostgreSQL: {version[:60]}')
        print(f'Tabelas publicas: {tables}')
        await conn.close()
        pwd = quote_plus('#@Rigfy2026#@')
        print(f'\nURL correta para .env:')
        print(f'DATABASE_URL=postgresql+asyncpg://postgres.zoxzmbsuzycskzdfdspk:{pwd}@aws-1-sa-east-1.pooler.supabase.com:5432/postgres?ssl=require')
    except Exception as e:
        print(f'ERRO: {type(e).__name__}: {e}')

asyncio.run(main())
