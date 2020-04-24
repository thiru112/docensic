CONTAINERS
===============

Get container logs - GET /containers/{id or name}/logs [`DONE`]

Get changes on the container filesystem -  GET /containers/{id or name}/changes [`DONE`]

Exporting a container - GET /containers/{id or name}/export [`CONFUSION`]

List running process in the container  - GET /containers/{id or name}/top [`DONE`]

Inspect a container - GET /container/{id or name}/json [`DONE`]

Create a new image from a container - POST /commit [with paramters refer docs] [`CONFUSION`]

Export a container - GET /containers/{id}/export [`CONFUSION`]
	

IMAGES
=======

Inspect an images -  GET /images/{image_name}/json [`DONE`]

Get the history of an image - GET /images/{image_name}/history [`DONE`]

EXEC
======

Inspect an exec instance id associated with the contianers [`DONE`]

VOLUMES
=======

Inspect the volume for corresponding container [`TO_DO`]

You can gain more information from the low-level information of the container [`??`]


NETWORKS
=========

Inspect a network for a corresponding container and get the mac and ip addresss and the 
network to which it was connected, and all the container that was connected to the network ID [#DONE]


OTHER_ARTIFACTS
===============

Extracting other artifacts such as VOLUME data, /etc/passwd and others [`IN_PROCESS`]

`http://localhost:5555/containers/mysql01/archive?path=/var/lib/mysql`


MISC
=====
Check what is sandbox_id, Endpoint ID and also about docker volumes [`NOT_GONNA_WORK`]