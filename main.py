from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_total_jobs
from exporter import save_to_file

app= Flask("jobScrapper")

DB = {}

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/search")
def search():
  try:
    word = request.args.get('word')
    word = word.lower()
    if word:
      if word in list(DB.keys()):
        total_jobs = DB[word]
      else:
        total_jobs = get_total_jobs(word)
        print(word)
        DB[word] = total_jobs
      return render_template("results.html", word = word, jobs = total_jobs, numOfJobs = len(total_jobs))
    else:
      return redirect("/")
  except:
    return redirect("/")


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = DB[word]
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    redirect("/")

app.run(host="0.0.0.0")
