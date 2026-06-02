- [ ] Inspect and confirm prediction wiring in `app.py` (which function UI calls)
- [ ] Implement a single unified two-stage predictor (done in `backend/predict_two_stage.py`)


- [x] Fix leaf-confidence mapping to match actual leaf-vs-non-leaf model output semantics (in progress—needs raw output verification)

- [x] Ensure `frontend/ui.py` calls only the unified predictor and expects the same keys
- [x] Add optional debug toggle in the UI to display raw leaf model output + computed probabilities


- [ ] Polish UI: improve result section layout + top predictions rendering + consistent cards
- [ ] Run Streamlit locally and test with images from `test/`
- [ ] Update README if needed (about debug toggle / behavior)

