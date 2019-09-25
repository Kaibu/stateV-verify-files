import json
import argparse
import requests
import time
import os
import hashlib
import urllib


"""
StateV.de client_resources download/verify tool
by Kaibu (github.com/Kaibu)/Malin (github.com/halloibimsmalin)

example usage:

python hash_resources.py "C:\\RAGE\\client_resources\\185.254.96.11_22005\\" "http://185.254.96.11:4100/"
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to client_resources/IP_PORT/ folder")
    parser.add_argument("api_url", help="website hosting state.json and files in /state/")
    args = parser.parse_args()

    path = str(args.path).replace("\\", "/")
    api_url = str(args.api_url)

    hashlist = get_hash_list(api_url)

    hash_mod(path, hashlist["Files"], api_url)


#download and parse state.json file
def get_hash_list(api_url):
    headers = {
        'User-Agent': 'Update Script @Kaibu',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        content = requests.get(api_url + "/state.json", headers=headers).content.decode('utf-8')
    except requests.exceptions.RequestException as e:  # catch all errors
        print("Host unreachable, maybe wrong ip, most likely stateV outage/restart")
        exit()

    return json.loads(content)


# hash files
def hash_mod(path, hashlist, api_url):
    delete_unused_files(path, hashlist)
    print("Starting to hash/check " + str(len(hashlist)) + " files")
    start = time.time()

    results = []

    for file in hashlist:
        results.append(hash_file(path, file))

    end = time.time()
    results = list(filter(None.__ne__, results))
    print("Hashing completed in " + str(round(end - start, 4)) + "s")
    print(str(len(results)) + " files missing or wrong")

    download_mod(path, results, api_url)

#hash single file
def hash_file(path, hashfile):
    file = os.path.join(str(path), str(hashfile["UrlPath"]).replace("\\", "/"), str(hashfile["Filename"]).replace("\\", "/"))
    if not (os.path.isfile(file)):
        return hashfile
    else:
        file_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if (file_hash.lower() != hashfile["Checksum"]):
            return hashfile

#download files in list
def download_mod(path, hashlist, api_url):
    print("Starting to download " + str(len(hashlist)) + " files (unknown size, the StateV API does not tell you about filezises for some reason)")

    start = time.time()

    for file in hashlist:
        download_file(path, file, api_url)

    end = time.time()

    print("Downloaded " + str(len(hashlist)) + " files in " + str(round(end - start, 4)) + "s")

#download file
def download_file(path, hashfile, api_url):
    print(hashfile)
    file = os.path.join(str(path), str(hashfile["UrlPath"]).replace("\\", "/"), str(hashfile["Filename"]).replace("\\", "/"))

    url = str(api_url).replace("\\", "/") + "/state/" + str(hashfile["UrlPath"]).replace("\\", "/") + "/" + str(hashfile["Filename"]).replace("\\", "/")

    if not os.path.isdir(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))

    print(url)
    urllib.request.urlretrieve(url, file)

#delete unused files (only by filename rn)
def delete_unused_files(path, hashlist):
    for root, directories, filenames in os.walk((str(path))):
        for filename in filenames:
            delete = True
            for file in hashlist:
                if file["Filename"] == filename:
                    delete = False
            if delete:
                path = str(os.path.join(root, filename))
                os.remove(path)
                print("Deleted: " + str(path))

if __name__ == "__main__":
    main()