import transformation
import os
import csv
import unittest


class TestTransformation(unittest.TestCase):
    def setUp(self):
        if os.getenv('KBC_DATADIR') is not None:
            self.data_dir = os.getenv('KBC_DATADIR')
        else:
            self.data_dir = '.'

    def test_transformation(self):
        data_dir = self.data_dir + '/01/'
        # generate absolute path before the application is run, because it may alter current working directory
        result_file = os.path.abspath(data_dir + '/out/tables/sample.csv')

        app = transformation.App(data_dir)
        app.run()

        self.assertTrue(os.path.isfile(result_file))
        with open(result_file, 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                self.assertEqual(int(row['biggerFunky']), (int(row['funkyNumber']) ** 3))

    def test_tagged_files(self,):
        data_dir = self.data_dir + '/02/'
        # generate absolute path before the application is run, because it may alter current working directory
        result_dir = os.path.abspath(data_dir)

        app = transformation.App(data_dir)
        app.run()

        self.assertTrue(os.path.isfile(result_dir + '/in/user/pokus'))
        self.assertTrue(os.path.isfile(result_dir + '/in/user/model'))
        self.assertTrue(os.path.isfile(result_dir + '/out/tables/sample.csv'))
        with open(result_dir + '/out/tables/sample.csv', 'rt') as sample:
            csv_reader = csv.DictReader(sample, delimiter=',', quotechar='"')
            for row in csv_reader:
                self.assertEqual(int(row['x']), 5)

    def test_package_error(self):
        data_dir = self.data_dir + '/03/'
        app = transformation.App(data_dir)
        with self.assertRaisesRegex(ValueError, "Failed to install package: some-non-existent-package"):
            app.run()

    def test_script_syntax_error(self):
        data_dir = self.data_dir + '/04/'
        app = transformation.App(data_dir)
        with self.assertRaisesRegex(ValueError, "Script failed."):
            app.run()
