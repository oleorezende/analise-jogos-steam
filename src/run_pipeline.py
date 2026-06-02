from src.build_database import main as build_database
from src.create_visualizations import main as create_visualizations
from src.export_powerbi_tables import main as export_powerbi_tables
from src.prepare_data import main as prepare_data


def main() -> None:
    prepare_data()
    build_database()
    export_powerbi_tables()
    create_visualizations()


if __name__ == "__main__":
    main()
