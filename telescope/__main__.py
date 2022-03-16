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
    # Exclusive Argument Group if you want to either specify a region or if you want to try all regions with your bucket name(s)
    region_group = parser.add_mutually_exclusive_group()
    region_group.add_argument('--regions', "-r", nargs="+", choices=DIGITAL_OCEAN_REGIONS, help="The Region(s) you want to check.")
    region_group.add_argument('--all_regions', "-R", action='store_true', help="Try all regions.")
    # Exclusive Argument Group if you want supply a bucket name (or names) at the command line or use a file
    bucket_group = parser.add_mutually_exclusive_group()
    bucket_group.add_argument('--buckets', "-b", nargs="+", help="The bucket(s) you want to check")
    bucket_group.add_argument('--bucket_file', "-f", help="The bucket(s) you want to check, stored in a file.")
    # More Options
    parser.add_argument("--download", action="store_true", help="Download all files, be careful.")
    parser.add_argument("--download_folder", type=str, default=".", help="If --download is used, this where the files will go.")
    args = parser.parse_args()
    # Get the list of regions that we are going to look into.
    region_list = []
    if args.all_regions:
        region_list = DIGITAL_OCEAN_REGIONS.copy()
    elif args.regions is not None:
        region_list = args.regions.copy()
    else:
        print('You must specify at least one region with -r, or all regions with -R.')
    # Now let's sort out the buckets we will look into.
    bucket_set = set()
    if args.bucket_file is not None:
        with open(args.bucket_file, 'r', encoding="UTF-8") as buckets_file:
            for _bucket in buckets_file:
                bucket_set.add(_bucket.rstrip())
    elif args.buckets is not None:
        for user_suplied_bucket in args.buckets:
            bucket_set.add(user_suplied_bucket)
    else:
        print('You must specify at least one bucket with -b, or a file with buckets with -f')
    buckets_to_check = set()
    for bucket in bucket_set:
        for region in region_list:
            bucket_url_to_check = f"https://{bucket}.{region}.{DIGITAL_OCEAN_SPACES_URL}"
            buckets_to_check.add(bucket_url_to_check)
    found_files = set()
    for bucket_to_check in buckets_to_check:
        results = requests.get(bucket_to_check)
        bucket_url = bucket_to_check
        if not results.status_code == 200:
            pass
        else:
            for result in SPACE_REGEX.findall(results.text):
                item = result.split(">")[1].split("<")[0]
                found_files.add(f"{bucket_url}/{item}")
    if len(found_files) > 0:
        print("Found the following files:")
        print("\n".join(list(found_files)))
    else:
        print("No files found.")
    # OLD WAY
    # for bucket in args.buckets:
    #     bucket_url = f"https://{bucket}.{args.region}.{DIGITAL_OCEAN_SPACES_URL}"
    #     results = requests.get(bucket_url).text
    #     for result in SPACE_REGEX.findall(results):
    #         item = result.split(">")[1].split("<")[0]
    #         found_files.add(f"{bucket_url}/{item}")
    # print(found_files)


if __name__ == '__main__':
    main()