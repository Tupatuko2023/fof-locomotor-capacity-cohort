# test_k50_synthetic_wide_test_control.R

project_root <- normalizePath(file.path(getwd(), "../.."), mustWork = FALSE)
if (!file.exists(file.path(project_root, "scripts", "K50", "K50.r"))) {
  project_root <- getwd()
}

load_k50_helpers <- function() {
  script_path <- file.path(project_root, "scripts", "K50", "K50.r")
  lines <- readLines(script_path, warn = FALSE)
  cli_start <- grep("^# --- CLI", lines)
  stopifnot(length(cli_start) == 1L)
  env <- new.env(parent = globalenv())
  eval(parse(text = paste(lines[seq_len(cli_start - 1L)], collapse = "\n")), envir = env)
  env
}

with_project_root <- function(code) {
  old_wd <- setwd(project_root)
  on.exit(setwd(old_wd), add = TRUE)
  force(code)
}

test_that("normal WIDE default keeps production authoritative lock selection", {
  k50 <- load_k50_helpers()
  production_lock <- normalizePath(
    file.path(project_root, "R-scripts", "K50", "k50_wide_authoritative_input.lock"),
    winslash = "/",
    mustWork = FALSE
  )

  with_project_root({
    if (file.exists(production_lock)) {
      data_ref <- k50$resolve_input_path("WIDE", NULL, FALSE)
      expect_identical(data_ref$lock_path, production_lock)
      expect_identical(data_ref$resolution, "authoritative_lock")
    } else {
      expect_error(
        k50$resolve_input_path("WIDE", NULL, FALSE),
        "R-scripts/K50/k50_wide_authoritative_input.lock",
        fixed = TRUE
      )
    }
  })
})

test_that("synthetic WIDE control selects only the approved synthetic lock and fixture", {
  k50 <- load_k50_helpers()
  expected_lock <- normalizePath(
    file.path(project_root, "data", "synthetic", "k50_wide_authoritative_test_control.lock"),
    winslash = "/",
    mustWork = TRUE
  )
  expected_fixture <- normalizePath(
    file.path(project_root, "data", "synthetic", "k50_wide_structural_fixture.csv"),
    winslash = "/",
    mustWork = TRUE
  )

  with_project_root({
    data_ref <- k50$resolve_input_path("WIDE", NULL, TRUE)
    expect_identical(data_ref$resolution, "synthetic_wide_test_control")
    expect_identical(data_ref$lock_path, expected_lock)
    expect_identical(data_ref$path, expected_fixture)
    expect_identical(data_ref$snapshot_role, "synthetic_wide_test_control")
    expect_true(startsWith(data_ref$snapshot_id, "SYN-K50-WIDE-"))
  })
})

test_that("synthetic WIDE control fails closed for incompatible combinations", {
  k50 <- load_k50_helpers()

  with_project_root({
    expect_error(
      k50$resolve_input_path("LONG", NULL, TRUE),
      "only valid with --shape WIDE",
      fixed = TRUE
    )
    expect_error(
      k50$resolve_input_path("WIDE", "data/synthetic/k50_wide_structural_fixture.csv", TRUE),
      "--data cannot be combined",
      fixed = TRUE
    )
  })
})

test_that("authoritative validation rejects tampered hash and metadata", {
  k50 <- load_k50_helpers()

  with_project_root({
    approved_lock <- file.path(project_root, "data", "synthetic", "k50_wide_authoritative_test_control.lock")
    tampered_hash_lock <- tempfile(fileext = ".lock")
    lock_lines <- readLines(approved_lock, warn = FALSE)
    writeLines(sub("^md5=.*$", "md5=00000000000000000000000000000000", lock_lines), tampered_hash_lock)
    expect_error(
      k50$resolve_authoritative_wide_input(tampered_hash_lock, "test_tampered_hash"),
      "md5 mismatch",
      fixed = TRUE
    )

    missing_metadata_lock <- tempfile(fileext = ".lock")
    writeLines(lock_lines[!grepl("^snapshot_id=", lock_lines)], missing_metadata_lock)
    expect_error(
      k50$resolve_authoritative_wide_input(missing_metadata_lock, "test_missing_metadata"),
      "missing keys: snapshot_id",
      fixed = TRUE
    )
  })
})

test_that("malformed synthetic WIDE control invocation rejects path injection", {
  rscript <- Sys.which("Rscript")
  if (!nzchar(rscript)) {
    skip("Rscript not available")
  }
  required_packages <- c("dplyr", "readr", "tidyr", "tibble", "here", "lme4", "lmerTest")
  missing_packages <- required_packages[!vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)]
  if (length(missing_packages) > 0L) {
    skip(paste("Required packages not available:", paste(missing_packages, collapse = ", ")))
  }

  script_path <- file.path(project_root, "scripts", "K50", "K50.r")
  result <- suppressWarnings(
    system2(
      rscript,
      c(
        script_path,
        "--shape", "WIDE",
        "--outcome", "locomotor_capacity",
        "--synthetic-wide-test-control", "data/synthetic/k50_wide_authoritative_test_control.lock"
      ),
      stdout = TRUE,
      stderr = TRUE
    )
  )
  expect_false(identical(attr(result, "status"), 0L))
  expect_true(any(grepl("--synthetic-wide-test-control does not accept a value or path", result, fixed = TRUE)))
})
