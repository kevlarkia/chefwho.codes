"use client";

import { booksIn, LEFT_OFF_THE_SHELF } from "@/lib/canon/shelf";
import type { Book } from "@/lib/canon/types";
import { useCanon } from "./CanonProvider";

function BookList({
  books,
  action,
  onMove,
}: {
  books: Book[];
  action: string;
  onMove: (id: string) => void;
}) {
  if (books.length === 0) {
    return <p>None.</p>;
  }
  return (
    <ul className="canon-sources">
      {books.map((book) => (
        <li key={book.id} className="canon-claim">
          <h3>{book.title}</h3>
          {book.author ? <p>{book.author}</p> : null}
          {book.note ? <p>{book.note}</p> : null}
          <button
            type="button"
            className="secondary-button"
            onClick={() => onMove(book.id)}
          >
            {action}
          </button>
        </li>
      ))}
    </ul>
  );
}

export function BooksRoom() {
  const { state, placeBook } = useCanon();
  const read = booksIn(state.shelf, "read");
  const toGet = booksIn(state.shelf, "to-get");

  return (
    <section className="canon-stack">
      <h2>Books</h2>
      <p>
        A shelf, not a set of claims. Moving a title does not delete it. Books
        are not read aloud.
      </p>
      <h3>Read</h3>
      <BookList
        books={read}
        action="Move to to-get"
        onMove={(id) => placeBook(id, "to-get")}
      />
      <h3>To get</h3>
      <BookList
        books={toGet}
        action="Move to read"
        onMove={(id) => placeBook(id, "read")}
      />
      <h3>Left off the shelf</h3>
      <ul className="canon-plain">
        {LEFT_OFF_THE_SHELF.map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>
    </section>
  );
}
