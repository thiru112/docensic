#!/usr/bin/python3
from api.docapi import Docapi
from argsparser import argsparser

def main():
    argsparser.parse_args()
    
    dc = Docapi()

    dc.load_config()


if __name__ == "__main__":
    main()