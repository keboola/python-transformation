import transformation
import os
import csv

class TestTransformation:
    def test_transformation(self, dataDir):
        if (os.getenv('KBC_DATA_DIR') != None):
            dataDir = os.getenv('KBC_DATA_DIR')
        dataDir = dataDir + '/01/'
        # generate absolute path before the application is run, because it may alter current working directory 
        resultFile = os.path.abspath(dataDir + '/out/tables/sample.csv')
        
        app = transformation.App(dataDir)
        app.run()

        assert(os.path.isfile(resultFile))
        with open(resultFile, 'rt') as sample:
            csvReader = csv.DictReader(sample, delimiter = ',', quotechar = '"')
            for row in csvReader:
                expected = (int(row['funkyNumber']) ** 3)
                assert(expected == int(row['biggerFunky']))            

    def test_taggedFiles(self, dataDir):
        if (os.getenv('KBC_DATA_DIR') != None):
            dataDir = os.getenv('KBC_DATA_DIR')
        dataDir = dataDir + '/02/'
        # generate absolute path before the application is run, because it may alter current working directory 
        resultDir = os.path.abspath(dataDir)
                    
        app = transformation.App(dataDir)
        app.run()

        assert(os.path.isfile(resultDir + '/in/user/pokus'))
        assert(os.path.isfile(resultDir + '/in/user/model'))        
        assert(os.path.isfile(resultDir + '/out/tables/sample.csv'))
        with open(resultDir + '/out/tables/sample.csv', 'rt') as sample:
            csvReader = csv.DictReader(sample, delimiter = ',', quotechar = '"')
            for row in csvReader:
                assert(6 == int(row['x']))            
        
    def test_packageError(self, dataDir):
        if (os.getenv('KBC_DATA_DIR') != None):
            dataDir = os.getenv('KBC_DATA_DIR')
        dataDir = dataDir + '/03/'
        app = transformation.App(dataDir)
        try:
            app.run()
            pytest.xfail("Must raise exception.")
        except (ValueError):
            pass        
