# Contributing to Numerics

Thank you for your interest in contributing to Numerics-Python-Examples! We welcome bug reports, feature requests, validation results, and other feedback from the community.

## Review Capacity

This software is maintained by a small team within the U.S. Army Corps of Engineers Risk Management Center (USACE-RMC). **Our capacity to review external pull requests is very limited.** We prioritize issues and bug reports, which are always welcome and will be reviewed as resources permit.

If you plan to submit a pull request, please open an issue first to discuss your proposed change. This helps avoid duplicated effort and ensures your contribution aligns with the project's direction.

## How to Contribute

### Report a Bug

If you find a bug, please [open an issue](../../issues/new) and include:

- Steps to reproduce the problem
- Input data and configuration (if applicable)
- Expected behavior vs. actual behavior
- Software version and operating system
- Any relevant error messages or screenshots

### Request a Feature

Feature requests are welcome. Please [open an issue](../../issues/new) describing:

- The use case or problem you are trying to solve
- How you envision the feature working
- Any references to statistical methods or published literature

### Report Validation Results

Given the life-safety applications of Numerics, which this demo is an extension of, independent validation is especially valuable. If you have compared this software's results against other software (e.g., R packages, published tables, or analytical solutions), we would appreciate hearing about it through an issue.

### Submit a Pull Request

Pull requests may take several weeks or longer to review. Before submitting code:

1. **Open an issue first** to discuss the proposed change
2. **Follow PEP 8** and add docstrings to new functions and modules; clear notebook outputs before submitting (`jupyter nbconvert --clear-output --inplace notebooks/*.ipynb`)
3. **Include validation** against known results (R, SciPy, Mathematica, or published tables) where applicable
4. **Ensure notebooks run end to end** without errors in a fresh virtual environment

## Developer Certificate of Origin

By submitting a pull request, you certify under the [Developer Certificate of Origin (DCO) Version 1.1](https://developercertificate.org/) that you have the right to submit the work under the license associated with this project and that you agree to the DCO.

All contributions will be released under the same license as the project (see [LICENSE](LICENSE)).

## Federal Government Contributors

U.S. Federal law prevents the government from accepting gratuitous services unless certain conditions are met. By submitting a pull request, you acknowledge that your services are offered without expectation of payment and that you expressly waive any future pay claims against the U.S. Federal government related to your contribution.

If you are a U.S. Federal government employee and use a `*.mil` or `*.gov` email address, your contribution is understood to have been created in whole or in part as part of your official duties and is not subject to domestic copyright protection under 17 USC 105.

## Security

If you discover a security vulnerability, please do **not** open a public issue. Instead, contact the RMC team directly through official USACE-RMC channels.

## License

See [LICENSE](LICENSE) for details. This software is released under the Zero-Clause BSD (0BSD) license.