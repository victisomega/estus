#!/usr/bin/python3

import argparse
import importlib
import logging
import os
import pip
import sys


# TODO: Add More Options for ORM
# TODO: Add Way for quick Blueprint (Module) Creation
# TODO: Change wsgi_template.py location to default package location
# TODO: Add a prompt for Caching and Middleware installation

# NOTE: Logging should be done within the root of the project for creation?


# Building Arguments

parser = argparse.ArgumentParser(description="Builds an MVC minded System using the Flask Microframework")
parser.add_argument('name', type=str, help='The name of your site or project')
parser.add_argument('--path', type=str, help='the path to build the project (defaults to .)')
parser.add_argument('--orm', help='The ORM to use for the project (defaults to SQLAlchemy if none specified)')
parser.add_argument('--design', help='Design schema of the project. options(modular, monolithic)')
parser.add_argument('--log', help='A place to store the log file (defaults to /var/log/estus/estus.log)')

args = parser.parse_args()

# Done

# Building Logging System

log_location = '/var/log/estus/' if args.log == '' or args.log is None else args.log

logger = logging.getLogger(__name__)
try:
    fhandler = logging.FileHandler(log_location + 'estus.log')
    fhandler.setLevel(logging.DEBUG)
except FileNotFoundError:
    try:
        os.makedirs(log_location)
        fhandler = logging.FileHandler(log_location + 'estus.log')
        fhandler.setLevel(logging.DEBUG)
    except PermissionError:
        cont = input('Root Permissions Needed, Allow? (y/n)')
        if cont == 'y' or cont == 'Y' or cont == 'yes' or cont == 'Yes':
            import subprocess
            subprocess.run(["sudo", "mkdir", "-p", log_location])
            subprocess.run(["sudo", "chmod", "+w", log_location])
            subprocess.run(["sudo", "touch", str(log_location + 'estus.log')])
            subprocess.run(["sudo", "chmod", "777", str(log_location + 'estus.log')])
            fhandler = logging.FileHandler(log_location + 'estus.log')
            fhandler.setLevel(logging.DEBUG)
        else:
            print('Unable to create Logger, Exiting')
            sys.exit()


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)

logger.addHandler(fhandler)

# Done

# Define init Function


def init():
    pass


def install(package):
    try:
        pip.main(['install', package])
        return True
    except SyntaxError:
        msg = 'Installation of %s using pip Failed... Exiting' % package
        logger.critical(msg)


def check_for_pkg(package):
    found = importlib.util.find_spec(package)
    if found is None:
        msg = '%s is NOT installed, Prompting for install.' % package
        logger.warn(msg)
        proceed = input('%s is NOT installed, install it? (y/n)' % package)
        if proceed == 'y' or proceed == 'yes':
            success = install(package)
            return success
        else:
            msg = '%s is NOT installed, killing Build' % package
            logger.critical(msg)

            msg = 'Stopping Build, Please See Logs for more information'
            logger.critical(msg)

            return False
    else:
        return True


def build_app_by_design(design):
    msg = 'Attempting to Build Directory Structure based on Selected Design'
    logger.info(msg)
    path = os.getcwd()

    os.makedirs(path + '/config/', exist_ok=False)
    os.makedirs(path + '/module/', exist_ok=False)
    os.makedirs(path + '/vendor/', exist_ok=False)

    if design == 'monolithic':
        msg = 'Using Monolithic Template'
        logger.info(msg)

        os.makedirs(path + '/controller/', exist_ok=False)
        os.makedirs(path + '/model/', exist_ok=False)
        os.makedirs(path + '/static/', exist_ok=False)
        os.makedirs(path + '/static/img', exist_ok=False)
        os.makedirs(path + '/static/js', exist_ok=False)
        os.makedirs(path + '/static/css', exist_ok=False)
        os.makedirs(path + '/view', exist_ok=False)
        t = 'monolithic'

    elif design == 'modular':
        msg = 'Using Modular Template'
        logger.info(msg)
        t = 'modular'

    else:
        msg = 'Invalid Template type, Exiting'
        logger.critical(msg)
        return False

    f = open(str(path + '/config/settings.ini'), 'w')
    f.write("[SETTINGS]\r\nTYPE=%s\r\nDEBUG=True\r\nPORT=8080\r\nLISTEN=127.0.0.1" % t)
    f.close()
    return True


def create_path(p_path):
    msg = 'Attempting to Create Basic Directory structure'
    logger.info(msg)

    try:
        os.makedirs(p_path, exist_ok=True)
    except OSError:
        if not os.path.isdir(p_path):
            raise
        msg = 'Invalid Directory, please specified a Valid Directory'
        cont1 = input(msg)
        create_path(cont1)


# Defining main Function

def main():
    logger.info('Starting Build')
    logger.info('Checking for Flask install')

    success = check_for_pkg('flask')

    if success:
        success = check_for_pkg('beaker')
        if success:
            p_name = args.name
            p_path = args.path
            p_orm = args.orm
            p_design = args.design

            if p_orm == 'SQLAlchemy':

                logger.info('SQLAlchemy Selected for ORM. Checking for install.')
                success = check_for_pkg('sqlalchemy')
                if not success:
                    sys.exit()
                else:
                    msg = 'Skipping Install of SQLAlchemy, Application WILL NOT function properly, continue? (y/n)'
                    logger.warn(msg)
                    cont1 = input(msg)
                    if cont1 == 'y' or cont1 == 'yes':
                        logger.warn('Continuing Broken Build!')
                    else:
                        logger.warn('Stopping Build, Exiting')
                        sys.exit()

            msg = 'ORM Install Check Complete!'
            logger.info(msg)

            if p_name == '' or p_name is None:
                p_name = 'estus_testapp'
            msg = 'Project Name set as %s' % p_name
            logger.info(msg)

            if p_path == '' or p_path is None:
                msg = 'Path to Project not specified. Specify Path (Default: %s)' % str(os.getcwd() + '/' + p_name)
                cont1 = input(msg)
                if cont1 == '' or cont1 is None:
                    p = str(os.getcwd() + '/' + p_name)
                else:
                    p = cont1 + p_name
            else:
                p = p_path + p_name

            create_path(p)
            os.chdir(p)

            msg = 'Path Setup Complete! Using Directory %s' % p
            logger.info(msg)

            if p_design == '' or p_design is None:
                msg = 'Application Design type not specified, specify now? (Default: monolithic)'
                cont1 = input(msg)
                if cont1 != 'monolithic' and cont1 != 'modular':
                    msg = 'Invalid Design type specified, Exiting.'
                    logger.critical(msg)
                    sys.exit()
                else:
                    des = cont1
            else:
                des = p_design
            success = build_app_by_design(des)
            if not success:
                msg = 'Invalid Template Specified, Build Failed. Exiting (Check Log for more info)'
                logger.critical(msg)
                sys.exit()

            with open(os.path.join(sys.path[0], 'wsgi_template.py')) as of:
                lines = of.readlines()
                with open(str(p + "/wsgi.py"), "w") as f1:
                    f1.writelines(lines)
        else:
            logger.critical('Beaker is not Installed. Exiting')
            sys.exit()
    else:
        logger.critical('Program Error, Check Logs for more info. Exiting')
        sys.exit()

# Configuration Complete, running Main Function

if __name__ == '__main__':
    main()
