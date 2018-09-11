#!/usr/bin/python3

# # Get PLAZA information for Galaxy
# 
# Get all genomes and annotations available in PLAZA v4, formatted to be used in Galaxy
# The genome annotations were curated so they always match the genome info


import json
import os
from jinja2 import Environment
import urllib
import urllib.request
from urllib.error import HTTPError, URLError


# Template for genomes entries 
#genome_j2 = """genomes:{% for genome in genomes %}
#    - url_genome: {{ genome.url_genome }}
#      name: {{ genome.name }}
#      id: {{ genome.id }}{% endfor %}"""



# Template for annotations entries 
builds_j2 = """genomes:{% for build in builds %}
    - genome_id: {{ build.genome_id}}
      name: {{ build.name }}
      build_id: {{ build.build_id }}
      genome: {{ build.url_genome }}
      transcriptome: {{ build.url_transcriptome }}
      gff_annotations: 	
          {% for key, value in build.annotations.items() -%} 
              {{key}}: {{value}} 
          {% endfor -%}
      {% endfor %}"""


      #url_annotation_all_tx_all_features : {{ build.url_annotation_all_tx_all_features }}
      #url_annotation_all_tx_exon_features : {{ build.url_annotation_all_tx_exon_features }}
      #url_annotation_rep_tx_all_features : {{ build.url_annotation_rep_tx_all_features }}
      #url_annotation_rep_tx_exon_features : {{ build.url_annotation_rep_tx_exon_features }}

# ## Getting genome information available for Galaxy through PLAZA API

plaza_api_calls = {
    # Global API call all available PLAZA instances, merges the results,
    'plaza_global': 'https://bioinformatics.psb.ugent.be/plaza/api/get_species_data'

    #instance specific calls     
    #'dicots_v4': 'https://bioinformatics.psb.ugent.be/plaza/versions/plaza_v4_dicots/api/get_species_data'
    #'monocots_v4': 'https://bioinformatics.psb.ugent.be/plaza/versions/plaza_v4_monocots/api/get_species_data"'
}


call_results = []

for key, api_call in plaza_api_calls.items():
    print("Getting info for {}".format(key))
    try:
        with urllib.request.urlopen(api_call) as response:
            html = response.read()
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        pass
    plaza_list = json.loads(html.decode('utf-8'))
    call_results.append(plaza_list)


builds={}
for plaza_list in call_results:

    for item in plaza_list: 
        print(item['common_name'])

        
        if item['eco_type'] == None:
            name = "{common_name} {version}".format(**item)
            gid = "{common_name} {version}".format(**item).replace(' ','_')
        else:
            name = "{common_name} {eco_type} {version}".format(**item)
            gid = "{common_name} {eco_type} {version}".format(**item).replace(' ','_')
        if name in builds:
            print("\tGenome for {} already captured".format(item['common_name']))
            continue

        try:
            url_genome = item['fasta']['genome']['location']
            url_transcriptome = item['fasta']['transcripts']['location']
	    #GFFs list:
            annotations_entries= {}
            for annotation in item['gff']:
                annotation_type = annotation['used_transcripts'] + '_' + annotation['used_features'] 
                location = annotation['location']
                annotations_entries[annotation_type]=location
            #print(name)
            builds[name] = { \
		'build_id': gid,\
	        'genome_id': gid,\
		'name': name,\
		'genome': url_genome, \
                'transcriptome': url_transcriptome,\
                'annotations': annotations_entries, \
		#'url_annotation_all_tx_all_features': url_annotation_all_tx_all_features,\
		#'url_annotation_all_tx_exon_features' :url_annotation_all_tx_exon_features,\
		#'url_annotation_rep_tx_all_features': url_annotation_rep_tx_all_features,\
		#'url_annotation_rep_tx_exon_features': url_annotation_rep_tx_exon_features,\
                }
        except TypeError:
            #print("\n!!! Not all necessary fields are provided !!!")
            #print(json.dumps(item, sort_keys=True, indent=4))
            print("\n")

        except :
            print("Error")
            #print(json.dumps(item, sort_keys=True, indent=4))
        #print(json.dumps(item, sort_keys=True, indent=4))  


print("\nGenomes found on PLAZA FTP: {}".format(len(builds)))


# ## Write genomes to file


#genome_list = []
builds_list = []
#for k, v in sorted(genomes.items()):
#    genome_list.append(v)

for k, v in sorted(builds.items()):
    builds_list.append(v)

print(len(builds_list))
with open('genomes.yaml', 'w') as f:
#    f.write(Environment().from_string(genome_j2).render(genomes=genome_list))
#    f.write('\n\n')
    f.write(Environment().from_string(builds_j2).render(builds=builds_list))


## Get complete yaml file to use as input to ephemeris

os.system('echo "\\n" >> genomes.yaml # making sure there is a new line at the end') 
os.system('cat genomes.yaml data_managers.yaml > genome_data_manager.yaml')

