import { marcoShelf } from "./shelf-marco-2026-09-29";
import type { Book, BookPlace } from "./types";

export const LEFT_OFF_THE_SHELF = [
  "HBR Guide to Your Personal Growth was cut off at the top of the page and was not placed on either list.",
  "A trailing police fragment on that page was not part of the library. The fragment itself was not kept.",
  "The Secret was not placed. Marco Andrade asked for a synopsis before he approves it. Looked up, and not treated as his citation: Rhonda Byrne, Atria Books/Beyond Words, 2006. The book says thought, called the law of attraction, brings what a person wants. He has not approved it.",
] as const;

function book(
  id: string,
  title: string,
  author: string,
  place: BookPlace,
  note?: string,
): Book {
  return note ? { id, title, author, place, note } : { id, title, author, place };
}

export function seedShelf(): Book[] {
  return [
    book("book-my-big-toe", "My Big TOE", "Thomas Campbell", "read"),
    book("book-remote-viewing", "Remote Viewing", "David Morehouse", "read"),
    book(
      "book-conspiracy-theories-unveiled",
      "Conspiracy Theories Unveiled",
      "Logan Cross",
      "read",
    ),
    book("book-mind-is-the-master", "Mind is the Master", "James Allen", "read"),
    book(
      "book-sociotechnical-insights",
      "Sociotechnical Insights and AI Driverless Cars, Practical Innovations in AI and Machine Learning",
      "Lance Eliot",
      "read",
    ),
    book(
      "book-hbr-insights-ai",
      "Insights You Need From Harvard Business Review: Artificial Intelligence",
      "Harvard Business Review",
      "read",
    ),
    book(
      "book-hbr-10-ai",
      "HBR's 10 Must Reads on AI",
      "Harvard Business Review",
      "read",
    ),
    book(
      "book-life-application",
      "Life Application Study Bible, third edition, personal size, NLT",
      "Tyndale",
      "to-get",
    ),
    book("book-meditations", "Meditations", "Marcus Aurelius", "to-get"),
    book("book-ethics", "Ethics", "Benedictus de Spinoza", "to-get"),
    book("book-art-of-war", "The Art of War", "Sunzi", "to-get"),
    book(
      "book-egyptian-dead",
      "The Egyptian Book of the Dead",
      "Author unknown",
      "to-get",
      "Translation credit as given: D. Le Page and Edouard Naville. The note as written spelled the second name Edouord.",
    ),
    book(
      "book-four-dimensional-vistas",
      "Four Dimensional Vistas",
      "Claude Fayette Bragdon",
      "to-get",
    ),
    book(
      "book-48-laws",
      "The 48 Laws of Power",
      "Robert Greene",
      "to-get",
    ),
    book(
      "book-33-strategies",
      "The 33 Strategies of War",
      "Robert Greene",
      "to-get",
    ),
    book(
      "book-art-of-seduction",
      "The Art of Seduction",
      "Robert Greene",
      "to-get",
    ),
    book(
      "book-bitcoin-starting",
      "A starting book on Bitcoin",
      "",
      "to-get",
      "Recommended as the first crypto book. The title was not kept.",
    ),
    book(
      "book-hbr-agile",
      "Insights You Need from Harvard Business Review: Agile",
      "",
      "to-get",
    ),
    book(
      "book-hbr-blockchain",
      "Insights You Need from Harvard Business Review: Blockchain",
      "",
      "to-get",
    ),
    book(
      "book-hbr-cybersecurity",
      "Insights You Need from Harvard Business Review: Cybersecurity",
      "",
      "to-get",
    ),
    book(
      "book-hbr-monopolies",
      "Insights You Need from Harvard Business Review: Monopolies and Tech Giants",
      "",
      "to-get",
    ),
    book(
      "book-hbr-strategic-analytics",
      "Insights You Need from Harvard Business Review: Strategic Analytics",
      "",
      "to-get",
    ),
    book(
      "book-hbr-essentials",
      "HBR's 10 Must Reads: The Essentials",
      "",
      "to-get",
    ),
    book(
      "book-hbr-new-managers",
      "HBR's 10 Must Reads for New Managers",
      "",
      "to-get",
    ),
    book(
      "book-hbr-change",
      "HBR's 10 Must Reads on Change Management",
      "",
      "to-get",
    ),
    book(
      "book-hbr-communication",
      "HBR's 10 Must Reads on Communication",
      "",
      "to-get",
    ),
    book(
      "book-hbr-diversity",
      "HBR's 10 Must Reads on Diversity",
      "",
      "to-get",
    ),
    book(
      "book-hbr-emotional",
      "HBR's 10 Must Reads on Emotional Intelligence",
      "",
      "to-get",
    ),
    book(
      "book-hbr-leadership",
      "HBR's 10 Must Reads on Leadership",
      "",
      "to-get",
    ),
    book(
      "book-hbr-managing-people",
      "HBR's 10 Must Reads on Managing People",
      "",
      "to-get",
    ),
    ...marcoShelf(),
  ];
}

export function mergeShelf(stored: Book[]): Book[] {
  const seen = new Set(stored.map((item) => item.id));
  return [...stored, ...seedShelf().filter((item) => !seen.has(item.id))];
}

export function moveBook(shelf: Book[], id: string, place: BookPlace): Book[] {
  return shelf.map((item) => (item.id === id ? { ...item, place } : item));
}

export function booksIn(shelf: Book[], place: BookPlace): Book[] {
  return shelf.filter((item) => item.place === place);
}
