# AI Usage

## AI Assistance

Generative AI tools were used during the development of this assignment as a development and learning aid.

The AI assistance was primarily used for:

- Planning the project structure
- Designing the scraping pipeline
- Understanding web scraping concepts
- Creating initial code snippets
- Debugging Python errors
- Improving retry and error-handling logic
- Designing cleaning and validation functions
- Designing the deduplication approach
- Creating unit-test cases
- Improving documentation structure

## Human Review and Verification

All generated code was reviewed, integrated, and tested during development.

The implementation was manually executed and verified against the provided scraping sources.

Unit tests were executed using pytest, and the final test suite passed successfully.

The final scraping run was also executed successfully.

## Important Implementation Decisions

The following parts were reviewed and adapted during development:

- Requests were configured with retries for temporary HTTP errors.
- Request timeouts and delays were used to avoid aggressive scraping.
- Separate error handling was implemented for each source.
- Data cleaning and validation were separated into processing modules.
- SHA-256 fingerprints were used for duplicate detection.
- Unit tests were created for cleaning, validation, and deduplication.
- CSV and JSON outputs were generated as required by the assignment.

AI-generated suggestions were not treated as a substitute for testing or understanding the implementation. The final code was reviewed and verified by running the project and its test suite.