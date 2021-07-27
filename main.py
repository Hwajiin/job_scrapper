import requests
from flask import Flask, render_template, request, redirect, send_file
from bs4 import BeautifulSoup
from we import wework_get_jobs
from remote import remote_get_jobs
from so import so_search
from exporter import save_to_file


app = Flask("jobsearch")

db = {}

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
  if request.method == 'GET':
    term = request.args.get('job')
    if term:
      term = term.lower()
      fromDb = db.get(term)
      if fromDb:
        datalist = fromDb
      else:
        try: 
          wework_datalist = wework_get_jobs(term)
          remote_datalist = remote_get_jobs(term)
          so_datalist = so_search(term)
          datalist = wework_datalist + remote_datalist + so_datalist
          save_to_file(datalist)
          db[term] = datalist
        except:
          error = 'Nothing Found'
          return render_template('home.html', error=error)
    else:
      return redirect('/')
    return render_template('result.html', term = term, datalist = datalist)

@app.route('/export')
def export():
  try:
    term = request.args.get('job')
    if not term:
      raise Exception()
    term = term.lower()
    datalist = db.get(term)
    if not datalist:
      raise Exception()
    save_to_file(datalist)
    return send_file('jobs.csv')
  except:
    return redirect('/')
     

app.run(debug=True, threaded=True)