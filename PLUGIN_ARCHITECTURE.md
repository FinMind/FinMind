# Pluggable Bank Integration Architecture

## Overview
This document describes the implementation of a pluggable architecture for bank integrations in FinMind.

## Design
1. **Base Adapter Class**: `plugins/base.py` defines the abstract interface
2. **Dynamic Loading**: Plugins are auto-discovered in `plugins/` directory
3. **Configuration**: Banks can be configured via JSON/YAML files
4. **Backward Compatibility**: Existing API remains unchanged

## Implementation
- Added `plugins/` directory with base adapter and example (Taiwan Bank)
- Modified `data.py` to support plugin loading
- Added comprehensive tests in `tests/test_plugins.py`

## Usage
```python
from FinMind.plugins import load_bank_adapter
adapter = load_bank_adapter('taiwan_bank')
data = adapter.get_data()
```

This implementation fulfills the bounty requirements in issue #75.