#!/bin/bash

cd react-src
npm run build
cd ..
export FLASK_APP=app/__init__.py
flask run
