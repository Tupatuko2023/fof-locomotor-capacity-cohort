#!/usr/bin/env Rscript

disclaimer <- paste(
  "SYNTHETIC WORKFLOW DEMONSTRATION",
  intToUtf8(0x2014L),
  "NOT A RESEARCH RESULT"
)
entrypoint <- "scripts/demo/run_public_traceability.R"
default_output_root <- "outputs/demo"

fail <- function(...) stop(..., call. = FALSE)

parse_args <- function(args) {
  if (length(args) == 0L) return(default_output_root)
  if (length(args) == 2L && identical(args[[1]], "--output-root")) {
    if (!nzchar(args[[2]])) fail("--output-root requires a non-empty path.")
    return(args[[2]])
  }
  fail("Only an optional --output-root PATH argument is supported.")
}

read_lock <- function(path) {
  lines <- trimws(readLines(path, warn = FALSE))
  lines <- lines[nzchar(lines)]
  if (any(!grepl("^[^=]+=.*$", lines))) fail("Synthetic lock contains an invalid line.")
  values <- sub("^[^=]*=", "", lines)
  names(values) <- sub("=.*$", "", lines)
  values
}

sha256_file <- function(path) {
  command <- Sys.which("sha256sum")
  if (nzchar(command)) {
    result <- system2(command, shQuote(path), stdout = TRUE, stderr = TRUE)
    status <- attr(result, "status")
    if (is.null(status) || identical(status, 0L)) {
      return(strsplit(result[[1]], "[[:space:]]+")[[1]][[1]])
    }
  }
  if (requireNamespace("digest", quietly = TRUE)) {
    return(digest::digest(file = path, algo = "sha256", serialize = FALSE))
  }
  fail("No SHA-256 implementation is available.")
}

json_string <- function(value) {
  value <- gsub("\\\\", "\\\\\\\\", value)
  value <- gsub('"', '\\\\"', value, fixed = TRUE)
  paste0('"', value, '"')
}

json_array <- function(values) {
  paste0("[", paste(vapply(values, json_string, character(1)), collapse = ", "), "]")
}

repo_root <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
if (!file.exists(file.path(repo_root, entrypoint))) {
  fail("Run the public traceability entrypoint from the repository root.")
}
if (nzchar(Sys.getenv("DATA_ROOT", unset = ""))) {
  fail("DATA_ROOT is prohibited for the public synthetic traceability demo.")
}

output_root_arg <- parse_args(commandArgs(trailingOnly = TRUE))
output_root <- normalizePath(output_root_arg, winslash = "/", mustWork = FALSE)
dir.create(output_root, recursive = TRUE, showWarnings = FALSE)
output_root <- normalizePath(output_root, winslash = "/", mustWork = TRUE)

lock_rel <- "data/synthetic/k50_wide_authoritative_test_control.lock"
fixture_rel <- "data/synthetic/k50_wide_structural_fixture.csv"
lock <- read_lock(file.path(repo_root, lock_rel))
required_lock <- c("snapshot_role", "snapshot_id", "path", "md5", "sha256")
if (!all(required_lock %in% names(lock))) fail("Synthetic lock is incomplete.")
if (!identical(unname(lock[["snapshot_role"]]), "synthetic_wide_test_control")) {
  fail("Synthetic snapshot role is invalid.")
}
if (!startsWith(unname(lock[["snapshot_id"]]), "SYN-K50-WIDE-")) {
  fail("Synthetic snapshot identity is invalid.")
}
if (!identical(unname(lock[["path"]]), fixture_rel)) fail("Synthetic lock path is invalid.")

fixture_path <- file.path(repo_root, fixture_rel)
if (!file.exists(fixture_path)) fail("Approved synthetic fixture is missing.")
md5_ok <- identical(unname(tools::md5sum(fixture_path)), unname(lock[["md5"]]))
sha256_ok <- identical(sha256_file(fixture_path), unname(lock[["sha256"]]))
fixture_names <- names(utils::read.csv(fixture_path, nrows = 0L, check.names = FALSE))
required_schema <- c(
  "id", "FOF_status", "age", "sex", "BMI",
  "locomotor_capacity_0", "locomotor_capacity_12m", "z3_0", "z3_12m"
)
schema_ok <- identical(fixture_names, required_schema)

