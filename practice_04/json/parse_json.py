import json
import os

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "sample-data.json")

with open(file_path, "r") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 79)
print(f"{'Interface':<12} {'Description':<20} {'Speed':<10} {'MTU':<6}")
print("-" * 12 + " " + "-" * 20 + " " + "-" * 10 + " " + "-" * 6)

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]

    interface = attrs.get("id", "")
    descr = attrs.get("descr") or "N/A"
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    print(f"{interface:<12} {descr:<20} {speed:<10} {mtu:<6}")

