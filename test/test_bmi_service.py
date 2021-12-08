import unittest
from bmi_service.bmi_service import BMIService
from common_utils.helper_functions import load_json


class BMIServiceTest(unittest.TestCase):
    def setUp(self):
        bmi_config = load_json("test_data/test_bmi_config.json")
        patient_data_path = "test_data/test_patient_data.json"
        self.bmi_obj = BMIService(bmi_config, patient_data_path)

    def test_validate_data(self):
        self.assertTrue(self.bmi_obj._BMIService__validate_patient_data({"Gender": "Female", "HeightCm": 167, "WeightKg": 82}))
        self.assertTrue(self.bmi_obj._BMIService__validate_patient_data({"HeightCm": 167, "WeightKg": 82}))
        self.assertFalse(self.bmi_obj._BMIService__validate_patient_data({"Gender":"Male", "WeightKg": 82}))
        self.assertFalse(self.bmi_obj._BMIService__validate_patient_data({"Gender": "Male", "HeightCm": 167}))
        self.assertFalse(self.bmi_obj._BMIService__validate_patient_data({"Gender" : "Female"}))
        self.assertFalse(self.bmi_obj._BMIService__validate_patient_data({"Gender": "Female", "HeightCm": 0, "WeightKg": 82}))
        self.assertFalse(
            self.bmi_obj._BMIService__validate_patient_data({"Gender": "Female", "HeightCm": -58, "WeightKg": 82}))
        self.assertTrue(
            self.bmi_obj._BMIService__validate_patient_data({"Gender": "Female", "HeightCm": 12, "WeightKg": 0}))
        self.assertFalse(
            self.bmi_obj._BMIService__validate_patient_data({"Gender": "Female", "HeightCm": 200, "WeightKg": -58}))

    def test_calculate_bmi(self):
        self.assertEqual(self.bmi_obj._BMIService__calculate_bmi(96,1.71), 32.83)
        self.assertNotEqual(self.bmi_obj._BMIService__calculate_bmi(25,2),7.25)
        self.assertEqual(self.bmi_obj._BMIService__calculate_bmi(0,2),0)
        with self.assertRaises(ValueError):
            self.bmi_obj._BMIService__calculate_bmi(-5, 2)

        with self.assertRaises(ValueError):
            self.bmi_obj._BMIService__calculate_bmi(45, 0)

        with self.assertRaises(ValueError):
            self.bmi_obj._BMIService__calculate_bmi(45, -5)

    def test_get_bmi_info(self):
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(18.4), ("Underweight", "Malnutrition risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(9.5), ("Underweight", "Malnutrition risk"))

        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(18.5), ("Normal weight", "Low risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(23.5), ("Normal weight", "Low risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(24.9), ("Normal weight", "Low risk"))

        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(25), ("Overweight", "Enhanced risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(27.8), ("Overweight", "Enhanced risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(29.9), ("Overweight", "Enhanced risk"))

        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(30), ("Moderately obese", "Medium risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(32), ("Moderately obese", "Medium risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(34.9), ("Moderately obese", "Medium risk"))

        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(35), ("Severely obese", "High risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(39.8), ("Severely obese", "High risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(39.9), ("Severely obese", "High risk"))

        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(40), ("Very severely obese", "Very high risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(40.1), ("Very severely obese", "Very high risk"))
        self.assertTupleEqual(self.bmi_obj._BMIService__get_bmi_info(100), ("Very severely obese", "Very high risk"))

    def test_generate_result(self):
        self.assertEqual(self.bmi_obj.generate_result(), 2)
        self.assertNotEqual(self.bmi_obj.generate_result(), 5)


if __name__ == '__main__':
    unittest.main()
