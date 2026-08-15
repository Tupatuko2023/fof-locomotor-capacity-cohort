# Synthetic-safe aggregate evidence helpers for SCI-03C.
#
# These functions operate on an in-environment availability frame. The frame is
# participant-level and MUST remain inside the approved execution environment.
# Only the disclosure-controlled tables returned by
# build_sci03c_release_package() are candidates for egress.

sci03c_rules <- c(
  ANY_COMPONENT = 1L,
  MIN_2_OF_3 = 2L,
  REQUIRE_3_OF_3 = 3L
)

validate_sci03c_input <- function(x) {
  required <- c(
    "subject_key", "timepoint", "fof_group", "gait_available",
    "chair_available", "balance_available", "k50_covariates_complete"
  )
  missing <- setdiff(required, names(x))
  if (length(missing)) {
    stop("SCI-03C input is missing columns: ", paste(missing, collapse = ", "), call. = FALSE)
  }
  if (anyDuplicated(x[c("subject_key", "timepoint")])) {
    stop("SCI-03C input must have one row per subject_key and timepoint.", call. = FALSE)
  }
  if (!all(x$timepoint %in% c("baseline", "12m"))) {
    stop("timepoint must contain only baseline or 12m.", call. = FALSE)
  }
  logical_columns <- c(
    "gait_available", "chair_available", "balance_available",
    "k50_covariates_complete"
  )
  if (any(vapply(x[logical_columns], function(value) {
    !is.logical(value) || anyNA(value)
  }, logical(1)))) {
    stop("Availability and complete-case columns must be non-missing logical values.", call. = FALSE)
  }
  invisible(TRUE)
}

sci03c_add_coverage <- function(x) {
  validate_sci03c_input(x)
  x$components_observed <- rowSums(x[c(
    "gait_available", "chair_available", "balance_available"
  )])
  x
}

sci03c_count_rows <- function(x, group_columns, value_columns = character()) {
  keys <- c(group_columns, value_columns)
  if (!length(keys)) return(data.frame(n = nrow(x)))
  result <- aggregate(rep.int(1L, nrow(x)), x[keys], sum, drop = FALSE)
  names(result)[ncol(result)] <- "n"
  # aggregate(..., drop = FALSE) represents structurally empty combinations as
  # NA. They are true zero-count cells in this contract.
  result$n[is.na(result$n)] <- 0L
  result
}

sci03c_add_denominator <- function(counts, data, group_columns) {
  denominators <- sci03c_count_rows(data, group_columns)
  names(denominators)[names(denominators) == "n"] <- "denominator_n"
  if (!length(group_columns)) {
    counts$denominator_n <- nrow(data)
  } else {
    counts <- merge(counts, denominators, by = group_columns, all.x = TRUE, sort = FALSE)
  }
  counts$pct <- ifelse(counts$denominator_n > 0, 100 * counts$n / counts$denominator_n, NA_real_)
  counts
}

sci03c_coverage_distribution <- function(x, stratified = FALSE) {
  groups <- c(if (stratified) "fof_group", "timepoint")
  counts <- sci03c_count_rows(x, groups, "components_observed")
  counts <- sci03c_add_denominator(counts, x, groups)
  counts$scope <- if (stratified) "FOF_STRATIFIED" else "OVERALL"
  if (!stratified) counts$fof_group <- "ALL"
  counts[c("scope", "fof_group", "timepoint", "components_observed", "denominator_n", "n", "pct")]
}

sci03c_component_missingness <- function(x, stratified = FALSE) {
  component_columns <- c(
    gait = "gait_available", chair = "chair_available", balance = "balance_available"
  )
  groups <- c(if (stratified) "fof_group", "timepoint")
  pieces <- lapply(names(component_columns), function(component) {
    col <- component_columns[[component]]
    counts <- sci03c_count_rows(transform(x, missing = !x[[col]]), groups, "missing")
    counts <- sci03c_add_denominator(counts, x, groups)
    counts$component <- component
    counts
  })
  result <- do.call(rbind, pieces)
  result$scope <- if (stratified) "FOF_STRATIFIED" else "OVERALL"
  if (!stratified) result$fof_group <- "ALL"
  result[c("scope", "fof_group", "timepoint", "component", "missing", "denominator_n", "n", "pct")]
}

