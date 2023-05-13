#!/bin/bash

if [[ -z "$DIST_DIR" ]]; then
    echo "Error: DIST_DIR is not set"
    exit 1
fi

if [[ "$DIST_DIR" == "/" ]]; then
    echo "Error: DIST_DIR cannot be root directory"
    exit 1
fi

if [[ "$DIST_DIR" == "." ]]; then
    echo "Error: DIST_DIR cannot be current directory"
    exit 1
fi

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
rm -rf "$DIST_DIR/*"

mkdir -p $BUILD_DIR
mkdir -p $DIST_DIR
mkdir -p $DIST_DIR/static
mkdir -p $DIST_DIR/templates

tsc
npx webpack

cp -a src/static/. $DIST_DIR/static/
cp -a src/templates/. $DIST_DIR/templates/
