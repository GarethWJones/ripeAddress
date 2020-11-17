# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 21:42:54 2020

@author: Gareth W. Jones
"""

import base58check
import binascii
import argparse
from hashlib import sha256

"""
To create a BTC address, the wallet holder's public ECDSA key is required.  The RIPEMD-16 hash
is initially calculated from the SHA-256 hash of the public key.  Unless you have some insane
computing power, you will not be able to get the public key from the RIPEMD-16 hash.

To go from the RIPEMD-16 hash to the BTC address, simply prepend '00' to the hash, then take the
SHA-256 of that (un-hexed), then take the SHA-256 hash of the previous hash.  Then take the first
four bytes of the second hash and append them to the '00'+RIPEMD-16 hash.  Finally, encode it with
base58 encoding and you have a BTC address.
"""

def toAddress(ripe):
    netBytes = "00"+ripe
    firstSHA = sha256(binascii.unhexlify(netBytes)).hexdigest()
    secondSHA = sha256(binascii.unhexlify(firstSHA)).hexdigest()
    firstFour = secondSHA[:8]
    hexa = netBytes+firstFour
    address = base58check.b58encode(binascii.unhexlify(bytes(hexa, "utf-8")))
    return str(address)

"""
To go back from a BTC to a RIPEMD-16 hash, simply decode the base58 encoded address, then take off
the '00' at the beginning and the last four bytes - that's why it's encoded into hex bytes.
"""

def toRipeMD16(address):
    hexa = binascii.hexlify(base58check.b58decode(address))
    return hexa[2:-8]

def main():
    parser = argparse.ArgumentParser(description="Find a BTC from a RipeMD16 hash and vice versa by Gareth W. Jones")
    parser.add_argument("--findHash", dest="addrFile", type=str, help="Supply BTC address file to find RipeMD16 hashes.")
    parser.add_argument("--findAddress", dest="hashFile", type=str, help="Supply RipeMD16 file to find BTC addresses.")
    parser.add_argument("-o", dest="outFile", type=str, help="Supply output filename you wish to write results to.")
    args = parser.parse_args()
    
    if args.outFile == None:
        parser.print_help()
        exit(0)
    
    if args.addrFile == None and args.hashFile == None:
        parser.print_help()
        exit(0)
    
    if args.addrFile == None:
        pass
    else:
        f = open(args.addrFile, "r")
        g = open(args.outFile, "w")
        for i in f.readlines():
            if "\n" in i:
                newLine = toRipeMD16(i[:-1]).upper()
            else:
                newLine = toRipeMD16(i).upper()
            g.write(str(newLine)[2:-1]+"\n")
        f.close()
        g.close()
        print("Done!  Please see output in "+args.outFile+".  Exiting...")
    
    if args.hashFile == None:
        pass
    else:
        f = open(args.hashFile, "r")
        g = open(args.outFile, "w")
        for i in f.readlines():
            if "\n" in i:
                newLine = toAddress(i[:-1])
            else:
                newLine = toAddress(i)
            g.write(str(newLine)[2:-1]+"\n")
        f.close()
        g.close()
        print("Done!  Please see output in "+args.outFile+".  Exiting...")


if __name__ == "__main__":
    main()