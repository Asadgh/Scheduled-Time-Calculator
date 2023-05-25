from flask import Flask, render_template, request, jsonify, redirect, make_response, abort, session
import json
import pandas as pd
import re


app = Flask(__name__)
app.secret_key = 'something_secret'

data = pd.read_csv('Health_Facilities.csv')
nests = data['NEST_NAME'].unique().tolist()
nests.sort()

facilities = {}

for nest in nests:
    nests_facilities = data.loc[data['NEST_NAME'] == nest]
    facs = nests_facilities[["DELIVERY_SITE_NAME", 
                             "DELIVERY_SITE_ID",
                             "HEALTH_FACILITY_NAME",
                             "HEALTH_FACILITY_ID",
                             "IS_DIRECT_DELIVERY_SITE"]].sort_values("HEALTH_FACILITY_NAME")
    nest_facs = []
    for row in facs.itertuples():
        if row[-1]:
            nest_facs.append(f'{row[3]}  ({row[4]})')
        else:
            nest_facs.append(f'{row[3]} Via {row[1]}  ({row[4]})')

    facilities[nest] = nest_facs


@app.route('/')
def index():
    return_data = {
        'nests': ['--Select--'] + nests,
        'facilities': facilities
    }
    return render_template('index.html', data=return_data)


@app.route('/api/process', methods=['POST'])
def process_data():
    schedule_data = request.get_json()  # Retrieve the JSON data from the request body

    # Process the data

    selected_nest = schedule_data['nest']
    facility = schedule_data['facility']
    time = schedule_data['time']
    is_multiple = schedule_data['multiple']

    pattern = r'\((.*?)\)'  
    matches = re.findall(pattern, facility)
    facility_id = matches[0]

    nest_data = data[data["NEST_NAME"] == selected_nest]
    matched_row = nest_data[nest_data["HEALTH_FACILITY_ID"] == int(facility_id)]
    
    eta = matched_row["ESTIMATED_TIME_TO_DELIVERY_SITE"]

    schedule_time = pd.Timestamp(time)
    flight_time = pd.Timedelta(seconds=int(eta.iloc[0]))

    window = pd.Timedelta(minutes=15)

    min_window = (schedule_time - window)
    max_window = (schedule_time + window)
    time_to_pack = (min_window - flight_time)

    if is_multiple:
        launch_time = time_to_pack + pd.Timedelta(minutes=10)
    else:
        launch_time = schedule_time - flight_time
    
    hours = flight_time.components.hours
    minutes = flight_time.components.minutes
    seconds = flight_time.components.seconds

    eta_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    pattern2 = r'\([^)]*\)'
    facility_name = re.sub(pattern2, '', facility).strip()

    processed_data = {
        'facility': facility_name,
        'flight_time': eta_string,
        'min_window': min_window.time().strftime("%H:%M:%S"),
        'max_window': max_window.time().strftime("%H:%M:%S"),
        'time_to_pack': time_to_pack.time().strftime("%H:%M:%S"),
        'launch_time': launch_time.time().strftime("%H:%M:%S")
    }

    return jsonify(processed_data) 


if __name__ == '__main__':
    app.run(debug=False)
