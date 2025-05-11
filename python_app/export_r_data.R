# Load the R data files
load("../R/ddf.rda")
load("../R/original_question_df.rda")

# Create data directory if it doesn't exist
dir.create("data", showWarnings = FALSE)

# Export data frames to CSV
write.csv(ddf, "data/survey_data.csv", row.names = FALSE)
write.csv(original_question_df, "data/questions.csv", row.names = FALSE) 