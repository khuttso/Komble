import assert from 'node:assert/strict';
import { afterEach, beforeEach, describe, test } from 'node:test';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { seedPacks } from '../data/seedPacks.js';
import { filterPacks, parsePackForm } from '../lib/packUtils.js';
import { loadPersonalPacks, savePersonalPacks } from '../lib/packStorage.js';

const storageKey = 'interviewcoach.personal-packs.v1';
const qaQuestions = [
  'How would you test a login form?',
  'What would you include in a bug report?',
];
const validForm = {
  title: 'QA Intern Practice',
  role: 'QA Intern',
  tags: 'testing, junior',
  questions: qaQuestions.join('\n'),
};
const projectRoot = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));

async function applicationFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.name === 'tests') continue;
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await applicationFiles(entryPath));
    else if (/\.(?:js|jsx)$/.test(entry.name)) files.push(entryPath);
  }
  return files;
}

test('the starter library has at least three complete packs with unique IDs', () => {
  assert.ok(seedPacks.length >= 3);
  assert.equal(new Set(seedPacks.map((pack) => pack.id)).size, seedPacks.length);
  for (const pack of seedPacks) {
    assert.ok(pack.title.trim());
    assert.ok(pack.role.trim());
    assert.ok(Array.isArray(pack.tags));
    assert.ok(pack.questions.length > 0);
    assert.ok(pack.questions.every((question) => typeof question === 'string' && question.trim()));
  }
});

test('search finds the golden frontend pack regardless of case and surrounding spaces', () => {
  assert.deepEqual(filterPacks(seedPacks, '  FRONTEND  ').map((pack) => pack.title), [
    'Junior Frontend Developer',
  ]);
});

test('search independently matches a title, a role, and a tag', () => {
  const packs = [{ id: 'personal-search', title: 'Technical Round', role: 'Quality Engineer', tags: ['regression'] }];
  for (const term of ['technical', 'quality', 'regression']) {
    assert.deepEqual(filterPacks(packs, term), packs);
  }
  assert.deepEqual(filterPacks(packs, 'unrelated'), []);
});

test('search leaves the original library unchanged and an empty query shows all packs', () => {
  const original = structuredClone(seedPacks);
  filterPacks(seedPacks, 'frontend');
  assert.deepEqual(filterPacks(seedPacks, '   '), original);
  assert.deepEqual(seedPacks, original);
});

test('the Pack Hub has no external request or remote-asset code', async () => {
  const sourceFiles = await applicationFiles(path.join(projectRoot, 'src'));
  const source = await Promise.all(sourceFiles.map((file) => readFile(file, 'utf8')));
  const indexHtml = await readFile(path.join(projectRoot, 'index.html'), 'utf8');

  // The local-only feature must not quietly acquire an API, model, or remote asset.
  for (const text of source) {
    assert.doesNotMatch(text, /\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\b/);
    assert.doesNotMatch(text, /\b(?:axios|openrouter|openai)\b/i);
    assert.doesNotMatch(text, /https?:\/\//i);
  }
  assert.doesNotMatch(indexHtml, /(?:src|href)=["']https?:\/\//i);
});

test('a valid form trims text, removes blank lines, and deduplicates optional tags', () => {
  const { pack, errors } = parsePackForm({
    ...validForm,
    title: '  QA Intern Practice  ',
    role: ' QA Intern ',
    tags: ' testing, junior, testing, , ',
    questions: `  ${qaQuestions[0]} \r\n\r\n ${qaQuestions[1]} \r\n`,
  });
  assert.deepEqual(pack, {
    title: 'QA Intern Practice', role: 'QA Intern', tags: ['testing', 'junior'], questions: qaQuestions,
  });
  assert.ok(Object.values(errors).every((error) => error === ''));
  assert.deepEqual(parsePackForm({ ...validForm, tags: '' }).pack.tags, []);
});

for (const field of ['title', 'role', 'questions']) {
  test(`a whitespace-only ${field} is rejected before a pack can be saved`, () => {
    const { pack, errors } = parsePackForm({ ...validForm, [field]: ' \r\n ' });
    assert.equal(pack, null);
    assert.ok(errors[field]);
  });
}

describe('personal pack storage', () => {
  let values;
  let writes;
  let originalWindow;

  beforeEach(() => {
    values = new Map();
    writes = 0;
    originalWindow = Object.getOwnPropertyDescriptor(globalThis, 'window');
    // Only the browser boundary is replaced; all production storage code runs unchanged.
    globalThis.window = {
      localStorage: {
        getItem: (key) => values.get(key) ?? null,
        setItem: (key, value) => { writes += 1; values.set(key, value); },
      },
    };
  });

  afterEach(() => {
    if (originalWindow) Object.defineProperty(globalThis, 'window', originalWindow);
    else delete globalThis.window;
  });

  test('a first visit starts with no personal packs and makes no storage writes', () => {
    assert.deepEqual(loadPersonalPacks(), { packs: [], error: '' });
    assert.equal(writes, 0);
  });

  test('the golden QA pack survives a fresh read with its exact metadata and questions', () => {
    const { pack } = parsePackForm(validForm);
    const personalPack = { id: 'personal-qa-test', ...pack };
    assert.equal(savePersonalPacks([personalPack]), '');
    assert.equal(writes, 1);
    assert.deepEqual(loadPersonalPacks(), { packs: [personalPack], error: '' });
    assert.deepEqual(JSON.parse(values.get(storageKey)), [personalPack]);
  });

  test('malformed JSON, invalid records, and duplicate IDs are rejected without overwriting data', () => {
    const personalPack = { id: 'personal-qa-test', ...parsePackForm(validForm).pack };
    for (const raw of [
      '{broken JSON',
      JSON.stringify({ packs: [] }),
      JSON.stringify([{ ...personalPack, questions: [] }]),
      JSON.stringify([{ ...personalPack, id: 'seed-frontend' }]),
      JSON.stringify([personalPack, personalPack]),
    ]) {
      values.set(storageKey, raw);
      const result = loadPersonalPacks();
      assert.deepEqual(result.packs, []);
      assert.match(result.error, /left unchanged/);
      assert.equal(values.get(storageKey), raw);
    }
    assert.equal(writes, 0);
  });

  test('unknown stored fields are discarded while question text stays plain text', () => {
    const personalPack = { id: 'personal-qa-test', ...parsePackForm(validForm).pack };
    personalPack.questions = ['<script>This is question text, not executable code.</script>'];
    values.set(storageKey, JSON.stringify([{ ...personalPack, unexpected: 'discard me' }]));
    assert.deepEqual(loadPersonalPacks(), { packs: [personalPack], error: '' });
  });

  test('blocked reads and quota-exceeded writes return readable errors', () => {
    window.localStorage.getItem = () => { throw new Error('Storage blocked'); };
    window.localStorage.setItem = () => { throw new Error('Quota exceeded'); };
    assert.match(loadPersonalPacks().error, /could not be read/);
    assert.match(savePersonalPacks([]), /Your form is still here/);
  });
});