checks <- data.frame(
  check_id = c("SYNTHETIC_ROLE", "LOCK_PATH", "MD5_INTEGRITY", "SHA256_INTEGRITY", "WIDE_SCHEMA"),
  check_role = c("metadata", "input_resolution", "integrity", "integrity", "structure"),
  status = c(TRUE, TRUE, md5_ok, sha256_ok, schema_ok),
  synthetic_snapshot_id = rep(unname(lock[["snapshot_id"]]), 5L),
  artifact_role = rep("PUBLIC_SYNTHETIC_STRUCTURAL_DEMO", 5L),
  disclaimer = rep(disclaimer, 5L),
  stringsAsFactors = FALSE
)
checks$status <- ifelse(checks$status, "PASS", "FAIL")

qc_path <- file.path(output_root, "traceability_qc.csv")
figure_path <- file.path(output_root, "traceability_qc.png")
html_path <- file.path(output_root, "public_traceability_demo.html")
receipt_path <- file.path(output_root, "traceability_receipt.json")
utils::write.csv(checks, qc_path, row.names = FALSE, na = "", fileEncoding = "UTF-8")

grDevices::png(figure_path, width = 1400, height = 850, res = 150)
graphics::par(mar = c(7, 10, 5, 2))
colors <- ifelse(checks$status == "PASS", "#2E7D32", "#B71C1C")
graphics::barplot(
  rep(1, nrow(checks)), names.arg = checks$check_id, horiz = TRUE,
  las = 1, col = colors, border = NA, xlim = c(0, 1), axes = FALSE,
  main = disclaimer
)
graphics::axis(1, at = c(0, 1), labels = c("NOT PASSED", "PASS"))
graphics::mtext("Structural and integrity checks on wholly synthetic input", side = 1, line = 5)
grDevices::dev.off()

revision <- suppressWarnings(system2("git", c("rev-parse", "HEAD"), stdout = TRUE, stderr = FALSE))
if (length(revision) != 1L || !grepl("^[0-9a-f]{40}$", revision)) revision <- "UNAVAILABLE"
output_names <- c(
  "traceability_qc.csv", "traceability_qc.png",
  "public_traceability_demo.html", "traceability_receipt.json"
)
output_roles <- c("qc_table", "qc_figure", "quarto_report", "provenance_receipt")
receipt_lines <- c(
  "{",
  paste0('  "repository_revision": ', json_string(revision), ","),
  paste0('  "synthetic_snapshot_id": ', json_string(unname(lock[["snapshot_id"]])), ","),
  paste0('  "synthetic_snapshot_role": ', json_string(unname(lock[["snapshot_role"]])), ","),
  paste0('  "input_relative_path": ', json_string(fixture_rel), ","),
  paste0('  "input_integrity_status": ', json_string(if (all(checks$status == "PASS")) "PASS" else "FAIL"), ","),
  paste0('  "analysis_entrypoint": ', json_string(entrypoint), ","),
  paste0('  "invocation_profile": ', json_string("public_synthetic_default"), ","),
  paste0('  "output_relative_paths": ', json_array(output_names), ","),
  paste0('  "output_roles": ', json_array(output_roles), ","),
  paste0('  "generation_status": ', json_string("COMPLETE"), ","),
  paste0('  "synthetic_disclaimer": ', json_string(disclaimer)),
  "}"
)
writeLines(receipt_lines, receipt_path, useBytes = TRUE)

if (!all(checks$status == "PASS")) fail("One or more synthetic structural checks failed.")
quarto <- Sys.which("quarto")
if (!nzchar(quarto)) fail("Quarto is required to complete the traceability chain.")
qmd_path <- file.path(repo_root, "manuscript", "public_traceability_demo.qmd")
render_env <- c(paste0("TRACE_OUTPUT_ROOT=", output_root))
render <- system2(
  quarto,
  c("render", shQuote(qmd_path)),
  stdout = TRUE,
  stderr = TRUE,
  env = render_env
)
render_status <- attr(render, "status")
if (!is.null(render_status) && !identical(render_status, 0L)) {
  fail("Quarto rendering failed: ", paste(render, collapse = "\n"))
}
rendered_html <- file.path(repo_root, "outputs", "manuscript", "public_traceability_demo.html")
if (!file.exists(rendered_html)) fail("Quarto did not create the expected HTML artifact.")
if (!file.rename(rendered_html, html_path)) fail("Could not place the rendered HTML artifact.")

produced <- sort(basename(list.files(output_root, full.names = TRUE, recursive = FALSE)))
if (!identical(produced, sort(output_names))) {
  fail("Unexpected output manifest: ", paste(produced, collapse = ", "))
}
message("Public synthetic traceability demo completed: ", output_root_arg)
