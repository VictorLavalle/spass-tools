# Contributing to spass-tools

Thanks for your interest in contributing! Here's how to get started.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/spass-tools.git
   cd spass-tools
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Create a branch for your change:
   ```bash
   git checkout -b my-feature
   ```

## Making Changes

- Keep changes focused — one feature or fix per PR
- Follow the existing code style
- Test your changes with both encrypt and decrypt flows
- Update documentation if your change affects usage

## Submitting a Pull Request

1. Push your branch to your fork
2. Open a PR against `main`
3. Describe what your change does and why

## Reporting Bugs

Open an [issue](https://github.com/VictorLavalle/spass-tools/issues) with:
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

## Security Issues

See [SECURITY.md](SECURITY.md) for reporting vulnerabilities.
