# coding=utf-8
from keboola import docker
import os
import csv

class App:

    def __init__(self, data_dir = None):
        self.data_dir = data_dir
        
    def run(self):
        import pip
        import sys
        import traceback
        # initialize KBC configuration 
        cfg = docker.Config(self.data_dir)
        # validate application parameters
        parameters = cfg.get_parameters()
        script_content = parameters.get('script')
        tags = parameters.get('tags')
        if (tags is None):
            tags = []
        packages = parameters.get('packages')
        if (packages is None):
            packages = []
                    
        if (script_content is None):
            raise ValueError('script_content is required parameter.')
        
        # install packages
        for package in packages:
            if pip.main(['install', '--disable-pip-version-check', '--no-cache-dir', '--cert=/tmp/cacert.pem', package]) != 0:
                raise ValueError('Failed to install package: ' + package)
        
        # prepare tagged files
        self.prepare_tagged_files(cfg, tags)
        
        script_file = cfg.get_data_dir() + 'script.py'
        print('Script file ' + script_file)
        with open(script_file, 'wt') as script:
            for line in script_content:
                script.write(line)
                script.write('\n')
            
        # Change current working directory so that relative paths work
        os.chdir(cfg.get_data_dir())
        # Execute the actual script
        with open('script.py', 'rt') as script:
            try:
                exec(script.read(), globals())
                print('Script finished')
            except Exception as err:
                _, _, tb = sys.exc_info()
                stack_len = len(traceback.extract_tb(tb)) - 1
                print(err, file=sys.stderr)
                traceback.print_exception(*sys.exc_info(), -stack_len, file=sys.stderr, chain = True)
                raise ValueError('Script failed.')

    def prepare_tagged_files(self, cfg, tags):
        """
        When supplied a list of tags, select input files with the given tags and prepare the 
        most recent file of those into a /user/ folder

        Args:
            cfg: keboola.docker.Config object 
            tags: List of tag names.
        """
        from datetime import datetime, timezone
        from shutil import copyfile
        
        if not os.path.exists(os.path.join(cfg.get_data_dir(), 'in', 'user')):
            os.makedirs(os.path.join(cfg.get_data_dir(), 'in', 'user'))

        for tag in tags:
            last_time = datetime(1, 1, 1, 0, 0, 0, 0, timezone.utc)
            last_manifest = ''
            for file in cfg.get_input_files():
                manifest = cfg.get_file_manifest(file)
                if (tag in manifest['tags']):
                    file_time = datetime.strptime(manifest['created'], '%Y-%m-%dT%H:%M:%S%z')
                    if (file_time > last_time):
                        last_time = file_time
                        last_manifest = file
            if (last_manifest == ''):
                raise ValueError("No files were found for tag: " + tag) 
            else:
                copyfile(file, os.path.join(cfg.get_data_dir(), 'in', 'user', tag))
                copyfile(file + '.manifest', os.path.join(cfg.get_data_dir(), 'in', 'user', tag + '.manifest'))
                
