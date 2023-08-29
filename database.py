import sqlite3
from dataclasses import dataclass


@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db + '.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL)")
        
    def add(self, note):
        self.cur.execute("INSERT INTO note (title, content) VALUES (?, ?)", (note.title, note.content))
        self.conn.commit()

    def get_all(self):
        self.cur.execute("SELECT id, title, content FROM note")
        rows = self.cur.fetchall()
        return [Note(row[0], row[1], row[2]) for row in rows]
    
    def get_by_id(self, note_id):
        self.cur.execute("SELECT id, title, content FROM note WHERE id = ?", (note_id,))
        row = self.cur.fetchone()
        return Note(row[0], row[1], row[2]) if row else None
    
    def update(self, note):
        self.cur.execute("UPDATE note SET title = ?, content = ? WHERE id = ?", (note.title, note.content, note.id))
        self.conn.commit()
        

    def delete(self, note_id):
        self.cur.execute("DELETE FROM note WHERE id = ?", (note_id,))
        self.conn.commit()