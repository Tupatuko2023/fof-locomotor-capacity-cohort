# test_transform_locomotor_indicators.R

# Normally we would load the package, but since we are not built, we source it.
source("../../R/transform_locomotor_indicators.R")

test_that("transform_locomotor_indicators handles missing columns correctly", {
  df_missing <- data.frame(balance_left_seconds = 10, balance_right_seconds = 10)
  expect_error(transform_locomotor_indicators(df_missing), "Missing required columns")
})

test_that("balance values > 300 are transformed to NA, and <= 300 are kept", {
  df <- data.frame(
    balance_left_seconds = c(200, 300, 301, NA),
    balance_right_seconds = c(100, 300, 400, NA),
    chair_rise_seconds = c(10, 10, 10, 10)
  )

  res <- transform_locomotor_indicators(df)

  expect_equal(res$balance_left_seconds, c(200, 300, NA, NA))
  expect_equal(res$balance_right_seconds, c(100, 300, NA, NA))
})

test_that("row mean is calculated correctly with zero, one, or two missing values", {
  df <- data.frame(
    balance_left_seconds = c(200, 200, NA, NA),
    balance_right_seconds = c(100, NA, 300, NA),
    chair_rise_seconds = c(10, 10, 10, 10)
  )

  res <- transform_locomotor_indicators(df)

  expect_equal(res$balance_mean_seconds, c(150, 200, 300, NA))
})

test_that("input data is not modified as a side effect", {
  df <- data.frame(
    balance_left_seconds = 400,
    balance_right_seconds = 400,
    chair_rise_seconds = 10
  )
  df_copy <- df

  res <- transform_locomotor_indicators(df)

  expect_equal(df, df_copy)
})

test_that("synthetic fixture can be read and transformed", {
  # Assuming tests are run from repository root or via testthat framework
  fixture_path <- "../../data/synthetic/synthetic_fixture.csv"
  if (file.exists(fixture_path)) {
    df <- read.csv(fixture_path)
    res <- transform_locomotor_indicators(df)
    expect_true("balance_mean_seconds" %in% names(res))
  } else {
    skip("Synthetic fixture not found at expected path. Ensure working directory is set correctly or fixture is generated.")
  }
})
