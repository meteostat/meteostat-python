# Meteostat Python Constitution

## Core Principles

### I. Data Integrity First
**Weather data must be accurate, reliable, and traceable.**
- All data sources must be verified and documented
- Data transformations must be transparent and reversible
- Missing data must be handled explicitly (never silently fill with assumptions)
- Interpolation methods must be scientifically sound and clearly documented
- Cache mechanisms must ensure data consistency and freshness

### II. API Stability & Backward Compatibility
**User-facing APIs are sacred contracts.**
- Public API changes require major version bumps
- Internal properties must be prefixed with underscore (`_`)
- All public exports must be listed in `__all__`
- Deprecation warnings required 1 major version before removal
- Breaking changes must include migration guides

### III. Test-Driven Development
**All features must be tested before implementation.**
- Unit tests for all core logic (target: >90% coverage)
- Integration tests for API endpoints and data providers
- E2E tests for complete user workflows
- Test structure: `tests/{unit|integration|e2e|provider|system}`
- Mock external dependencies (network, file system) in unit and integration tests

### IV. Type Safety & Code Quality
**Code must be statically analyzable and maintainable.**
- Type hints required for all public functions (enforce via mypy)
- Code formatted with Black (non-negotiable)
- Linting with pylint (see `.pylintrc` for rules)
- No ignored type errors without documented justification
- `py.typed` marker present for PEP 561 compliance

### V. Performance & Resource Efficiency
**Handle large datasets gracefully.**
- Lazy loading where possible (don't fetch until needed)
- Efficient caching with automatic cleanup
- Support for data aggregation and filtering at source
- Memory-conscious pandas operations
- Configurable timeouts and retry logic

### VI. User Experience & Documentation
**Simple things should be simple; complex things should be possible.**
- Intuitive API with sensible defaults
- Rich examples in docstrings and README
- Clear error messages with actionable guidance
- Configuration system for power users
- Support both programmatic and interactive usage (e.g., matplotlib integration)

## Architecture Standards

### Module Organization
- **`api/`**: User-facing endpoint classes (Station, Point, hourly, daily, etc.)
- **`core/`**: Internal infrastructure (loader, config, cache)
- **`providers/`**: Data source integrations
- **`interpolation/`**: Spatial/temporal interpolation algorithms
- **`utils/`**: Helpers, validators, parsers, filters, decorators
- **`enumerations.py`**: Shared enums (Parameter, Provider, TTL)
- **`parameters.py`**: Weather parameter definitions
- **`units.py`**: Unit conversion utilities
- **`typing.py`**: Custom type definitions

### Data Flow Principles
1. User requests data via API classes
2. Core loader fetches from cache or remote
3. Provider-specific adapters normalize data
4. Interpolation/aggregation applied if requested
5. Return pandas DataFrame for analysis

### Dependencies
- **Core**: `requests`, `pandas`, `pytz` (minimize dependencies)
- **Dev**: `mypy`, `black`, `pytest`, `pytest-mock`
- **Optional**: `matplotlib`, `metar`, `lxml` (extras only)

## Development Workflow

### Before Starting Work
1. Check existing tests to understand expected behavior
2. Review related modules in CHECKLIST.md (if applicable)
3. Verify dependencies are up to date (`poetry install`)

### Making Changes
1. Write/update tests first (TDD)
2. Implement minimal changes to pass tests
3. Run full test suite: `pytest tests/`
4. Type check: `mypy meteostat/`
5. Format code: `black meteostat/ tests/`
6. Lint: `pylint meteostat/`

### Code Review Requirements
- All tests pass (unit, integration, e2e)
- Type checking passes with no errors
- Code formatted and linted
- Documentation updated if API changed
- No performance regressions on large datasets

### Testing Standards
- **Unit**: Test individual functions/methods in isolation
- **Integration**: Test interactions between modules
- **Provider**: Test data source integrations (may require mocking)
- **E2E**: Test complete user workflows
- **System**: Test configuration and environment handling

## Quality Gates

### Pre-Commit (Local)
- [ ] Black formatting applied
- [ ] Type hints present on new functions
- [ ] Tests written and passing locally

### Pre-Merge (CI/CD)
- [ ] Full test suite passes
- [ ] Mypy type checking passes
- [ ] Pylint score acceptable
- [ ] No new security vulnerabilities
- [ ] Documentation builds successfully

### Pre-Release
- [ ] All integration tests pass with real data sources
- [ ] Examples in README verified
- [ ] CHANGELOG.md updated
- [ ] Version bumped according to semver
- [ ] Migration guide written (if breaking changes)

## Data Licensing & Attribution

**Weather data licensing must be respected.**
- Meteostat data: CC BY-NC 4.0 International
- Attribution required in derivative works
- Commercial use requires separate licensing
- Code licensed under MIT (separate from data)

## Governance

### Amendment Process
1. Propose change via issue/discussion
2. Document rationale and impact
3. Require maintainer approval
4. Update constitution version
5. Announce in CHANGELOG

### Conflict Resolution
- Constitution supersedes all other documentation
- When unclear, prioritize: Data Integrity → API Stability → User Experience
- Maintainers have final decision authority
- Document exceptions with clear justification

### Continuous Improvement
- Review constitution quarterly
- Gather feedback from contributors
- Update based on lessons learned
- Archive old versions for reference

**Version**: 1.0.0 | **Ratified**: 2025-10-22 | **Last Amended**: 2025-10-22
