import unittest
from test_spacex_udp_sender import TestSpacexUDPSender
from test_mysql_wrapper import TestMySQLWrapper

if __name__ == '__main__':
    test_classes = [TestSpacexUDPSender, TestMySQLWrapper]
    loader = unittest.TestLoader()
    suites = []
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites.append(suite)

    all_tests = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    results = runner.run(all_tests)
