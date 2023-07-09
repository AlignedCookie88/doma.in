import socket
import argparse
import os
import threading
import requests

def download_tlds():
    r = requests.get("https://data.iana.org/TLD/tlds-alpha-by-domain.txt", timeout=500)
    f = open("tlds.txt", "w+")
    f.truncate(0)
    f.write(r.text)
    f.close()

def is_domain_taken(domain: str) -> bool:
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False

def parse_tlds() -> list:
    if not os.path.isfile("tlds.txt"):
        raise Exception("Missing tlds.txt file. Use the --download argument to download the file.")
    out = []
    f = open("tlds.txt", "r")
    for line in f.readlines():
        if line[0] == "#":
            continue
        if line.startswith("XN--"):
            continue
        out.append(line.lower().strip())
    f.close()
    return out

def generate_domains(words: list, log: bool = False) -> list:
    tlds = parse_tlds()
    out = []
    amount = len(words)
    _id = 0
    for word in words:
        word = word.lower()
        if log:
            _id = _id +1
            percentage = (_id/amount)*100
            print(f"({percentage:.2f}%) Finding domains for '{word}'...")
        for tld in tlds:
            if word.endswith(tld):
                domain = word[:-len(tld)]+"."+tld
                if not domain.startswith("."):
                    out.append(domain)
        #common_tlds = [".com", ".net", ".org", ".me"]
        #for tld in common_tlds:
        #    out.append(word+tld)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='doma.in',
                        description='A generator for short domains with dots.',
                        epilog='If you want more in-depth help, README.md exists for a reason!')

    parser.add_argument("--download-tlds", action="store_true", dest="download",
                        help="Download an up-to-date list of TLDs and exit.")
    parser.add_argument("-g", "--generate", metavar="TEXT", dest="generation_text", nargs="*", default=[],
                        help="Generates a list of domains based on the inputted text. Can be used multiple times.")
    parser.add_argument("-d","--dns-check", action="store_true", dest="dns_check",
                        help="Checks if each domain has a valid A record, if it does it is eliminated from the output.")
    parser.add_argument("--outfile", metavar="FILE", type=argparse.FileType("w+"), dest="outfile",
                        help="Dumps the domains found to a file. The domains are seperated by newlines.")
    parser.add_argument("--dictionary", action="store", dest="dictionary", default=0, type=int, metavar="LENGTH",
                        help="Adds all the words in the english dictionary with a length equal or below the input as a -g argument.")

    args = parser.parse_args()

    if args.download:
        print("Downloading TLDs...")
        download_tlds()
        print("Done!")
        quit()
    
    words = args.generation_text

    if args.dictionary:
        print("Grabbing dictionary...")
        from english_words import get_english_words_set
        dictionary = get_english_words_set(['web2'], lower=True)
        for word in dictionary:
            if len(word) <= args.dictionary:
                words.append(word)
    
    print("Generating domains...")
    domains = generate_domains(words, False)

    if args.dns_check:
        print("Checking DNS...")
        if len(domains) > 10:
            print("More than 10 domains found, splitting DNS check into multiple threads!")
            checks = []
            _id = 0
            currentcheck = []
            for domain in domains:
                currentcheck.append(domain)
                _id = _id + 1
                if _id == 10:
                    _id = 0
                    checks.append(currentcheck)
                    currentcheck = []
            if not len(currentcheck) == 0:
                checks.append(currentcheck)
        else:
            checks = [domains]

        threads = []
        out = []
        def threaded_check(_in, out):
            for domain in _in:
                if not is_domain_taken(domain):
                    out.append(domain)
        
        for check in checks:
            thread = threading.Thread(target=threaded_check, args=(check, out), daemon=True)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    
        domains = out

    if args.outfile:
        print("Writing domains to file...")
        args.outfile.truncate(0)
        args.outfile.write("\n".join(domains)+"\n")
        args.outfile.close()
        print("Done!")
    else:
        print("\n".join(domains))