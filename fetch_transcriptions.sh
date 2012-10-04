#!/bin/bash

mkdir -p transcriptions
curl "http://www.ohnorobot.com/archive.pl?comic=636;page=[1-60];show=2" -o "transcriptions/#1.html"
