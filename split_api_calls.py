import asyncio
from multi_tool_agent.splitting_agent import split_text
from google.genai import types
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    input_text = """
    ANIMAL KINGDOM

3737

CHAPTER  4
ANIMAL KINGDOM

4.1 Basis of

Classification

4.2 Classification of

Animals

When you look around, you will observe different animals with different
structures and forms.  As over a million species of animals have been
described  till  now,  the  need  for  classification  becomes  all  the  more
important. The classification also helps in assigning a systematic position
to newly described species.

4.1 BASIS OF CLASSIFICATION

Inspite of differences in structure and form of different animals, there are
fundamental features common to various individuals in relation to the
arrangement  of  cells,  body  symmetry,  nature  of  coelom,  patterns  of
digestive, circulatory or reproductive systems. These features are used
as the basis of animal classification and some of them are discussed here.

4.1.1 Levels of Organisation

Though all members of Animalia are multicellular, all of them do not
exhibit the same pattern of organisation of cells. For example, in sponges,
the cells are arranged as loose cell aggregates, i.e., they exhibit cellular
level of organisation. Some division of labour (activities) occur among
the cells. In coelenterates, the arrangement of cells is more complex. Here
the cells performing the same function are arranged into tissues, hence is
called tissue level of organisation. A still higher level of organisation, i.e.,
organ level is exhibited by members of Platyhelminthes and other higher
phyla where tissues are grouped together to form organs, each specialised
for a particular function. In animals like Annelids, Arthropods, Molluscs,

Reprint 2025-2638

BIOLOGY

Echinoderms  and  Chordates,  organs  have
associated to form functional systems, each
system concerned with a specific physiological
function. This pattern is called organ system
level of organisation. Organ systems in different
groups of animals exhibit various patterns of
complexities. For example, the digestive system
in Platyhelminthes has only a single opening
to the outside of the body that serves as both
mouth  and  anus,  and  is  hence  called
incomplete. A complete digestive system has
two openings, mouth and anus. Similarly, the
circulatory system may be of two types:

(i) open type in which the blood is pumped
out of the heart and the cells and tissues are
directly bathed in it and

(ii) closed type in which the blood is circulated
through a series of vessels of varying diameters
(arteries, veins and capillaries).

4.1.2 Symmetry

Animals can be categorised on the basis of their
symmetry. Sponges are mostly  asymmetrical,
i.e., any plane that passes through the centre
does not divide them into equal halves. When
any plane passing through the central axis of
the body divides the organism into two identical
halves,  it  is  called  radial  symmetry.
Coelenterates, ctenophores and echinoderms
have  this  kind  of  body  plan  (Figure  4.1a).
Animals like annelids, arthropods, etc., where
the body can be divided into identical left and
right halves in only one plane, exhibit bilateral
symmetry (Figure 4.1b).

4.1.3 Diploblastic and Triploblastic

Organisation

Animals in which the cells are arranged in two
embryonic layers, an external ectoderm and
an internal endoderm, are called diploblastic
animals, e.g., coelenterates. An undifferentiated
layer,  mesoglea,  is  present  in  between  the
ectoderm  and  the  endoderm  (Figure  4.2a).

Figure  4.1  (a)    Radial  symmetry

Figure  4.1  (b)  Bilateral  symmetry

Mesoglea

Ectoderm

Endoderm

(a)

Mesoderm

(b)

Figure  4.2 Showing  germinal  layers  :

(a)  Diploblastic  (b)  Triploblastic

Reprint 2025-26ANIMAL KINGDOM

3939

Those animals in which the developing embryo has a third germinal layer,
mesoderm,  in  between  the  ectoderm  and  endoderm,  are  called
triploblastic animals (platyhelminthes to chordates, Figure 4.2b).

4.1.4 Coelom

Presence or absence of a cavity between the body
wall  and  the  gut  wall  is  very  important  in
classification. The body cavity, which is lined
by  mesoderm  is  called  coelom.  Animals
possessing coelom are called coelomates, e.g.,
annelids, molluscs, arthropods, echinoderms,
hemichordates and chordates (Figure 4.3a). In
some animals, the body cavity is not lined by
mesoderm, instead, the mesoderm is present as
scattered pouches in between the ectoderm and
endoderm.  Such  a  body  cavity  is  called
pseudocoelom and the animals possessing them
are  called  pseudocoelomates,  e.g.,
aschelminthes  (Figure  4.3b). The animals in
which  the  body  cavity  is  absent  are  called
acoelomates, e.g., platyhelminthes (Figure 4.3c).

Figure  4.3 Diagrammatic  sectional  view  of  :
(a) Coelomate (b) Pseudocoelomate
(c)  Acoelomate

4.1.5 Segmentation

In  some  animals,  the  body  is  externally  and  internally  divided  into
segments with a serial repetition of at least some organs. For example, in
earthworm, the body shows this pattern called metameric segmentation
and the phenomenon is known as metamerism.

4.1.6 Notochord

Notochord is a mesodermally derived rod-like structure formed on the
dorsal side during embryonic development in some animals. Animals with
notochord are called chordates and those animals which do not form this
structure are called non-chordates, e.g., porifera to echinoderms.

4.2 CLASSIFICATION OF ANIMALS

The broad classification of Animalia, based on common fundamental
features as mentioned in the preceding sections, is given in Figure  4.4.

Reprint 2025-2640

BIOLOGY

*Echinodermata exhibits radial or bilateral symmetry depending on the stage.

Figure  4.4    Broad  classification  of  Kingdom  Animalia  based  on  common  fundamental  features

The important characteristic features of the

different phyla are described.

4.2.1 Phylum – Porifera

Members of this phylum are commonly known
as sponges. They are generally marine and mostly
asymmetrical  animals  (Figure  4.5).  These  are
primitive multicellular animals and have cellular
level  of  organisation.  Sponges  have  a  water
transport or canal system. Water enters through
minute pores (ostia) in the body wall into a central
cavity,  spongocoel,  from  where  it  goes  out
through  the  osculum.  This  pathway  of  water
transport is helpful in food gathering, respiratory
exchange and removal of waste. Choanocytes
or collar cells line the spongocoel and the canals.
Digestion is intracellular. The body is supported
by a skeleton made up of spicules or spongin
fibres. Sexes are not separate (hermaphrodite),
i.e., eggs and sperms are produced by the same
individual.  Sponges  reproduce  asexually  by
fragmentation  and  sexually  by  formation  of
gametes. Fertilisation is internal and development
is  indirect  having  a  larval  stage  which  is
morphologically distinct from the adult.

(a)

(b)

(c)

Figure  4.5 Examples  of  Porifera  :  (a)  Sycon

(b) Euspongia  (c) Spongilla

Reprint 2025-26ANIMAL KINGDOM

4141

Examples: Sycon (Scypha), Spongilla (Fresh water sponge) and Euspongia
(Bath sponge).

4.2.2 Phylum – Coelenterata (Cnidaria)

They  are  aquatic,  mostly  marine,  sessile  or  free-swimming,  radially
symmetrical animals (Figure 4.6). The name cnidaria is derived from the

(a)

(b)

Figure  4.6 Examples  of    Coelenterata  indicating  outline  of  their  body  form  :

(a) Aurelia (Medusa) (b)  Adamsia (Polyp)

cnidoblasts  or  cnidocytes  (which  contain  the  stinging  capsules  or
nematocysts) present on the tentacles and the body. Cnidoblasts are used
for anchorage, defense and for the capture of prey (Figure 4.7). Cnidarians
exhibit tissue level of organisation and are diploblastic. They have a central
gastro-vascular cavity with a single opening, mouth on  hypostome.
Digestion is extracellular and intracellular. Some of the cnidarians, e.g.,
corals have a skeleton composed of calcium carbonate. Cnidarians exhibit
two basic body forms called polyp and medusa (Figure 4.6). The former
is a sessile and cylindrical form like Hydra, Adamsia, etc. whereas, the
latter is umbrella-shaped and free-swimming like Aurelia or jelly fish.
Those  cnidarians  which  exist  in  both  forms  exhibit  alternation  of
generations (Metagenesis), i.e., polyps produce medusae asexually and
medusae form the polyps sexually (e.g., Obelia).

Examples: Physalia (Portuguese man-of-war), Adamsia (Sea anemone),
Pennatula (Sea-pen), Gorgonia (Sea-fan) and Meandrina (Brain coral).

Figure  4.7
Diagrammatic view of
Cnidoblast

Reprint 2025-2642

BIOLOGY

4.2.3 Phylum  –  Ctenophora

Ctenophores,  commonly  known  as  sea  walnuts  or  comb
jellies are exclusively marine, radially symmetrical, diploblastic
organisms with tissue level of organisation. The body bears
eight  external  rows  of  ciliated comb  plates,  which  help  in
locomotion (Figure 4.8). Digestion is both extracellular and
intracellular.  Bioluminescence  (the  property  of  a  living
organism to emit light) is well-marked in ctenophores. Sexes
are  not  separate.  Reproduction  takes  place  only  by  sexual
means. Fertilisation is external with indirect development.

Examples: Pleurobrachia and Ctenoplana.

4.2.4 Phylum – Platyhelminthes

They  have  dorso-ventrally  flattened  body,  hence  are  called
flatworms (Figure 4.9). These are mostly endoparasites found
in animals including human beings. Flatworms are bilaterally
symmetrical, triploblastic and acoelomate animals with organ
level of organisation. Hooks and suckers are present in the
parasitic forms. Some of them absorb nutrients from the host
directly through their body surface. Specialised cells called
flame cells help in osmoregulation and excretion. Sexes are not
separate. Fertilisation is internal and development is through
many larval stages. Some members like Planaria possess high
regeneration capacity.

Examples: Taenia (Tapeworm), Fasciola (Liver fluke).

Figure  4.8 Example of
Ctenophora
(Pleurobrachia)

(a)

(b)

Figure 4.9 Examples of Platyhelminthes : (a) Tape worm (b) Liver fluke

Reprint 2025-26ANIMAL KINGDOM

4343

Male

Female

Figure  4.10 Example of

Aschelminthes:
Roundworm

4.2.5 Phylum – Aschelminthes

The  body  of  the  aschelminthes  is  circular  in
cross-section, hence, the name roundworms
(Figure 4.10). They may be freeliving, aquatic
and terrestrial or parasitic in plants and animals.
Roundworms have organ-system level of body
organisation. They are bilaterally symmetrical,
triploblastic  and  pseudocoelomate  animals.
Alimentary  canal  is  complete  with  a  well-
developed  muscular  pharynx.  An  excretory
tube removes body wastes from the body cavity
through the excretory pore. Sexes are separate
(dioecious), i.e., males and females are distinct.
Often females are longer than males. Fertilisation
is internal and development may be direct (the
young ones resemble the adult) or indirect.

Examples : Ascaris (Roundworm), Wuchereria
(Filaria worm), Ancylostoma (Hookworm).

4.2.6 Phylum – Annelida

They may be aquatic (marine and fresh water) or
terrestrial; free-living, and sometimes parasitic.
They  exhibit  organ-system  level  of  body
organisation and bilateral symmetry. They are
triploblastic,  metamerically  segmented  and
coelomate  animals.  Their  body  surface  is
distinctly  marked  out  into  segments  or
metameres  and,  hence,  the  phylum  name
Annelida (Latin, annulus : little ring) (Figure 4.11).
They possess longitudinal and circular muscles
which help in locomotion. Aquatic annelids like
Nereis possess lateral appendages, parapodia,
which help in swimming. A closed circulatory
system is present. Nephridia (sing. nephridium)
help in osmoregulation and excretion. Neural
system consists of paired ganglia (sing. ganglion)
connected by lateral nerves to a double ventral
nerve cord. Nereis, an aquatic form, is dioecious,
but earthworms and leeches are monoecious.
Reproduction is sexual.

Examples : Nereis, Pheretima (Earthworm) and
Hirudinaria (Blood sucking leech).

Figure  4.11 Examples of Annelida : (a) Nereis

(b) Hirudinaria

Reprint 2025-2644

BIOLOGY

4.2.7 Phylum  –  Arthropoda

This is the largest phylum of Animalia which
includes insects. Over two-thirds of all named
species on earth are arthropods (Figure 4.12).
They have organ-system level of organisation.
They are bilaterally symmetrical, triploblastic,
segmented and coelomate animals. The body
of  arthropods  is  covered  by  chitinous
exoskeleton. The body consists of head, thorax
and abdomen. They have jointed appendages
(arthros-joint, poda-appendages). Respiratory
organs  are  gills,  book  gills,  book  lungs  or
tracheal system. Circulatory system is of open
type.  Sensory  organs  like  antennae,  eyes
(compound  and  simple),  statocysts  or
balancing organs are present.  Excretion takes
place through malpighian tubules. They are
mostly  dioecious.  Fertilisation  is  usually
internal.  They  are  mostly  oviparous.
Development may be direct or indirect.
Examples: Economically important insects –
Apis (Honey bee), Bombyx (Silkworm), Laccifer
(Lac insect)
Vectors  –  Anopheles,  Culex  and  Aedes
(Mosquitoes)
Gregarious pest – Locusta (Locust)
Living fossil – Limulus (King crab).

4.2.8 Phylum – Mollusca

This  is  the  second  largest  animal  phylum
(Figure 4.13). Molluscs are terrestrial or aquatic
(marine or fresh water) having an organ-system
level  of  organisation.  They  are  bilaterally
symmetrical,  triploblastic  and  coelomate
animals. Body is covered by a calcareous shell
and  is  unsegmented  with  a  distinct  head,
muscular foot and visceral hump. A soft and
spongy layer of skin forms a mantle over the
visceral hump. The space between the hump
and the mantle is called the mantle cavity in
which feather like gills are present. They have
respiratory  and  excretory  functions.  The
anterior head region has sensory tentacles. The
mouth  contains  a  file-like  rasping  organ  for
feeding, called radula.

 (a)

 (b)

 (c)

 (d)

Figure  4.12 Examples  of  Arthropoda :

(a)  Locust  (b)  Butterfly
(c)  Scorpion  (d)  Prawn

(a)

Figure  4.13 Examples  of  Mollusca :

(a) Pila  (b) Octopus

(b)

Reprint 2025-26ANIMAL KINGDOM

4545

They  are  usually  dioecious  and  oviparous  with  indirect
development.
Examples: Pila (Apple snail), Pinctada (Pearl oyster), Sepia
(Cuttlefish), Loligo (Squid), Octopus (Devil fish), Aplysia (Sea-
hare), Dentalium (Tusk shell) and Chaetopleura (Chiton).

4.2.9 Phylum  –  Echinodermata

These animals have an endoskeleton of calcareous ossicles
and, hence, the name Echinodermata (Spiny bodied, Figure
4.14). All are marine with organ-system level of organisation.
The adult echinoderms are radially symmetrical but larvae
are  bilaterally  symmetrical.  They  are  triploblastic  and
coelomate animals. Digestive system is complete with mouth
on the lower (ventral) side and anus on the upper (dorsal)
side.  The  most  distinctive  feature  of  echinoderms  is  the
presence  of  water  vascular  system  which  helps  in
locomotion, capture and transport of food and respiration.
An  excretory  system  is  absent.  Sexes  are  separate.
Reproduction  is  sexual.  Fertilisation  is  usually  external.
Development is indirect with free-swimming larva.
Examples: Asterias (Star fish), Echinus (Sea urchin), Antedon
(Sea lily), Cucumaria (Sea cucumber) and Ophiura (Brittle star).

4.2.10 Phylum – Hemichordata

Hemichordata was earlier considered as a sub-phylum under
phylum Chordata. But now it is placed as a separate phylum
under  non-chordata.  Hemichordates  have  a  rudimentary
structure in the collar region called stomochord, a structure
similar to notochord.

This  phylum  consists  of  a  small  group  of  worm-like
marine animals with organ-system level of organisation. They
are  bilaterally  symmetrical,  triploblastic  and  coelomate
animals.  The  body  is  cylindrical  and  is  composed  of  an
anterior proboscis, a collar and a long trunk (Figure 4.15).
Circulatory system is of  open type. Respiration takes place
through gills. Excretory organ is proboscis gland. Sexes are
separate. Fertilisation is external. Development is indirect.

Examples: Balanoglossus and Saccoglossus.

4.2.11 Phylum – Chordata

(a)

(b)

Figure  4.14 Examples  of

Echinodermata  :
(a)  Asterias
(b) Ophiura

Proboscis

Collar

Trunk

Animals belonging to phylum Chordata are fundamentally
characterised  by  the  presence  of  a  notochord,  a  dorsal

Figure  4.15  Balanoglossus

Reprint 2025-2646

BIOLOGY

Nerve cord

Notochord

Post-anal part

Gill slits

Figure  4.16    Chordata  characteristics

hollow  nerve  cord  and  paired  pharyngeal
gill  slits  (Figure  4.16).  These  are  bilaterally
symmetrical,  triploblastic,    coelomate  with
organ-system  level  of  organisation.  They
possess a post anal tail and a closed circulatory
system.
Table  4.1  presents  a  comparison  of  salient
features of chordates and non-chordates.

TABLE  4.1  Comparison  of  Chordates  and  Non-chordates

S.No. Chordates

Notochord  present.

Non-chordates

Notochord  absent.

1.

2.

3.

4.

5.
"""
    try:
        asyncio.run(split_text(input_text=input_text))
    except Exception as e:
        print(f"An error occurred: {e}")