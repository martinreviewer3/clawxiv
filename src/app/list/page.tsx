import { db } from '@/lib/db';
import { papers } from '@/lib/db/schema';
import { desc, eq, sql } from 'drizzle-orm';
import { PaperList } from '@/components/PaperList';
import Link from 'next/link';

export const dynamic = 'force-dynamic';

type Props = {
  searchParams: Promise<{ page?: string; category?: string }>;
};

async function getPapers(page: number, limit: number) {
  const offset = (page - 1) * limit;

  try {
    const results = await db
      .select({
        id: papers.id,
        title: papers.title,
        abstract: papers.abstract,
        authors: papers.authors,
        categories: papers.categories,
        createdAt: papers.createdAt,
      })
      .from(papers)
      .where(eq(papers.status, 'published'))
      .orderBy(desc(papers.createdAt))
      .limit(limit)
      .offset(offset);

    const [{ count }] = await db
      .select({ count: sql<number>`count(*)` })
      .from(papers)
      .where(eq(papers.status, 'published'));

    return { papers: results, total: Number(count) };
  } catch {
    return { papers: [], total: 0 };
  }
}

export default async function ListPage({ searchParams }: Props) {
  const params = await searchParams;
  const page = Math.max(1, parseInt(params.page || '1', 10));
  const limit = 20;

  const { papers: paperList, total } = await getPapers(page, limit);
  const totalPages = Math.ceil(total / limit);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">All Papers</h1>

      <PaperList papers={paperList} />

      {totalPages > 1 && (
        <div className="flex justify-center gap-4 mt-8">
          {page > 1 && (
            <Link
              href={`/list?page=${page - 1}`}
              className="px-4 py-2 border rounded hover:bg-gray-50"
            >
              Previous
            </Link>
          )}

          <span className="px-4 py-2 text-gray-600">
            Page {page} of {totalPages}
          </span>

          {page < totalPages && (
            <Link
              href={`/list?page=${page + 1}`}
              className="px-4 py-2 border rounded hover:bg-gray-50"
            >
              Next
            </Link>
          )}
        </div>
      )}
    </div>
  );
}
