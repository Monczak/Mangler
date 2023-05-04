#!/bin/bash

rm -rf $BUILD_DIR/*

mkdir -p $BUILD_DIR
mkdir -p $BUILD_DIR/static
mkdir -p $BUILD_DIR/templates

cp -a src/static/css/. $BUILD_DIR/static/css
cp -a src/static/img/. $BUILD_DIR/static/img
cp -a src/templates/. $BUILD_DIR/templates/

tsc