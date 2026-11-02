import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
const manifest = JSON.parse(readFileSync('manifest.json', 'utf8'));
for (const skill of manifest.skills) {
  const content = readFileSync(skill.path + '/SKILL.md', 'utf8');
  assert.ok(content.startsWith('---\nname: ' + skill.name + '\n'));
  for (const reference of content.matchAll(/\]\((references\/[^)]+)\)/g)) assert.ok(existsSync(skill.path + '/' + reference[1]));
}
assert.equal(spawnSync('python3', ['-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], { stdio: 'inherit', env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' } }).status, 0);
