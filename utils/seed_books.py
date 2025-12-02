import random
from typing import List

from faker import Faker

from core.database import Base, SessionLocal, engine
from models import Author, Book, Review


faker = Faker()


def ensure_authors(session, desired_count: int = 10) -> List[Author]:
    """Ensure there are at least `desired_count` authors in the database."""
    authors = session.query(Author).all()
    if len(authors) >= desired_count:
        return authors

    for _ in range(len(authors), desired_count):
        session.add(Author(name=faker.name()))
    session.commit()
    return session.query(Author).all()


def seed_books(total_books: int = 100, min_reviews: int = 1, max_reviews: int = 3) -> None:
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        authors = ensure_authors(session)
        author_ids = [author.id for author in authors]
        if not author_ids:
            raise RuntimeError("No authors available to assign to books.")

        for index in range(total_books):
            book = Book(
                title=faker.sentence(nb_words=4).rstrip("."),
                description=faker.paragraph(nb_sentences=3),
                author_id=random.choice(author_ids),
            )
            session.add(book)
            session.flush()  # ensure book has an ID for reviews

            review_count = random.randint(min_reviews, max_reviews)
            for review_index in range(review_count):
                review = Review(
                    content=faker.paragraph(nb_sentences=2),
                    rating=random.randint(1, 5),
                    book_id=book.id,
                )
                session.add(review)

        session.commit()
        print(
            f"Inserted {total_books} books along with reviews ("
            f"{min_reviews}-{max_reviews} per book) and ensured authors exist."
        )
    finally:
        session.close()


if __name__ == "__main__":
    seed_books()
