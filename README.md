# ninecat
nine cat shares a life with you

## Container images

Two images are published to GHCR and deployed by [`pankgeorg/infra`](https://github.com/pankgeorg/infra) on the k3s cluster:

| Image | Built from | Serves |
|---|---|---|
| `ghcr.io/pankgeorg/ninecat-py`  | `backend/Dockerfile` | FastAPI backend (`api.pankgeorg.com`) |
| `ghcr.io/pankgeorg/ninecat-web` | `Dockerfile`         | CRA SPA + `/api` proxy (`pankgeorg.com`) |

Both are `linux/arm64` and tagged `:latest` and `:sha-<short>`.

### Automated (CI)
`.github/workflows/build.yml` builds and pushes both images on every push to `main`
that touches the build inputs, using GitHub-hosted `ubuntu-24.04-arm` runners.

### Native build + push (faster / fallback)
On a native arm64 host (e.g. georgettarm). One-time auth with a `write:packages` token:

```sh
gh auth refresh -h github.com -s write:packages
gh auth token | docker login ghcr.io -u pankgeorg --password-stdin
```

Then:

```sh
scripts/build-and-push.sh           # :latest + :sha-<short>
scripts/build-and-push.sh v0.2.2    # also :v0.2.2
```
