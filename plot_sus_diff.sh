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



proj='N0/6i'
step=1.5

layer=x0_apriori

$gmt surface ${layer}.xyz -Rd -I${step}d -G${layer}.grd

layer=model_reslt_sh

$gmt surface ${layer}.xyz -Rd -I${step}d -G${layer}.grd


$gmt grdmath x0_apriori.grd model_reslt_sh.grd SUB = sus_difference.grd

layer=sus_difference

$gmt makecpt -Chaxby -T-0.04/0.04/0.01 > colorbar.cpt

$gmt grdimage ${layer}.grd -Rd -J${proj} -Ccolorbar.cpt -P -K > ${layer}.ps
$gmt pscoast -Dl -Rd -J${proj} -Ba90g30f5/a30g30f5wesn -V -Dc -Wthick -O -K >> ${layer}.ps

$gmt psscale -Dx1i/-0.4i+w4i/0.5c+h  -Ccolorbar.cpt -I0 -B0.02:"Difference":/:"SI": -O >> ${layer}.ps
$gmt ps2raster -A+r ${layer}.ps

rm colorbar.cpt

rm gmt.history
rm *.ps
rm *.grd