sci03c_pair_frame <- function(x) {
  baseline <- x[x$timepoint == "baseline", c(
    "subject_key", "fof_group", "components_observed", "k50_covariates_complete"
  )]
  followup <- x[x$timepoint == "12m", c(
    "subject_key", "fof_group", "components_observed", "k50_covariates_complete"
  )]
  names(baseline)[-1] <- paste0(names(baseline)[-1], "_baseline")
  names(followup)[-1] <- paste0(names(followup)[-1], "_12m")
  paired <- merge(baseline, followup, by = "subject_key", all = FALSE, sort = FALSE)
  if (any(paired$fof_group_baseline != paired$fof_group_12m)) {
    stop("FOF group must be stable between baseline and 12m for this decision package.", call. = FALSE)
  }
  paired$fof_group <- paired$fof_group_baseline
  paired
}

sci03c_paired_transition <- function(paired, stratified = FALSE) {
  groups <- if (stratified) "fof_group" else character()
  counts <- sci03c_count_rows(
    paired, groups, c("components_observed_baseline", "components_observed_12m")
  )
  counts <- sci03c_add_denominator(counts, paired, groups)
  counts$scope <- if (stratified) "FOF_STRATIFIED" else "OVERALL"
  if (!stratified) counts$fof_group <- "ALL"
  counts[c(
    "scope", "fof_group", "components_observed_baseline", "components_observed_12m",
    "denominator_n", "n", "pct"
  )]
}

sci03c_rule_eligibility <- function(x, paired, stratified = FALSE) {
  groups <- if (stratified) "fof_group" else character()
  pieces <- list()
  index <- 1L
  for (rule in names(sci03c_rules)) {
    threshold <- unname(sci03c_rules[[rule]])
    for (timepoint in c("baseline", "12m")) {
      subset <- x[x$timepoint == timepoint, , drop = FALSE]
      for (group_value in if (stratified) unique(subset$fof_group) else "ALL") {
        group_data <- if (stratified) subset[subset$fof_group == group_value, , drop = FALSE] else subset
        eligible <- sum(group_data$components_observed >= threshold)
        pieces[[index]] <- data.frame(
          scope = if (stratified) "FOF_STRATIFIED" else "OVERALL",
          fof_group = group_value, window = timepoint, rule = rule,
          denominator_n = nrow(group_data), n = eligible,
          pct = if (nrow(group_data)) 100 * eligible / nrow(group_data) else NA_real_
        )
        index <- index + 1L
      }
    }
    for (group_value in if (stratified) unique(paired$fof_group) else "ALL") {
      group_data <- if (stratified) paired[paired$fof_group == group_value, , drop = FALSE] else paired
      eligible <- sum(
        group_data$components_observed_baseline >= threshold &
          group_data$components_observed_12m >= threshold
      )
      pieces[[index]] <- data.frame(
        scope = if (stratified) "FOF_STRATIFIED" else "OVERALL",
        fof_group = group_value, window = "paired", rule = rule,
        denominator_n = nrow(group_data), n = eligible,
        pct = if (nrow(group_data)) 100 * eligible / nrow(group_data) else NA_real_
      )
      index <- index + 1L
    }
  }
  do.call(rbind, pieces)
}

sci03c_k50_population <- function(paired, stratified = FALSE) {
  pieces <- list()
  index <- 1L
  for (rule in names(sci03c_rules)) {
    threshold <- unname(sci03c_rules[[rule]])
    for (group_value in if (stratified) unique(paired$fof_group) else "ALL") {
      group_data <- if (stratified) paired[paired$fof_group == group_value, , drop = FALSE] else paired
      coverage_ok <- group_data$components_observed_baseline >= threshold &
        group_data$components_observed_12m >= threshold
      complete_ok <- group_data$k50_covariates_complete_baseline &
        group_data$k50_covariates_complete_12m
      stage_counts <- c(
        SOURCE_PAIRED = nrow(group_data),
        COVERAGE_ELIGIBLE = sum(coverage_ok),
        K50_COMPLETE_CASE = sum(coverage_ok & complete_ok)
      )
      for (stage in names(stage_counts)) {
        pieces[[index]] <- data.frame(
          scope = if (stratified) "FOF_STRATIFIED" else "OVERALL",
          fof_group = group_value, rule = rule, stage = stage,
          denominator_n = nrow(group_data), n = unname(stage_counts[[stage]]),
          pct = if (nrow(group_data)) 100 * unname(stage_counts[[stage]]) / nrow(group_data) else NA_real_
        )
        index <- index + 1L
      }
    }
  }
  do.call(rbind, pieces)
}

