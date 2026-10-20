import { useEffect, useRef } from 'react';

export default function PackPreview({ pack, onClose }) {
  const dialog = useRef(null);
  useEffect(() => {
    const element = dialog.current;
    element.showModal();
    return () => element.close();
  }, []);

  return (
    <dialog ref={dialog} className="modal preview-modal" aria-labelledby="preview-title" onCancel={onClose}>
      <div className="modal-heading">
        <p className="eyebrow">PACK PREVIEW</p>
        <button className="icon-button" onClick={onClose} aria-label="Close pack preview">×</button>
      </div>
      <p className="preview-role">{pack.role}</p>
      <h2 id="preview-title">{pack.title}</h2>
      <div className="preview-meta"><span>{pack.questions.length} {pack.questions.length === 1 ? 'question' : 'questions'}</span>
        <span aria-hidden="true">·</span><span>{pack.id.startsWith('seed-') ? 'Starter pack' : 'Your personal pack'}</span></div>
      {pack.tags.length > 0 && <div className="tag-list preview-tags">{pack.tags.map((tag, i) => <span className="tag" key={`${tag}-${i}`}>{tag}</span>)}</div>}
      <h3 className="question-list-title">Inside this pack</h3>
      <ol className="question-list">{pack.questions.map((question, index) => <li key={index}><span>{question}</span></li>)}</ol>
      <div className="preview-footer"><span>One question is a good place to start.</span>
        <button className="button secondary" onClick={onClose}>Back to hub</button></div>
    </dialog>
  );
}
