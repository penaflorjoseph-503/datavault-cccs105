/* DataVault DBMS — main.js */

// Sidebar toggle (mobile)
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// Auto-dismiss alerts after 4s
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => {
    el.style.opacity = '0';
    el.style.transition = 'opacity .3s';
    setTimeout(() => el.remove(), 300);
  }, 4000);
});

// Delete confirm modal
function confirmDelete(formId) {
  if (confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
    document.getElementById(formId).submit();
  }
}

// Generic detail modal
const viewModal   = document.getElementById('viewModal');
const viewModalClose = document.querySelectorAll('.modal-close, .modal-backdrop-click');

function openViewModal(url) {
  fetch(url)
    .then(r => r.json())
    .then(data => {
      const body = document.getElementById('viewModalBody');
      if (!body) return;
      const ignore = ['password'];
      let html = '<div class="detail-grid">';
      for (const [k, v] of Object.entries(data)) {
        if (ignore.includes(k)) continue;
        const label = k.replace(/_/g, ' ');
        html += `
          <div class="detail-item">
            <div class="detail-label">${label}</div>
            <div class="detail-value">${v ?? '—'}</div>
          </div>`;
      }
      html += '</div>';
      body.innerHTML = html;
      if (viewModal) viewModal.classList.add('open');
    })
    .catch(() => alert('Could not load record details.'));
}

if (viewModal) {
  viewModal.addEventListener('click', (e) => {
    if (e.target === viewModal) viewModal.classList.remove('open');
  });
  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', () => viewModal.classList.remove('open'));
  });
}

// Animate stat bars on load
window.addEventListener('load', () => {
  document.querySelectorAll('.dept-bar-fill').forEach(bar => {
    const w = bar.dataset.width;
    bar.style.width = w + '%';
  });
});
