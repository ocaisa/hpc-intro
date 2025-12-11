##
## R script to chain-load hierarchical lesson configuration YAML files.
## Top-level configuration is typically "../config.yaml".
##

library(yaml)
library(tools)
library(knitr)

# -------------------------------------------------------------------
# Define placeholder config and snippets() early so it always exists
# -------------------------------------------------------------------
config <- NULL
snippets <- function(child_file) {
  stop("snippets() called before configuration was loaded.")
}

# -------------------------------------------------------------------
# Utility: Get the snippet directory next to a config file
# -------------------------------------------------------------------

get_snippet_subdir <- function(file, must_exist = TRUE) {
  full_file <- normalizePath(file)
  dir <- file.path(dirname(full_file), "snippets")
  
  if (must_exist && !dir.exists(dir)) {
    stop("Snippet directory does not exist: ", dir)
  }
  
  return(dir)
}

# -------------------------------------------------------------------
# Load lesson configuration
# -------------------------------------------------------------------
config_file <- normalizePath("config.yaml")
if(!file.exists(config_file)) {
  # exactly where the config file is depends on what stage we are in the workflow
  config_file <- normalizePath("../config.yaml")
}
if(!file.exists(config_file)) {
  stop("Could not find lesson configuration: ", config_file)
}
lesson_config <- yaml.load_file(config_file)
# message("Loaded lesson config")

# -------------------------------------------------------------------
# Validate required fields
# -------------------------------------------------------------------

if (is.null(lesson_config$default_config)) {
  stop("default_config is not defined in top-level configuration: ", config_file)
}

if (!file.exists(lesson_config$default_config)) {
  stop("Default configuration file does not exist: ", lesson_config$default_config)
}

# -------------------------------------------------------------------
# Load fallback/default config
# -------------------------------------------------------------------

config <- yaml.load_file(lesson_config$default_config)
fallback_snippets <- get_snippet_subdir(lesson_config$default_config)

# -------------------------------------------------------------------
# Load optional custom config and merge
# -------------------------------------------------------------------

# Get environment variable
custom_config_file <- Sys.getenv("HPC_CARPENTRY_CUSTOMIZATION")

# If not set, fall back to lesson_config$custom_config (which may be NULL)
if (custom_config_file == "") {
  custom_config_file <- lesson_config$custom_config
}
if (!is.null(custom_config_file)) {
  if (file.exists(custom_config_file)) {
    
    custom_config <- yaml.load_file(custom_config_file)
    
    # merge: custom overrides default
    config <- modifyList(config, custom_config)
    
    # snippet directory for custom configs does NOT have to exist
    main_snippets <- get_snippet_subdir(
      custom_config_file,
      must_exist = FALSE
    )
  } else {
    stop("Custom configuration provided but does not exist: ", custom_config_file)
  }
  
} else {
  # no custom config → only fallback snippets available
  main_snippets <- fallback_snippets
}

# message("Main config snippets from ", main_snippets, ", fallbacks from ", fallback_snippets)
# -------------------------------------------------------------------
# snippets(): pick main-override version or fallback version
# -------------------------------------------------------------------

snippets <- function(child_file) {
  
  # directory of the *currently-rendered* file
  current_dir <- dirname(knitr::current_input(dir = TRUE))
  
  # Construct absolute paths to the snippet candidates
  doc_paths <- list(
    main     = file.path(main_snippets, child_file),
    fallback = file.path(fallback_snippets, child_file)
  )
  
  # print(doc_paths)
  
  if (file.exists(doc_paths$main)) {
    message("Using MAIN snippet: ", doc_paths$main)
    return(doc_paths$main)
  }
  
  if (file.exists(doc_paths$fallback)) {
    message("Using FALLBACK snippet: ", doc_paths$fallback)
    return(doc_paths$fallback)
  }
  
  stop("No snippet file exists: ", child_file,
       "\nMain path: ",     doc_paths$main,
       "\nFallback path: ", doc_paths$fallback)
}

# -------------------------------------------------------------------
# End of script
# -------------------------------------------------------------------
