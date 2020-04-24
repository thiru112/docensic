#!/usr/bin/python3
from api.docapi import Docapi
from argumentparser.argsparser import argsparser

def main():
    argsparser.parse_args()
    
    dc = Docapi()

    if not dc.load_config():
        exit(0)

    dc.get_container_lowlevel_info('mysql01')

if __name__ == "__main__":
    main()