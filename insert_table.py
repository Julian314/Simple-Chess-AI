from create_connection import create_connection

def insert_table_dataset(conn,input):
    sql = f'INSERT INTO dataset(binary,eval) VALUES(?,?)'
    cur = conn.cursor()
    cur.execute(sql, input)
    conn.commit()

def insert_table_shessgames(conn,input):
    sql = f'INSERT INTO shessgames(fen,binary,white_elo,black_elo,eval) VALUES(?,?,?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, input)
    conn.commit()
