# Adding PLAZA genomes in Galaxy

Building a set of .yaml files that can be used as input for ephemeris to automatically add all plant genome build available in the PLAZA data warehouse and run the index-building data managers on these.

## How it works


### To install the data in a running instance:

- Install the required data managers (located in data_managers.yaml.lock). This file is ready to be used with ephemeris:
  ```bash
     shed-tools install -t genomes/data_managers_list.yaml.lock -g $GALAXY_URL -a $API_KEY
  ```

- Run `genomes/PLAZA_get_galaxy_information.py`. This script calls the PLAZA API to retrieve updated genome information and writes the output in predefined files:
	- `genomes.yaml` file: This contains a yaml-structured file with all the information retrieved.
	- `genome_data_manager_run.yaml` and `transcriptome_data_manager_run.yaml`: These files combines the genome builds information in genomes.yaml with the different data managers configuration in a way that makes these directly usable by ephemeris to install the data.

- Run the data managers.This is done in 2 steps:
  - Run the genome dependant data managers (genome_data_manager_run.yaml): This creates the corresponding entries in the dbkeys table, installs the genomes fasta files, annotations, and runs the index on these: 
  ```bash
  run-data-managers --config genome_data_manager_run.yaml -g $GALAXY_URL -a $API_KEY
  ```
  - (OPTIONAL) If you also want to install the transcriptomes and indexes associated with these, run the transcriptome dependant data managers (transcriptome_data_manager_run.yaml). This installs the transcriptomes, linking them with the previoisly created dbkey, and finally creates the corresponding indexes based on these files:
  ```bash
  run-data-managers --config transcriptome_data_manager_run.yaml -g $GALAXY_URL -a $API_KEY
  ```


### To deploy a docker-based Galaxy instance and install the data there:
- On command line

  ```bash
    cd build
    sh build.sh
  ```

- alternatively:

  ```bash
    cd build
    cp build_public.sh.sample build_public.sh

    # update the content with the right url and API key

    sh build_public.sh
  ```


## Requirements

- python3
- docker: In case of deploying a docker-based Galaxy instance.
- ephemeris, which can be installed in different ways.
  - Install directly from repo src code. This has the advantage of installing the latest version, which is much faster to deploy a large number of genomes:
    ```bash
       pip install -e git+https://github.com/galaxyproject/ephemeris.git@dm#egg=ephemeris
    ```
  - Install with conda (use Miniconda3 in order to prevent conflicts with python3 ):
     ```bash
       conda create --channel bioconda --name ephemeris ephemeris 
       source ~/miniconda2/bin/activate ephemeris
     ```
  - Install inside a python virtualenv:
     ```bash
       virtualenv .venv
       . .venv/bin/activate
       pip install -U pip
       pip install -e git+https://github.com/galaxyproject/ephemeris.git@dm#egg=ephemeris
     ```
- The run-data-managers methods in ephemeris requires the "watch_tool_data_dir” setting in galaxy.ini to be True (see https://ephemeris.readthedocs.io/en/latest/commands/run-data-managers.html) when running multiple data managers that are interdependent, as is the case with genome_data_manager_run.yaml and transcriptome_data_manager_run.yaml.
  
  
## Adding new data managers

New data managers can be added to `genomes/data_managers_genome_based.yaml` or `genomes/data_managers_transcriptome_based.yaml`, after running `genomes/PLAZA_get_galaxy_information.py` these will be added in the corresponding conf file to be used with ephemeris.

- how to find the ID: run it in Galaxy and check the info
- to make it work you need the version at the end of the ID!
- for the right parameters go into the wrapper in the repo of the tool (link in ToolShed)

## Known issues

- Docker instance gives error in bowtie indexing (file not found), public server did work with same script. Updating the docker image might be required
