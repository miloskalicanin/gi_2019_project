# Projektni zadatak iz predmeta Genomska informatika

Boyer-Moore algoritam koristi heuristike (Bad character and Good suffix rule) za preskakanje nepotrebnih poređenja karaktera pri pretraživanju. Definisati na sličan način dve heuristike (heuristika 1 i heuristika 2) koje mogu biti primenjivane za sračunavanje maksimalno dozvoljenog pomeraja. Za formiranje heuristika koristiti samo patern - algoritam treba da ostane on-line (10 poena).

Izvršiti merenje i poređenje vremena izvršavanja i memorijskog zauzeća seta on-line Exact Matching algoritama:
* Boyer-Moore - Heuristika 1 + Heuristika 2
* Boyer-Moore - Heuristika 1
* Boyer-Moore - Heuristika 2
* Boyer-Moore - Strong good suffix rule and bad character rule

Napisati wrapper funkciju ili klasu u programskom jeziku Python koja ima mogućnost izvršavanja zadate varijante algoritma na osnovu ulaznog parametra. Kao test podatke koristiti 3 seta podataka (5 poena):
  1. Tekst: Coffea arabica, Chromosome 1c i paterni: ATGCATG, TCTCTCTA, TTCACTACTCTCA (ftp://ftp.ncbi.nlm.nih.gov/genomes/Coffea_arabica/CHR_1c/13443_ref_Cara_1.0_chr1c.fa.gz)
  2. Tekst: Mus pahari chromosome X, i paterni: ATGATG, CTCTCTA, TCACTACTCTCA (ftp://ftp.ncbi.nlm.nih.gov/genomes/Mus_pahari/CHR_X/10093_ref_PAHARI_EIJ_v1.1_chrX.fa.gz)
  3. Genom po slobodnom izboru iz NIH baze i proizvoljna 3 paterna različite dužine. (ftp://ftp.ncbi.nlm.nih.gov/genomes/)

Dobijene rezultate predstaviti tabelarno i grafički (Python matplotlib). Grafički način (dijagram) treba da bude dovoljno intuitivan da onaj koji ga čita može brzo izvući potrebne zaključke vezane za performanse zadatih varijanti algoritama (5 poena).

Za svaku od funkcija u kodu napisati testove (5 poena).

Pripremiti prezentaciju (Google slides ili power point) algoritama koji se testiraju, kao i samih rezultata (5 poena).

Pripremiti video prezentaciju projekta (3 - 5 minuta trajanja) koja će biti dostupna na YouTube ili drugom video servisu na kojem mu je moguće pristupiti (10 poena).


## Uputstvo za pokretanje benchmark-a:

- Test primeri treba se nalaze u test direktorijumu. Inicijalno se tu nalaze upakovane verzije fajlova nad kojima se test izvrsava. Da bi se pokrenulo testiranje potrebno ih je raspakovati i modifikovati prema uputstvu koje je dato u nastavku.
- Test primere je potrebno modifikovati tako da se u prvom redu nalaze paterni. Ako paterna ima vise potrebno ih je odvojiti zarezom, bez razmaka. Primer: patern1,patern2,...,paternN.
- Od drugog reda treba da se nalazi string koji se pretrazuje.
- Ako korisnik zeli da doda svoj test, dovoljno je samo da doda fajl u gore pomenutom obliku u test direktorijum. Program je prilagodjen da sam iscrtava grafike na osnovu sadrzaja test direktorijuma.
- Da bi se izvrsilo testiranje neophodno je pokrenuti fajl benchmark.py.


## Video prezentacija
Video prezentacija je dostupna na Youtube servisu preko linka: https://youtu.be/lC5LGlFL2N8
