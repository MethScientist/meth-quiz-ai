let token = localStorage.getItem('token');
const headers = () => ({
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + token
});

// Auth UI elements
const loginBtn = document.getElementById('login-btn');
const regBtn = document.getElementById('register-btn');
const logoutBtn = document.getElementById('logout-btn');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const contentDiv = document.getElementById('content');

function showAuth() {
  loginBtn.style.display = 'inline-block';
  regBtn.style.display = 'inline-block';
  logoutBtn.style.display = 'none';
  contentDiv.style.display = 'none';
}
function showApp() {
  loginBtn.style.display = 'none';
  regBtn.style.display = 'none';
  logoutBtn.style.display = 'inline-block';
  contentDiv.style.display = 'flex';
  fetchSubjects();
}

loginBtn.onclick = () => { loginForm.style.display='block'; registerForm.style.display='none'; };
regBtn.onclick   = () => { registerForm.style.display='block'; loginForm.style.display='none'; };
logoutBtn.onclick= () => { localStorage.removeItem('token'); token=null; showAuth(); };

registerForm.onsubmit = async e => {
  e.preventDefault();
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;
  const res = await fetch('/register', {
    method:'POST',
    headers:{'Content-Type':'application/x-www-form-urlencoded'},
    body:`username=${email}&password=${password}`
  });
  const data = await res.json();
  if (data.access_token) {
    token = data.access_token;
    localStorage.setItem('token', token);
    showApp();
  }
};

loginForm.onsubmit = async e => {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  const res = await fetch('/token', {
    method:'POST',
    headers:{'Content-Type':'application/x-www-form-urlencoded'},
    body:`username=${email}&password=${password}`
  });
  const data = await res.json();
  if (data.access_token) {
    token = data.access_token;
    localStorage.setItem('token', token);
    showApp();
  }
};

if (token) showApp();
else showAuth();

// Fetch and render subjects in the sidebar
async function fetchSubjects() {
  const res = await fetch('/subjects', { headers: headers() });
  const subjects = await res.json();
  const ul = document.getElementById('subject-list');
  ul.innerHTML = '';
  subjects.forEach(sub => {
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.textContent = sub;
    btn.dataset.tooltip = sub;
    btn.onclick = () => loadChapters(sub);
    li.appendChild(btn);
    ul.appendChild(li);
  });
}

// Placeholder: load video & lesson for a subject
async function loadChapters(subject) {
  document.getElementById('video-lesson').innerHTML =
    `<h2>${subject} Lesson 1</h2>
     <video controls src="/static/videos/sample.mp4"></video>
     <p>Lesson content here...</p>`;
}

// Tab switching
document.querySelectorAll('.tab').forEach(tab =>
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab, .tab-content').forEach(el =>
      el.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.tab).classList.add('active');
  })
);

// Generate Quiz
document.getElementById('generate-quiz').onclick = async () => {
  const text = document.getElementById('video-lesson').innerText;
  const subject = document.querySelector('#subject-list button.active')?.textContent || '';
  const res = await fetch('/generate_quiz', {
    method:'POST', headers: headers(),
    body: JSON.stringify({ text, subject })
  });
  const data = await res.json();
  document.getElementById('ai-quiz').textContent = data.quiz;
};

// Save User Notes
document.getElementById('save-notes').onclick = async () => {
  const content = document.getElementById('user-notes').value;
  const subject = document.querySelector('#subject-list button.active')?.textContent || '';
  const lesson = 'Lesson 1';
  await fetch('/notes', {
    method:'POST', headers: headers(),
    body: JSON.stringify({ subject, lesson, content })
  });
  alert('Notes saved!');
};
