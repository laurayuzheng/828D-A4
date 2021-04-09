import csv
import pandas as pd
import pandas.io.sql as psql
import datetime
try:
    import simplejson as json
except ImportError:
    import json
from flask import Flask,request,Response,render_template
import psycopg2 # use this package to work with postgresql
app = Flask(__name__)

# global variables
GLOBAL_BIN_RANGES = []
DATE_RANGES = {"min": "", "max": ""}
DATE_RANGES_WHOLE = {"min": "", "max": ""}
GLOBAL_MIN = -1
GLOBAL_MAX = -1
DB_USERNAME = "cmsc828d"
DB_PASSWORD = "cmsc828d"
DB_NAME = "a2database"
TABLE_NAME = "anime"
GENRE_LIST = ['action', 'adventure', 'cars', 'comedy', 
              'dementia', 'demons', 'drama', 'fantasy', 
              'game', 'harem', 'historical', 'horror', 
              'josei', 'kids', 'magic', 'martial arts', 
              'mecha', 'military', 'music', 'mystery', 
              'parody', 'police', 'psychological', 'romance', 
              'samurai', 'school', 'sci-fi', 'seinen', 
              'shoujo', 'shoujo ai', 'shounen', 'shounen ai', 
              'slice of life', 'space', 'sports', 
              'super power', 'supernatural', 'thriller', 
              'vampire']

@app.route('/')
def renderPage():
  return render_template("index.html")

''' retrieves one record from DB for purposes of getting column name, 
doesn't actually get the whole dataset :) '''
@app.route('/get-data')
def getData():
  print("getting data")
  try:
    # only get 1 record to get column name description
    postgreSQL_select_Query = 'SELECT * FROM ' + TABLE_NAME
    cursor.execute(postgreSQL_select_Query)

    small_df = cursor.fetchall() 
    # print(small_df)
    colnames = [desc[0] for desc in cursor.description]
    data = pd.DataFrame(small_df, columns=colnames) # (3)
    # print(data)
    
    resp = Response(response=data.to_json(orient='records'),status=200, mimetype='application/json')
    h = resp.headers
    h['Access-Control-Allow-Origin'] = "*"
    return resp
  except Exception as err:
    raise err

