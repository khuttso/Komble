import { useState } from 'react';
import { seedPacks } from './data/seedPacks.js';
import { loadPersonalPacks, savePersonalPacks } from './lib/packStorage.js';
import { filterPacks } from './lib/packUtils.js';
import PackSearch from './components/PackSearch.jsx';
import PackCard from './components/PackCard.jsx';
import PackForm from './components/PackForm.jsx';
import PackPreview from './components/PackPreview.jsx';

export default function App() {
  const [saved, setSaved] = useState(loadPersonalPacks);
  const [query, setQuery] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [selectedPack, setSelectedPack] = useState(null);
  const [message, setMessage] = useState('');
  const packs = [...seedPacks, ...saved.packs];
  const visiblePacks = filterPacks(packs, query);

  function addPack(pack) {
    const nextPacks = [...saved.packs, pack];
    const error = savePersonalPacks(nextPacks);
    if (error) return error;
    // Only announce success and close the form after browser storage accepts the pack.
    setSaved({ packs: nextPacks, error: '' });
    setQuery('');
    setShowForm(false);
    setMessage(`“${pack.title}” was added to your library.`);
    return '';
  }

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="#" aria-label="InterviewCoach home">
          <span className="brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7"><path d="M5 5h14v10H10l-5 4z" /><path d="M9 9h6m-6 3h4" /></svg></span>
          Interview<span className="brand-light">Coach</span>
        </a>
        <span className="header-section">Pack hub</span>
        <span className="local-indicator"><span />Your local library</span>
      </header>
      <main id="main-content">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy"><p className="eyebrow">GOOD PREPARATION. GREAT POSSIBILITIES.</p>
            <h1 id="hero-title">Your next chapter<br />starts with <em>practice.</em></h1>
            <p className="hero-description">Find the questions for your next opportunity.<br className="desktop-break" /> Build a little confidence, one pack at a time.</p>
            <button className="button primary" onClick={() => setShowForm(true)} disabled={Boolean(saved.error)}><span aria-hidden="true">＋</span> Create a pack</button>
          </div>
          <div className="hero-note"><div className="note-heading"><span className="note-dot" /> A SMALL REMINDER</div>
            <p>You don’t need<br />all the answers.<br /><em>Just a place to start.</em></p>
            <span className="note-rule" /><span className="note-caption">Make room for your next opportunity.</span>
            <span className="note-spark" aria-hidden="true">✳</span>
          </div>
        </section>
        <section className="library" aria-labelledby="library-title">
          <div className="library-heading"><div><p className="eyebrow">YOUR PREPARATION LIBRARY</p><h2 id="library-title">Find your starting point.</h2></div>
            <p>Ready-made questions.<br />Room for your own.</p></div>
          {saved.error && <p className="notice error-notice" role="alert">{saved.error}</p>}
          <p className="save-message" role="status" aria-live="polite">{message}</p>
          <PackSearch query={query} onQueryChange={setQuery} resultCount={visiblePacks.length} totalCount={packs.length} />
          {visiblePacks.length ? <div className="pack-grid">{visiblePacks.map((pack, index) => <PackCard key={pack.id} pack={pack} index={index} onOpen={setSelectedPack} />)}</div>
            : <div className="empty-state"><span aria-hidden="true">↗</span><h3>No packs found.</h3><p>Try a different role, title, or tag. Your next starting point might be a pack of your own.</p><button className="button secondary" onClick={() => setQuery('')}>Clear search</button></div>}
          <div className="library-footnote"><span className="footnote-symbol" aria-hidden="true">◇</span><p>Your personal packs stay in this browser. No account needed.</p></div>
        </section>
      </main>
      <footer className="site-footer"><span>InterviewCoach <span aria-hidden="true">/</span> Pack Hub</span><span>A little more ready for what’s next.</span></footer>
      {showForm && <PackForm onSave={addPack} onClose={() => setShowForm(false)} />}
      {selectedPack && <PackPreview pack={selectedPack} onClose={() => setSelectedPack(null)} />}
    </div>
  );
}
