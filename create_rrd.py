import rrdtool

def create_rrd():
    # DS:ds-name:DST:heartbeat:min:max
    #
    # - DS = Data Source
    # - dns-name = a name describing the contents of the data source
    # - DST = Data Source Type (GAUGE, COUNTER, DERIVE, ABSOLUTE)
    # - heartbeat = the maximum number of seconds that may pass between two
    #   updates of this data source before the value of the data source is
    #   assumed to be *UNKNOWN* (usually steps*2) 

    # RRA:CF:xff:steps:rows
    #
    # - RRA = Round Robin Archive
    # - CF = Consolidation Function
    # - xff = xfiles factor (always 0.5)
    # - steps = the 'resolution' of an archive
    # - rows = the time span an archive can hold
    #   - get it by dividing the wanted time span with the resolution
    #    Example: 12 hours with 15-minute resolution
    #        12 hours in seconds: 60*60*12 = 43200 seconds
    #        15 minutes in seconds: 60*15 = 900 seconds
    #        43200/900 = 48
    #
    # With a step size of 300 seconds, one day equals 288 steps (300s * 288 = 86400s = 1440min = 24h).
    # Nicely expalined at https://apfelboymchen.net/gnu/rrd/create/

    # FISHINO 1 DHT11
    rrdtool.create('fishino_1.rrd', '--step', '300',
        'DS:temp:GAUGE:600:-20:100',
        'DS:humid:GAUGE:600:0:100',
        'RRA:MAX:0.5:1:288', # 1 day, 5min resolution
        'RRA:AVERAGE:0.5:3:672', # 7 days, 15min resolution (7 * 288 / 3) -- why 3? because 5min step * 3 = 15min
        'RRA:AVERAGE:0.5:12:720', # 30 days, 1h resolution (30 * 288 / 12)
        'RRA:AVERAGE:0.5:24:2160', # 180 days, 2h resolution (180 * 288 / 24)
        'RRA:AVERAGE:0.5:36:2920', # 365 days, 3h resolution (365 * 288 / 36)
        'RRA:AVERAGE:0.5:72:16000') # 4000 days (over 10 years), 6h resolution (4000 * 288 / 72)

    # FISHINO 2 DHT11
    rrdtool.create('fishino_2.rrd', '--step', '300',
        'DS:temp:GAUGE:600:-20:100',
        'DS:humid:GAUGE:600:0:100',
        'RRA:MAX:0.5:1:288', # 1 day, 5min resolution
        'RRA:AVERAGE:0.5:3:672', # 7 days, 15min resolution (7 * 288 / 3) -- why 3? because 5min step * 3 = 15min
        'RRA:AVERAGE:0.5:12:720', # 30 days, 1h resolution (30 * 288 / 12)
        'RRA:AVERAGE:0.5:24:2160', # 180 days, 2h resolution (180 * 288 / 24)
        'RRA:AVERAGE:0.5:36:2920', # 365 days, 3h resolution (365 * 288 / 36)
        'RRA:AVERAGE:0.5:72:16000') # 4000 days (over 10 years), 6h resolution (4000 * 288 / 72)

    # AIGRADIENT 1
    rrdtool.create('airgradient_1.rrd', '--step', '300',
        'DS:temp:GAUGE:600:-20:100',
        'DS:humid:GAUGE:600:0:100',
        'DS:co2:GAUGE:600:0:5000',
        'DS:pm:GAUGE:600:0:500',
        'RRA:MAX:0.5:1:288', # 1 day, 5min resolution
        'RRA:AVERAGE:0.5:3:672', # 7 days, 15min resolution (7 * 288 / 3) -- why 3? because 5min step * 3 = 15min
        'RRA:AVERAGE:0.5:12:720', # 30 days, 1h resolution (30 * 288 / 12)
        'RRA:AVERAGE:0.5:24:2160', # 180 days, 2h resolution (180 * 288 / 24)
        'RRA:AVERAGE:0.5:36:2920', # 365 days, 3h resolution (365 * 288 / 36)
        'RRA:AVERAGE:0.5:72:16000') # 4000 days (over 10 years), 6h resolution (4000 * 288 / 72)

if __name__ == '__main__':
    create_rrd()
