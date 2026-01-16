import datetime

import polars as pl

from neural_ai.processors.processing.factory import create_time_alignment_service


def test_time_alignment():
    """Gyors teszt a TimeAlignmentService-hez."""
    # Mesterséges hiányos DataFrame generálás
    timestamps = [
        datetime.datetime(2023, 1, 1, 10, 0),
        datetime.datetime(2023, 1, 1, 10, 2),
        datetime.datetime(2023, 1, 1, 10, 4),
    ]
    df = pl.DataFrame({"timestamp": timestamps, "close": [1.0, 1.2, 1.4]}).with_columns(
        pl.col("timestamp").cast(pl.Datetime)
    )

    # Service létrehozása
    service = create_time_alignment_service()

    # reindex_to_grid futtatás
    aligned = service.reindex_to_grid(df, "1m")

    # handle_gaps futtatás
    filled = service.handle_gaps(aligned, "forward_fill")

    # Lyukmentes kimenet ellenőrzés
    assert filled["close"].null_count() == 0, "Lyukak maradtak a close oszlopban!"
    assert len(filled) == 5, f"Hibás hossz: {len(filled)} helyett 5"

    print("✅ TimeAlignmentService teszt sikeres!")


if __name__ == "__main__":
    test_time_alignment()
