import transformation
import os
import csv

class TestTransformation:
    def test_transformation(self, data_dir):
        if (os.getenv('KBC_DATA_DIR') != None):
            data_dir = os.getenv('KBC_DATA_DIR')
        data_dir = data_dir + '/01/'
        # generate absolute path before the application is run, because it may alter current working directory 
        resultFile = os.path.abspath(data_dir + '/out/tables/sample.csv')
        
        app = transformation.App(data_dir)
        app.run()

        assert(os.path.isfile(resultFile))
        with open(resultFile, 'rt') as sample:
            csvReader = csv.DictReader(sample, delimiter = ',', quotechar = '"')
            for row in csvReader:
                expected = (int(row['funkyNumber']) ** 3)
                assert(expected == int(row['biggerFunky']))            

    def test_tagged_files(self, data_dir):
        if (os.getenv('KBC_DATA_DIR') != None):
            data_dir = os.getenv('KBC_DATA_DIR')
        data_dir = data_dir + '/02/'
        # generate absolute path before the application is run, because it may alter current working directory 
        resultDir = os.path.abspath(data_dir)
                    
        app = transformation.App(data_dir)
        app.run()

        assert(os.path.isfile(resultDir + '/in/user/pokus'))
        assert(os.path.isfile(resultDir + '/in/user/model'))        
        assert(os.path.isfile(resultDir + '/out/tables/sample.csv'))
        with open(resultDir + '/out/tables/sample.csv', 'rt') as sample:
            csvReader = csv.DictReader(sample, delimiter = ',', quotechar = '"')
            for row in csvReader:
                assert(6 == int(row['x']))            
        
    def test_package_error(self, data_dir):
        if (os.getenv('KBC_DATA_DIR') != None):
            data_dir = os.getenv('KBC_DATA_DIR')
        data_dir = data_dir + '/03/'
        app = transformation.App(data_dir)
        try:
            app.run()
            pytest.xfail("Must raise exception.")
        except (ValueError):
            pass        

    def test_script_syntax_error(self, data_dir):
        if (os.getenv('KBC_DATA_DIR') != None):
            data_dir = os.getenv('KBC_DATA_DIR')
        data_dir = data_dir + '/04/'
        app = transformation.App(data_dir)
        try:
            app.run()
            pytest.xfail("Must raise exception.")
        except (ValueError):
            pass        
