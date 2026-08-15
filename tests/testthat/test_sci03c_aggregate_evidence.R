# test_sci03c_aggregate_evidence.R

project_root <- normalizePath(file.path(getwd(), "../.."), mustWork = FALSE)
if (!file.exists(file.path(project_root, "R", "functions", "sci03c_aggregate_evidence.R"))) {
  project_root <- getwd()
}
source(file.path(project_root, "R", "functions", "sci03c_aggregate_evidence.R"))

make_fixture <- function() {
  data.frame(
    subject_key = rep(sprintf("SYN-%02d", 1:8), each = 2),
    timepoint = rep(c("baseline", "12m"), 8),
    fof_group = rep(rep(c("FOF_NO", "FOF_YES"), each = 4), each = 2),
    gait_available = rep(c(FALSE, TRUE), 8),
    chair_available = rep(c(FALSE, FALSE, TRUE, TRUE), 4),
    balance_available = rep(c(FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, TRUE), each = 2),
    k50_covariates_complete = rep(c(TRUE, TRUE, TRUE, FALSE), 4),
    stringsAsFactors = FALSE
  )
}

test_that("coverage rules are monotonic and paired counts reconcile", {
  fixture <- sci03c_add_coverage(make_fixture())
  paired <- sci03c_pair_frame(fixture)
  eligibility <- sci03c_rule_eligibility(fixture, paired, FALSE)
  for (window in c("baseline", "12m", "paired")) {
    values <- eligibility$n[eligibility$window == window]
    names(values) <- eligibility$rule[eligibility$window == window]
    expect_gte(values[["ANY_COMPONENT"]], values[["MIN_2_OF_3"]])
    expect_gte(values[["MIN_2_OF_3"]], values[["REQUIRE_3_OF_3"]])
  }
  transition <- sci03c_paired_transition(paired, FALSE)
  expect_equal(sum(transition$n), nrow(paired))
})

test_that("input validation fails closed", {
  fixture <- make_fixture()
  expect_error(validate_sci03c_input(fixture[-1]), "missing columns: subject_key", fixed = TRUE)
  fixture$gait_available[[1]] <- NA
  expect_error(validate_sci03c_input(fixture), "non-missing logical", fixed = TRUE)
})

test_that("primary and conservative secondary suppression remove releasable values", {
  table <- data.frame(
    partition = c("A", "A", "B", "B"),
    n = c(1L, 9L, 5L, 6L),
    pct = c(10, 90, 45.5, 54.5)
  )
  result <- sci03c_suppress(table, threshold = 3L, partition_columns = "partition")
  expect_identical(result$disclosure_status, c(
    "PRIMARY_SUPPRESSED", "SECONDARY_SUPPRESSED", "RELEASED", "RELEASED"
  ))
  expect_true(all(is.na(result$n[1:2])))
  expect_true(all(is.na(result$pct[1:2])))
  expect_error(sci03c_suppress(table, NA_integer_, "partition"), "authority-supplied integer")
})

test_that("release package contains only contracted aggregate fields", {
  package <- build_sci03c_release_package(make_fixture(), small_cell_threshold = 2L)
  expect_setequal(names(package), c(
    "coverage_distribution", "component_missingness", "paired_transition",
    "rule_eligibility", "k50_population", "sci03d_comparison"
  ))
  forbidden <- c(
    "subject_key", "gait_available", "chair_available", "balance_available",
    "k50_covariates_complete"
  )
  expect_true(all(vapply(package, function(x) !any(forbidden %in% names(x)), logical(1))))
  expect_true(all(vapply(package, function(x) "disclosure_status" %in% names(x), logical(1))))
  sci03d <- package$sci03d_comparison
  suppressed <- sci03d$disclosure_status != "RELEASED"
  expect_true(all(is.na(sci03d$nonmissing_share[suppressed])))
  expect_true(all(is.na(sci03d$producer_gate_result[suppressed])))
})

test_that("synthetic dry-run entrypoint writes aggregate-only package and receipt", {
  rscript <- Sys.which("Rscript")
  if (!nzchar(rscript)) skip("Rscript not available")
  output_dir <- tempfile("sci03c-dry-run-")
  script <- file.path(project_root, "scripts", "SCI03C", "run_synthetic_dry_run.R")
  result <- system2(
    rscript,
    c(script, "--output-dir", output_dir, "--synthetic-test-threshold", "3"),
    stdout = TRUE, stderr = TRUE
  )
  expect_null(attr(result, "status"))
  expect_true(any(grepl("synthetic dry run PASS", result, fixed = TRUE)))
  expected <- c(
    paste0(names(build_sci03c_release_package(make_fixture(), 2L)), ".csv"),
    "synthetic_run_receipt.txt"
  )
  expect_setequal(list.files(output_dir), expected)
  receipt <- readLines(file.path(output_dir, "synthetic_run_receipt.txt"), warn = FALSE)
  expect_true("mode=SYNTHETIC_ONLY" %in% receipt)
  expect_true("protected_execution_authorized=NO" %in% receipt)
  csv_names <- unlist(lapply(list.files(output_dir, pattern = "[.]csv$", full.names = TRUE), function(path) {
    names(read.csv(path, check.names = FALSE))
  }))
  expect_false(any(c("subject_key", "synthetic_id", "participant_id") %in% csv_names))
})
