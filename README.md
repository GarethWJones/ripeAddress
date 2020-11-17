# ripeAddress

## Convert BTC addresses to the RIPEMD-16 hashes they were calculated from and vice versa.

### About

To create a BTC address, the wallet holder's public ECDSA key is required.  The RIPEMD-16 hash
is initially calculated from the SHA-256 hash of the public key.  Unless you have some insane
computing power, you will not be able to get the public key from the RIPEMD-16 hash.

To go from the RIPEMD-16 hash to the BTC address, simply prepend '00' to the hash, then take the
SHA-256 of that (un-hexed), then take the SHA-256 hash of the previous hash.  Then take the first
four bytes of the second hash and append them to the '00'+RIPEMD-16 hash.  Finally, encode it with
base58 encoding and you have a BTC address.

To go back from a BTC to a RIPEMD-16 hash, simply decode the base58 encoded address, then take off
the '00' at the beginning and the last four bytes - that's why it's encoded into hex bytes.

### Help and Usage

* --findHash, Supply BTC address file to find RipeMD16 hashes.
* --findAddress, Supply RipeMD16 file to find BTC addresses.
* -o, Supply output filename you wish to write results to.

python3 ripeAddress.py --findHash {hash file} -o {output file name}
python3 ripeAddress.py --findAddress {BTC address file} -o {output file name}

**The input files must have one hash per line, or one BTC address per line.**

This script is for Python 3 and requires the following libraries:

* base58check
* binascii
* argparse
* hashlib

**This has not yet been tested on Linux.**
