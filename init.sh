#!/bin/bash

# Constant
BASEDIR=$(dirname "$(realpath "$0")")
VENVDIR="article_generator"

# Venv 
if [ ! -d "${BASEDIR}/${VENVDIR}" ]; then
  python3 -m venv "${BASEDIR}/${VENVDIR}"
fi

# Activate
if [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == CYGWIN* ]]; then
  # Windows (Git Bash, Cygwin) specific code
  source "${BASEDIR}/${VENVDIR}/Scripts/activate"
else
  # Linux/Mac specific code
  source "${BASEDIR}/${VENVDIR}/bin/activate"
fi
