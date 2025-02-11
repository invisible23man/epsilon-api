## 📌 Summary
<!-- Describe the purpose of this PR in a few sentences -->

## 🔹 Changes Implemented
✅ **FastAPI Enhancements**
- [ ] Implemented modular routers (`auth`, `insights`, `trends`)
- [ ] Fixed Swagger UI (`/docs`) and OpenAPI schema handling
- [ ] Improved error handling and request validation

✅ **Dockerization**
- [ ] Added Dockerfile for FastAPI
- [ ] Configured `.dockerignore`
- [ ] Fixed Poetry installation inside the container

✅ **CI/CD Automation**
- [ ] GitHub Actions for testing and Docker builds
- [ ] Auto-deployments for `dev` and `main` branches
- [ ] Pushes Docker images to **GitHub Container Registry (GHCR)**

✅ **Testing & Code Quality**
- [ ] Fixed pytest failures in CI (`--only main`)
- [ ] Ensured all JWT authentication tests pass
- [ ] Enforced CI testing on every commit

## 🔜 Next Steps
- [ ] Integrate **Google Trends API**
- [ ] Improve authentication (DB-backed & role-based)
- [ ] Set up a staging environment for `feature` branches

---

### ✅ **Checklist Before Merge**
- [ ] My code follows the repository’s style
- [ ] I have added tests for my changes
- [ ] I have updated documentation (if applicable)
- [ ] All tests pass on CI

🔄 **Linked Issue:** [Issue #XXX] (If applicable)

---

🔥 **Note:** This PR is part of our **continuous integration & automation efforts** to ensure a scalable and maintainable backend for Epsilon. 🚀
