const STORAGE_KEY = 'interviewcoach.personal-packs.v1';

function isPersonalPack(pack) {
  // Saved browser data can be edited externally, so validate it before rendering.
  return pack && typeof pack.id === 'string' && pack.id.startsWith('personal-')
    && typeof pack.title === 'string' && pack.title.trim().length > 0
    && typeof pack.role === 'string' && pack.role.trim().length > 0
    && Array.isArray(pack.tags) && pack.tags.every((tag) => typeof tag === 'string')
    && Array.isArray(pack.questions) && pack.questions.length > 0
    && pack.questions.every((question) => typeof question === 'string' && question.trim().length > 0);
}

export function loadPersonalPacks() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    const packs = raw === null ? [] : JSON.parse(raw);
    if (!Array.isArray(packs) || !packs.every(isPersonalPack)
      || new Set(packs.map((pack) => pack.id)).size !== packs.length) {
      throw new Error('Invalid saved packs');
    }
    return {
      // Discard unexpected stored fields instead of passing them on to the UI.
      packs: packs.map(({ id, title, role, tags, questions }) => ({ id, title, role, tags, questions })),
      error: '',
    };
  } catch {
    // Never erase unreadable data: it may still be recoverable by its owner.
    return {
      packs: [],
      error: 'Your saved packs could not be read. Existing data has been left unchanged. You can still browse the starter packs; adding packs is unavailable until browser storage is accessible and valid.',
    };
  }
}

export function savePersonalPacks(packs) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(packs));
    return '';
  } catch {
    return 'This pack could not be saved in your browser. Check that local storage is enabled and has space, then try again. Your form is still here.';
  }
}
