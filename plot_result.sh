#!/bin/sh

unamestr="$(uname)"
gmt=/Applications/GMT-5.3.3.app/Contents/Resources/bin/gmt
echo $unamestr
if [ "$unamestr" = 'Linux' ]
then
    gmt=gmt
    #gmt=/opt/gmt/gmt-5.1.1/bin/gmt
    $gmt gmtset DIR_GSHHG=/opt/gmt/gshhg-gmt-2.3.7
fi

$gmt gmtset PS_MEDIA=a2
$gmt gmtset ANNOT_FONT_SIZE_PRIMARY=16p



proj='W0/6i'
step=1.5

layer=$1

$gmt surface ${layer}.xyz -Rd -I${step}d -G${layer}.grd

$gmt makecpt -Chaxby -T0.0/0.1/0.005 > colorbar.cpt

$gmt grdimage ${layer}.grd -Rd -J${proj} -Ccolorbar.cpt -P -K > ${layer}.ps
$gmt pscoast -Rd -J${proj} -Ba90g30f5/a30g30f5WeSn -V -Dc -Wthin -O -K >> ${layer}.ps

$gmt grdimage ${layer}.grd -Rd-180/180/-90/-60 -Js0/-90/7i/30 -Ccolorbar.cpt -Y3.2i  -O -K  >> ${layer}.ps
$gmt pscoast -Rd-180/180/-90/-60 -Js0/-90/7i/30 -Ba90g30f30/wesn -V -Dc -Wthin  -O -K >> ${layer}.ps

$gmt grdimage ${layer}.grd -Rd-180/180/60/90 -Js0/90/2.3i/30 -Ccolorbar.cpt -X3.8i  -O -K  >> ${layer}.ps
$gmt pscoast -Rd-180/180/60/90 -Js0/90/2.3i/30 -Ba90g30f30/wesn -V -Dc -Wthin -O -K >> ${layer}.ps


$gmt psscale -Dx1i/-0.4i+w2.0i/0.5c+ef  -Ccolorbar.cpt -I0 -B0.02:"Susceptibility":/:"SI": -X-2.3i -Y0.5i -O >> ${layer}.ps
$gmt ps2raster -A+r ${layer}.ps

rm colorbar.cpt

rm gmt.history
rm *.ps
rm *.grd
