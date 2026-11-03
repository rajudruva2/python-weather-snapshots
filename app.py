import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI(title="Weather Snapshots")
class Snapshot(BaseModel):
 city:str
 temperature_c:float
 condition:str
with sqlite3.connect("weather.db") as c:c.execute("CREATE TABLE IF NOT EXISTS snapshots(id INTEGER PRIMARY KEY,city TEXT,temp REAL,condition TEXT)")
@app.get("/health")
def health():return {"status":"ok"}
@app.get("/snapshots")
def list_snapshots():
 with sqlite3.connect("weather.db") as c: rows=c.execute("SELECT id,city,temp,condition FROM snapshots ORDER BY id DESC").fetchall()
 return [{"id":r[0],"city":r[1],"temperature_c":r[2],"condition":r[3]} for r in rows]
@app.post("/snapshots",status_code=201)
def add_snapshot(s:Snapshot):
 with sqlite3.connect("weather.db") as c:
  cur=c.execute("INSERT INTO snapshots(city,temp,condition) VALUES(?,?,?)",(s.city,s.temperature_c,s.condition))
  return {"id":cur.lastrowid,**s.model_dump()}
