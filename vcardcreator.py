import os
import pandas as pd
from datetime import date, datetime

if os.path.exists("vcard.vcf"): os.remove("vcard.vcf")
os.remove("Connections_sanitized.csv")

# Sanitize quotes
with open("Connections.csv") as file:
    data = file.read().replace('""', "~")
    data = data.replace('"', "")

newFile = open("Connections_sanitized.csv", "a")
newFile.write(data)
newFile.close()

# First Name
# Last Name
# E-Mail
# Address
# Company
# Position
# Connected on
names = ["First Name", "Last Name", "Email Address", "Company", "Position", "Connected on"]
df = pd.read_csv("Connections_sanitized.csv", quotechar="~", skipinitialspace=True, names=names)
df = df.drop("Email Address", axis=1)
df = df.head(1)

# File
f = open("vcard.vcf", "a")

for index, row in df.iterrows():
    f.write("BEGIN:VCARD\n")
    f.write("VERSION:3.0\n")
    f.write(f"N:{row['Last Name']};{row['First Name']}\n")
    f.write(f"ORG:{row['Company']}\n")
    f.write(f"TITLE:{str(row['Position']).replace(',', '')}\n")
    # f.write(f"LABEL;TYPE=")
    f.write(
        f"NOTE:Imported from LinkedIn, Connected on: {datetime.strptime(row['Connected on'], '%d %b %Y').strftime('%m-%d-%y')}\n")
    f.write(f"REV:{date.today().strftime('%m-%d-%y')}\n")
    f.write("END:VCARD\n")

f.close()
