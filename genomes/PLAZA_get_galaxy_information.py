#!/usr/bin/python3

# # Get PLAZA information for Galaxy
# 
# Get all genomes and annotations available in PLAZA data warehouse, formatted to be used by Ephemeris


import json
import os
from jinja2 import Environment
import urllib
import urllib.request
from urllib.error import HTTPError, URLError


# Template for annotations entries 
builds_j2 = """genomes:{% for build in builds %}
    - genome_id: {{ build.genome_id}}
      name: {{ build.name }}
      build_id: {{ build.build_id }}
      genome: {{ build.genome }}
      all_tx_transcriptome: {{ build.all_tx_transcriptome }}
      selected_tx_transcriptome: {{ build.selected_tx_transcriptome }}
      all_tx_tx2gene: {{ build.all_tx_tx2gene }}
      selected_tx_tx2gene: {{ build.selected_tx_tx2gene }}
      gff_selected_tx_exon_features: {{ build.gff_selected_tx_exon_features}} 
      gff_selected_tx_all_features: {{ build.gff_selected_tx_all_features}}
      gff_all_tx_all_features: {{ build.gff_all_tx_all_features}}
      gff_all_tx_exon_features: {{ build.gff_all_tx_exon_features}}
      {% endfor %}"""




# ## Getting genome information available for Galaxy through PLAZA API
plaza_api_calls = {
    # Global API call all available PLAZA instances, contains a merge of all instances.
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
            #url_transcriptome = item['fasta']['transcripts']['location']
            for transcriptome in item['fasta']['transcripts']:
                if transcriptome["used_transcripts"]=="selected_transcript":
                        selected_tx_fasta=transcriptome['location']
                if transcriptome["used_transcripts"]=="all_transcripts":
                        all_tx_fasta=transcriptome['location']
            for tx2gene in item['transcript_mapping']:
                if tx2gene['used_transcripts']=="selected_transcript":
                        tx2gene_selected_tx = tx2gene['location']	
                if tx2gene['used_transcripts']=="all_transcripts":
                        tx2gene_all_tx = tx2gene['location']
            for annotation in item['gff']:
                if annotation['used_transcripts'] == 'all_transcripts':
                        if annotation['used_features'] == 'exon_features':
                                gff_all_tx_exon_features=annotation['location']
                        if annotation['used_features'] == 'all_features':
                                gff_all_tx_all_features=annotation['location']
                if annotation['used_transcripts'] == 'selected_transcript':
                        if annotation['used_features'] == 'exon_features':
                                gff_selected_tx_exon_features=annotation['location']
                        if annotation['used_features'] == 'all_features':
                                gff_selected_tx_all_features=annotation['location']
            #print(name)
            builds[name] = { \
		'build_id': gid,\
	        'genome_id': gid,\
		'name': name,\
		'genome': url_genome,\
                'gff_all_tx_exon_features': gff_all_tx_exon_features,\
                'gff_all_tx_all_features': gff_all_tx_all_features,\
		'gff_selected_tx_exon_features': gff_selected_tx_exon_features,\
		'gff_selected_tx_all_features': gff_selected_tx_all_features,\
                'all_tx_transcriptome': all_tx_fasta,\
		'selected_tx_transcriptome': selected_tx_fasta,\
		'all_tx_tx2gene': tx2gene_all_tx,\
		'selected_tx_tx2gene': tx2gene_selected_tx,\
                }
        except TypeError:
            #print("\n!!! Not all necessary fields are provided !!!")
            #print(json.dumps(item, sort_keys=True, indent=4))
            print("\n")

        #except :
        #    print("Error")
            #print(json.dumps(item, sort_keys=True, indent=4))
        #print(json.dumps(item, sort_keys=True, indent=4))  


print("\nGenomes found on PLAZA FTP: {}".format(len(builds)))


# ## Write genomes to file
builds_list = []
for k, v in sorted(builds.items()):
    builds_list.append(v)

with open('genomes.yaml', 'w') as f:
    f.write(Environment().from_string(builds_j2).render(builds=builds_list))

genomes_dir=os.path.dirname(os.path.realpath(__file__)) 

## Get complete yaml file to use as input to ephemeris

os.system('echo "\\n" >> genomes.yaml # making sure there is a new line at the end') 
os.system('cat genomes.yaml ' + genomes_dir+ '/data_managers_genome_based.yaml > genome_data_manager_run.yaml')
os.system('cat genomes.yaml ' + genomes_dir+ '/data_managers_transcriptome_based.yaml > transcriptome_data_manager_run.yaml')
