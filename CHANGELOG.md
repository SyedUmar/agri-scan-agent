# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Changed
- Refactored `app.py` to consume shared helpers from `agent_logic.py` and `model_loader.py` to remove duplicated logic.
- Replaced dangerous generic YOLO fallback behavior with explicit agricultural-model loading failure in `model_loader.py`.
- Added basic per-session rate limiting for analysis requests to reduce API quota abuse risk.
- Added language selection, tabbed result presentation, and lightweight in-app feedback controls for better mobile usability and flow.
- Added basic application logging for detection outcomes and unexpected errors.
