date=$(date +%s)
raspistill -ex fixedfps -ss 4000 -co 100 -ev 0 -o "$date".jpg -n
echo "$date.jpg"
