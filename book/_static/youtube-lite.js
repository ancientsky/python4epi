/* Lite YouTube Embed — click thumbnail to load iframe and autoplay */
document.addEventListener("click", function (e) {
  var el = e.target.closest(".youtube-lite");
  if (!el || el.classList.contains("yt-activated")) return;

  var id = el.getAttribute("data-id");
  if (!id) return;

  el.classList.add("yt-activated");
  var iframe = document.createElement("iframe");
  iframe.src =
    "https://www.youtube.com/embed/" +
    id +
    "?autoplay=1&rel=0&modestbranding=1";
  iframe.allow = "autoplay; encrypted-media";
  iframe.allowFullscreen = true;
  el.appendChild(iframe);
});