@app.route('/get-unique-values')
def getUniqueValues():
    try:
        attribute = request.args.get("attribute")
        
        query = "SELECT DISTINCT " + attribute + " FROM " + TABLE_NAME +  \
            " ORDER BY " + attribute + ";"
            
        cursor.execute(query)
        unique_vals = cursor.fetchall()
        # print(unique_vals)
        
        response = json.dumps(unique_vals) # (3)
        resp = Response(response=response, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp
    except Exception as err:
        raise err
        
@app.route('/get-scatter-data')
def getScatterData():
    try:
        x_attribute = request.args.get("xAttribute")
        y_attribute = request.args.get("yAttribute")
        
        query = "SELECT " + x_attribute + "," + y_attribute + " FROM " \
            + TABLE_NAME + " WHERE start_airing <= '" \
            + DATE_RANGES["max"] + "'::date"
        
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        
        if len(result) > 0:
            result = [{"xCoord": float(str(i)),"yCoord": float(str(j))} for i,j in result if str(i) != 'None' and str(i) != 'None']
            
        # print("result: ", result)
        response = json.dumps(result) # (3)
        resp = Response(response=response, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp
    except Exception as err:
        raise err

@app.route('/get-distinct-count')
def getDistinctCount():
    try:
        attribute = request.args.get("attribute")
        
        query = ""
        counts = []
        if attribute == "genres":
            for genre in GENRE_LIST:
                query = "SELECT COUNT(*) FROM " + TABLE_NAME + " WHERE '" \
                    + genre + "'=ANY(genres) AND start_airing <= '" \
                        + DATE_RANGES["max"] + "'::date"
                cursor.execute(query)
                temp = cursor.fetchone()[0]
                print("fetch result: ", temp)
                counts.append({"attr": genre, "count":int(temp)})
            
            counts = sorted(counts, key=lambda item: item["count"], reverse=True)
        else:
            # + " WHERE start_airing <" + DATE_RANGES["max"] \
            query = "SELECT DISTINCT " + attribute + ", SUM(CASE WHEN " \
                + attribute + " IS NOT NULL THEN 1 ELSE 0 END)" + " FROM " \
                    + "(SELECT * FROM " + TABLE_NAME + " WHERE start_airing <= '" + DATE_RANGES["max"] + "'::date) AS daterange" \
                    + " GROUP BY " + attribute + " ORDER BY " + " SUM(CASE WHEN " \
                        + attribute + " IS NOT NULL THEN 1 ELSE 0 END) DESC"
            
            # print(query)
            cursor.execute(query)
            counts = cursor.fetchall()
            counts = [{"attr": key, "count":int(value)} for key,value in counts]
        
        # print(counts)
        
        counts = [c for c in counts if c['attr'] != None and c['attr'] != "-"]
                
        response = json.dumps(counts) 
        resp = Response(response=response, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp
    except Exception as err:
        raise err

''' calculates the bins '''
@app.route('/get-bins')
def getBins():
  try:
    attribute = request.args.get("attribute")

    # create a copy... just in case :)
    binRanges = GLOBAL_BIN_RANGES.copy()

    # building the query
    query = "SELECT count(*) FILTER (WHERE " + \
      attribute + " BETWEEN " + str(binRanges[0]["rangeMin"]) \
        + " AND " + str(binRanges[0]["rangeMax"])

    # include the range slider conditions if it exists
    if GLOBAL_MIN > -1:
      query += " AND " + attribute + " >= " + str(GLOBAL_MIN) 
    
    if GLOBAL_MAX > -1:
      query += " AND " + attribute + " <= " + str(GLOBAL_MAX) 

    query += ")"

    # build the query for the rest of the bin ranges
    # I separated the first part from the rest because of the comma formatting
    for i in range(1, len(binRanges)):
        query += ", count(*) FILTER (WHERE " \
            + attribute + " BETWEEN " + str(binRanges[i]["rangeMin"]) \
            + " AND " + str(binRanges[i]["rangeMax"])

        if GLOBAL_MIN > -1:
          query += " AND " + attribute + " >= " + str(GLOBAL_MIN)
        
        if GLOBAL_MAX > -1:
          query += " AND " + attribute + " <= " + str(GLOBAL_MAX)

        query += ")"

    # finish the query to specify which table
    query += " from " + TABLE_NAME + ";"

    cursor.execute(query) # (4) bin count calculated using Postgres

    # binCounts holds aggregate count of records in each bin according to binRanges
    binCounts = cursor.fetchone()

    response = json.dumps(binCounts) # (3)
    resp = Response(response=response, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

  except Exception as err:
    print(err)
    raise err

''' calculates the bin ranges,
this is done purely in Python and not Postgres  '''
@app.route('/get-binranges')
def getBinRanges():
  try:
    mn = float(request.args.get('mn'))
    mx = float(request.args.get('mx'))
    totalBins = int(request.args.get('totalBins'))

    step = (mx - mn) / totalBins
    binRanges = []
    prev = mn

    for i in range(totalBins):
      binRanges.append({"rangeMin": prev, "rangeMax": prev+step})
      prev += step

    binRanges[len(binRanges) - 1]["rangeMax"] = mx
    global GLOBAL_BIN_RANGES 
    GLOBAL_BIN_RANGES = binRanges

    response = json.dumps(binRanges) # (3) calculated binRanges
    resp = Response(response=response, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

  except Exception as err:
    print(err)
    raise err

''' this method's sole purpose is to update the global variables,
called whenever the range sliders are moved in the visualization '''
@app.route('/update-rangevars')
def updateRangeVars():
  try: 
    minRange = float(request.args.get('minRange'))
    maxRange = float(request.args.get('maxRange'))
    global GLOBAL_MIN
    global GLOBAL_MAX
    GLOBAL_MIN = minRange
    GLOBAL_MAX = maxRange

    response = json.dumps({}) # (3) empty response; just updating variables
    resp = Response(response=response,status=200, mimetype='application/json')
    h = resp.headers
    h['Access-Control-Allow-Origin'] = "*"
    return resp
  except Exception as err:
    print(err)
    raise err

@app.route('/update-timerange')
def updateTimeRange():
    try:
        maxRange = request.args.get('maxRange')
        reset = request.args.get('reset')
        
        print("reset is ", reset)
        if reset == "true":
            # global DATE_RANGES
            # global DATE_RANGES_WHOLE
            # global DATE_RANGES
            DATE_RANGES["max"] = DATE_RANGES_WHOLE["max"]
            
        else:   
            print("Not resetting. Maxrange is ", maxRange)
            maxList = maxRange.split(" ")
            maxList = maxList[:6]
            maxRange = " ".join(maxList)
            
            date_time_obj = datetime.datetime.strptime(maxRange, "%a %b %d %Y %H:%M:%S GMT%z")
            
            # global DATE_RANGES
            # global DATE_RANGES
            DATE_RANGES["max"] = str(date_time_obj.date())
            
            print("max time: ", DATE_RANGES["max"])
            
        print("DATE RANGES CHANGED, MAX NOW ", DATE_RANGES["max"])
        response = json.dumps({}) # (3) empty response; just updating variables
        resp = Response(response=response,status=200, mimetype='application/json')
        h = resp.headers
        h['Access-Control-Allow-Origin'] = "*"
        return resp
        
    except Exception as err:
        print(err)
        raise err

''' calculates the min and max using Postgres '''
@app.route('/get-extrema')
def getExtrema():
  try:
    attribute = request.args.get('attribute')
    query = "select min(" + attribute + ") from " + TABLE_NAME # (4) min
    cursor.execute(query)
    minimum = cursor.fetchall()[0][0]

    query = "select max(" + attribute + ") from " + TABLE_NAME # (4) max
    cursor.execute(query)
    maximum = cursor.fetchall()[0][0]
    
    if attribute == "start_airing":
        global DATE_RANGES
        DATE_RANGES = {"min": str(minimum), "max":str(maximum)}
        
    response = json.dumps({"min": str(minimum), "max":str(maximum)}) # (3) min and max
    resp = Response(response=response,status=200, mimetype='application/json')
    h = resp.headers
    h['Access-Control-Allow-Origin'] = "*"
    return resp
  except Exception as err:
    print(err)
    raise err


'''
FOR A1 THE SERVER MUST:
1) connect to a local version of psycopg2 with user 'cmsc828d' and database 'a1database'
2) only fetch data from postgresql (you cannot just work with the raw data file using this server.py file)
3) only return aggregated data (you cannot just return the full dataset from postgresql to index.html)
4) The data must be filtered and aggregated using postgresql. This means you have to compute the bins and bin counts using postgresql.
Note: it is fine if you decide to calculate the bins outside of postgresql. But the extrema of the dataset (minimum, maximum) and actual bin counts must be calculated using postgresql.
'''

if __name__ == "__main__":

  # (1)
  try: 
    
    print("connecting to postgresql database.. ")
    conn = psycopg2.connect(
      host="localhost",
      database=DB_NAME,
      user=DB_USERNAME, 
      password=DB_PASSWORD)
    conn.set_client_encoding('UTF8')
    cursor = conn.cursor()
    
    query = "select max(start_airing) from " + TABLE_NAME # (4) max
    cursor.execute(query)
    maximum = cursor.fetchall()[0][0]
    # print(maximum)
    
    DATE_RANGES_WHOLE["max"] = str(maximum)
    DATE_RANGES["max"] = str(maximum)
    
  except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)


  app.run(debug=True,port=8000)
