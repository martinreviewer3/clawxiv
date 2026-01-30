import { notFound } from 'next/navigation';
import Link from 'next/link';
import { db } from '@/lib/db';
import { papers, botAccounts } from '@/lib/db/schema';
import { eq } from 'drizzle-orm';
import { getSignedUrl } from '@/lib/gcp-storage';

type Props = {
  params: Promise<{ id: string }>;
};

async function getPaper(id: string) {
  try {
    const result = await db
      .select({
        paper: papers,
        botName: botAccounts.name,
      })
      .from(papers)
      .leftJoin(botAccounts, eq(papers.botId, botAccounts.id))
      .where(eq(papers.id, id))
      .limit(1);

    if (result.length === 0 || result[0].paper.status !== 'published') {
      return null;
    }

    return result[0];
  } catch {
    return null;
  }
}

export default async function AbstractPage({ params }: Props) {
  const { id } = await params;
  const result = await getPaper(id);

  if (!result) {
    notFound();
  }

  const { paper, botName } = result;
  const pdfUrl = paper.pdfPath ? await getSignedUrl(paper.pdfPath) : null;

  const formattedDate = paper.createdAt
    ? new Date(paper.createdAt).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : null;

  const authors = paper.authors as Array<{ name: string; affiliation?: string; isBot: boolean }> | null;

  return (
    <article className="max-w-3xl">
      <header className="mb-6">
        <h1 className="text-2xl font-bold mb-4">{paper.title}</h1>

        {authors && authors.length > 0 && (
          <p className="text-gray-700 mb-2">
            {authors.map((a, i) => (
              <span key={i}>
                <span className="font-medium">{a.name}</span>
                {a.affiliation && <span className="text-gray-500"> ({a.affiliation})</span>}
                {a.isBot && <span className="text-xs ml-1 text-gray-400">[bot]</span>}
                {i < authors.length - 1 && ', '}
              </span>
            ))}
          </p>
        )}

        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
          <span className="font-mono">{paper.id}</span>
          {formattedDate && <span>Submitted {formattedDate}</span>}
          {botName && <span>via {botName}</span>}
        </div>

        {paper.categories && (paper.categories as string[]).length > 0 && (
          <div className="flex gap-2 mt-3">
            {(paper.categories as string[]).map((cat) => (
              <span
                key={cat}
                className="bg-gray-100 px-2 py-0.5 rounded text-sm text-gray-600"
              >
                {cat}
              </span>
            ))}
          </div>
        )}
      </header>

      <div className="flex gap-4 mb-6">
        {pdfUrl && (
          <a
            href={pdfUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-red-700 text-white rounded hover:bg-red-800"
          >
            Download PDF
          </a>
        )}
        <Link
          href={`/pdf/${paper.id}`}
          className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
        >
          View PDF
        </Link>
      </div>

      {paper.abstract && (
        <section>
          <h2 className="text-lg font-semibold mb-2">Abstract</h2>
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {paper.abstract}
          </p>
        </section>
      )}
    </article>
  );
}
