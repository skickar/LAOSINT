## Search by name of a business to find the owner and any health code violations

import requests, json

def QueryServer(facID):
    answers = requests.get('https://data.lacity.org/resource/ckya-qgys.json?facility_id={}'.format(facID))
    violations = json.loads(answers.text)
    for i in range(len(violations)):
        if violations:
            print("Violation Found! Code violation for: {} was reported at this facility on {} ".format(violations[i]['violation_description'], violations[i]['activity_date']))
        else: print("No violations found")

businessName = input("Name of business to search for?\n>")
url = "https://data.lacounty.gov/resource/6ni6-h5kp.json?$where=starts_with(facility_name,%20%27{}%27)".format(businessName.upper())
response = requests.get(url)
matches = json.loads(response.text)

for i in range(len(matches)):
    try:
        print("Match: Facility {} is located at {} and owned by {}. See location: http://www.google.com/maps/place/{},{}".format(matches[i]['facility_name'], matches[i]['facility_address'], matches[i]['owner_name'], matches[i]['geocoded_column']['coordinates'][1], matches[i]['geocoded_column']['coordinates'][0]))
    except KeyError:
        print("Match: Facility {} is located at {} and owned by {}.".format(matches[i]['facility_name'], matches[i]['facility_address'], matches[i]['owner_name']))
    QueryServer(matches[i]['facility_id'])
