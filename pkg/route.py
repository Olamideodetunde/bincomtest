from pkg import app,db
from pkg.models import Party,Announced_lga_results,Polling_unit,Announced_pu_results,Lga
from flask import render_template,request,jsonify
@app.route('/')
def home():
  list_of_party=db.session.query(Party).all()
  results=db.session.query(Announced_lga_results).all()
  return render_template('index.html',list_of_party=list_of_party,results=results)
@app.route('/all-results')
def all_results():
  list_of_polling=db.session.query(Polling_unit).all()
  return render_template('all_results.html',list_of_polling=list_of_polling)
@app.route('/unit-result/<id>')
def indivi_results(id):
  unit=db.session.query(Polling_unit).filter(Polling_unit.uniqueid==id).first()
  inresults=db.session.query(Announced_pu_results).filter(Announced_pu_results.polling_unit_uniqueid==id).all()
  return render_template('indivi_results.html',inresults=inresults,unit=unit)
@app.route('/all_lga',methods=['POST','GET'])
def all_lga():
  if request.method=='GET':
    list_of_lga=db.session.query(Lga).all()
    return render_template('all_lga.html',list_of_lga=list_of_lga)
  else:
    lga=request.form.get('lga')
    all_poll=db.session.query(Polling_unit,Announced_pu_results).join(Announced_pu_results).filter(Polling_unit.lga_id==lga).all()
    response=''
    counter=1
    for x,y in all_poll:
      response=f'''<tr>
                <td>{counter}</td>
                <th>{y.party_abbreviation}</th>
                <th>{y.party_score}</th>
                <th>{x.lgadeets.lga_name}</th>
              </tr>
                '''
      counter+=1
    return response