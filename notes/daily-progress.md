
### 2021 Feb 14
    - Separete champion base stats with ayumilove ranking, although same source;
    - Spiders now write json result to files;
    - Connected with remote git, did some renaming;
    - Dockerized crawler;
    - Create hdb-api container with PHP, WIP

    Evening:
    - Combined crawler with api, because:
        a) of the convenience to crawl using API, and 
        b) having problems syncing folders

        NOTE: it fails when I tried to sync two different folders (from two containers) using a same Docker Volume
        AND those two folders are both subfolders whose parent folder are also synced using other Docker Volumes

        See example below:

```
container1:
    ...
    volume:
        - somepath:/folder-in-container-1
        - volume:/folder-in-container-1/subfolder
    ...

container2:
    ...
    volume:    
        - somepath2:/folder-in-container-2
        - volume:/folder-in-container-2/subfolder
```

### 2021 Feb 07
    - git init
    - grabbing Ayumilove rank