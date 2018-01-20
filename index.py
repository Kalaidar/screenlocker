
# coding: utf-8

import MySQLdb
import sys
import datetime

def printer(list, color, legend, output):
    for minion in list:
        minionName = str(minion[0])
        print(minionName)
        minionTimestamp = str(minion[1])
        output += "<tr><td><p id=\""+color+"\">" + minionName + "</p></td><td><p id=\""+color+"\">" + minionTimestamp + "</p></td>"
        if legend != []:
            output += legend.pop(0) + "</tr>\n"
        else:
            output += "<td></td><td></td></tr>\n"
    return(output)

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    try:
        db = MySQLdb.connect(host="localhost", user="salter", passwd="maBLDw9hMddCCUVjb1mN", db="salter", charset='utf8')
    except:
        sys.exit("Cannot connect to mysql")
    dbc = db.cursor()

    request = "SELECT * FROM minions WHERE seen_timestamp <= (NOW() - INTERVAL 6 DAY) OR seen_timestamp IS NULL ORDER BY minion_name"
    dbc.execute(request)
    resultRed = dbc.fetchall()
    lostCount = len(resultRed)

    request = "SELECT * FROM minions WHERE seen_timestamp > (NOW() - INTERVAL 6 DAY) AND seen_timestamp < (NOW() - INTERVAL 1 DAY) ORDER BY minion_name"
    dbc.execute(request)
    resultYellow = dbc.fetchall()

    request = "SELECT * FROM minions WHERE seen_timestamp >= (NOW() - INTERVAL 1 DAY) ORDER BY minion_name"
    dbc.execute(request)
    resultGreen = dbc.fetchall()

    totalCount = len(resultRed) + len (resultYellow) + len(resultGreen)
    global legend

    legend = [ "<td width=\"100\"></td><td width=\"500\"><p id=\"green\">Отзывался не больше 24 часов назад</p></td>",
        "<td width=\"100\"></td><td width=\"500\"><p id=\"yellow\">Отзывался 1-7 дней назад</p></td>",
        "<td width=\"100\"></td><td width=\"500\"><p id=\"red\">Отзывался больше недели назад (" + str(lostCount) + ")</p></td>",
        "<td width=\"100\"></td><td width=\"500\"><p id=\"grey\">Всего " + str(totalCount) + "</p></td>" ]

    output = "<html><head><meta charset=\"utf-8\"><title>Salter</title>\n \
        <style>#red { background-color: lightsalmon; font-family: arial; font-weight: bold; }</style>\n \
        <style>#green{ background-color: darkseagreen; font-family: arial; font-weight: bold; }</style>\n \
        <style>#yellow{ background-color: palegoldenrod; font-family: arial; font-weight: bold; }</style>\n \
        <style>#grey{ background-color: lightgrey; font-family: arial; font-weight: bold; }</style>\n \
	</head><body><table>\n \
        <tr><td><p id=\"grey\">УЗЕЛ</p></td><td><p id=\"grey\">ПОСЛЕДНИЙ ОТВЕТ</p></td><td id=\"grey\"></td><td><p id=\"grey\">ЛЕГЕНДА</p></td></tr>\n"

    output = printer(resultRed, "red", legend, output)
    output = printer(resultYellow, "yellow", legend, output)
    output = printer(resultGreen, "green", legend, output)
    
    output += "</table></body></html>"

    byteOutput = str.encode(output)
    return(byteOutput)

#print(application(1,2))

