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
$gmt gmtset COLOR_BACKGROUND=blue
$gmt gmtset COLOR_FOREGROUND=red

proj='W0/6i'
step=1.5

layer1=$1
layer2=$2
layer=$3

$gmt surface ${layer1}.xyz -Rd -I${step}d -G${layer1}.grd
$gmt surface ${layer2}.xyz -Rd -I${step}d -G${layer2}.grd
$gmt grdmath ${layer1}.grd ${layer2}.grd SUB = ${layer}.grd

$gmt grdinfo ${layer}.grd -T | grep -Eo '[+-]?[0-9]+([.][0-9]+)?' > grdinfo.log
GRDMIN=$(sed -n '1p' grdinfo.log)
GRDMAX=$(sed -n '2p' grdinfo.log)
myvar=$(echo "scale=2;(- $GRDMIN + $GRDMAX)/10.0" | bc)
myvar2=$(awk "BEGIN {printf \"%1.1f\", $myvar}")
myvar3=$(awk "BEGIN {printf \"%1.1f\", $myvar*2.0}")


echo ${GRDMIN}
echo ${GRDMAX}
echo ${myvar2}

if [ $4 -eq 1 ]
then
	$gmt grd2cpt ${layer}.grd -Cpolar -T= > colorbar.cpt
else
	$gmt grd2cpt ${layer}.grd -Cpolar -T=//${myvar2} > colorbar.cpt
	#$gmt makecpt -Chaxby -T-3/3/0.5> colorbar.cpt
fi

$gmt grdimage ${layer}.grd -Rd -J${proj} -Ccolorbar.cpt -P -K > ${layer}.ps
$gmt pscoast -Dl -Rd -J${proj} -Ba90g30f5/a30g30f5wesn -V -Dc -Wthick -O -K >> ${layer}.ps

if [ $4 -eq 1 ]
then
	$gmt psscale -Dx1i/-0.4i+w4i/0.5c+h  -Ccolorbar.cpt -I0 -B2.5:"Magnetic Field Difference (Bz)":/:"nT": -O >> ${layer}.ps
else
	$gmt psscale -Dx1i/-0.4i+w4i/0.5c+h  -Ccolorbar.cpt -I0 -B${myvar3}:"Magnetic Field Difference (Bz)":/:"nT": -O >> ${layer}.ps
fi

$gmt ps2raster -A+r ${layer}.ps

rm colorbar.cpt

rm gmt.history
rm *.ps
rm *.grd
