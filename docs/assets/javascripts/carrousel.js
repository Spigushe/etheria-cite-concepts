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

  La même vue plein écran sert à toute image du contenu portant la
  classe `zoomable` (attr_list : `![alt](img.png){ .zoomable }`).
  L'image agrandie est celle de `data-zoom-src` si présent, sinon la
  source elle-même. Les images `.zoomable` d'un même paragraphe
  forment un groupe parcourable avec les flèches (ex. recto/verso).
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
      makeActivable(img, function () {
        openLightbox(Array.from(track.querySelectorAll("img")), i, zoomSrc);
      });
    });
  }

  function makeActivable(img, open) {
    img.tabIndex = 0;
    img.setAttribute("role", "button");
    img.addEventListener("click", open);
    img.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        open();
      }
    });
  }

  // --- Images isolées : classe .zoomable ---

  function zoomableSrc(img) {
    return img.dataset.zoomSrc || img.currentSrc || img.src;
  }

  function setupZoomable(img) {
    if (img.dataset.zoomReady) return;
    img.dataset.zoomReady = "1";
    makeActivable(img, function () {
      var group = Array.from(
        (img.parentElement || document).querySelectorAll("img.zoomable")
      );
      openLightbox(group, group.indexOf(img), zoomableSrc);
    });
  }

  // --- Lightbox : une seule instance, partagée par tous les carrousels ---

  var lightbox = null;
  var lbImage = null;
  var lbImages = [];
  var lbIndex = 0;
  var lbSrcFor = null;
  var lastFocused = null;

  function zoomSrc(img) {
    return (img.currentSrc || img.src).replace(/\.png(\?.*)?$/, "@2x.png$1");
  }

  function buildLightbox() {
    var el = document.createElement("div");
    el.className = "carte-lightbox";
    el.hidden = true;
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", "Image en plein écran");
    el.innerHTML =
      '<button type="button" class="carte-lightbox__fermer" aria-label="Fermer">&times;</button>' +
      '<button type="button" class="carte-lightbox__prec" aria-label="Image précédente">&lsaquo;</button>' +
      '<img class="carte-lightbox__image" alt="">' +
      '<button type="button" class="carte-lightbox__suivant" aria-label="Image suivante">&rsaquo;</button>';
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
    lbImage.src = lbSrcFor(img);
    lbImage.alt = img.alt;
  }

  function openLightbox(images, index, srcFor) {
    if (!lightbox) buildLightbox();
    lbImages = images;
    lbSrcFor = srcFor;
    // Une seule image : pas de navigation à proposer.
    var seule = images.length < 2;
    lightbox.querySelector(".carte-lightbox__prec").hidden = seule;
    lightbox.querySelector(".carte-lightbox__suivant").hidden = seule;
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
    document.querySelectorAll("img.zoomable").forEach(setupZoomable);
  });
})();
