// Rebuild Canvas-safe fragments from their separate teaching Markdown sources.
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const pairs = [
  ['modules/01-walker-and-godot/lesson.md', 'canvas/01-module-1-walker-and-godot.html'],
  ['assignments/01-extend-walker-jumpman.md', 'canvas/02-assignment-1-extend-walker-jumpman.html'],
  ['assignments/02-generate-walker-art-sound-music.md', 'canvas/03-assignment-2-generate-walker-art-sound-music.html'],
];
for (const [source, target] of pairs) {
  let html = execFileSync('pandoc', [path.join(root, source), '--from=gfm', '--to=html5', '--wrap=none', '--shift-heading-level-by=1'], {encoding: 'utf8'});
  html = html.replace(/<table>/g, '<table style="border-collapse: collapse; width: 100%; margin: 1em 0;">')
    .replace(/<th\b([^>]*)>/g, (_, attrs) => '<th' + attrs.replace(/ style="[^"]*"/g, '') + ' style="border: 1px solid #999; padding: 0.6em; text-align: left; vertical-align: top;" scope="col">')
    .replace(/<td\b([^>]*)>/g, (_, attrs) => '<td' + attrs.replace(/ style="[^"]*"/g, '') + ' style="border: 1px solid #999; padding: 0.6em; text-align: left; vertical-align: top;">')
    .replace(/<pre\b([^>]*)>/g, '<pre$1 style="white-space: pre-wrap; overflow-wrap: anywhere; background-color: #f4f4f4; padding: 1em;">')
    .replace(/(<th\b[^>]*style=")([^"]*)("[^>]*>Points<\/th>)/g, '$1$2 width: 15%; min-width: 4em;$3');
  const fragment = '<div style="line-height: 1.6; overflow-wrap: anywhere;">\n' + html + '</div>\n';
  if (/href="(?!https:\/\/)/.test(fragment)) throw new Error('Non-HTTPS link in ' + target);
  if (/<(?:script|iframe|img)\b/.test(fragment)) throw new Error('Unexpected external asset in ' + target);
  fs.mkdirSync(path.dirname(path.join(root, target)), {recursive: true});
  fs.writeFileSync(path.join(root, target), fragment);
  console.log('Built ' + target);
}
