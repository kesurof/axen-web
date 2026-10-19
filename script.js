(() => {
  'use strict';
  const toggle = document.querySelector('.nav-toggle');
  const links = document.getElementById('primary-links');
  if (toggle && links) {
    const close = () => { links.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Ouvrir le menu'); };
    toggle.addEventListener('click', () => {
      const next = toggle.getAttribute('aria-expanded') !== 'true';
      links.classList.toggle('is-open', next);
      toggle.setAttribute('aria-expanded', String(next));
      toggle.setAttribute('aria-label', next ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') { close(); toggle.focus(); } });
    document.addEventListener('click', e => { if (!links.contains(e.target) && !toggle.contains(e.target)) close(); });
  }
  const header = document.querySelector('.site-header');
  let ticking = false;
  function applyScroll() { header?.classList.toggle('has-scrolled', window.scrollY > 12); ticking = false; }
  addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(applyScroll); ticking = true; } }, {passive:true});
  applyScroll();
  document.querySelectorAll('#year').forEach(el => { el.textContent = String(new Date().getFullYear()); });
  const form = document.getElementById('contact-form');
  const feedback = document.getElementById('form-feedback');
  form?.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const email = typeof window.AXEN_SITE_CONFIG?.contactEmail === 'string' ? window.AXEN_SITE_CONFIG.contactEmail.trim() : '';
    const subject = `Demande AXEN — ${data.get('subject')}`;
    const body = `Bonjour,\n\nJe souhaite échanger avec AXEN au sujet de mon projet.\n\nNom : ${data.get('name')}\nEmail : ${data.get('email')}\nEntreprise : ${data.get('company') || 'Non renseignée'}\nObjet : ${data.get('subject')}\n\n${data.get('message')}\n\nCordialement.`;
    if (email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      feedback.textContent = 'Votre messagerie va s’ouvrir avec la demande préparée. Pensez à envoyer le message pour nous contacter.';
      window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      return;
    }
    const text = `${subject}\n\n${body}`;
    try {
      await navigator.clipboard.writeText(text);
      feedback.textContent = 'Votre demande a été copiée. Les coordonnées de contact AXEN seront ajoutées prochainement au site ; aucun message n’a été envoyé.';
    } catch {
      feedback.textContent = 'Les coordonnées de contact ne sont pas encore configurées. Aucun message n’a été envoyé. Merci de réessayer ultérieurement.';
    }
  });
})();
