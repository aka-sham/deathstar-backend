#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

###
# Project          : deathstar-backend
# FileName         : util.py
# -----------------------------------------------------------------------------
# Author           : Sébastien Metzger
# E-Mail           : sebastien.metzger@nomogi.org
##

import os
import sys
import logging
import logging.config


def get_exe_dir():
    """Gets Executable directory."""
    if "falcon" in os.path.basename(sys.executable).lower():
        exe_dir = os.path.abspath(sys.executable)
    else:
        exe_dir = os.path.abspath(".")

    return exe_dir


def init_logging():
    """Loads logging configuration file and inits logging system."""
    exe_dir = get_exe_dir()

    # Log directory
    log_dir = os.path.join(exe_dir, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # Configuration file for logger
    log_file = os.path.join(exe_dir, "logging.conf")
    # Load configuration file
    logging.config.fileConfig(log_file)

    return logging.getLogger("falcon")


# EOF
