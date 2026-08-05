# fof-locomotor-capacity-cohort
Analysis code and reproducibility materials for a 12-month cohort study on fear of falling (FOF) and locomotor capacity in older adults. Includes R scripts, Quarto manuscript, and synthetic test data. No restricted patient data included.

## Tarkoitus
Tämä on tutkimuskohtainen R- ja Quarto-pohjainen analyysirepositorio, jonka tarkoituksena on dokumentoida 12 kuukauden kohorttianalyysi. Repositorio tekee näkyväksi analyysien, taulukoiden, kuvioiden ja lisämateriaalien yhteydet toisiinsa. Tämä MVP (Minimum Viable Product) sisältää toistaiseksi vain turvallisen scaffold-rakenteen ja synteettistä testidataa. **Oikeaa analyysikoodia tai käsikirjoitusta ei ole vielä migroitu.**

> **This repository currently contains only a reproducibility scaffold. No analytical results are included.**

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
│   └── transform_locomotor_indicators.R
├── scripts/
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
    ├── reproducibility_scope.md
    └── restricted_data_policy.md
```

## Ympäristön palauttaminen ja riippuvuudet
Projekti käyttää `renv`-pakettia (asennetaan myöhemmin). Tällä hetkellä riippuvuudet ja ympäristö ovat vain luonnoksena.
Kun renv on käytössä, voit palauttaa ympäristön: `renv::restore()`.

## Synteettisen testin ja testien ajaminen
Koska kyseessä on synteettinen data, testien ja koodin ajoa varten käytetään synteettistä aineistoa, jolla voidaan varmistaa koodin tekninen toimivuus.

Voit generoida synteettisen datan uudelleen ajamalla:
```R
source("scripts/01_generate_synthetic_fixture.R")
```

Suorita R-testit (esim. transform-funktiolle):
```R
testthat::test_dir("tests/testthat")
```

## Quarto-renderöinti
Renderöi smoke test varmistaaksesi putken toiminnan:
```bash
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
- Käsikirjoitusta ja analyysikoodeja ei ole vielä migroitu.
- Chair-rise-muuttujan reverse-coding-kaava vaatii varmentamisen (NEEDS_VERIFICATION).
