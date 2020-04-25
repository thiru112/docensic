from argparse import ArgumentParser, RawTextHelpFormatter

argsparser = ArgumentParser(prog='Docensic',
                            description='Simple docker artifact gathering tool',
                            usage='# ./%(prog)s [optional arguments]',
                            formatter_class=RawTextHelpFormatter)

# Either -ci or -li should run, so grouping of arguments is done here
container_group = argsparser.add_mutually_exclusive_group(required=True)

# To list all the running containers in the target
container_group.add_argument('-ls', '--list_containers', action="store_true",
                        help='To list all the container in the system')

# To get artifacts for a single container by passing a container_id
container_group.add_argument('-c', '--container_id', type=str,
                            nargs=1, action='store',
                            help='To get artifacts for a partical container')

# To get artifacts for a list of containers, delimited with space
container_group.add_argument('-li', '--list_id', type=str,
                            nargs='+', action='store',
                            help='Find a artifacts for list of containers')

# To get artifacts from images
container_group.add_argument('-i', '--images', type=str,
                        nargs='+', action='store',
                        help='To get articats from the container images')

# To display the version of this tool
container_group.add_argument('-v', '--version', action='store_true',
                        help='Display version of the tool')
