import Link from 'next/link';

type Author = {
  name: string;
  affiliation?: string;
  isBot: boolean;
};

type PaperCardProps = {
  id: string;
  title: string;
  abstract: string | null;
  authors: Author[] | null;
  categories: string[] | null;
  createdAt: Date | null;
};

export function PaperCard({ id, title, abstract, authors, categories, createdAt }: PaperCardProps) {
  const formattedDate = createdAt
    ? new Date(createdAt).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      })
    : null;

  return (
    <article className="border-b border-gray-200 py-4">
      <div className="flex items-start gap-4">
        <div className="flex-1">
          <h2 className="text-lg font-medium">
            <Link href={`/abs/${id}`} className="text-blue-700 hover:text-blue-900">
              {title}
            </Link>
          </h2>

          {authors && authors.length > 0 && (
            <p className="text-sm text-gray-600 mt-1">
              {authors.map((a, i) => (
                <span key={i}>
                  {a.name}
                  {a.isBot && <span className="text-xs ml-1">[bot]</span>}
                  {i < authors.length - 1 && ', '}
                </span>
              ))}
            </p>
          )}

          {abstract && (
            <p className="text-sm text-gray-700 mt-2 line-clamp-3">
              {abstract}
            </p>
          )}

          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
            <span className="font-mono">{id}</span>
            {formattedDate && <span>{formattedDate}</span>}
            {categories && categories.length > 0 && (
              <span className="flex gap-1">
                {categories.map((cat) => (
                  <span
                    key={cat}
                    className="bg-gray-100 px-1.5 py-0.5 rounded"
                  >
                    {cat}
                  </span>
                ))}
              </span>
            )}
          </div>
        </div>

        <Link
          href={`/pdf/${id}`}
          className="text-sm text-red-700 hover:text-red-900 whitespace-nowrap"
        >
          pdf
        </Link>
      </div>
    </article>
  );
}
