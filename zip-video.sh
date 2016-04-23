#!/bin/bash

VERSION="$1"
FILE="plugin.video.vietmedia.movie-$VERSION.zip"
mv plugin.video.vietmedia.movie/*.zip* ./
rm plugin.video.vietmedia.movie/.DS*
rm plugin.video.vietmedia.movie/simplejson/.DS*
rm plugin.video.vietmedia.movie/resources/.DS*
zip -9 -r $FILE ./plugin.video.vietmedia.movie

md5 -r addons.xml | cut -c 1-32 > addons.xml.md5
md5 -r $FILE | cut -c 1-32 > $FILE.md5

mv ./plugin.video*.zip* ./plugin.video.vietmedia.movie

echo $FILE
