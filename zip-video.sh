#!/bin/bash

VERSION="$1"
FILE="plugin.video.vietmediaF-$VERSION.zip"
mv plugin.video.vietmediaF/*.zip* ./
rm plugin.video.vietmediaF/.DS*
rm plugin.video.vietmediaF/simplejson/.DS*
rm plugin.video.vietmediaF/resources/.DS*
zip -9 -r $FILE ./plugin.video.vietmediaF

md5 -r addons.xml | cut -c 1-32 > addons.xml.md5
md5 -r $FILE | cut -c 1-32 > $FILE.md5

mv ./plugin.video*.zip* ./plugin.video.vietmediaF

echo $FILE
