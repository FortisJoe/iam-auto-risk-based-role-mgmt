import csv
import random
from faker import Faker

# Initialize Faker to generate realistic names
fake = Faker()

# Function to generate unique email addresses
def generate_unique_emails(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}@risk.local"


# Generating 100 unique records with actual names
data = []
account_id = 100000  # starting account ID
first_run = True
manager = None

for i in range(100):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = generate_unique_emails(first_name, last_name)
    job = fake.job()
    company = "Risk PLC"
    dept = fake.catch_phrase()
    account_id += 1
    if first_run:
        first_run = False
        manager = f"{account_id:06d}"
        data.append(
            [
                first_name,
                last_name,
                email,
                f"{account_id:06d}",
                job,
                company,
                dept,
                None
            ]
        )
    else:
        data.append(
            [
                first_name,
                last_name,
                email,
                f"{account_id:06d}",
                job,
                company,
                dept,
                manager
            ]
        )

# Writing data to a CSV file
with open("people_data_names.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "First Name",
            "Last Name",
            "Email",
            "AccountID",
            "Job",
            "Company",
            "Department",
            "Manager",
        ]
    )
    writer.writerows(data)

print(
    "CSV file 'people_data_names.csv' generated successfully with 100 unique records."
)

group_names = set()

while True:
    group = fake.job()
    group = group.replace(", ", " - ")
    group = group.replace("/", " ")
    group_names.add(group)
    if len(group_names) == 20:
        break

groups = []
owners = random.sample(data, 20)
for name in group_names:
    owner = owners.pop()
    owner_id = owner[3]
    groups.append(
        [
            name,
            owner_id
        ]
    )

# Writing data to a CSV file
with open("groups.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Group", "Owner"
        ]
    )
    writer.writerows(groups)

print(
    "CSV file 'groups.csv' generated successfully with 20 unique records."
)

memberships = []
for user in data:
    userid = user[3]
    number_of_groups = random.randrange(1, 5)
    groups_for_membership = random.sample(list(group_names), number_of_groups)
    for group_for_membership in groups_for_membership:
        memberships.append(
            [
                userid,
                group_for_membership
            ]
        )

# Writing data to a CSV file
with open("mbrs.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Account",
            "Group"
        ]
    )
    writer.writerows(memberships)

print(
    f"CSV file 'mbrs.csv' generated successfully with {len(memberships)} "
    f"unique records."
)
