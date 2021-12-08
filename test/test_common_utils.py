import unittest
from common_utils.helper_functions import load_json


class CommonUtilsTest(unittest.TestCase):
    def test_load_json(self):
        self.assertListEqual(load_json("test_data/test_bmi_config.json"),
                              [
                                  {"lower_limit": None, "upper_limit": 18.4, "bmi_category": "Underweight",
                                   "health_risk": "Malnutrition risk"},
                                  {"lower_limit": 18.5, "upper_limit": 24.9, "bmi_category": "Normal weight",
                                   "health_risk": "Low risk"},
                                  {"lower_limit": 25, "upper_limit": 29.9, "bmi_category": "Overweight",
                                   "health_risk": "Enhanced risk"},
                                  {"lower_limit": 30, "upper_limit": 34.9, "bmi_category": "Moderately obese",
                                   "health_risk": "Medium risk"},
                                  {"lower_limit": 35, "upper_limit": 39.9, "bmi_category": "Severely obese",
                                   "health_risk": "High risk"},
                                  {"lower_limit": 40, "upper_limit": None, "bmi_category": "Very severely obese",
                                   "health_risk": "Very high risk"}
                              ]
                              )

        with self.assertRaises(FileNotFoundError):
            load_json("path_dont_exits/test_bmi_config.json")


if __name__ == '__main__':
    unittest.main()
