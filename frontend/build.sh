#!/bin/bash

if [[ -z "$BUILD_DIR" ]]; then
    echo "Error: BUILD_DIR is not set"
    exit 1
fi

if [[ "$BUILD_DIR" == "/" ]]; then
    echo "Error: BUILD_DIR cannot be root directory"
    exit 1
fi

if [[ "$BUILD_DIR" == "." ]]; then
    echo "Error: BUILD_DIR cannot be current directory"
    exit 1
fi

rm -rf "$BUILD_DIR/*"

mkdir -p $BUILD_DIR
mkdir -p $BUILD_DIR/static
mkdir -p $BUILD_DIR/templates

cp -a src/static/css/. $BUILD_DIR/static/css
cp -a src/static/img/. $BUILD_DIR/static/img
cp -a src/templates/. $BUILD_DIR/templates/

tsc