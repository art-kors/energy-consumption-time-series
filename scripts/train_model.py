"""Model training script."""

from pathlib import Path

from library.functional import pickle_model


def main() -> None:
    """Train models and save them."""
    file_ending_length = 11

    for company in Path("./data/companies/").iterdir():
        company_name = company.name[:-file_ending_length]
        if not Path(f"./data/models/{company_name}_regressor.pkl").exists():
            pickle_model(company_name)


if __name__ == "__main__":
    main()
