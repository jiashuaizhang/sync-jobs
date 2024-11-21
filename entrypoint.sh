#!/bin/bash

WORKDIR="/opt/sync-jobs"
if [ ! -d "$WORKDIR" ]; then
    mkdir -p $WORKDIR
fi
if [ -z "$(ls -A "$WORKDIR")" ]; then
    mv /tmp/sync-jobs/* $WORKDIR
    rm -rf /tmp/sync-jobs
fi

if [ -z "$SYNC" ]; then
    export SYNC=1
fi

if [ "$SYNC" -eq 0 ]; then
    echo "不执行同步任务"
else
    # shellcheck disable=SC2164
    cd $WORKDIR
    python sync.py
fi