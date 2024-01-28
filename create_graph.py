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
                               '-w820', '-h180', '-aPNG', \
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
                               f'CDEF:voc_calc=voc,0.1,*', \
                               'AREA:pm#ffd700:PM2.5(ug/m)', \
                               'LINE2:humid#FF00FF:Humid. (%)', \
                               'LINE2:temp#0000FF:Temp. (C)', \
                               'LINE2:co2_calc#FF0000:CO2 (ppm/100)', \
                               'LINE2:voc_calc#20b2aa:VOC (idx/10)', \
                               'LINE2:nox#654321:NOx (idx)', \
                               'COMMENT:                 ', \
                               'GPRINT:pm:LAST:CUR\: PM2.5\: %3.0lfug/m', \
                               'GPRINT:humid:LAST:Humid\: %2.1lf%%', \
                               'GPRINT:temp:LAST:Temp\: %2.1lfC', \
                               'GPRINT:co2:LAST:CO2\: %4.0lfppm', \
                               'GPRINT:voc:LAST:VOC\: %3.0lf', \
                               'GPRINT:nox:LAST:NOx\: %3.0lf', \
                               'COMMENT:                 ', \
                               'GPRINT:pm:MIN:MIN\: PM2.5\: %3.0lfug/m', \
                               'GPRINT:humid:MIN:Humid\: %2.1lf%%', \
                               'GPRINT:temp:MIN:Temp\: %2.1lfC', \
                               'GPRINT:co2:MIN:CO2\: %4.0lfppm', \
                               'GPRINT:voc:MIN:VOC\: %3.0lf', \
                               'GPRINT:nox:MIN:NOx\: %3.0lf', \
                               'COMMENT:                 ', \
                               'GPRINT:pm:MAX:MAX\: PM2.5\: %3.0lfug/m', \
                               'GPRINT:humid:MAX:Humid\: %2.1lf%%', \
                               'GPRINT:temp:MAX:Temp\: %2.1lfC', \
                               'GPRINT:co2:MAX:CO2\: %4.0lfppm', \
                               'GPRINT:voc:MAX:VOC\: %3.0lf', \
                               'GPRINT:nox:MAX:NOx\: %3.0lf', \
                               'COMMENT:                 ', \
                               'GPRINT:pm:AVERAGE:AVG\: PM2.5\: %3.0lfug/m', \
                               'GPRINT:humid:AVERAGE:Humid\: %2.1lf%%', \
                               'GPRINT:temp:AVERAGE:Temp\: %2.1lfC', \
                               'GPRINT:co2:AVERAGE:CO2\: %4.0lfppm', \
                               'GPRINT:voc:AVERAGE:VOC\: %3.0lf', \
                               'GPRINT:nox:MAX:NOx\: %3.0lf', \
                               'COMMENT:                 ', \
                            )
            else:
                rrdtool.graph(f'{rrd.rsplit(".", 1)[0] + f"-{s}.png"}', \
                            '-w820', '-h180', '-aPNG', \
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
                            'LINE2:humid#FF00FF:Humidity (%)', \
                            'LINE2:temp#0000FF:Temperature (C)', \
                            'GPRINT:temp:LAST:Cur\: %5.2lf', \
                            'GPRINT:temp:AVERAGE:Avg\: %5.2lf', \
                            'GPRINT:temp:MAX:Max\: %5.2lf', \
                            'GPRINT:temp:MIN:Min\: %5.2lf\t\t\t')
                            

if __name__ == '__main__':          
    create_graph()
