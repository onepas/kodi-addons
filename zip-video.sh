#!/bin/bash

VERSION="$1"
FILE="plugin.video.vietmediaplay-$VERSION.zip"
mv plugin.video.vietmediaplay/*.zip* ./
rm plugin.video.vietmediaplay/.DS*
rm plugin.video.vietmediaplay/simplejson/.DS*
rm plugin.video.vietmediaplay/resources/.DS*
zip -9 -r $FILE ./plugin.video.vietmediaplay

md5 -r addons.xml | cut -c 1-32 > addons.xml.md5
md5 -r $FILE | cut -c 1-32 > $FILE.md5

mv ./plugin.video*.zip* ./plugin.video.vietmediaplay

echo $FILE
