# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-11-23

### 🎉 Major Release - Production Ready

### Added
- ✅ Comprehensive error handling across all modules
- ✅ Input validation and sanitization
- ✅ Cross-platform compatibility (Windows, macOS, Linux)
- ✅ Automatic directory creation for datasets
- ✅ User-friendly feedback system with ✓, ⚠, ❌ indicators
- ✅ Resource management (camera release, window cleanup)
- ✅ Boundary checking for image processing
- ✅ Named constants for all configuration parameters
- ✅ Function docstrings and improved documentation
- ✅ Alpha channel blending for transparent filters
- ✅ Interactive input prompts with validation
- ✅ Progress indicators during data collection
- ✅ CSV export for filter coordinates
- ✅ Complete setup documentation

### Changed
- 🔄 Migrated from hardcoded absolute paths to relative paths
- 🔄 Improved filter positioning (sunglasses span both eyes)
- 🔄 Enhanced moustache placement (below nose, not on it)
- 🔄 Better filter scaling based on facial feature dimensions
- 🔄 Optimized face cropping with boundary detection
- 🔄 Improved user messages and feedback
- 🔄 Restructured code with modular architecture

### Fixed
- 🐛 Fixed typo: `traiing_set` → `training_set`
- 🐛 Fixed typo: `prdict` → `predict`
- 🐛 Fixed camera initialization without validation
- 🐛 Fixed missing file checks for images and templates
- 🐛 Fixed dataset validation (checks for .npy files)
- 🐛 Fixed empty input acceptance
- 🐛 Fixed alpha channel removal in filters (was creating rectangular overlays)
- 🐛 Fixed duplicate comments in snap.py
- 🐛 Fixed potential crashes near frame edges
- 🐛 Fixed negative array indices in face cropping
- 🐛 Fixed frame read validation

### Removed
- ❌ Removed hardcoded paths to `/Users/armanmalik/Desktop/`
- ❌ Removed magic numbers (replaced with named constants)
- ❌ Removed duplicate comments

---

## [1.0.0] - 2025-11-XX

### Initial Release

### Added
- Basic face recognition using custom KNN implementation
- Real-time webcam processing
- Face data collection module
- AR filter application (sunglasses, moustache)
- Haar Cascade face detection
- NumPy-based data storage (.npy format)

### Known Issues
- Hardcoded paths not portable
- No error handling
- No input validation
- Alpha channel issues in filters
- Missing camera validation
- No boundary checking

---

## Version History Summary

| Version | Date | Status | Highlights |
|---------|------|--------|-----------|
| **2.0.0** | 2025-11-23 | ✅ Stable | Production-ready, fully documented |
| **1.0.0** | 2025-11-XX | ⚠️ Beta | Initial working version |

---

## Upcoming Features (Roadmap)

### v2.1.0 (Planned)
- [ ] Confidence score display
- [ ] Unknown person detection
- [ ] Performance metrics dashboard
- [ ] Multiple algorithm comparison

### v3.0.0 (Future)
- [ ] Web interface (Flask/FastAPI)
- [ ] REST API for recognition service
- [ ] SQLite database integration
- [ ] Mobile app support
- [ ] Deep learning models (CNN)

---

## Migration Guide

### From v1.0.0 to v2.0.0

**Breaking Changes:**
- Dataset path changed from absolute to relative
  - Old: `/Users/armanmalik/Desktop/face_recog/`
  - New: `./face_dataset/` (in project directory)

**Action Required:**
1. Move existing `.npy` files to `face_dataset/` folder
2. Update any custom scripts using absolute paths
3. No code changes needed if using default configuration

**Benefits:**
- ✅ Works on any computer
- ✅ Easy to share and deploy
- ✅ No configuration needed

---

## Contributors

- **Arman Malik** - Initial work and v2.0.0 refactor

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

