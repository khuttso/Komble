export default function PackCard({ pack, index, onOpen }) {
  return (
    <button className={`pack-card tone-${index % 3}`} onClick={() => onOpen(pack)}
      aria-label={`Preview ${pack.title}`}>
      <span className="card-topline">
        <span className="pack-symbol" aria-hidden="true">
          <svg viewBox="0 0 28 28" fill="none" stroke="currentColor" strokeWidth="1.5">
            <rect x="6" y="7" width="15" height="17" rx="2" />
            <path d="M10 7V4h15v16h-4M10 12h7m-7 4h7m-7 4h4" />
          </svg>
        </span>
        <span className="pack-origin">{pack.id.startsWith('seed-') ? 'Starter pack' : 'Your pack'}</span>
      </span>
      <span className="card-role">{pack.role}</span>
      <span className="card-title">{pack.title}</span>
      <span className="card-description">{pack.description || 'Your questions, your next opportunity. Make this pack your own starting point.'}</span>
      <span className="tag-list">{pack.tags.map((tag, i) => <span className="tag" key={`${tag}-${i}`}>{tag}</span>)}</span>
      <span className="card-bottomline">
        <span>{pack.questions.length} {pack.questions.length === 1 ? 'question' : 'questions'}</span>
        <span className="card-preview">Preview pack <span aria-hidden="true">↗</span></span>
      </span>
    </button>
  );
}
