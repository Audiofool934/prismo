// Draw the original high-resolution artwork at the screen's actual pixel density.
// The pose matrices are measured from the pet atlas, in its 192 x 208 coordinates.
function createPrismoRenderer(canvas, sources, poses) {
  const context = canvas.getContext('2d');
  const images = {};
  let ready = false;
  let row = 0;
  let column = 0;
  let resolutionQuery;

  function draw() {
    if (!ready) return;
    const bounds = canvas.getBoundingClientRect();
    const density = Math.min(window.devicePixelRatio || 1, 4);
    const width = Math.max(1, Math.round(bounds.width * density));
    const height = Math.max(1, Math.round(bounds.height * density));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
    }
    context.setTransform(1, 0, 0, 1, 0, 0);
    context.clearRect(0, 0, width, height);
    context.imageSmoothingEnabled = true;
    context.imageSmoothingQuality = 'high';
    for (const part of poses[row][column]) {
      const image = images[part.image];
      context.setTransform(width / 192, 0, 0, height / 208, 0, 0);
      context.transform(...part.matrix);
      if (part.crop) {
        const [x, y, w, h] = part.crop;
        context.drawImage(image, x, y, w, h, 0, 0, w, h);
      } else {
        context.drawImage(image, 0, 0);
      }
    }
  }

  function watchResolution() {
    if (resolutionQuery) resolutionQuery.removeEventListener('change', watchResolution);
    resolutionQuery = matchMedia(`(resolution: ${window.devicePixelRatio || 1}dppx)`);
    resolutionQuery.addEventListener('change', watchResolution);
    draw();
  }

  const loaded = Promise.all(Object.entries(sources).map(async ([name, src]) => {
    const image = new Image();
    image.src = src;
    await image.decode();
    images[name] = image;
  })).then(() => {
    ready = true;
    canvas.dataset.ready = 'true';
    draw();
  });

  new ResizeObserver(draw).observe(canvas);
  window.addEventListener('resize', draw);
  watchResolution();

  return {
    ready: loaded,
    show(nextRow, nextColumn) {
      row = nextRow;
      column = nextColumn;
      canvas.dataset.row = String(row);
      canvas.dataset.frame = String(column);
      draw();
    }
  };
}
