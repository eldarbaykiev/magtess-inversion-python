import gmi_misc
import gmi_config

import numpy as np
import math
import os

gmi_config.read_config()

import matplotlib.pyplot as plt


def _trunc_fn(fn):
	return fn[0:len(fn)-4]

def _ident_pont_pos(fl):
	if fl <= 1:
		return int(math.log10(round(1/fl)))+1
	else:
		return -int(math.log10(round(fl)))+1

def plot_global_grid(grid_array, name, minv, maxv, cs, text_val, text_unit):
	if minv > maxv:
		gmi_misc.warning('minv IS BIGGER THAN maxv, swapping')
		return
	
	actual_maxv = grid_array.flatten().max()
	actual_minv = grid_array.flatten().min()

	lat_N = len(grid_array[:, 0])
	lon_N = len(grid_array[0, :])
	
	tempfname = 'temp.xyz'
	
	with open(tempfname, 'w') as tempf:
		for i in range(0, lon_N):
			for j in range(0, lat_N):
				tempf.write(str(0.0+i*360.0/float(lon_N)) + ' ' +  str(90.0-j*180.0/float(lat_N)) + ' ' + str(grid_array[j, i]) + '\n')		
	
	lon_step = 360.0 / float(lon_N)
	lat_step = 180.0 / float(lat_N)
				
	gmt_command = 'gmt'
	import platform
	gmi_misc.info('Operating system: ' + platform.system())
	if platform.system() == "Linux":
		gmt_command = 'gmt'
	elif platform.system() == "Darwin":
		gmt_command = '/Applications/GMT-5.3.3.app/Contents/Resources/bin/gmt'
	else:
		pass
		
	
	def gmt(com):
		cmd = gmt_command + ' ' + com + '\n'
		gmi_misc.info(cmd)
		os.system(cmd)
		return
	
	gmt('gmtset PS_MEDIA=a2')
	gmt('gmtset ANNOT_FONT_SIZE_PRIMARY=14p')
	
	if cs == 'polar':
		gmt('gmtset COLOR_BACKGROUND=blue')
		gmt('gmtset COLOR_FOREGROUND=red')
		
	elif cs == 'haxby':
		gmt('gmtset COLOR_BACKGROUND=black')
		gmt('gmtset COLOR_FOREGROUND=white')
	else:
		pass
		
	proj='W0/6i'
	
	cticks = 6
	
	gmt('nearneighbor {} -Rd -I{}d -S{}d -G{}.grd'.format(tempfname, np.minimum(lon_step, lat_step), 2.0*np.minimum(lon_step, lat_step), _trunc_fn(tempfname)) )
	
	diff = abs(maxv-minv)
	i = _ident_pont_pos(diff)
	cstep = 0.5*float((int(diff * 10.0**i) // cticks)) * 10.0**(-i)
	tstep = cstep*2.0
	
	gmt('makecpt -C{} -T{}/{}/{} > {}.cpt'.format(cs, minv, maxv, cstep, _trunc_fn(tempfname)))
	gmt('grdimage {}.grd -Rd -J{} -C{}.cpt -P -K > {}.ps'.format(_trunc_fn(tempfname), proj ,_trunc_fn(tempfname), _trunc_fn(tempfname)) )
	gmt('pscoast -Rd -J{} -Ba90g30f5/a30g30f5WeSn -V -Dc -Wthin -O -K >> {}.ps'.format( proj , _trunc_fn(tempfname)))
	
	gmt('grdimage {}.grd -Rd-180/180/-90/-60 -Js0/-90/7i/30 -C{}.cpt -Y3.2i  -O -K  >> {}.ps'.format(_trunc_fn(tempfname), _trunc_fn(tempfname), _trunc_fn(tempfname)) )
	gmt('pscoast -Rd-180/180/-90/-60 -Js0/-90/7i/30 -Ba90g30f5/a30g30f5WeSn -V -Dc -Wthin -O -K >> {}.ps'.format(_trunc_fn(tempfname)))
	
	gmt('grdimage {}.grd -Rd-180/180/60/90 -Js0/90/2.3i/30 -C{}.cpt -X3.8i  -O -K  >> {}.ps'.format(_trunc_fn(tempfname), _trunc_fn(tempfname), _trunc_fn(tempfname)) )
	gmt('pscoast -Rd-180/180/60/90 -Js0/90/2.3i/30 -Ba90g30f5/a30g30f5WeSn -V -Dc -Wthin -O -K >> {}.ps'.format(_trunc_fn(tempfname)))
	
	fb_add = ''
	if ((actual_minv < minv) or (actual_maxv > maxv)):
		fb_add = '+e'
		if actual_minv < minv:
			fb_add = fb_add + 'b'
		if actual_maxv > maxv:
			fb_add = fb_add + 'f'
		
		
	gmt('psscale -Dx1i/-0.4i+w2.0i/0.5c{}  -C{}.cpt -I0 -B{}:"{}":/:"{}": -X-2.3i -Y0.5i -O >> {}.ps'.format(fb_add, _trunc_fn(tempfname), tstep, text_val, text_unit, (_trunc_fn(tempfname))))
	gmt('ps2raster -A+r {}.ps'.format(_trunc_fn(tempfname)))
	
	import matplotlib.image as mpimg
	img=mpimg.imread(_trunc_fn(tempfname) + '.jpg')
	imgplot = plt.imshow(img)
	plt.show()
	
	
	
