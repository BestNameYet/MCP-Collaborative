# MIS Solver Adapter Handoff

This folder preserves the exact `MIS-Solver-Adapter-Handoff-2026-08-30.zip` archive for remote transfer.

The GitHub connector used to archive it only accepts UTF-8 text, so the ZIP is stored losslessly as Base64 in:

`MIS-Solver-Adapter-Handoff-2026-08-30.zip.b64`

Original ZIP SHA-256:

`a721b4fbc18c1e7ff8f04f074ed1f0a450db28298528e439e0c17586ce1ef93f`

## Reconstruct on Linux/macOS

```bash
base64 -d MIS-Solver-Adapter-Handoff-2026-08-30.zip.b64 > MIS-Solver-Adapter-Handoff-2026-08-30.zip
sha256sum MIS-Solver-Adapter-Handoff-2026-08-30.zip
unzip MIS-Solver-Adapter-Handoff-2026-08-30.zip
```

## Reconstruct on PowerShell

```powershell
[IO.File]::WriteAllBytes(
  "MIS-Solver-Adapter-Handoff-2026-08-30.zip",
  [Convert]::FromBase64String((Get-Content "MIS-Solver-Adapter-Handoff-2026-08-30.zip.b64" -Raw))
)
Get-FileHash "MIS-Solver-Adapter-Handoff-2026-08-30.zip" -Algorithm SHA256
Expand-Archive "MIS-Solver-Adapter-Handoff-2026-08-30.zip" -DestinationPath .
```

The handoff package itself contains `HANDOFF.md`, `REMOTE_APPLY.md`, reference MIS/controller integration code, retrieval adapter code, server integration code, and tests. Its stated purpose is to revise MIS so a Solver Architecture KB adapter can be attached without changing the transaction protocol or using recursive MCP self-calls.
