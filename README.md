# fof-locomotor-capacity-cohort
Analysis code and reproducibility materials for a 12-month cohort study on fear of falling (FOF) and locomotor capacity in older adults. Includes R scripts, Quarto manuscript, and synthetic test data. No restricted patient data included.

## Tarkoitus
Tämä on tutkimuskohtainen R- ja Quarto-pohjainen analyysirepositorio, jonka tarkoituksena on dokumentoida 12 kuukauden kohorttianalyysi. Repositorio tekee näkyväksi analyysien, taulukoiden, kuvioiden ja lisämateriaalien yhteydet toisiinsa. MVP sisältää turvallisen scaffold-rakenteen, synteettistä testidataa ja migroidun K50-analyysiytimen. Oikeaa osallistujatason dataa ei säilytetä tässä repositoriossa.

> **No protected participant-level data or protected analytical results are published in this repository.**

## A1/K50:n nykytila

A1/K50:n tieteellinen vaihe on suljettu tilassa
`CLOSED_WITH_DEFERRED_SCIENTIFIC_ITEMS`. Normatiivinen päätös- ja
rajausrekisteri on [docs/project_specification.md](docs/project_specification.md#14-a1k50-scientific-phase-closeout).

Puolustettavissa oleva väite on: “A1/K50 conforms structurally and
methodologically to the currently Owner-approved analysis contracts, with z3
coverage, final cohort semantics, and scientific approval of the 0.40 producer
threshold explicitly deferred.” Tämä ei tarkoita numeerista pariteettia,
toistamista, vaikutusekvivalenssia, täydellistä validointia tai kliinistä
validiteettia eikä anna julkaisu-, disclosure-, data-egress- tai
retention-hyväksyntää.

## Repository Tree
```
fof-locomotor-capacity-cohort/
├── AGENTS.md
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── .gitignore
├── .Rprofile
├── DESCRIPTION
├── fof-locomotor-capacity-cohort.Rproj
├── _quarto.yml
├── R/
│   ├── functions/
│   └── transform_locomotor_indicators.R
├── scripts/
│   ├── K50/
│   └── 01_generate_synthetic_fixture.R
├── data/
│   ├── README.md
│   └── synthetic/
│       └── synthetic_fixture.csv
├── manuscript/
│   └── smoke_test.qmd
├── outputs/
│   ├── tables/
│   └── figures/
├── tests/
│   ├── testthat.R
│   └── testthat/
│       └── test_transform_locomotor_indicators.R
└── docs/
    ├── project_specification.md
    ├── k50_migration_provenance.md
    ├── reproducibility_scope.md
    └── restricted_data_policy.md
```

## Ympäristön palauttaminen ja riippuvuudet
Projektin riippuvuuksien auktoriteetti on `DESCRIPTION`. Projektissa ei ole
aktiivista `renv`-ympäristöä eikä target-kohtaista `renv.lock`-tiedostoa.

R-testit toimivat natiivissa Termux-ympäristössä. Quarto-renderöinti suoritetaan
Ubuntu PRoot -ympäristössä, jotta Quarto, R ja niiden kirjastot käyttävät samaa
glibc-runtimea. Smoke-renderöinnissä validoidussa ympäristössä oli R 4.5.2 ja
Quarto 1.9.38 ARM64-alustalla. Koko R-testiketju edellyttää, että kaikki
`DESCRIPTION`-riippuvuudet on ensin asennettu samaan PRoot-ympäristöön.

Käynnistä Ubuntu PRoot ja rajaa ympäristö GNU/Linux-polkuihin:

```bash
proot-distro login --shared-home ubuntu -- \
  env -u PREFIX -u LD_PRELOAD -u LD_LIBRARY_PATH \
  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  /bin/bash --noprofile --norc
```

CRAN toimittaa tämän ympäristön paketit lähdekoodina. PRootissa pitää siksi olla
R-lähdepakettien kääntämiseen soveltuva toolchain (`make`, C/C++- ja
Fortran-kääntäjät sekä CMake). Ubuntussa tarvittavan perustan tarjoavat
`r-base-dev` ja `cmake`. Järjestelmäpakettien asentaminen muuttaa PRootia ja
vaatii erillisen ympäristökohtaisen hyväksynnän.

Asenna hyväksytyt build-prerequisitet Ubuntu PRootissa:

```bash
apt-get update
apt-get install --no-install-recommends r-base-dev cmake
```

Kun build-prerequisitet ovat saatavilla, siirry repositoryn juureen ja asenna
`DESCRIPTION`issa ilmoitetut runtime-, testi- ja renderöintiriippuvuudet
hyväksytystä CRAN-lähteestä:

```bash
Rscript -e 'install.packages(c(
  "dplyr", "here", "lme4", "lmerTest", "readr", "readxl", "tibble", "tidyr",
  "broom.mixed", "digest", "knitr", "rmarkdown", "testthat"
), repos = "https://cloud.r-project.org")'
```

R käyttää jo asennettuja paketteja uudelleen ja asentaa lisäksi tarvittavat
transitiiviset riippuvuudet. `rmarkdown` kuuluu renderöinnin
`Suggests`-riippuvuuksiin ja sen pitää olla saatavilla ennen
Quarto-validointia.

Ympäristö ei lukitse pakettiversioita. Tämä menettely tukee julkisen ja
synteettisen scaffoldin rakenne-, testi- ja renderöintitoistettavuutta, mutta
ei osoita numeerista tai tieteellistä pariteettia eikä oikean tutkimusaineiston
toistettavuutta.

## Synteettisen testin ja testien ajaminen
Koska kyseessä on synteettinen data, testien ja koodin ajoa varten käytetään synteettistä aineistoa, jolla voidaan varmistaa koodin tekninen toimivuus.

Voit generoida synteettisen datan uudelleen ajamalla:
```R
source("scripts/01_generate_synthetic_fixture.R")
```

Suorita R-testit repositoryn juuresta:
```bash
Rscript tests/testthat.R
```

Suorita K50:n kohdennettu synteettinen testisarja:
```bash
Rscript -e 'testthat::test_file("tests/testthat/test_k50_synthetic_wide_test_control.R")'
```

## Quarto-renderöinti
Renderöi smoke test varmistaaksesi putken toiminnan:
```bash
quarto check
quarto render manuscript/smoke_test.qmd
```

## Data Availability
Alkuperäinen aineisto on sensitiivistä geriatrista rekisteriaineistoa, eikä sitä jaeta tässä repositoriossa (Data Availability -luonnos, ks. [docs/restricted_data_policy.md](docs/restricted_data_policy.md)).

## Tietosuojarajoitteet
1. Ainoastaan **synteettinen data** on sallittua Gitissä.
2. Oikeaa osallistujatason dataa **EI SAA KOSKAAN** kommitoida.
3. Kts. `.gitignore` ja `AGENTS.md` turvallisuusrajoitteista.

## Tunnetut puutteet ja TODO
- Lopullinen lisenssi puuttuu (käytössä placeholder).
- `SCI-03C`: 0.40 producer -kynnyksen tieteellinen hyväksyntä vaatii varmentamisen.
- `SCI-SEM-COHORT`: lopullisten kohorttisemantiikkojen tieteellinen hyväksyntä vaatii varmentamisen.
- `RET-01`: retention-käytäntö vaatii auktoritatiivisen policy-viitteen.
