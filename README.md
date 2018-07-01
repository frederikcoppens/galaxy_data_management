# Adding PLAZA genomes in Galaxy

Building a .yaml file to automatically add all plant genomes available in the PLAZA FTP and run data managers on it.

## How it works

- Run the Jupyter notebook in the folder genomes
  - calls the PLAZA API
  - writes genomes.yaml file
  - combines the data_managers and genomes yaml files to one
- On command line

```
  cd build
  sh build.sh
```

- alternatively:

```
  cd build
  cp build_public.sh.sample build_public.sh

  # update the content with the right url and API key

  sh build_public.sh
```

## Data managers included

- all_fasta
- bowtie2

## Requirements

- virtualenv
- docker
- others?

## Adding new data managers

edit the file data_managers.yaml and add a new item.

- how to find the ID: run it in Galaxy and check the info
- to make it work you need the version at the end of the ID !
- for the right parameters go into the wrapper in the repo of the tool (link in ToolShed)

## Known issues

- Docker instance gives error in bowtie indexing (file not found), public server did work with same script. Updating the docker image might be required
