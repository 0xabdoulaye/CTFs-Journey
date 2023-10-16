#!/bin/bash

read -p "Enter your Rot13 here :" rot13

echo $rot13 | tr 'A-Za-z' 'N-ZA-Mn-za-m'
