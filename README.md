# REBASE Restriction Enzyme Database

Auto-updated restriction enzyme database parsed from [REBASE](http://rebase.neb.com) - The Restriction Enzyme Database, containing all **commercially available** enzymes in the database.

## Direct Access

**Latest enzyme database**: https://raw.githubusercontent.com/nathanaelandrews/rebase-db/main/enzymes.tsv

- Updated monthly from REBASE
- 584+ commercially available restriction enzymes
- IUPAC ambiguous bases preserved for flexibility
- Ready for direct download/import

## Database Format

The database is provided as a tab-separated file (TSV) with the following columns:

| Column | Description |
|--------|-------------|
| `enzyme_name` | Name of the restriction enzyme |
| `recognition_seq_5to3` | Recognition sequence (5' to 3') with IUPAC codes |
| `antisense_seq_5to3` | Reverse complement of recognition sequence |
| `prototype` | Name of the prototype enzyme (if isoschizomer) |
| `commercial_sources` | Single-letter codes for commercial suppliers |

### Example Entries

```
enzyme_name	recognition_seq_5to3	antisense_seq_5to3	prototype	commercial_sources
BsaI	GGTCTC	GAGACC	BsaI	BIKMNQRSX
EcoRI	GAATTC	GAATTC	EcoRI	BIKMNQRSX
BamHI	GGATCC	GGATCC	BamHI	BIKMNQRSX
AccI	GTMKAC	GTMKAC	AccI	JNQVX
SgeI	CNNGNNNNNNNNN	NNNNNNNNCNNG	SgeI	B
```

### Commercial Source Codes

- B = Thermo Fisher Scientific
- I = SibEnzyme Ltd.
- J = Nippon Gene Co., Ltd.
- K = Takara Bio Inc.
- M = Roche Custom Biotech
- N = New England Biolabs
- Q = Molecular Biology Resources - CHIMERx
- R = Promega Corporation
- S = Sigma Chemical Corporation
- V = Vivantis Technologies
- X = EURx Ltd.

## Usage Examples

### Command Line
```bash
# Download latest database
curl -o enzymes.tsv https://raw.githubusercontent.com/nathanaelandrews/rebase-db/main/enzymes.tsv

# Get all BsaI-like enzymes
grep "BsaI" enzymes.tsv
```

## Data Source

This database is automatically generated from [REBASE](http://rebase.neb.com) (The Restriction Enzyme Database), maintained by Dr. Richard J. Roberts at New England Biolabs.

**Citation**: Roberts, R.J., Vincze, T., Posfai, J., and Macelis, D. (2015) REBASE--a database for DNA restriction and modification: enzymes, genes and genomes. *Nucleic Acids Res.*, DOI = 10.1093/nar/gku1046.

## Updates

The database is automatically updated monthly via GitHub Actions. Version information is tracked to ensure only new releases trigger updates.

## License

The REBASE data is used under academic/research purposes. Please refer to [REBASE terms of use](http://rebase.neb.com) for commercial applications.

## Contact

Repository maintained by [@nathanaelandrews](https://github.com/nathanaelandrews).
