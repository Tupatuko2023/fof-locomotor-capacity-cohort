test_that("public traceability demo produces the exact synthetic artifact chain", {
  project_root <- normalizePath(file.path(getwd(), "../.."), mustWork = FALSE)
  if (!file.exists(file.path(project_root, "scripts", "demo", "run_public_traceability.R"))) {
    project_root <- getwd()
  }
  rscript <- Sys.which("Rscript")
  quarto <- Sys.which("quarto")
  if (!nzchar(rscript)) skip("Rscript is not available")
  if (!nzchar(quarto)) skip("Quarto is not available in this validation environment")

  output_root <- tempfile("public-traceability-")
  dir.create(output_root)
  on.exit(unlink(output_root, recursive = TRUE, force = TRUE), add = TRUE)
  old_wd <- setwd(project_root)
  on.exit(setwd(old_wd), add = TRUE)

  result <- system2(
    rscript,
    c("scripts/demo/run_public_traceability.R", "--output-root", output_root),
    stdout = TRUE,
    stderr = TRUE
  )
  expect_null(attr(result, "status"), info = paste(result, collapse = "\n"))

  expected <- sort(c(
    "public_traceability_demo.html",
    "traceability_qc.csv",
    "traceability_qc.png",
    "traceability_receipt.json"
  ))
  expect_identical(sort(list.files(output_root)), expected)

  qc <- utils::read.csv(
    file.path(output_root, "traceability_qc.csv"),
    check.names = FALSE,
    fileEncoding = "UTF-8"
  )
  expect_identical(
    names(qc),
    c("check_id", "check_role", "status", "synthetic_snapshot_id", "artifact_role", "disclaimer")
  )
  expect_identical(
    qc$check_id,
    c("SYNTHETIC_ROLE", "LOCK_PATH", "MD5_INTEGRITY", "SHA256_INTEGRITY", "WIDE_SCHEMA")
  )
  expect_true(all(qc$status == "PASS"))
  expected_disclaimer <- paste(
    "SYNTHETIC WORKFLOW DEMONSTRATION",
    intToUtf8(0x2014L),
    "NOT A RESEARCH RESULT"
  )
  expect_true(all(qc$disclaimer == expected_disclaimer))
  expect_gt(file.info(file.path(output_root, "traceability_qc.png"))$size, 0)

  receipt <- paste(readLines(file.path(output_root, "traceability_receipt.json"), warn = FALSE), collapse = "\n")
  required_fields <- c(
    "repository_revision", "synthetic_snapshot_id", "synthetic_snapshot_role",
    "input_relative_path", "input_integrity_status", "analysis_entrypoint",
    "invocation_profile", "output_relative_paths", "output_roles",
    "generation_status", "synthetic_disclaimer"
  )
  expect_true(all(vapply(required_fields, function(field) grepl(paste0('"', field, '"'), receipt, fixed = TRUE), logical(1))))

  html <- paste(readLines(file.path(output_root, "public_traceability_demo.html"), warn = FALSE), collapse = "\n")
  expect_true(grepl("SYNTHETIC WORKFLOW DEMONSTRATION", html, fixed = TRUE))
  expect_true(grepl("not a research result", tolower(html), fixed = TRUE))

  public_text <- paste(c(receipt, html), collapse = "\n")
  expect_false(grepl(project_root, public_text, fixed = TRUE))
  expect_false(grepl("DATA_ROOT", public_text, fixed = TRUE))
  expect_false(grepl("participant_id|cohort_count|missingness_count", public_text, ignore.case = TRUE))
})

test_that("public traceability entrypoint rejects non-contract arguments", {
  project_root <- normalizePath(file.path(getwd(), "../.."), mustWork = FALSE)
  if (!file.exists(file.path(project_root, "scripts", "demo", "run_public_traceability.R"))) {
    project_root <- getwd()
  }
  old_wd <- setwd(project_root)
  on.exit(setwd(old_wd), add = TRUE)
  result <- suppressWarnings(system2(
    Sys.which("Rscript"),
    c("scripts/demo/run_public_traceability.R", "--data", "anything.csv"),
    stdout = TRUE,
    stderr = TRUE
  ))
  expect_false(is.null(attr(result, "status")))
  expect_true(any(grepl("Only an optional --output-root", result, fixed = TRUE)))
})
