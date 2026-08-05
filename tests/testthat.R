if (!requireNamespace("testthat", quietly = TRUE)) {
  stop("Package 'testthat' is required to run the tests.")
}

testthat::test_dir("tests/testthat")
