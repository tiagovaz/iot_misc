#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Author  : Tiago Bortoletto Vaz <tvaz@riseup.net>
# Updated : Thu Nov  2 22:54:32 UTC 2023

import rrdtool
from datetime import datetime

RRD_FILES = ['fishino_1.rrd', 'fishino_2.rrd', 'airgradient_1.rrd']

def create_graph():
    scales = ('day', 'week', 'month', 'quarter', 'half', 'year')
    resolutions = {'day': '-24hours', 'week':'-7d', 'month':'-30d', 'quarter':'-90d',
  'half':'-6months', 'year':'-1y'}

    for rrd in RRD_FILES:
        for s in scales:
            if rrd == 'airgradient_1.rrd':
                rrdtool.graph(f'{rrd.rsplit(".", 1)[0] + f"-{s}.png"}', \
                               '-w720', '-h140', '-aPNG', \
                               '--start',  f'{resolutions[s]}', \
                               '--end', 'now', \
                               '--slope-mode', \
                               '--font=DEFAULT:10:', \
                               f'--title=AirGradient DIY BASIC', \
                               f'--watermark={datetime.now().replace(microsecond=0)}', \
                               '--lower-limit=0', \
                               '--right-axis=1:0', \
                               '--alt-y-grid', '--rigid', \
                               f'DEF:temp={rrd}:temp:AVERAGE', \
                               f'DEF:humid={rrd}:humid:AVERAGE', \
                               f'DEF:voc={rrd}:voc:AVERAGE', \
                               f'DEF:nox={rrd}:nox:AVERAGE', \
                               f'DEF:pm={rrd}:pm:AVERAGE', \
                               f'DEF:co2={rrd}:co2:AVERAGE', \
                               f'CDEF:co2_calc=co2,0.01,*', \
                               'AREA:pm#00FF00:PM2.5(ug/m)', \
                               'LINE1:humid#FF00FF:Humid. (%)', \
                               'LINE2:temp#0000FF:Temp. (C)', \
                               'LINE4:co2_calc#00FFFF:CO2 (ppm/100)', \
                               'LINE5:voc#ffb91d:VOC (idx)', \
                               'LINE6:nox#c41e3a:NOx (idx)', \
#                               'GPRINT:temp:LAST:\tTempCur\: %5.2lf', \
#                               'GPRINT:temp:AVERAGE:TempAvg\: %5.2lf', \
#                               'GPRINT:temp:MAX:TempMax\: %5.2lf', \
#                               'GPRINT:temp:MIN:TempMin\: %5.2lf\\n', \
#                               'GPRINT:pm:LAST:\t\t\t\t\t\t               PM25Cur\: %5.2lf', \
#                               'GPRINT:pm:AVERAGE:PM25Avg\: %5.2lf', \
#                               'GPRINT:pm:MAX:PM25Max\: %5.2lf', \
#                               'GPRINT:pm:MIN:PM25Min\: %5.2lf\\n', \
#                               'GPRINT:co2_calc:LAST:\t\t\t\t\t\t               CO2Cur\: %5.2lf', \
#                               'GPRINT:co2_calc:AVERAGE: CO2Avg\: %5.2lf', \
#                               'GPRINT:co2_calc:MAX: CO2Max\: %5.2lf', \
#                               'GPRINT:co2_calc:MIN: CO2Min\: %5.2lf\\n', \
                               
                            )
            else:
                rrdtool.graph(f'{rrd.rsplit(".", 1)[0] + f"-{s}.png"}', \
                            '-w720', '-h140', '-aPNG', \
                            '--start',  f'{resolutions[s]}', \
                            '--end', 'now', \
                            '--slope-mode', \
                            '--font=DEFAULT:10:', \
                            f'--title=TEMP & HUMID ({rrd.rsplit(".", 1)[0]})', \
                            f'--watermark={datetime.now().replace(microsecond=0)}', \
                            '--vertical-label=Temp. (C) & Humid. (%)', \
                            '--lower-limit=0', \
                            '--right-axis=1:0', \
                            '--alt-y-grid', '--rigid', \
                            f'DEF:temp={rrd}:temp:AVERAGE', \
                            f'DEF:humid={rrd}:humid:AVERAGE', \
                            'LINE1:humid#FF00FF:Humidity (%)', \
                            'LINE2:temp#0000FF:Temperature (C)', \
                            'GPRINT:temp:LAST:Cur\: %5.2lf', \
                            'GPRINT:temp:AVERAGE:Avg\: %5.2lf', \
                            'GPRINT:temp:MAX:Max\: %5.2lf', \
                            'GPRINT:temp:MIN:Min\: %5.2lf\t\t\t')
                            

if __name__ == '__main__':          
    create_graph()
