#!/bin/bash

wget -O  "universal-sentence-encoder_4.tar.gz" "https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed"
mkdir "universal-sentence-encoder_4"
tar -xvzf "universal-sentence-encoder_4.tar.gz -C universal-sentence-encoder_4/"
rm "universal-sentence-encoder_4.tar.gz"
