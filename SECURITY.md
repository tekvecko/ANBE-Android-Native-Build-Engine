# Security Policy

## Release signing secrets

Never commit Android signing material to this repository.

ANBE expects release credentials through:

- `ANBE_KEYSTORE`
- `ANBE_KEYSTORE_PASSWORD`
- `ANBE_KEY_ALIAS`
- `ANBE_KEY_PASSWORD`

Keep keystores outside project repositories and protect backups carefully.

ANBE reports may contain non-secret metadata such as artifact hashes,
application IDs and signer certificate fingerprints.

## Vulnerability reporting

Do not publish exploitable vulnerabilities in a public issue before
maintainers have had a reasonable opportunity to review them.

Use GitHub private security reporting when available.
