from flask import Flask, request, Response, jsonify, abort, render_template
from pymongo import MongoClient
from credentials import username, password
import json
from pprint import pprint

app = Flask(__name__)

# Define your credentials and DBname
client = MongoClient('localhost', 27017)  # Replace with your MongoDB connection details

# Test if connected to the MongoDB Atlas
# print(client.list_database_names())

dbname = 'metrolinx'
db = client[dbname]  # MongoDB database
print(db.list_collection_names())

# assign each collection to a variable

trains = db['trains']
buses = db['buses']
trip_updates = db['trip_updates']
service_messages = db['service_messages']
vechile_position = db['vechile_position']
train_cancelled = db['train_cancelled']
bus_cancelled = db['bus_cancelled']
all_cancelled = db['all_cancelled']

@app.route("/trains")
def get_train_delays():
    pipeline = [
        {
            '$group': {
                '_id': {
                    'FirstStopCode': '$FirstStopCode',
                    'LastStopCode': '$LastStopCode',
                    'Course': '$Course'
                },
                'AverageDelay': {'$avg': '$DelaySeconds'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'FirstStopCode': '$_id.FirstStopCode',
                'LastStopCode': '$_id.LastStopCode',
                'Course': '$_id.Course',
                'AverageDelay': 1
            }
        }
    ]
    result = list(trains.aggregate(pipeline))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)


# # Welcome Page


# @app.route("/")
# def main_page():
#     return render_template('index.html')

# # Mortality Rate by Province
# @app.route("/mortality_rate")
# def mortality_data():
#     collection = db['dataset_1']  # Update with the appropriate collection
#     pipeline = [
#         {
#             "$group": {
#                 "_id": "$Province",
#                 "MortalityRate": {"$max": "$Mortality rate"},
#                 "Date": {"$max": "$Date"}
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "Province": "$_id",
#                 "Mortality rate": "$MortalityRate"
#             }
#         },
#         {
#             "$sort": {
#                 "Mortality rate": 1
#             }
#         }
#     ]
#     results = collection.aggregate(pipeline)
#     results_list = list(results)

#     return jsonify(results_list)


# @app.route("/age")
# def vaccines_ages():
#     collection = db['dataset_4_updated_dataset_2']
#     # Define the grouping pipeline
#     pipeline = [
#         {
#             "$group": {
#                 "_id": "$Age",
#                 "TotalVaccinedose1": {"$max": "$Cumulative number of people (Vaccinedose1)"},
#                 "Date": {"$max": "$Date"}
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "Age": "$_id",
#                 "TotalVaccinedose1": "$TotalVaccinedose1"
#             }
#         },
#         {
#             "$sort": {
#                 "Age": 1
#             }
#         }
#     ]

#     results = collection.aggregate(pipeline)
#     results_list = list(results)
#     return jsonify(results_list)

# # Vaccines based on age and gender


# @app.route("/gender_age")
# def vaccines():
#     query = {}
#     results = dataset_2.find(query)
#     results_list = [convert_object_id(result) for result in results]
#     return jsonify(results_list)


# @app.route("/activecases_perday")
# def activecases_perday():
#     collection = db['dataset_1']
#     pipeline = [
#         {
#             "$project": {
#                 "_id": 0,
#                 "Active Cases per day": 1,
#                 "Province": 1,
#                 "Date": 1
#             }
#         },
#         {
#             "$sort": {
#                 "Date": 1
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$Province",
#                 "data": {
#                     "$push": {
#                         "Date": "$Date",
#                         "Active Cases per day": "$Active Cases per day"
#                     }
#                 }
#             }
#         }
#     ]
#     results = collection.aggregate(pipeline)
#     results_list = list(results)
#     return jsonify(results_list)


# # TARUNA CODE API ROUTES////////////////////////////////////////////////////////////////////////////////////ENDING

# # JIBEK CODE API ROUTES////////////////////////////////////////////////////////////////////////////////STARTS
# # Vaccination per Province
# @app.route("/vaccinated_people_province")
# def vaccine_data():
#     pipeline = [
#         {
#             '$group': {
#                 '_id': '$Province',
#                 'cumm_vaccinated_people': {'$max': '$Cumulative number of people (Vaccinedose1)'},
#                 "Date": {"$max": "$Date"}
#             }
#         },
#         {
#             '$sort': {
#                 'cumm_vaccinated_people': 1,
#             }
#         }
#     ]

#     results = list(dataset_3.aggregate(pipeline))
#     return jsonify(results)

# # Vaccination Data


# @app.route("/vaccines")
# def vaccine_rate():
#     query = {}
#     results = dataset_3.find(query)
#     results_list = [convert_object_id(result) for result in results]

#     return jsonify(results_list)

# # JIBEK CODE API ROUTES////////////////////////////////////////////////////////////////////////////////ENDS

# # RILEY CODE API ROUTE STARTS //////////////////////////////////////////////////////////////////////////


# @app.route("/mortalityrate")
# def mortality():
#     query = {}
#     fields = {'Province': 1, 'Date': 1, 'Mortality rate': 1}
#     results = dataset_1.find(query, fields)
#     results_list = [convert_object_id(result) for result in results]

#     return jsonify(results_list)
# # RILEY CODE API ROUTE ENDS //////////////////////////////////////////////////////////////////////////

# # SHAKHNOZA CODE STARTS /////////////////////////////////////////////////////////////////////////////

# # Confirmed Cases per Day


# @app.route("/daily_cases")
# def daily_confirmed_data():
#     query = {}
#     fields = {'Province': 1, 'Date': 1, 'Confirmed cases per day': 1}
#     results = dataset_1.find(query, fields)
#     output_list = [convert_object_id(result) for result in results]

#     return jsonify(output_list)

# # Cumulative Confirmed by Province


# @app.route("/cumulative_cases_province")
# def confirmed_data():
#     pipeline = [
#         {
#             '$group': {
#                 '_id': '$Province',
#                 'cum_confirmed_cases': {'$max': '$Cumulative confirmed cases'},
#                 'date': {'$max': '$Date'}
#             }
#         },
#         {
#             '$sort': {
#                 'cum_confirmed_cases': 1
#             }
#         }
#     ]

#     results = list(dataset_1.aggregate(pipeline))
#     return jsonify(results)

# # SHAKHNOZA CODE ENDS /////////////////////////////////////////////////////////////////////////////


# def convert_object_id(result):
#     result['_id'] = str(result['_id'])
#     return result


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
