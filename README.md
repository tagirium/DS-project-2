# DS-project-2

DockerHub [naming server image](https://hub.docker.com/repository/docker/tagirium/ds-project-2-naming), [storage server image](https://hub.docker.com/repository/docker/tagirium/ds-project-2-storage)

## Contents

* [Team Members and Roles](#team-members-and-roles)

* [The Problem](#the-problem)

* [The Solution](#the-solution)

* [Conclusion](#conclusion)

* [How to Run](#how-to-run)

* [Output](#output)

* [References](#references)

## Team Members and Roles

* **Jameel Mukhutdinov BS18-SE-02**

Naming Server implementation

* **Marina Nikolaeva BS18-DS-02**

Client implementation, report

* **Tagir Shigapov BS18-SE-01**

Storage Server implementation, creation Docker Images, report


## The Problem

The task is to create Distributed File System. DFS have to support file reading, writing, creation, deletion, copy, moving and info queries. It should also support certain directory operations - listing, creation, changing and deletion. Files must be replicated on multiple storage servers.

## Architectural diagram

![diagram](https://github.com/tagirium/DS-project-2/blob/main/diagram.png)

## AWS Deployment
1. Create instance, assign elastic IPs to avoid changes of IP after rebooting
2. Write IPs of your StorageServers in **active_storages** dictionary and in **storages** list (the format in dictionary - 'IP' : [ ]) 
3. Then update your OS on instance and install docker engine. More detailed instructions are [here](https://docs.docker.com/engine/install/ubuntu/)
4. Then run images by running the following code in command console **firstly, for all storages, then for naming server**:
* For storages: ''' sudo docker run -it -p 8801:8801 tagirium/ds-project-2-storage
* For naming server: ''' sudo docker run -it -p 8800:8800 tagirium/ds-project-2-naming

### Prerequisites
* Ubuntu 20.04
* 18.156.127.12 - Name server
* 18.193.5.107 - Storage Server

## How to Run
1. Change NAMING_SERVER_IP field in client.py to the ip of the Naming server
2. Start client.py
3. Type _init_
3. Type in one of the following commands:
* _file_create_ and then on a new line full path with a desired name and extension of the file
* _file_read_ and then on a new line full path of the file
* _file_write_ and then full path of the file you will send and full path of the location of the file on a server (both on new lines)
* _file_delete_ and then on a new line full path of the file
* _file_info_ and then on a new line full path of the file
* _file_copy_ and then full path of the file current location and full path of the location of the copied file(both on new lines)
* _file_move_ and then full path of the file current location and full path of the new location of the file(both on new lines)
* _dir_read_ and then on a new line full path of the directory
* _dir_make_ and then on a new line full path of the new directory with its name
* _dir_delete_ and then on a new line full path of the directory
* _quit_


## Output

![output1](https://github.com/tagirium/DS-project-2/blob/main/output1.png)

![output2](https://github.com/tagirium/DS-project-2/blob/main/output2.png)




## References

[Assignment](https://docs.google.com/document/d/1Is2QFO20RjxVrZMSMCxsBa-FUgGgaIJ7e_o3CeQKN6w/edit#)

[Naming Server](https://hub.docker.com/repository/docker/tagirium/ds-project-2-naming)

[Storage Server](https://hub.docker.com/repository/docker/tagirium/ds-project-2-storage)

