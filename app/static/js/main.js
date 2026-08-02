// ---- Dark mode toggle ----
(function () {
  const root = document.documentElement;
  const stored = localStorage.getItem('devboard-theme');
  if (stored) {
    root.setAttribute('data-theme', stored);
  }

  document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
      updateToggleIcon();
      toggleBtn.addEventListener('click', () => {
        const current = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', current);
        localStorage.setItem('devboard-theme', current);
        updateToggleIcon();
      });
    }

    // ---- Mobile sidebar toggle ----
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle && sidebar) {
      sidebarToggle.addEventListener('click', () => sidebar.classList.add('show'));
    }
    if (sidebarClose && sidebar) {
      sidebarClose.addEventListener('click', () => sidebar.classList.remove('show'));
    }
    // Close sidebar when clicking outside of it on mobile
    document.addEventListener('click', (e) => {
      if (!sidebar) return;
      const isOpen = sidebar.classList.contains('show');
      const clickedInside = sidebar.contains(e.target) || (sidebarToggle && sidebarToggle.contains(e.target));
      if (isOpen && !clickedInside) {
        sidebar.classList.remove('show');
      }
    });

    // ---- Auto-dismiss alerts ----
    document.querySelectorAll('.alert').forEach((alert) => {
      setTimeout(() => {
        alert.classList.remove('show');
        alert.classList.add('fade');
      }, 4000);
    });
  });

  function updateToggleIcon() {
    const toggleBtn = document.getElementById('themeToggle');
    if (!toggleBtn) return;
    const isDark = root.getAttribute('data-theme') === 'dark';
    toggleBtn.innerHTML = isDark
      ? '<i class="bi bi-sun"></i>'
      : '<i class="bi bi-moon-stars"></i>';
  }
})();

// ---- Delete confirmation ----
function confirmDelete(formId, itemName) {
  if (confirm(`Are you sure you want to delete "${itemName}"? This cannot be undone.`)) {
    document.getElementById(formId).submit();
  }
}
