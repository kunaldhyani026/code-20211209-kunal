import os
import json
import in_place
from common_utils.helper_functions import get_current_datetime, create_missing_directory, create_unique_string


class BMIService:
    """
    This service is used to calculate the bmi, bmi category and health risk of the patients
    after considering data as per the defined bmi configurations
    """
    def __init__(self, bmi_config, patient_data_path):
        self.bmi_config = bmi_config
        self.patient_data_path = patient_data_path

    @staticmethod
    def __calculate_bmi(mass_in_kg, height_in_meter):
        """
        :param mass_in_kg: mass of the person in kilo grams
        :param height_in_meter: height of the person in meters
        :return: bmi of the person calculated as per - (mass_in_kg)/(height_in_meter*height_in_meter),
                 rounded to 2 decimal places
        """
        if mass_in_kg < 0 or height_in_meter <= 0:
            raise ValueError("Invalid weight or height value")
        bmi = (mass_in_kg/(height_in_meter * height_in_meter))
        return round(bmi, 2)

    def __get_bmi_info(self, bmi):
        """
        :param bmi: bmi of the person
        :return: bmi category and health risk of the person
        """
        bmi_category = None
        bmi_health_risk = None

        for row in self.bmi_config:
            lower_limit = row["lower_limit"]
            upper_limit = row["upper_limit"]

            if lower_limit is None:
                lower_limit = 0

            if upper_limit is None:
                if bmi >= lower_limit:
                    bmi_category = row["bmi_category"]
                    bmi_health_risk = row["health_risk"]
            else:
                if lower_limit <= bmi <= upper_limit:
                    bmi_category = row["bmi_category"]
                    bmi_health_risk = row["health_risk"]

        return bmi_category, bmi_health_risk

    @staticmethod
    def __validate_patient_data(data):
        """
        :param data: patient data
        :return: True if data is valid else False
                Checks for non-negative weight and non-zero height data
        """
        weight = data.get("WeightKg", -1)
        height = data.get("HeightCm", -1)

        if weight < 0 or height <= 0:
            return False

        return True

    def generate_result(self):
        """
        :return: adds bmi, category and health risk to patient data and returns total number of overweight patients
        """
        overweight_patient_count = 0
        with in_place.InPlace(self.patient_data_path) as file:
            for line in file:
                line = line.strip("\n")
                start_of_line = False
                end_of_line = False

                if not line:
                    continue

                if line[0] == "[":
                    start_of_line = True
                if line[-1] == "]":
                    end_of_line = True

                line = line.strip("[").strip("]").strip(",")

                patient_data = json.loads(line)

                if self.__validate_patient_data(patient_data):
                    bmi = self.__calculate_bmi(patient_data["WeightKg"], patient_data["HeightCm"]/100)
                    category, health_risk = self.__get_bmi_info(bmi)
                else:
                    bmi = None
                    category = None
                    health_risk = None

                patient_data["bmi"] = bmi
                patient_data["category"] = category
                patient_data["health_risk"] = health_risk

                if category == "Overweight":
                    overweight_patient_count += 1

                patient_data_string = json.dumps(patient_data)
                if start_of_line and end_of_line:
                    data_to_write = "[" + patient_data_string + "]" + "\n"
                elif start_of_line:
                    data_to_write = "[" + patient_data_string + "," + "\n"
                elif end_of_line:
                    data_to_write = patient_data_string + "]" + "\n"
                else:
                    data_to_write = patient_data_string + "," + "\n"

                file.write(data_to_write)

        return overweight_patient_count
