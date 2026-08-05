# 01_generate_synthetic_fixture.R
# This script generates synthetic test data that is explicitly fake and meant only
# for testing the data pipeline and rendering smoke tests.
# It DOES NOT mimic the original study data or estimates in any way.

set.seed(42)

n_samples <- 20

synthetic_data <- data.frame(
  synthetic_id = sprintf("S-%03d", 1:n_samples),
  time = rep(c(0, 12), length.out = n_samples),
  fof = sample(c("Yes", "No", "Unknown"), n_samples, replace = TRUE),
  gait_speed = round(runif(n_samples, 0.5, 1.8), 2),
  chair_rise_seconds = round(runif(n_samples, 8, 25), 1),
  balance_left_seconds = c(round(runif(n_samples - 5, 0, 150)), 300, 305, 400, NA, NA),
  balance_right_seconds = c(round(runif(n_samples - 4, 0, 150)), 300, 350, NA, NA)
)

# Shuffle the columns slightly to mix up the manually added edge cases
synthetic_data$balance_left_seconds <- sample(synthetic_data$balance_left_seconds)
synthetic_data$balance_right_seconds <- sample(synthetic_data$balance_right_seconds)

write.csv(synthetic_data, "data/synthetic/synthetic_fixture.csv", row.names = FALSE)

cat("Generated synthetic fixture at data/synthetic/synthetic_fixture.csv\n")
