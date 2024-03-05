import csv
import random

from idmlib import core


class CreateRiskInfo:

    def __init__(self):
        self.low_confidentiality_1 = 3
        self.low_confidentiality_2 = 5
        self.low_confidentiality_3 = 1
        self.medium_confidentiality_1 = 6
        self.medium_confidentiality_2 = 4
        self.medium_confidentiality_3 = 7
        self.high_confidentiality_1 = 9
        self.high_confidentiality_2 = 8
        self.high_confidentiality_3 = 10
        self.low_integrity_1 = 5
        self.low_integrity_2 = 1
        self.low_integrity_3 = 3
        self.medium_integrity_1 = 7
        self.medium_integrity_2 = 6
        self.medium_integrity_3 = 4
        self.high_integrity_1 = 10
        self.high_integrity_2 = 9
        self.high_integrity_3 = 8
        self.low_availability_1 = 1
        self.low_availability_2 = 3
        self.low_availability_3 = 5
        self.medium_availability_1 = 4
        self.medium_availability_2 = 7
        self.medium_availability_3 = 6
        self.high_availability_1 = 8
        self.high_availability_2 = 10
        self.high_availability_3 = 9
        self.low_aro_1 = 0.1
        self.low_aro_2 = 0.4
        self.low_aro_3 = 0.8
        self.medium_aro_1 = 2.0
        self.medium_aro_2 = 2.9
        self.medium_aro_3 = 1.3
        self.high_aro_1 = 2.0
        self.high_aro_2 = 5.1
        self.high_aro_3 = 8.4

    def generate_data(self):
        with open("info.csv", 'wt', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "Type", "ID", "ID2", "Deficit Level", "Surplus Level"
            ])
            writer.writeheader()
            for resource in core.api.ResourceFind("TMPL", []):
                tmpl_id = resource["resourceid"]
                deficit_data_set = random.randint(1, 3)
                surplus_data_set = random.randint(1, 3)
                deficit_level = random.choice(["high", "medium", "low"])
                surplus_level = random.choice(["high", "medium", "low"])
                deficit_confidentiality = getattr(self, f"{deficit_level}_confidentiality_{deficit_data_set}")
                deficit_integrity = getattr(self, f"{deficit_level}_integrity_{deficit_data_set}")
                deficit_availability = getattr(self, f"{deficit_level}_availability_{deficit_data_set}")
                deficit_aro = getattr(self, f"{deficit_level}_aro_{deficit_data_set}")
                surplus_confidentiality = getattr(self, f"{surplus_level}_confidentiality_{surplus_data_set}")
                surplus_integrity = getattr(self, f"{surplus_level}_integrity_{surplus_data_set}")
                surplus_availability = getattr(self, f"{surplus_level}_availability_{surplus_data_set}")
                surplus_aro = getattr(self, f"{surplus_level}_aro_{surplus_data_set}")
                core.api.ResourceAttrsSet(tmpl_id, "", "TMPL", 1, {
                    "DEFICIT_CONFIDENTIALITY_IMPACT": [str(deficit_confidentiality)],
                    "DEFICIT_INTEGRITY_IMPACT": [str(deficit_integrity)],
                    "DEFICIT_AVAILABILITY_IMPACT": [str(deficit_availability)],
                    "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE": [str(deficit_aro)],
                    "SURPLUS_CONFIDENTIALITY_IMPACT": [str(surplus_confidentiality)],
                    "SURPLUS_INTEGRITY_IMPACT": [str(surplus_integrity)],
                    "SURPLUS_AVAILABILITY_IMPACT": [str(surplus_availability)],
                    "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE": [str(surplus_aro)]
                })
                writer.writerow({
                    "Type": "Template",
                    "ID": tmpl_id,
                    "ID2": "",
                    "Deficit Level": deficit_level,
                    "Surplus Level": surplus_level
                })
            for resource in core.api.ResourceFind("MGRP", []):
                mgrp_id1 = resource["resourceid"]
                mgrp_id2 = resource["resourceid2"]
                hostid = None
                shortid = None
                for result in core.api.ResourceGet(mgrp_id1, mgrp_id2, "", "MGRP"):
                    if result[0] == "hostid":
                        hostid = result[1]
                    elif result[0] == "shortid":
                        shortid = result[1]
                deficit_data_set = random.randint(1, 3)
                surplus_data_set = random.randint(1, 3)
                deficit_level = random.choice(["high", "medium", "low"])
                surplus_level = random.choice(["high", "medium", "low"])
                deficit_confidentiality = getattr(self, f"{deficit_level}_confidentiality_{deficit_data_set}")
                deficit_integrity = getattr(self, f"{deficit_level}_integrity_{deficit_data_set}")
                deficit_availability = getattr(self, f"{deficit_level}_availability_{deficit_data_set}")
                deficit_aro = getattr(self, f"{deficit_level}_aro_{deficit_data_set}")
                surplus_confidentiality = getattr(self, f"{surplus_level}_confidentiality_{surplus_data_set}")
                surplus_integrity = getattr(self, f"{surplus_level}_integrity_{surplus_data_set}")
                surplus_availability = getattr(self, f"{surplus_level}_availability_{surplus_data_set}")
                surplus_aro = getattr(self, f"{surplus_level}_aro_{surplus_data_set}")
                core.api.ResourceAttrsSet(mgrp_id1, mgrp_id2, "MGRP", 1, {
                    "DEFICIT_CONFIDENTIALITY_IMPACT": [str(deficit_confidentiality)],
                    "DEFICIT_INTEGRITY_IMPACT": [str(deficit_integrity)],
                    "DEFICIT_AVAILABILITY_IMPACT": [str(deficit_availability)],
                    "DEFICIT_ANNUAL_RISK_OF_OCCURRENCE": [str(deficit_aro)],
                    "SURPLUS_CONFIDENTIALITY_IMPACT": [str(surplus_confidentiality)],
                    "SURPLUS_INTEGRITY_IMPACT": [str(surplus_integrity)],
                    "SURPLUS_AVAILABILITY_IMPACT": [str(surplus_availability)],
                    "SURPLUS_ANNUAL_RISK_OF_OCCURRENCE": [str(surplus_aro)]
                })
                writer.writerow({
                    "Type": "Group",
                    "ID": hostid,
                    "ID2": shortid,
                    "Deficit Level": deficit_level,
                    "Surplus Level": surplus_level
                })


if __name__ == "__main__":
    CreateRiskInfo().generate_data()
