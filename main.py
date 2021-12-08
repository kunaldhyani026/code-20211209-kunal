
from bmi_service.bmi_service import BMIService
from common_utils.helper_functions import load_json
import time

if __name__ == '__main__':
    start_time = time.time()

    bmi_config = load_json("data/bmi_config.json")
    patient_data_path = "data/patient_data.json"

    bmi_obj = BMIService(bmi_config, patient_data_path)
    overweight_patient_count = bmi_obj.generate_result()

    print("Total Overweight Patients : ", overweight_patient_count)

    print(f"Data processed successfully in {time.time() - start_time} secs")

