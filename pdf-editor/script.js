let pdfDoc = null;
let currentPage = 1;
let scale = 1.5;
let highlightMode = false;
let highlights = {}; // page -> array of rects
let mergedPdfBytes = null;

const fileInput = document.getElementById('file-input');
const mergeInput = document.getElementById('merge-input');
const mergeBtn = document.getElementById('merge-btn');
const prevPageBtn = document.getElementById('prev-page');
const nextPageBtn = document.getElementById('next-page');
const downloadPageBtn = document.getElementById('download-page');
const downloadPdfBtn = document.getElementById('download-pdf');
const highlightToggle = document.getElementById('highlight-toggle');
const pdfCanvas = document.getElementById('pdf-canvas');
const highlightCanvas = document.getElementById('highlight-canvas');
const ctx = pdfCanvas.getContext('2d');
const hCtx = highlightCanvas.getContext('2d');

fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function() {
      loadPdf(new Uint8Array(this.result));
    };
    reader.readAsArrayBuffer(file);
  }
});

mergeBtn.addEventListener('click', async () => {
  const files = mergeInput.files;
  if (!files.length) return;
  const merged = await PDFLib.PDFDocument.create();
  for (let i = 0; i < files.length; i++) {
    const bytes = new Uint8Array(await files[i].arrayBuffer());
    const pdf = await PDFLib.PDFDocument.load(bytes);
    const copiedPages = await merged.copyPages(pdf, pdf.getPageIndices());
    copiedPages.forEach((p) => merged.addPage(p));
  }
  mergedPdfBytes = await merged.save();
  loadPdf(mergedPdfBytes);
});

prevPageBtn.addEventListener('click', () => {
  if (currentPage <= 1) return;
  currentPage--;
  renderPage();
});

nextPageBtn.addEventListener('click', () => {
  if (currentPage >= pdfDoc.numPages) return;
  currentPage++;
  renderPage();
});

downloadPageBtn.addEventListener('click', () => {
  const link = document.createElement('a');
  link.download = `page-${currentPage}.png`;
  link.href = pdfCanvas.toDataURL('image/png');
  link.click();
});

downloadPdfBtn.addEventListener('click', () => {
  if (!mergedPdfBytes) return;
  const blob = new Blob([mergedPdfBytes], { type: 'application/pdf' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'merged.pdf';
  link.click();
});

highlightToggle.addEventListener('click', () => {
  highlightMode = !highlightMode;
  highlightCanvas.style.pointerEvents = highlightMode ? 'auto' : 'none';
});

highlightCanvas.addEventListener('mousedown', startHighlight);

async function loadPdf(data) {
  const loadingTask = pdfjsLib.getDocument({ data });
  pdfDoc = await loadingTask.promise;
  currentPage = 1;
  highlights = {};
  mergedPdfBytes = data;
  renderPage();
}

async function renderPage() {
  const page = await pdfDoc.getPage(currentPage);
  const viewport = page.getViewport({ scale });
  pdfCanvas.width = viewport.width;
  pdfCanvas.height = viewport.height;
  highlightCanvas.width = viewport.width;
  highlightCanvas.height = viewport.height;

  const renderContext = {
    canvasContext: ctx,
    viewport: viewport
  };
  await page.render(renderContext).promise;

  redrawHighlights();
}

function startHighlight(e) {
  if (!highlightMode) return;
  const rect = { startX: e.offsetX, startY: e.offsetY, endX: e.offsetX, endY: e.offsetY };
  const move = (ev) => {
    rect.endX = ev.offsetX;
    rect.endY = ev.offsetY;
    redrawHighlights(rect);
  };
  const up = () => {
    highlightCanvas.removeEventListener('mousemove', move);
    highlightCanvas.removeEventListener('mouseup', up);
    storeHighlight(rect);
    redrawHighlights();
  };
  highlightCanvas.addEventListener('mousemove', move);
  highlightCanvas.addEventListener('mouseup', up);
}

function storeHighlight(rect) {
  if (!highlights[currentPage]) highlights[currentPage] = [];
  highlights[currentPage].push(rect);
}

function redrawHighlights(tempRect) {
  hCtx.clearRect(0, 0, highlightCanvas.width, highlightCanvas.height);
  const rects = highlights[currentPage] || [];
  rects.forEach(drawRect);
  if (tempRect) drawRect(tempRect);
}

function drawRect(rect) {
  const x = Math.min(rect.startX, rect.endX);
  const y = Math.min(rect.startY, rect.endY);
  const w = Math.abs(rect.endX - rect.startX);
  const h = Math.abs(rect.endY - rect.startY);
  hCtx.fillStyle = 'rgba(255,255,0,0.5)';
  hCtx.fillRect(x, y, w, h);
}
