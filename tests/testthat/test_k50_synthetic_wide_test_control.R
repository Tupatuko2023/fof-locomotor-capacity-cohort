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

test_that("synthetic output directory is explicit, isolated, and empty", {
  k50 <- load_k50_helpers()
  expect_true(is.function(k50$validate_public_synthetic_receipt))

  rscript <- Sys.which("Rscript")
  if (!nzchar(rscript)) skip("Rscript not available")
  script_path <- file.path(project_root, "scripts", "K50", "K50.r")

  missing_output <- suppressWarnings(system2(
    rscript,
    c(script_path, "--shape", "WIDE", "--outcome", "locomotor_capacity",
      "--synthetic-wide-test-control"),
    stdout = TRUE, stderr = TRUE
  ))
  expect_false(identical(attr(missing_output, "status"), 0L))
  expect_true(any(grepl("requires an explicit --synthetic-output-dir", missing_output, fixed = TRUE)))

  nonempty_output <- tempfile("k50-synthetic-nonempty-")
  dir.create(nonempty_output)
  on.exit(unlink(nonempty_output, recursive = TRUE), add = TRUE)
  writeLines("sentinel", file.path(nonempty_output, "existing.txt"))
  nonempty_result <- suppressWarnings(system2(
    rscript,
    c(script_path, "--shape", "WIDE", "--outcome", "locomotor_capacity",
      "--synthetic-wide-test-control", "--synthetic-output-dir", nonempty_output),
    stdout = TRUE, stderr = TRUE
  ))
  expect_false(identical(attr(nonempty_result, "status"), 0L))
  expect_true(any(grepl("must be empty", nonempty_result, fixed = TRUE)))
})

test_that("FI22 synthetic execution emits only public-safe provenance", {
  rscript <- Sys.which("Rscript")
  if (!nzchar(rscript)) skip("Rscript not available")
  required_packages <- c("dplyr", "readr", "tidyr", "tibble", "here", "lme4", "lmerTest")
  missing_packages <- required_packages[!vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)]
  if (length(missing_packages) > 0L) {
    skip(paste("Required packages not available:", paste(missing_packages, collapse = ", ")))
  }

  output_dir <- tempfile("k50-synthetic-fi22-")
  on.exit(unlink(output_dir, recursive = TRUE), add = TRUE)
  script_path <- file.path(project_root, "scripts", "K50", "K50.r")
  result <- with_project_root(suppressWarnings(system2(
      rscript,
      c(script_path, "--shape", "WIDE", "--outcome", "locomotor_capacity",
        "--fi22", "on", "--synthetic-wide-test-control",
        "--synthetic-output-dir", output_dir),
      stdout = TRUE, stderr = TRUE
    )))
  if (!is.null(attr(result, "status"))) {
    fail(paste("FI22 synthetic execution failed:", paste(result, collapse = "\n")))
    return(invisible())
  }

  fi22_path <- file.path(output_dir, "k50_wide_locomotor_capacity_model_terms_fi22.csv")
  receipt_path <- file.path(output_dir, "k50_wide_locomotor_capacity_public_synthetic_receipt.txt")
  expect_true(file.exists(fi22_path))
  expect_true(file.exists(receipt_path))
  expect_false(file.exists(file.path(output_dir, "k50_wide_locomotor_capacity_input_receipt.txt")))
  expect_false(file.exists(file.path(output_dir, "k50_wide_locomotor_capacity_modeled_cohort_provenance.txt")))
  expect_false(file.exists(file.path(output_dir, "k50_wide_locomotor_capacity_decision_log.txt")))
  expect_false(file.exists(file.path(output_dir, "k50_wide_locomotor_capacity_sessioninfo.txt")))

  fi22 <- suppressMessages(readr::read_csv(fi22_path, show_col_types = FALSE))
  expect_identical(names(fi22), c(
    "term", "estimate", "std.error", "statistic", "p.value", "conf.low",
    "conf.high", "branch", "outcome", "model_role", "formula", "n"
  ))
  expect_true(all(fi22$model_role == "fi22_sensitivity"))
  expect_true(all(grepl("FI22_nonperformance_KAAOS", fi22$formula, fixed = TRUE)))

  k50 <- load_k50_helpers()
  receipt <- k50$read_key_value_file(receipt_path)
  expect_silent(k50$validate_public_synthetic_receipt(receipt))
  expect_identical(receipt$receipt_classification, "PUBLIC_SYNTHETIC")
  expect_identical(receipt$input_classification, "PUBLIC_SYNTHETIC_INPUT")
  expect_identical(receipt$fi22_enabled, "true")
  expect_identical(receipt$input_reference, "data/synthetic/k50_wide_structural_fixture.csv")
  output_reference_keys <- grep("^output_.*_reference$", names(receipt), value = TRUE)
  for (reference_key in output_reference_keys) {
    sha_key <- sub("_reference$", "_sha256", reference_key)
    expect_identical(
      receipt[[sha_key]],
      k50$compute_sha256(file.path(output_dir, receipt[[reference_key]]))
    )
  }
  expect_false(any(grepl(
    "(?i)(^[/~]|^[a-z]:[\\\\/]|/data/|/home/|com\\.termux|production|protected|participant[_ -]?id|subject[_ -]?id|patient[_ -]?id|password|api[_ -]?key|authorization[[:space:]]*:[[:space:]]*bearer|ghp_[a-z0-9]+)",
    unlist(receipt, use.names = FALSE), perl = TRUE
  )))

  unsafe_path <- receipt
  unsafe_path$input_reference <- "/private/input.csv"
  expect_error(k50$validate_public_synthetic_receipt(unsafe_path), "PUBLIC_RECEIPT_FORBIDDEN_METADATA")
  production_id <- receipt
  production_id$snapshot_id <- "production-snapshot"
  expect_error(k50$validate_public_synthetic_receipt(production_id), "PUBLIC_RECEIPT_FORBIDDEN_METADATA")
  unrelated_hash <- receipt
  unrelated_hash$input_sha256 <- paste(rep("0", 64), collapse = "")
  expect_error(k50$validate_public_synthetic_receipt(unrelated_hash), "PUBLIC_RECEIPT_CONTROL_BINDING")
  identifier_field <- receipt
  identifier_field$participant_id <- "synthetic-id"
  expect_error(k50$validate_public_synthetic_receipt(identifier_field), "PUBLIC_RECEIPT_UNEXPECTED_FIELD")
  free_error <- receipt
  free_error$error_payload <- "filesystem details"
  expect_error(k50$validate_public_synthetic_receipt(free_error), "PUBLIC_RECEIPT_UNEXPECTED_FIELD")
  secret_value <- receipt
  secret_value$runtime_platform <- "password=example"
  expect_error(k50$validate_public_synthetic_receipt(secret_value), "PUBLIC_RECEIPT_UNSAFE_VALUE|PUBLIC_RECEIPT_FORBIDDEN_METADATA")
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
