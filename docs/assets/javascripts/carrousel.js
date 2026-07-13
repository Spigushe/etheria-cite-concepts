/*
  Carrousel de cartes, sans dépendance externe.
  Repose sur un défilement horizontal natif (scroll-snap) : les
  boutons ne font qu'appeler scrollBy, tout le reste (glisser au
  doigt, molette, clavier une fois la piste au focus) marche déjà
  nativement.

  document$ est l'observable RxJS exposé par Material pour MkDocs
  (voir bundle.js) : il notifie aussi bien au premier chargement
  qu'après une navigation instantanée (theme.features:
  navigation.instant), donc un seul point d'entrée suffit ici.

  Chaque vignette est servie en 150 DPI ; cliquer ou toucher une
  carte ouvre une vue plein écran qui charge la version @2x
  (300 DPI, générée par scripts/cards.py) seulement à ce moment-là,
  pour ne pas alourdir le défilement sur mobile.
*/
(function () {
  function setupCarrousel(el) {
    var track = el.querySelector(".carte-carrousel__piste");
    var prev = el.querySelector(".carte-carrousel__prec");
    var next = el.querySelector(".carte-carrousel__suivant");
    if (!track || !prev || !next || track.dataset.carrouselReady) return;
    track.dataset.carrouselReady = "1";

    function step() {
      var img = track.querySelector("img");
      return img ? img.getBoundingClientRect().width + 12 : track.clientWidth;
    }

    prev.addEventListener("click", function () {
      track.scrollBy({ left: -step(), behavior: "smooth" });
    });
    next.addEventListener("click", function () {
      track.scrollBy({ left: step(), behavior: "smooth" });
    });

    track.querySelectorAll("img").forEach(function (img, i) {
      img.tabIndex = 0;
      img.setAttribute("role", "button");
      img.addEventListener("click", function () {
        openLightbox(track, i);
      });
      img.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          openLightbox(track, i);
        }
      });
    });
  }

  // --- Lightbox : une seule instance, partagée par tous les carrousels ---

  var lightbox = null;
  var lbImage = null;
  var lbImages = [];
  var lbIndex = 0;
  var lastFocused = null;

  function zoomSrc(src) {
    return src.replace(/\.png(\?.*)?$/, "@2x.png$1");
  }

  function buildLightbox() {
    var el = document.createElement("div");
    el.className = "carte-lightbox";
    el.hidden = true;
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", "Carte en plein écran");
    el.innerHTML =
      '<button type="button" class="carte-lightbox__fermer" aria-label="Fermer">&times;</button>' +
      '<button type="button" class="carte-lightbox__prec" aria-label="Carte précédente">&lsaquo;</button>' +
      '<img class="carte-lightbox__image" alt="">' +
      '<button type="button" class="carte-lightbox__suivant" aria-label="Carte suivante">&rsaquo;</button>';
    document.body.appendChild(el);

    el.querySelector(".carte-lightbox__fermer").addEventListener(
      "click",
      closeLightbox
    );
    el.querySelector(".carte-lightbox__prec").addEventListener(
      "click",
      function () {
        showLightboxImage(lbIndex - 1);
      }
    );
    el.querySelector(".carte-lightbox__suivant").addEventListener(
      "click",
      function () {
        showLightboxImage(lbIndex + 1);
      }
    );
    // Un clic sur le fond (pas sur l'image ni les boutons) ferme.
    el.addEventListener("click", function (e) {
      if (e.target === el) closeLightbox();
    });

    lightbox = el;
    lbImage = el.querySelector(".carte-lightbox__image");
  }

  function showLightboxImage(i) {
    if (!lbImages.length) return;
    lbIndex = (i + lbImages.length) % lbImages.length;
    var img = lbImages[lbIndex];
    lbImage.src = zoomSrc(img.currentSrc || img.src);
    lbImage.alt = img.alt;
  }

  function openLightbox(track, index) {
    if (!lightbox) buildLightbox();
    lbImages = Array.from(track.querySelectorAll("img"));
    lastFocused = document.activeElement;
    showLightboxImage(index);
    lightbox.hidden = false;
    document.body.classList.add("carte-lightbox-ouverte");
    lightbox.querySelector(".carte-lightbox__fermer").focus();
  }

  function closeLightbox() {
    if (!lightbox || lightbox.hidden) return;
    lightbox.hidden = true;
    document.body.classList.remove("carte-lightbox-ouverte");
    lbImage.src = "";
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  document.addEventListener("keydown", function (e) {
    if (!lightbox || lightbox.hidden) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowRight") showLightboxImage(lbIndex + 1);
    if (e.key === "ArrowLeft") showLightboxImage(lbIndex - 1);
  });

  document$.subscribe(function () {
    document.querySelectorAll(".carte-carrousel").forEach(setupCarrousel);
  });
})();
