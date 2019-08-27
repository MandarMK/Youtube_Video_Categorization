
eXtended WordNet Domains (XWND)
-------------------------------

eXtended WordNet Domains (XWND) (Gonzalez-Agirre et al. 2012a, 2012b), a result of KNOW2 (TIN2009-14715-C04-01) project, is an ongoing work aiming to automatically improve WordNet Domains (Magnini and Cavaglià 2000, Bentivogli et al. 2004) (http://wndomains.fbk.eu/).

First, the original domain labels have been projected to WordNet 3.0 using the automatic mappings across WordNet versions. Since the automatic mapping is not complete (there are new synsets, changes in the structure, etc.), many synsets were left unlabeled. Thus, we carried out a simple inheritance process through the nominal and verbal hierarchies. Finally, we applied UKB (http://ixa2.si.ehu.es/ukb) to propagate the domain information through the WordNet structure. We used as a graph the one obtained from the WordNet relations enriched with relations between glosses. Instructions for preparing the binary graphs for UKB using WordNet relations are inside the UKB package. We compared the quality of both resources (the original labelling and the new one) in a common Word Sense Disambiguation task. As a gold-standard dataset, we used a random subset of 933 disambiguated words from the semantically disambiguated WordNet glosses (http://wordnet.princeton.edu/glosstag.shtml). This sample is also available within this package. The results show that the new labeling clearly outperform the original one by a large margin.

For more details on the XWND, including references to the original resources, please consult the following papers:

Gonzalez-Agirre A., Castillo M. and Rigau G. A graph-based method to improve WordNet Domains. Proceedings of 13th International Conference on Intelligent Text Processing and Computational Linguistics (CICLING'12). New Delhi, India. 2012.

Gonzalez-Agirre A., Castillo M. and Rigau G. A proposal for improving WordNet Domains. 8th international conference on Language Resources and Evaluation (LREC'12). Istambul, Turkey. 2012.

which can be downloaded at:
http://adimen.si.ehu.es/~rigau/publications/cicling12-gcr.pdf

Contents of the distribution
----------------------------

The current distribution of XWND consists of the following directories and files:

gloss/	    		 Evaluation dataset
README.txt               README file
xwnd-30g/		 Extended WordNet Domains using as a graph WN3.0 relations plus gloss relations

xwnd-30g
========

This directory consists of 170 files, one for each of the original WordNet Domains (WND). Each file contains a vector of 117,536 synsets sorted by weight, from highest lo lowest. Thus, the most representative synsets for a given domain are at the top positions. 

For instance, the first five lines of the file acoustics.ppv correspond to the first synset-weight pairs:

05718254-n    0.00686642
04981941-n    0.00580583
01452593-a    0.00475399
04985198-n    0.00458723
01213197-a    0.00452205
...

Each synset is identified in the format 'xxxxxxxx-y', where "xxxxxxxx" is a 8 digit offset number and their offset and "y" represents the part of speech: 'n' corresponds to noun, 'v' to verb, 'a' to adjective and 'r' to adverb.  For instance, the first line of this file, means that the nominal synset 05718254 <sound_2 auditory_sensation_1> having the gloss 'the subjective sensation of hearing something' has been labeled with the acoustics domain with the highest weight (0.00686642). 

gloss
=====

This directory contains	two files. The first one wnet30+g.v3.random.contexts contains the 933 random contexts selected from the semantically disambiguated WordNet glosses (http://wordnet.princeton.edu/glosstag.shtml) to be used as an evaluation dataset. The contexts follow the format used by UKB package (http://ixa2.si.ehu.es/ukb). For instance, the first context of the file wnet30+g.v3.random.contexts is:

ctx_00031921-n(belong_to#v#wf3#02719930-v)
00031921-n#n#wf0#2 00002137-n#n#wf2#2 belong_to#v#wf3#1 00356926-a#a#wf6#2 00001740-n#n#wf9#2 part#n#wf11#1 together#r#wf12#1

This means that	the first context corresponds to synset 00031921-n <relation_1> having the gloss 'an abstraction belonging to or characteristic of two entities or parts together'. The context identifier also contains the target word selected for the evaluation. In this case, the verb 'belong_to'. In the original semantically disambiguated WordNet glosses from Princeton, the selected synset for that word is 02719930-v.

The second file wnet30+g.v3.random.contexts.keys contains the gold-standard sorted list of 933 context and keys necessary for the senseval3 scorer (http://www.senseval.org/senseval3/scoring). 

License
-------

This package is distributed under Attribution 3.0 Unported (CC BY 3.0) license. You can find it at http://creativecommons.org/licenses/by/3.0

References
----------

Bentivogli L., Forner P., Magnini B. and Pianta E. Revising WordNet Domains Hierarchy: Semantics, Coverage, and Balancing. in COLING 2004 Workshop on "Multilingual Linguistic Resources", Geneva, Switzerland, August 28, 2004, pp. 101-108.

Gonzalez-Agirre A., Castillo M. and Rigau G. A graph-based method to improve WordNet Domains. Proceedings of 13th International Conference on Intelligent Text Processing and Computational Linguistics (CICLING'12). New Delhi, India. 2012.

Gonzalez-Agirre A., Castillo M. and Rigau G. A proposal for improving WordNet Domains. 8th international conference on Language Resources and Evaluation (LREC'12). Istambul, Turkey. 2012.

Magnini B. and Cavaglià G. Integrating Subject Field Codes into WordNet. in Gavrilidou M., Crayannis G., Markantonatu S., Piperidis S. and Stainhaouer G. (Eds.) Proceedings of LREC-2000, Second International Conference on Language Resources and Evaluation, Athens, Greece, 31 May - 2 June, 2000, pp. 1413-1418.

Additional information
----------------------

Ongoing development work on the XWND is done by a small group of researchers. Since our resources are VERY limited, we request that you please confine correspondence to the XWND topics only. Please check carefully this documentation and other resources to answer to your question or problem before contacting us.

English Princeton WordNet:
http://wordnet.princeton.edu

EuroWordNet project:
http://www.illc.uva.nl/EuroWordNet

WordNet Domains:
http://wndomains.fbk.eu

KNOW2 project:
http://ixa.si.ehu.es/know2

eXtended WordNet Domains:
http://adimen.si.ehu.es/web/XWND

Research groups involved
------------------------

IXA	http://ixa.si.ehu.es

Contact information
-------------------

German Rigau
IXA Group
University of the Basque Country
E-20018 San Sebastián

Version 1.0. Last updated: 2012/11/28
