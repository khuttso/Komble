import { useEffect, useRef, useState } from 'react';
import { parsePackForm, parseQuestions } from '../lib/packUtils.js';

export default function PackForm({ onSave, onClose }) {
  const dialog = useRef(null);
  const titleInput = useRef(null);
  const roleInput = useRef(null);
  const questionsInput = useRef(null);
  const [values, setValues] = useState({ title: '', role: '', tags: '', questions: '' });
  const [errors, setErrors] = useState({});
  const [saveError, setSaveError] = useState('');
  const questionCount = parseQuestions(values.questions).length;

  useEffect(() => {
    const element = dialog.current;
    element.showModal();
    return () => element.close();
  }, []);

  function update(event) {
    const { name, value } = event.target;
    setValues((previous) => ({ ...previous, [name]: value }));
    setErrors((previous) => ({ ...previous, [name]: '' }));
    setSaveError('');
  }

  function submit(event) {
    event.preventDefault();
    const { pack, errors: nextErrors } = parsePackForm(values);
    setErrors(nextErrors);
    if (!pack) {
      // Move keyboard focus to the first field the user needs to correct.
      (nextErrors.title ? titleInput : nextErrors.role ? roleInput : questionsInput).current.focus();
      return;
    }
    const error = onSave({ id: `personal-${crypto.randomUUID()}`, ...pack });
    if (error) setSaveError(error);
  }

  return (
    <dialog ref={dialog} className="modal form-modal" aria-labelledby="create-title" onCancel={onClose}>
      <div className="modal-heading">
        <div><p className="eyebrow">MAKE IT PERSONAL</p><h2 id="create-title">A pack of your own.</h2></div>
        <button className="icon-button" type="button" onClick={onClose} aria-label="Close add-pack form">×</button>
      </div>
      <p className="modal-intro">Collect the questions you want to feel ready for.</p>
      <form onSubmit={submit} noValidate>
        <label htmlFor="pack-title">Pack title</label>
        <input ref={titleInput} autoFocus id="pack-title" name="title" placeholder="e.g. QA Intern Practice" maxLength={100}
          value={values.title} onChange={update} aria-required="true" aria-invalid={Boolean(errors.title)}
          aria-describedby={errors.title ? 'title-error' : undefined} />
        {errors.title && <p id="title-error" className="field-error" role="alert">{errors.title}</p>}
        <label htmlFor="pack-role">Target role</label>
        <input ref={roleInput} id="pack-role" name="role" placeholder="e.g. QA Intern" maxLength={80}
          value={values.role} onChange={update} aria-required="true" aria-invalid={Boolean(errors.role)}
          aria-describedby={errors.role ? 'role-error' : undefined} />
        {errors.role && <p id="role-error" className="field-error" role="alert">{errors.role}</p>}
        <label htmlFor="pack-tags">Tags <span className="optional">optional</span></label>
        <input id="pack-tags" name="tags" placeholder="e.g. testing, junior" maxLength={200}
          value={values.tags} onChange={update} aria-describedby="tags-hint" />
        <p id="tags-hint" className="field-hint">Separate tags with commas.</p>
        <label htmlFor="pack-questions">Questions</label>
        <textarea ref={questionsInput} id="pack-questions" name="questions" rows={5}
          placeholder={'How would you test a login form?\nWhat would you include in a bug report?'}
          value={values.questions} onChange={update} aria-required="true"
          aria-invalid={Boolean(errors.questions)} aria-describedby="questions-hint questions-error" />
        <div className="question-hint"><p id="questions-hint" className="field-hint">One question per line. Blank lines are ignored.</p>
          <span>{questionCount} {questionCount === 1 ? 'question' : 'questions'}</span></div>
        <p id="questions-error" className="field-error" role={errors.questions ? 'alert' : undefined}>{errors.questions}</p>
        {saveError && <p className="notice error-notice" role="alert">{saveError}</p>}
        <div className="form-footer"><button className="button secondary" type="button" onClick={onClose}>Cancel</button>
          <button className="button primary" type="submit">Save pack <span aria-hidden="true">↗</span></button></div>
      </form>
    </dialog>
  );
}
