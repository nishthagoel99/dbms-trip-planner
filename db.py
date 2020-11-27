from flask import Flask, render_template, request
import mysql.connector


def connect():
    conn = mysql.connector.connect(host='localhost', password='root', user='root', database='trip_plan')
    cur = conn.cursor()

    cur.execute("QUERY")
    conn.commit()
    return mysql