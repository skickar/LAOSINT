import requests, json

def menu1():
    print("Welcome to LAOSINT: OSINT Data From The City of Los Angeles. \nPlease select an option from the list below:\n")
    searchType = input("1) Find the owner of a restaurant, bar or cafe (Restaurant and Market Health Inspection Records) \n2) Find health code violations for a restaurant, bar or cafe (Restaurant and Market Health Violations Records)\n3) Search list of active businesses (Listing of Active Businesses)\n>")
    try:
        selected = int(searchType)
        if selected == 1:
            return "https://data.lacounty.gov/resource/6ni6-h5kp.json?"
        if selected == 2:
            return "https://data.lacity.org/resource/ckya-qgys.json?"
        if selected == 3:
            return "https://data.lacity.org/resource/6rrh-rzua.json?"
    except ValueError:
        print("Bad selection, must pick a number. Try again."), menu1()

def searchBy():
    queryType = input("How would you like to search?\n\n1) Search by business name\n2) Search by owner name\n3) Search by address\n4) Search by facility ID\n5) Search by date\n6) Search by violation code\n>")
    try:
        selected = int(queryType)
        if selected == 1:
            return "facility_name"
        if selected == 2:
            return "owner_name"
        if selected == 3:
            return "facility_address"
        if selected == 4:
            return "facility_id"
        if selected == 5:
            return "activity_date"
        if selected == 6:
            return "violation_code"
    except ValueError:
        print("Bad selection, must pick a number. Try again."), searchBy()

def searchTerm():
    return input('Enter term to search for:\n>')

def parseResults(matches, mainURL):
    if mainURL == 'https://data.lacounty.gov/resource/6ni6-h5kp.json?':
        for i in range(len(matches)):
            try:
                print(
                    "Match: Facility {} is located at {} and owned by {}. See location: http://www.google.com/maps/place/{},{}".format(
                        matches[i]['facility_name'], matches[i]['facility_address'], matches[i]['owner_name'],
                        matches[i]['geocoded_column']['coordinates'][1],
                        matches[i]['geocoded_column']['coordinates'][0]))
            except KeyError:
                print("Match: Facility {} is located at {} and owned by {}.".format(matches[i]['facility_name'],
                                                                                    matches[i]['facility_address'],
                                                                                    matches[i]['owner_name']))
    if mainURL == 'https://data.lacity.org/resource/ckya-qgys.json?':
        violations = matches
        for i in range(len(violations)):
            if violations:
                try: print("Violation Found! Code violation of: {} was reported at this facility on {}\nAddress of location: {}, owned by {}\nSee location here:  See location: http://www.google.com/maps/place/{},{}".format(
                    violations[i]['violation_description'], violations[i]['activity_date'], violations[i]['facility_address'], violations[i]['owner_name'], violations[i]['geocoded_column']['coordinates'][1], violations[i]['geocoded_column']['coordinates'][0]))
                except KeyError: print("Violation Found! Code violation of: {} was reported at this facility on {}\nAddress of location: {}, owned by {}\n".format(
                    violations[i]['violation_description'], violations[i]['activity_date'], violations[i]['facility_address'], violations[i]['owner_name']))
            else:
                print("No violations found")
    if mainURL == 'https://data.lacity.org/resource/6rrh-rzua.json?':
        for i in range(len(matches)):
            if matches:
                try: print(
                    "Match: Facility {} is located at {} and owned by {}. See location: http://www.google.com/maps/place/{},{}".format(
                        matches[i]['business_name'], matches[i]['street_address'], matches[i]['primary_naics_description'],
                        matches[i]['geocoded_column']['coordinates'][1],
                        matches[i]['geocoded_column']['coordinates'][0]))
                except KeyError:
                    print("Match: Facility {} is located at {} and owned by {}.".format(matches[i]['primary_naics_description'],
                                                                                    matches[i]['primary_naics_description'],
                                                                                    matches[i]['primary_naics_description']))


mainURL = menu1()
filterType = searchBy()
searchField = searchTerm()
url = "{}$where=starts_with({},%20%27{}%27)".format(mainURL, filterType, searchField.upper())
response = requests.get(url)
matches = json.loads(response.text)
parseResults(matches, mainURL)
