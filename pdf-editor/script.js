let pdfDoc = null;
let scale = 1.5;
let highlightMode = false;
let highlights = {}; // page -> array of rects
let mergedPdfBytes = null;

const fileInput = document.getElementById('file-input');
const mergeInput = document.getElementById('merge-input');
const mergeBtn = document.getElementById('merge-btn');
const downloadPdfBtn = document.getElementById('download-pdf');
const highlightToggle = document.getElementById('highlight-toggle');
const viewerContainer = document.getElementById('viewer-container');

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
  document.querySelectorAll('.highlight-canvas').forEach((c) => {
    c.style.pointerEvents = highlightMode ? 'auto' : 'none';
  });
});

async function loadPdf(data) {
  const loadingTask = pdfjsLib.getDocument({ data });
  pdfDoc = await loadingTask.promise;
  highlights = {};
  mergedPdfBytes = data;
  viewerContainer.innerHTML = '';

  for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
    const page = await pdfDoc.getPage(pageNum);
    const viewport = page.getViewport({ scale });

    const canvas = document.createElement('canvas');
    canvas.className = 'pdf-page';
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    const ctx = canvas.getContext('2d');
    await page.render({ canvasContext: ctx, viewport }).promise;

    const hlCanvas = document.createElement('canvas');
    hlCanvas.className = 'highlight-canvas';
    hlCanvas.width = viewport.width;
    hlCanvas.height = viewport.height;
    hlCanvas.dataset.pageNum = pageNum;
    hlCanvas.style.pointerEvents = highlightMode ? "auto" : "none";
    hlCanvas.addEventListener("mousedown", (e) => startHighlight(e, pageNum, hlCanvas));

    const btn = document.createElement('button');
    btn.textContent = '下載此頁為圖片';
    btn.addEventListener('click', () => {
      const link = document.createElement('a');
      link.download = `page-${pageNum}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    });

    const pageDiv = document.createElement('div');
    pageDiv.className = 'page-container';
    pageDiv.appendChild(canvas);
    pageDiv.appendChild(hlCanvas);
    pageDiv.appendChild(btn);
    viewerContainer.appendChild(pageDiv);
  }
}

function startHighlight(e, pageNum, canvas) {
  if (!highlightMode) return;
  const rect = { startX: e.offsetX, startY: e.offsetY, endX: e.offsetX, endY: e.offsetY };
  const ctx = canvas.getContext('2d');
  const move = (ev) => {
    rect.endX = ev.offsetX;
    rect.endY = ev.offsetY;
    redrawHighlights(pageNum, ctx, canvas, rect);
  };
  const up = () => {
    canvas.removeEventListener('mousemove', move);
    canvas.removeEventListener('mouseup', up);
    storeHighlight(pageNum, rect);
    redrawHighlights(pageNum, ctx, canvas);
  };
  canvas.addEventListener('mousemove', move);
  canvas.addEventListener('mouseup', up);
}

function storeHighlight(pageNum, rect) {
  if (!highlights[pageNum]) highlights[pageNum] = [];
  highlights[pageNum].push(rect);
}

function redrawHighlights(pageNum, ctx, canvas, tempRect) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const rects = highlights[pageNum] || [];
  rects.forEach((r) => drawRect(ctx, r));
  if (tempRect) drawRect(ctx, tempRect);
}

function drawRect(ctx, rect) {
  const x = Math.min(rect.startX, rect.endX);
  const y = Math.min(rect.startY, rect.endY);
  const w = Math.abs(rect.endX - rect.startX);
  const h = Math.abs(rect.endY - rect.startY);
  ctx.fillStyle = 'rgba(255,255,0,0.5)';
  ctx.fillRect(x, y, w, h);
}
