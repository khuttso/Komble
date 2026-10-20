// Keep search and form rules independent of React so offline tests use the app's rules.
export function filterPacks(packs, query) {
  const term = query.trim().toLocaleLowerCase();
  return packs.filter((pack) => [pack.title, pack.role, ...pack.tags]
    .some((field) => field.toLocaleLowerCase().includes(term)));
}

export function parseQuestions(text) {
  // Both Windows and Unix line endings are accepted; blank lines are not questions.
  return text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
}

export function parsePackForm(values) {
  const title = values.title.trim();
  const role = values.role.trim();
  const questions = parseQuestions(values.questions);
  const errors = {
    title: title ? '' : 'Enter a pack title.',
    role: role ? '' : 'Enter a target role.',
    questions: questions.length ? '' : 'Add at least one question.',
  };

  // Invalid input never produces a pack that a caller could accidentally save.
  if (Object.values(errors).some(Boolean)) return { pack: null, errors };

  const tags = [...new Set(values.tags.split(',').map((tag) => tag.trim()).filter(Boolean))];
  return { pack: { title, role, tags, questions }, errors };
}
