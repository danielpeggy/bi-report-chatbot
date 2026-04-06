/* GenBI Chat Interface - Safe DOM manipulation (no innerHTML with user content) */
const CHAT_API = 'http://localhost:5001/api/chat';

function toggleChat() {
  const body = document.getElementById('chatBody');
  const toggle = document.getElementById('chatToggle');
  body.classList.toggle('open');
  toggle.classList.toggle('open');
  if (body.classList.contains('open')) {
    document.getElementById('chatInput').focus();
  }
}

function createEl(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text) el.textContent = text;
  return el;
}

function addUserMessage(text) {
  const msgs = document.getElementById('chatMessages');
  const div = createEl('div', 'chat-msg user', text);
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function addBotMessage(content) {
  const msgs = document.getElementById('chatMessages');
  const div = createEl('div', 'chat-msg bot');

  if (typeof content === 'string') {
    div.textContent = content;
  } else {
    div.appendChild(content);
  }

  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  return div;
}

function formatNum(val) {
  if (val === null || val === undefined) return 'NULL';
  if (typeof val === 'number') {
    return val >= 1000 ? val.toLocaleString('en-US', {maximumFractionDigits: 2}) : String(Number(val.toFixed(2)));
  }
  return String(val);
}

function buildResultTable(columns, rows) {
  const table = document.createElement('table');
  const thead = document.createElement('tr');
  columns.forEach(col => {
    const th = document.createElement('th');
    th.textContent = col;
    thead.appendChild(th);
  });
  table.appendChild(thead);

  rows.slice(0, 15).forEach(row => {
    const tr = document.createElement('tr');
    columns.forEach(col => {
      const td = document.createElement('td');
      td.textContent = formatNum(row[col]);
      tr.appendChild(td);
    });
    table.appendChild(tr);
  });

  return table;
}

function buildBotResponse(data) {
  const frag = document.createDocumentFragment();

  const header = createEl('b', null, 'GenBI Assistant');
  frag.appendChild(header);
  frag.appendChild(document.createElement('br'));

  // Results count
  const count = createEl('span', null, '\u{1F4CA} ' + data.row_count + ' results');
  frag.appendChild(count);
  frag.appendChild(document.createElement('br'));

  // Results table
  if (data.rows && data.rows.length > 0) {
    frag.appendChild(buildResultTable(data.columns, data.rows));
    if (data.rows.length > 15) {
      const more = createEl('em', null, '... ' + (data.rows.length - 15) + ' more rows');
      more.style.fontSize = '11px';
      more.style.color = '#888';
      frag.appendChild(more);
    }
  }

  frag.appendChild(document.createElement('br'));

  // Explanation
  if (data.explanation) {
    const expl = createEl('span', null, '\u{1F4DD} ' + data.explanation);
    frag.appendChild(expl);
  }

  // Data lineage
  if (data.lineage) {
    const lineage = createEl('div', 'lineage');
    const lineageTitle = createEl('b', null, '\u{1F50D} Data Lineage:');
    lineage.appendChild(lineageTitle);
    lineage.appendChild(document.createElement('br'));
    data.lineage.split('\n').forEach(function(line, idx, arr) {
      if (line.trim()) {
        lineage.appendChild(document.createTextNode(line));
      }
      if (idx < arr.length - 1) {
        lineage.appendChild(document.createElement('br'));
      }
    });
    lineage.style.whiteSpace = 'pre-wrap';
    frag.appendChild(lineage);
  }

  // SQL toggle
  if (data.sql) {
    const toggle = createEl('span', null, 'Show SQL');
    toggle.style.cssText = 'color:#FFC72C;cursor:pointer;font-size:11px;text-decoration:underline;margin-top:4px;display:inline-block';
    const pre = createEl('pre', null, data.sql);
    pre.style.display = 'none';
    toggle.addEventListener('click', function() {
      pre.style.display = pre.style.display === 'none' ? 'block' : 'none';
    });
    frag.appendChild(toggle);
    frag.appendChild(pre);
  }

  return frag;
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const question = input.value.trim();
  if (!question) return;

  input.value = '';
  addUserMessage(question);

  const btn = document.querySelector('.chat-input-row button');
  btn.disabled = true;

  const thinking = addBotMessage('Thinking & querying Redshift...');

  try {
    const res = await fetch(CHAT_API, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: question})
    });
    const data = await res.json();
    thinking.remove();

    if (data.error) {
      addBotMessage('Error: ' + data.error);
      return;
    }

    const responseContent = buildBotResponse(data);
    addBotMessage(responseContent);
  } catch (e) {
    thinking.remove();
    addBotMessage('Connection error. Is the API server running? Start with: python3 genbi/api.py');
  } finally {
    btn.disabled = false;
  }
}

// Auto-open chat panel after 1 second
setTimeout(function() { toggleChat(); }, 1000);
