# CryptoQuantFactory FAQ

**Q: How to switch language?**
A: Use the sidebar in the Web UI, or set the language in CLI arguments.

**Q: How to add a new strategy?**
A: Inherit from `BaseStrategy` and implement `generate_signals` and `set_params`.

**Q: How to use my own data?**
A: Place your CSV in the `data/` folder and upload via Web UI or specify in CLI.

**Q: How to ensure my API Key is safe?**
A: Use the encryption tool in `utils/security/crypto.py`.

**Q: How to run all tests?**
A: `pytest --cov=./ --cov-report=term`

**Q: Where to get help?**
A: [GitHub Discussions](https://github.com/yourname/cryptoquantfactory/discussions)
