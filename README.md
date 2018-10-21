# Adding PLAZA genomes in Galaxy

Building a set of .yaml files that can be used as input for ephemeris to automatically add all plant genome build available in the PLAZA data warehouse and run the index-building data managers on these.

## How it works


### To install the data in a running instance:

- Install the required data managers (located in data_managers.yaml.lock). This file is ready to be used with ephemeris:
     shed-tools install -t genomes/data_managers_list.yaml.lock -g $GALAXY_URL -a $API_KEY


- Run genomes/PLAZA_get_galaxy_information.py. This script calls the PLAZA API to retrieve updated genome information and writes 2 output files:
	- genomes.yaml file: This contains a yaml-structured file with all the information retrieved.
	- ################# TODO : EDIT Writes 2 files (genome_data_manager_run.yaml and transcriptome_data_manager_run.yaml) combining the different data managers lists with the genomes yaml files. These files are ready to be used by ephemeris to install the data.//

- Run the data managers. 
 - This is done in 2 steps:
	- Run the genomes dependant data managers (genome_data_manager_run.yaml): This creates the corresponding entries in the dbkeys table, installs the genomes fasta files and runs the index on these:
		run-data-managers --config genome_data_manager_run.yaml -g $ -a $API_KEY
        - Run the transcriptome dependant data managers (transcriptome_data_manager_run.yaml): This installs the transcriptomes, linking them with the previoisly created dbkey, installs the gff and other annotation related files, and finally creates the corresponding indexes based on these files. 
		


### To deploy a docker-based Galaxy instance and install the data there:
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
