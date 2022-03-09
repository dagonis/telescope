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
    # parser = argparse.ArgumentParser(yu)
    # parser.add_argument('--region', "-r", type=str, choices=DIGITAL_OCEAN_REGIONS, help="The Region you want to check.")
    # parser.add_argument('buckets', nargs="+", help="The bucket(s) you want to check")
    parser = argparse.ArgumentParser(description=BANNER)
    # Exclusive Argument Group if you want to either specify a region or if you want to try all regions with your bucket name(s)
    region_group = parser.add_mutually_exclusive_group()
    region_group.add_argument('--region', "-r",  choices=DIGITAL_OCEAN_REGIONS, help="The Region you want")
    region_group.add_argument('--all_regions', "-R", action='store_true')
    # Exclusive Argument Group if you want supply a bucket name (or names) at the command line or use a file
    bucket_group = parser.add_mutually_exclusive_group()
    bucket_group.add_argument('--buckets', "-b", nargs="+", help="The bucket(s) you want to check")
    bucket_group.add_argument('--bucket_file', "-f", help="The bucket(s) you want to check, stored in a file.")
    # More Options
    parser.add_argument("--download", action="store_true", help="Download all files, be careful.")
    parser.add_argument("--download_folder", type=str, default=".", help="If --download is used, this where the files will go.")
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