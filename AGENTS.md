# AGENTS.md

Tämä tiedosto sisältää ohjeita tekoälyagenteille, jotka työskentelevät tässä repositoriossa.

## Repositoryn tarkoitus
Tämä on turvallinen MVP-scaffold 12-kuukauden kohorttitutkimukselle (FOF ja locomotor capacity). Sen tarkoituksena on varmistaa täysi rakenne- ja renderöintitoistettavuus julkisilla materiaaleilla ja dokumentoida analyysiputki.

## Sallitut ja kielletyt datatyypit
- **Kielletty:** Oikean osallistujatason datan käyttö tai kommitointi. Oikeaa tutkimusdataa (raakadataa tai osallistujatason tiedostoja) ei saa lisätä.
- **Kielletty:** Älä lisää `.RData`, `.Rhistory`, `.env`, CSV/RDS/SAV-tiedostoja (joita ei voida todentaa synteettiseksi), tai salaisuuksia.
- **Sallittu:** Vain `data/synthetic/` hakemistossa oleva selvästi synteettiseksi merkitty ja generoitu testidata.
- **Sallittu:** Aggregoidut taulukot ja kuviot (`outputs/` kansion alla, kunhan niissä ei ole osallistujatietoa).

## Turvalliset työskentelypolut
- Data luetaan `data/synthetic/` -kansiosta.
- Testit sijaitsevat `tests/testthat/` -kansiossa.
- Tulosteet (taulukot ja kuviot) viedään `outputs/tables/` ja `outputs/figures/` -kansioihin.
- Renderöitävät tiedostot ovat `manuscript/` -kansiossa. Koodiskriptit ovat `R/` ja `scripts/` kansioissa.

## Testien ja renderöinnin komennot
1. **R-testit:** `testthat::test_dir("tests/testthat")`
2. **Renderöinti:** `quarto render manuscript/smoke_test.qmd`
3. **Data generointi:** `Rscript scripts/01_generate_synthetic_fixture.R` tai `source("scripts/01_generate_synthetic_fixture.R")` R:ssä.

## Oikea osallistujadata
**Oikeaa osallistujadataa ei saa käyttää.** Käsikirjoituksen mukaan analyysit perustuvat sensitiivisiin geriatrisiin rekisteriaineistoihin. Sitä ei ikinä tuoda repositorioon. Kaikki testaus tehdään vain synteettisellä datalla.

## Muutosten todentaminen
**Jokaisen muutoksen jälkeen on tarkistettava diff ja testit.** Agenteilla on velvollisuus ajaa vähintään `git diff --check` sekä R- ja Quarto-testit aina muutosten yhteydessä. Varmista, ettei osallistujatietoja ole vuotanut mihinkään tiedostoon.
