#!/bin/bash

#	Add your hugging face access token to huggingface-cli first.

#	repofolder is in this stupid relative path notation. maintainer/repo-type

#	change repotype depending on your repo

 huggingface-cli download --repo-type dataset <maintainer>/<gigaspeech> --include="data/metadata/*" --local-dir 
./gigaspeech_metadata