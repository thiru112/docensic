#!/usr/bin/python3
from sys import exit
from api.docapi import Docapi
from argumentparser.argsparser import argsparser

def main():
    args = argsparser.parse_args()
    
    dc = Docapi()

    def run(cont_id):
        if not dc.load_config():
            exit(0)

        if not dc.load_config():
            exit(0)

        if not dc.get_container_lowlevel_info(cont_id):
            exit(0)
        
        dc.get_container_process_info()
        dc.get_container_file_system_changes()
        dc.get_container_logs()
        dc.export_container_as_tarball()
        dc.get_image_corresponding_container()
        dc.get_image_history()
        dc.get_exec_info_for_contianer()
        dc.get_network_details()
        dc.extract_volume_data()

    con_id = None
    if args.container_id:
        con_id = args.container_id
    elif args.list_id:
        con_id = args.list_id
    elif args.list_containers:
        dc.load_config()
        dc.list_containers()
    elif args.version:
        print("docensic.py V 0.1")

    if type(con_id) is str:
        run(con_id)
    elif type(con_id) is list:
        for i in con_id:
            run(i)
    else:
        exit(0)

if __name__ == "__main__":
    main()