sci03c_sci03d_comparison <- function(rule_eligibility, producer_gate = 0.40) {
  result <- rule_eligibility
  result$nonmissing_share <- result$n / result$denominator_n
  result$producer_gate <- producer_gate
  result$producer_gate_result <- ifelse(
    !is.na(result$nonmissing_share) & result$nonmissing_share >= producer_gate,
    "PASS", "FAIL"
  )
  result
}

# Conservative disclosure control: a small positive cell is primary-suppressed;
# every other cell in the same logical partition is secondary-suppressed. This
# deliberately favors safety over utility until an authority approves a more
# specific complementary-suppression algorithm.
sci03c_suppress <- function(x, threshold, partition_columns) {
  if (length(threshold) != 1L || is.na(threshold) || threshold < 1 || threshold != as.integer(threshold)) {
    stop("small_cell_threshold must be a positive authority-supplied integer.", call. = FALSE)
  }
  if (!all(c("n", "pct") %in% names(x))) stop("Table must contain n and pct.", call. = FALSE)
  primary <- x$n > 0 & x$n < threshold
  suppress <- primary
  if (any(primary)) {
    partition_key <- if (length(partition_columns)) {
      interaction(x[partition_columns], drop = TRUE, lex.order = TRUE)
    } else {
      factor(rep.int("all", nrow(x)))
    }
    affected <- unique(partition_key[primary])
    suppress <- partition_key %in% affected
  }
  x$disclosure_status <- ifelse(primary, "PRIMARY_SUPPRESSED",
    ifelse(suppress, "SECONDARY_SUPPRESSED", "RELEASED")
  )
  x$n[suppress] <- NA_integer_
  x$pct[suppress] <- NA_real_
  if ("denominator_n" %in% names(x)) x$denominator_n[suppress] <- NA_integer_
  if ("nonmissing_share" %in% names(x)) x$nonmissing_share[suppress] <- NA_real_
  if ("producer_gate_result" %in% names(x)) x$producer_gate_result[suppress] <- NA_character_
  x
}

build_sci03c_release_package <- function(x, small_cell_threshold) {
  x <- sci03c_add_coverage(x)
  paired <- sci03c_pair_frame(x)
  coverage <- rbind(
    sci03c_coverage_distribution(x, FALSE),
    sci03c_coverage_distribution(x, TRUE)
  )
  component <- rbind(
    sci03c_component_missingness(x, FALSE),
    sci03c_component_missingness(x, TRUE)
  )
  transition <- rbind(
    sci03c_paired_transition(paired, FALSE),
    sci03c_paired_transition(paired, TRUE)
  )
  eligibility <- rbind(
    sci03c_rule_eligibility(x, paired, FALSE),
    sci03c_rule_eligibility(x, paired, TRUE)
  )
  k50 <- rbind(
    sci03c_k50_population(paired, FALSE),
    sci03c_k50_population(paired, TRUE)
  )
  sci03d <- sci03c_sci03d_comparison(eligibility)

  list(
    coverage_distribution = sci03c_suppress(
      coverage, small_cell_threshold, c("scope", "fof_group", "timepoint")
    ),
    component_missingness = sci03c_suppress(
      component, small_cell_threshold, c("scope", "fof_group", "timepoint", "component")
    ),
    paired_transition = sci03c_suppress(
      transition, small_cell_threshold, c("scope", "fof_group")
    ),
    rule_eligibility = sci03c_suppress(
      eligibility, small_cell_threshold, c("scope", "fof_group", "window")
    ),
    k50_population = sci03c_suppress(
      k50, small_cell_threshold, c("scope", "fof_group", "rule")
    ),
    sci03d_comparison = sci03c_suppress(
      sci03d, small_cell_threshold, c("scope", "fof_group", "window")
    )
  )
}
