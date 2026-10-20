export default function PackSearch({ query, onQueryChange, resultCount, totalCount }) {
  return (
    <div className="search-toolbar">
      <div className="search-field">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
          <circle cx="10.5" cy="10.5" r="6.5" /><path d="m16 16 4 4" />
        </svg>
        <label className="sr-only" htmlFor="pack-search">Search interview packs</label>
        <input id="pack-search" type="search" placeholder="Search by title, role, or tag…"
          value={query} onChange={(event) => onQueryChange(event.target.value)} />
      </div>
      <span className="result-count" role="status" aria-live="polite">
        {query.trim() ? `${resultCount} of ${totalCount} packs` : `${totalCount} packs to explore`}
      </span>
    </div>
  );
}
