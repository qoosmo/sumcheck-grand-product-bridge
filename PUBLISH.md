# Publish this standalone Git repository

The downloaded project is already initialized and committed in Git. Its intended GitHub name is:

`qoosmo/sumcheck-grand-product-bridge`

## Publish using GitHub's website and Git

1. Open https://github.com/new, choose the account `qoosmo`, and enter the repository name `sumcheck-grand-product-bridge`.
2. Choose visibility (public or private). **Do not** initialize with a README, license, or .gitignore: those already exist in this project.
3. Extract `sumcheck-grand-product-bridge.zip` and from the project directory run:

```bash
cd sumcheck-grand-product-bridge
git remote add origin https://github.com/qoosmo/sumcheck-grand-product-bridge.git
git push -u origin main
```

On macOS, Git should already be installed. GitHub will ask for appropriate authentication if necessary. This repository exists locally until the user creates the GitHub remote and performs the push; the URL above should not be considered live before that step.

## Alternative with GitHub CLI (if installed and authenticated)

```bash
cd sumcheck-grand-product-bridge
gh repo create qoosmo/sumcheck-grand-product-bridge --public --source=. --remote=origin --push
```

Change `--public` to `--private` if appropriate. The commands above are publish instructions, **not** claims that the remote has been created.
