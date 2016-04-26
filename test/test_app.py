import transformation
import os
import csv
import pytest


class TestTransformation:
    def test_transformation(self, data_dir):
        if (os.getenv('KBC_DATA_DIR') is not None):
            data_dir = os.getenv('KBC_DATA_DIR')
        data_dir = data_dir + '/01/'
        # generate absolute path before the application is run, because it may alter current working directory
        result_file = os.path.abspath(data_dir + '/out/tables/sample.csv')

        app = transformation.App(data_dir)
        app.run()

        assert(os.path.isfile(result_file))
        with open(result_file, 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                expected = (int(row['funkyNumber']) ** 3)
                assert(expected == int(row['biggerFunky']))

    def test_tagged_files(self, data_dir):
        if (os.getenv('KBC_DATA_DIR') is not None):
            data_dir = os.getenv('KBC_DATA_DIR')
        data_dir = data_dir + '/02/'
        # generate absolute path before the application is run, because it may alter current working directory
        result_dir = os.path.abspath(data_dir)

        app = transformation.App(data_dir)
        app.run()

        assert(os.path.isfile(result_dir + '/in/user/pokus'))
        assert(os.path.isfile(result_dir + '/in/user/model'))
        assert(os.path.isfile(result_dir + '/out/tables/sample.csv'))
        with open(result_dir + '/out/tables/sample.csv', 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                assert(6 == int(row['x']))

    def test_package_error(self, data_dir):
        if (os.getenv('KBC_DATA_DIR') is not None):
            data_dir = os.getenv('KBC_DATA_DIR')
        data_dir = data_dir + '/03/'
        app = transformation.App(data_dir)
        try:
            app.run()
            pytest.xfail("Must raise exception.")
        except (ValueError):
            pass

    def test_script_syntax_error(self, data_dir):
        if (os.getenv('KBC_DATA_DIR') is not None):
            data_dir = os.getenv('KBC_DATA_DIR')
        data_dir = data_dir + '/04/'
        app = transformation.App(data_dir)
        try:
            app.run()
            pytest.xfail("Must raise exception.")
        except (ValueError):
            pass
