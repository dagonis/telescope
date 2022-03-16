# telescope
Scan Digital Ocean spaces!

Digital Ocean spaces are the equivalent of S3 Buckets/Azure Blobs/etc. Telescope will look in spaces (which I just call buckets) to see if there any files you may be able to download.

You can download anything you find as well, be careful with this as there might be a significant amount of data. 
## Requirements/Installation
Requires Python 3.7+ (confirmed broken on anything older)

You need requests as well, install via

`python3 -m pip install requests.txt`

or with the requirements.txt file I put in the repo

`python3 -m pip install -r requirements.txt`

## Usage
### Basic (look for $some_bucket in the region $some_region)
`python3 telescope -r $some_region -b $some_bucket`

### POWER MODE (look for $buckets in $file_of_buckets in all regions)
`python3 telescope -R -f $file_of_buckets`

### Pilfer Mode (Download all files in $some_bucket in the region $some_region into a folder called found_files)
`python3 telescope -r $some_region -b $some_bucket --download --download_folder found_files`
### Full Help
```
python3 telescope -h
usage: telescope [-h] [--regions {nyc3,sgp1,sfo2,sfo3,ams3,fra1} [{nyc3,sgp1,sfo2,sfo3,ams3,fra1} ...] | --all_regions] [--buckets BUCKETS [BUCKETS ...] | --bucket_file
                 BUCKET_FILE] [--download] [--download_folder DOWNLOAD_FOLDER]

Telescope v.1

options:
  -h, --help            show this help message and exit
  --regions {nyc3,sgp1,sfo2,sfo3,ams3,fra1} [{nyc3,sgp1,sfo2,sfo3,ams3,fra1} ...], -r {nyc3,sgp1,sfo2,sfo3,ams3,fra1} [{nyc3,sgp1,sfo2,sfo3,ams3,fra1} ...]
                        The Region(s) you want to check.
  --all_regions, -R     Try all regions.
  --buckets BUCKETS [BUCKETS ...], -b BUCKETS [BUCKETS ...]
                        The bucket(s) you want to check
  --bucket_file BUCKET_FILE, -f BUCKET_FILE
                        The bucket(s) you want to check, stored in a file.
  --download            Download all files, be careful.
  --download_folder DOWNLOAD_FOLDER
                        If --download is used, this where the files will go.
                        ```