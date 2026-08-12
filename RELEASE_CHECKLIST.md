# CBBO Waste Collection – Release checklist

1. Update `custom_components/cbbo_waste_collection/manifest.json`.
2. Update `CHANGELOG.md`, `README.md` and `info.md` when needed.
3. Push the files to `main`.
4. Wait for **Validate**, **Validate with hassfest**, and the Python tests to pass.
5. Create the GitHub tag `vX.Y.Z`, exactly matching the manifest version.
6. Create a **full GitHub Release** from that tag; do not publish only a tag.
7. Mark the stable release as **Latest** and do not use draft/pre-release unless intended.
8. Check Actions after publication: HACS validation and Hassfest run again on the release event.
9. HACS custom repositories refresh through GitHub on their own schedule. Opening the repository in HACS or using **Update information** forces an immediate metadata refresh.
