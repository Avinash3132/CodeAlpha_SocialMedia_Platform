// ============================================
// CONNECTHUB - Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function () {

  // ── Dark Mode ──
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateToggleIcon(savedTheme);

  // ── Auto dismiss alerts ──
  setTimeout(function () {
    document.querySelectorAll('.alert-dismissible').forEach(function (el) {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 500);
    });
  }, 4000);

  // ── Image Preview on Upload ──
  const imageInputs = document.querySelectorAll(
    'input[type="file"][accept*="image"]'
  );
  imageInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      const file = this.files[0];
      if (!file) return;
      const preview = document.getElementById(this.dataset.preview);
      if (preview) {
        const reader = new FileReader();
        reader.onload = function (e) {
          preview.src = e.target.result;
          preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  });

  // ── Character Counter ──
  const postTextarea = document.getElementById('post-content');
  const charCounter = document.getElementById('char-counter');
  if (postTextarea && charCounter) {
    postTextarea.addEventListener('input', function () {
      const remaining = 500 - this.value.length;
      charCounter.textContent = remaining;
      charCounter.style.color =
        remaining < 50 ? '#ef4444' :
        remaining < 100 ? '#f59e0b' : '#94a3b8';
    });
  }

  // ── Like Animation ──
  document.querySelectorAll('.like-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const icon = this.querySelector('i');
      if (icon) {
        icon.classList.add('like-animated');
        setTimeout(function () {
          icon.classList.remove('like-animated');
        }, 300);
      }
    });
  });

  // ── Confirm Delete ──
  document.querySelectorAll('.delete-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm('Are you sure you want to delete this?')) {
        e.preventDefault();
      }
    });
  });

});

// ── Toggle Dark Mode ──
function toggleDarkMode() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateToggleIcon(next);
}

function updateToggleIcon(theme) {
  const btn = document.getElementById('dark-toggle-btn');
  if (!btn) return;
  if (theme === 'dark') {
    btn.innerHTML = '<i class="bi bi-sun-fill"></i> Light';
  } else {
    btn.innerHTML = '<i class="bi bi-moon-fill"></i> Dark';
  }
}