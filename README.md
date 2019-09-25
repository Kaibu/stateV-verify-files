# StateV.de client_resources download/verify tool

I got sick of downloading the whole folder all the time so I made this to check for changed files or verify them.

It uses the md5 checksum provided by their API to validate the files.

What it does:

- checks for files that are not used anymore (only by name rn)
- hashes all existing files and queues all the missing/wrong ones to download
- downloads the missing files

Currently not multithreaded to allow for easier .exe compiling (most tools for that don't like multithreading)

## example usage

```
python hash_resources.py "C:\\RAGE\\client_resources\\185.254.96.11_22005\\" "http://185.254.96.11:4100/"
```