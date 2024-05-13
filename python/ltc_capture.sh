#!/bin/bash

arecord -D 'hw:3,0' -f dat -r 48000 -c 2 | stdbuf -o0 ltcdump - > ltc_pipe
