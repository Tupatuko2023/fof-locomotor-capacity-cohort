#' Transform Locomotor Indicators
#'
#' Validates and transforms locomotor indicator variables safely.
#'
#' @param data A data frame containing at least `balance_left_seconds`, `balance_right_seconds`, and `chair_rise_seconds`.
#'
#' @return A new data frame with transformed locomotor indicators.
#' @export
transform_locomotor_indicators <- function(data) {

  # Validate required columns
  req_cols <- c("balance_left_seconds", "balance_right_seconds", "chair_rise_seconds")
  if (!all(req_cols %in% names(data))) {
    stop("Missing required columns. Data must contain: ", paste(req_cols, collapse = ", "))
  }

  # Copy data to avoid side effects
  out <- data

  # Transform balance > 300 to NA
  out$balance_left_seconds <- ifelse(out$balance_left_seconds > 300, NA, out$balance_left_seconds)
  out$balance_right_seconds <- ifelse(out$balance_right_seconds > 300, NA, out$balance_right_seconds)

  # Calculate row mean for balance (handles single missing observation natively with na.rm=TRUE)
  # When both are missing, mean(c(NA, NA), na.rm=TRUE) returns NaN, we convert it to NA
  row_means <- rowMeans(out[, c("balance_left_seconds", "balance_right_seconds")], na.rm = TRUE)
  out$balance_mean_seconds <- ifelse(is.nan(row_means), NA, row_means)

  # TODO / NEEDS_VERIFICATION:
  # Chair-rise reverse-coding transformation to describe "larger is better" is omitted in this MVP.
  # The mathematical formulation is missing from the script/manuscript snippet.
  # Do not apply undocumented clinical assumptions.

  return(out)
}
