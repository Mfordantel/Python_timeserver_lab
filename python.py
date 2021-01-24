import json
from tzlocal import get_localzone
from datetime import datetime
from pytz import timezone
from paste.httpserver import serve


def time_server(environ, start_response):

    #Method GET

    if environ['REQUEST_METHOD'] == 'GET':
        getTZ = environ['PATH_INFO'][1:]
        if not getTZ:
            getTZ = None
            text = 'Time - '
        else:
            try:
                getTZ = timezone(getTZ)
                text = 'Time in %s - ' % getTZ
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'Error: Unknown Time Zone']

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [bytes(text + datetime.now(getTZ).strftime('%H:%M:%S'), encoding='utf-8')]

    #Method POST

    elif environ['REQUEST_METHOD'] == 'POST':
        data = environ['wsgi.input'].read().decode("utf-8")
        data = json.loads(data)
        try:
            timezone1 = timezone(data['tz_start'])
        except KeyError:
            timezone1 = get_localzone()
        try:
            timezone2 = timezone(data['tz_end'])
        except KeyError:
            timezone2 = get_localzone()
        try:
            type = data['type']
        except:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes('Error in type Data', encoding='utf-8')]
        time_now = datetime.now(timezone1)
        tz1 = datetime.now(timezone1).utcoffset()
        tz2 = datetime.now(timezone2).utcoffset()
        if tz1 < tz2:
            dif = tz2 - tz1
        else:
            dif = '-' + str(tz1 - tz2)
        dif = str(dif)
        if data['type'] == 'time':
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes(json.dumps({'time': datetime.now(timezone1).strftime('%H:%M:%S'), 'timezone': str(timezone1)}), encoding='utf-8')]
        elif data['type'] == 'date':
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes(json.dumps({'date': datetime.now(timezone1).strftime('%d.%m.%Y'), 'timezone': str(timezone1)}), encoding='utf-8')]
        elif data['type'] == 'datedif':
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes(json.dumps({'time_diff': dif, 'timezone1': str(timezone1), 'timezone2': str(timezone2)}), encoding='utf-8')]


serve(time_server)


