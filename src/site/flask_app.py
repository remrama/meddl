'''
Webpage to log dream reports.

- morning survey is a comprehensive series of 
    questionnaires probing dream characteristics
    from a single sleep session
- quarterly survey is a series of questionnaires
    about general dream characteristics
'''

import time
import json
from flask import Flask, render_template, redirect, request, session, url_for

# create the application object
app = Flask(__name__)

app.secret_key = 'notsosecret'


# use decorators to link the function to a url
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wakeup')
def wakeup():
    # exports to /report
    # reset session variables
    session['counter'] = 0
    session['n_dreams'] = 0
    session['entry'] = {}
    session.modified = True
    return render_template('wakeup.html')

@app.route('/quarterly')
def quarterly():
    return render_template('quarterly.html')

@app.route('/postmed')
def postmed():
    return render_template('postmed.html')

@app.route('/append')
def append():
    return render_template('append.html')

@app.route('/report', methods=['GET','POST'])
def report():
    # exports back to itself, unless it gets redirected (at the end)

    if request.method == 'GET':
        return render_template('report.html', dream_num='TESTING')
    
    elif request.method == 'POST':

        # get the num of dreams if coming from /wakeup form
        if request.form.get('recall_count') is not None:
            # should only have a recall count from the wakeup form
            session['n_dreams'] = int(request.form.get('recall_count'))

        # always save the current data coming in
        session['entry'][session['counter']] = request.form
        session.modified = True

        if session['counter'] < session['n_dreams']:
            # there's another dream to report, do it again
            session['counter'] += 1
            session.modified = True
            # get the next report
            return render_template('report.html',dream_num=session['counter'],dream_total=session['n_dreams'])
        else:
            # all dreams have been reported, so save and end
            return redirect(url_for('export',form='morning'))


@app.route('/export/<form>', methods=['GET','POST'])
def export(form):
    # form type morning comes from GET method
    # others from POST
    if form in ['morning','quarterly','postmed']:
        # save all to json
        outdict = session['entry'] if form=='morning' else request.form
        stamp = time.strftime('%Y%m%d%H%M%S')
        fname = '../../data/{}/{}.txt'.format(form,stamp)
        with open(fname,'w') as outfile:
            json.dump(outdict,outfile)

    elif form == 'append':

        # load in the entry to append
        old_stamp = request.form['stamp2append']
        fname = '../../data/morning/{}.txt'.format(old_stamp)
        with open(fname,'r') as infile:
            old_entry = json.load(infile)

        # append the old json
        # append key values are of the form A1, A2, ..., AN for N appends
        # so add 1 to however many appends already exist
        n_appends = 1 + sum([ 1 for k in old_entry.keys() if 'A' in k ])
        current_stamp = time.strftime('%Y%m%d%H%M%S')
        appendment = {'A{:d}'.format(n_appends):
            dict(append_tstamp=current_stamp,comment=request.form['comment'])}
        old_entry.update(appendment)

        # save the new json out, overwriting the old one
        with open(fname,'w') as outfile:
            json.dump(old_entry,outfile)

    else:
        raise Warning('For some reason the form type wasnt relevant.')

    return render_template('saved.html',form=form,fname=fname)




# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)