import argparse
import re
import sys

import requests

BANNER = "Telescope v.1"

DIGITAL_OCEAN_SPACES_URL = "digitaloceanspaces.com"
SPACE_REGEX = re.compile(r'<Key>.+?</Key>') # Should get around to doing this with real XML parsing, but this works for now. 

DIGITAL_OCEAN_REGIONS = ['nyc3',
'sgp1',
'sfo2',
'sfo3',
'ams3',
'fra1']

def main() -> None:
    """Main function of telescope
    """
    parser = argparse.ArgumentParser(description=BANNER)
    parser.add_argument('--region', "-r", type=str, choices=DIGITAL_OCEAN_REGIONS, help="The Region you want to check.")
    parser.add_argument('buckets', nargs="+", help="The bucket(s) you want to check")
    args = parser.parse_args()
    found_files = set()
    for bucket in args.buckets:
        bucket_url = f"https://{bucket}.{args.region}.{DIGITAL_OCEAN_SPACES_URL}"
        results = requests.get(bucket_url).text
        for result in SPACE_REGEX.findall(results):
            item = result.split(">")[1].split("<")[0]
            found_files.add(f"{bucket_url}/{item}")
    print(found_files)


if __name__ == '__main__':
    main()