import yaml
import re
from datetime import date

genomes = yaml.load(open('genomes.yaml'))

pattern = re.compile("ftp://ftp.psb.ugent.be/pub/plaza/(plaza_public_(.*)_(\d+))/Genomes/")

plaza_versions = {}
genome_list = {}

for genome in genomes['genomes']:

    result = pattern.match(genome['genome'])
    plaza_version = result[1]
    if plaza_version not in plaza_versions:
        plaza_versions[plaza_version] = [genome['name']]
    else:
        plaza_versions[plaza_version].append(genome['name'])

    key = plaza_version + ":" + genome['genome_id']
    genome_list[key] = genome

header = []
for plaza_version in sorted(plaza_versions.keys()):
    pattern_version = re.compile("plaza_public_(.*_\d+)")
    result = pattern_version.match(plaza_version)
    header.append(result[1])

with open("../available_genomes.md", 'w') as out:

    out.write("# PLAZA genomes\n")

    out.write("On {} the following genomes were available:\n\n".format(date.today()))
    # tabbed
    # out.write(" "*80)
    #out.write("\t".join(header))
    # out.write("\n")
    out.write("| Genome |")
    out.write(" | ".join(header))
    out.write(" |\n")
    out.write("| --- |{}\n".format(":---:|"*len(plaza_versions.keys())))

    for name, genome in genome_list.items():
        plaza_version_match = []
        for plaza_version in sorted(plaza_versions.keys()):
            if genome['name'] in plaza_versions[plaza_version]:
                plaza_version_match.append("x")
            else:
                plaza_version_match.append("")

        out.write("| {} | {}".format(genome['name'], " | ".join(plaza_version_match)))
        out.write(" |\n")
