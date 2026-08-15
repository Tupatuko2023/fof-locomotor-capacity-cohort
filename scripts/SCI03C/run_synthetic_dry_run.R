#!/usr/bin/env Rscript

# SCI-03C protected-execution package: synthetic dry run only.
# No participant data or participant-derived output is permitted by this entrypoint.

args_all <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args_all, value = TRUE)
script_path <- if (length(file_arg)) sub("^--file=", "", file_arg[[1]]) else "scripts/SCI03C/run_synthetic_dry_run.R"
project_root <- normalizePath(file.path(dirname(script_path), "../.."), mustWork = TRUE)
source(file.path(project_root, "R", "functions", "sci03c_aggregate_evidence.R"))

args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(flag) {
  index <- match(flag, args)
  if (is.na(index) || index == length(args)) stop("Missing required argument: ", flag, call. = FALSE)
  args[[index + 1L]]
}

output_dir <- normalizePath(get_arg("--output-dir"), mustWork = FALSE)
threshold <- suppressWarnings(as.integer(get_arg("--synthetic-test-threshold")))
if (is.na(threshold) || threshold < 1L) {
  stop("--synthetic-test-threshold must be a positive integer used only for synthetic validation.", call. = FALSE)
}

set.seed(20260815)
subject_count <- 48L
subjects <- sprintf("SYN-SCI03C-%03d", seq_len(subject_count))
fixture <- expand.grid(
  subject_key = subjects,
  timepoint = c("baseline", "12m"),
  stringsAsFactors = FALSE
)
fixture$fof_group <- ifelse(as.integer(sub(".*-", "", fixture$subject_key)) %% 2L, "FOF_YES", "FOF_NO")
pattern <- (seq_len(nrow(fixture)) + rep(c(0L, 2L), each = subject_count)) %% 8L
fixture$gait_available <- bitwAnd(pattern, 1L) == 1L
fixture$chair_available <- bitwAnd(pattern, 2L) == 2L
fixture$balance_available <- bitwAnd(pattern, 4L) == 4L
fixture$k50_covariates_complete <- seq_len(nrow(fixture)) %% 7L != 0L

package <- build_sci03c_release_package(fixture, threshold)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
for (table_name in names(package)) {
  write.csv(package[[table_name]], file.path(output_dir, paste0(table_name, ".csv")), row.names = FALSE, na = "")
}

receipt <- c(
  "package=WP-A1-SCI-03C-PROTECTED-EXECUTION-PACKAGE-PREP",
  "mode=SYNTHETIC_ONLY",
  paste0("script=", basename(script_path)),
  paste0("synthetic_subjects=", subject_count),
  paste0("synthetic_test_threshold=", threshold),
  "institutional_small_cell_threshold=AUTHORITY_TO_DEFINE",
  "participant_level_egress=PROHIBITED",
  "protected_execution_authorized=NO",
  paste0("r_version=", paste(R.version$major, R.version$minor, sep = ".")),
  paste0("platform=", R.version$platform),
  paste0("locale=", Sys.getlocale()),
  paste0("timezone=", Sys.timezone()),
  "seed=20260815",
  "validation=PASS"
)
writeLines(receipt, file.path(output_dir, "synthetic_run_receipt.txt"))
cat("SCI-03C synthetic dry run PASS\n")
