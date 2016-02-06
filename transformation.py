# coding=utf-8
from keboola import docker
import os
import csv
import pip

class App:

    def __init__(self, dataDir = None):
        self.dataDir = dataDir
        
    def run(self):
        # initialize KBC configuration 
        cfg = docker.Config(self.dataDir)
        # validate application parameters
        parameters = cfg.getParameters()
        scriptContent = parameters.get('script')
        tags = parameters.get('tags')
        if (tags is None):
            tags = []
        packages = parameters.get('packages')
        if (packages is None):
            packages = []
                    
        if (scriptContent is None):
            raise ValueError('scriptContent is required parameter.')
        
        # install packages
        for package in packages:
            if pip.main(['install', package]) != 0:
                raise ValueError('Failed to install package: ' + package)
        
        # prepare tagged files
        self.prepareTaggedFiles(cfg, tags)
        
        scriptFile = cfg.getDataDir() + 'script.py'
        print('Script file ' + scriptFile)
        with open(scriptFile, 'wt') as script:
            for line in scriptContent:
                script.write(line)
                script.write('\n')
            
        # Change current working directory so that relative paths work
        os.chdir(cfg.getDataDir())
        # Execute the actual script
        with open('script.py', 'rt') as script:
            exec(script.read())
            
        print('Script finished')

    def prepareTaggedFiles(self, cfg, tags):
        """
        When supplied a list of tags, select input files with the given tags and prepare the 
        most recent file of those into a /user/ folder

        Args:
            cfg: keboola.docker.Config object 
            tags: List of tag names.
        """
        from datetime import datetime, timezone
        from shutil import copyfile
        
        if not os.path.exists(os.path.join(cfg.getDataDir(), 'in', 'user')):
            os.makedirs(os.path.join(cfg.getDataDir(), 'in', 'user'))

        for tag in tags:
            lastTime = datetime(1, 1, 1, 0, 0, 0, 0, timezone.utc)
            lastManifest = ''
            for file in cfg.getInputFiles():
                manifest = cfg.getFileManifest(file)
                if (tag in manifest['tags']):
                    fileTime = datetime.strptime(manifest['created'], '%Y-%m-%dT%H:%M:%S%z')
                    if (fileTime > lastTime):
                        lastTime = fileTime
                        lastManifest = file
            if (lastManifest == ''):
                raise ValueError("No files were found for tag: " + tag) 
            else:
                copyfile(file, os.path.join(cfg.getDataDir(), 'in', 'user', tag))
                copyfile(file + '.manifest', os.path.join(cfg.getDataDir(), 'in', 'user', tag + '.manifest'))
                