# Contributing to BABEL Protocol

Thank you for your interest in contributing to BABEL! We welcome contributions from the community.

## Ways to Contribute

- **Bug Reports:** Report issues via GitHub Issues
- **Feature Requests:** Propose new features or improvements
- **Code Contributions:** Submit pull requests
- **Documentation:** Improve docs, examples, or guides
- **Testing:** Test on different platforms and report results

## Getting Started

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/babel-protocol.git`
3. **Create** a branch: `git checkout -b feature/your-feature-name`
4. **Make** your changes
5. **Test** your changes
6. **Commit:** `git commit -m "Add: your feature description"`
7. **Push:** `git push origin feature/your-feature-name`
8. **Submit** a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all public functions
- Keep functions focused and concise

## Testing

Before submitting a PR:

```bash
# Validate your code doesn't break examples
python examples/simple_message.py
python examples/multi_ai_conversation.py

# Test validator
python tools/validator.py examples/test_message.json
```

## Documentation

- Update README.md if adding new features
- Add examples in `examples/` directory
- Update relevant docs in `docs/`

## Commit Messages

Use clear, descriptive commit messages:

- **Add:** New feature
- **Fix:** Bug fix
- **Update:** Improve existing feature
- **Refactor:** Code restructure
- **Docs:** Documentation only
- **Test:** Add or update tests

Examples:
```
Add: Support for binary message encoding
Fix: Axiom Θ2 validation for floating-point totals
Docs: Update QUICKSTART with Moltbook integration
```

## Pull Request Process

1. Ensure your code passes all examples
2. Update documentation as needed
3. Add a clear description of changes
4. Reference any related issues
5. Wait for review from maintainers

## Priority Areas

We especially welcome contributions in:

- **Platform Integrations:** Examples for major AI platforms (OpenClaw, Anthropic MCP, etc.)
- **Performance:** Optimization of validation and verification
- **Security:** Audit of cryptographic implementations
- **Testing:** Unit tests and integration tests
- **Documentation:** Tutorials, guides, and examples

## Questions?

- **GitHub Issues:** For bug reports and feature requests
- **GitHub Discussions:** For questions and general discussion
- **Email:** francesco.riva@angelia.cloud for direct contact

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Accept criticism gracefully
- Prioritize community welfare

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing private information

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make AI-to-AI communication more secure!**

— The BABEL Team @ Angelia srl SB
