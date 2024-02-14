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
                               'COMMENT:----------------------------------------------------------------------------------------------------------------------', \
                               'COMMENT:                 CUR                     MIN                     MAX                      AVG', \
                               'COMMENT:----------------------------------------------------------------------------------------------------------------------', \
                               'AREA:pm#ffd700:PM2.5(ug/m)', \
                               'GPRINT:pm:LAST:%4.0lf', \
                               'GPRINT:pm:MIN:%22.0lf', \
                               'GPRINT:pm:MAX:%22.0lf', \
                               'GPRINT:pm:AVERAGE:%22.0lf                        ', \
                               'LINE2:humid#FF00FF:Humid. (%) ', \
                               'GPRINT:humid:LAST:%4.1lf', \
                               'GPRINT:humid:MIN:%22.1lf', \
                               'GPRINT:humid:MAX:%22.1lf', \
                               'GPRINT:humid:AVERAGE:%22.0lf                        ', \
                               'LINE2:temp#0000FF:Temp. (C)  ', \
                               'GPRINT:temp:LAST:%4.1lf', \
                               'GPRINT:temp:MIN:%22.1lf', \
                               'GPRINT:temp:MAX:%22.1lf', \
                               'GPRINT:temp:AVERAGE:%22.0lf                        ', \
                               'LINE2:co2_calc#FF0000:CO2 ppm/100', \
                               'GPRINT:co2_calc:LAST:%4.1lf', \
                               'GPRINT:co2_calc:MIN:%22.1lf', \
                               'GPRINT:co2_calc:MAX:%22.1lf', \
                               'GPRINT:co2_calc:AVERAGE:%22.0lf                        ', \
                               'LINE2:voc_calc#20b2aa:VOC(idx/10)', \
                               'GPRINT:voc:LAST:%4.0lf', \
                               'GPRINT:voc:MIN:%22.0lf', \
                               'GPRINT:voc:MAX:%22.0lf', \
                               'GPRINT:voc:AVERAGE:%22.0lf                        ', \
                               'LINE2:nox#654321:NOx (idx)  ', \
                               'GPRINT:nox:LAST:%4.0lf', \
                               'GPRINT:nox:MIN:%22.0lf', \
                               'GPRINT:nox:MAX:%22.0lf', \
                               'GPRINT:nox:AVERAGE:%22.0lf                        ', \
                               'COMMENT:----------------------------------------------------------------------------------------------------------------------', \
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
