// Builds deck/why/EvidEO-why-it-matters.pptx (6 slides). Run from repo root:
//   node deck/why/build_why.js
// Numbers come from paper/analysis/results.json (run paper/analysis/experiments.py first).
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const SKILL = process.env.PPTX_SKILL;
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));
const ROOT = path.resolve(__dirname, "../..");
const R = JSON.parse(fs.readFileSync(path.join(ROOT, "paper/analysis/results.json"), "utf8"));
const OUT = path.join(__dirname, "EvidEO-why-it-matters.pptx");

const HEX = { navy: "1F5A99", ink: "1E2430", muted: "5B6472", line: "C9D3E0", tint: "EEF3F9", orange: "D9822B", teal: "2A9D8F", gray: "9A9A9A", white: "FFFFFF", sand: "F4E6D6" };
const THEME = {
  name: "EvidEO Plain",
  headFontFace: "Times New Roman",
  bodyFontFace: "Calibri",
  colors: { dk1: HEX.ink, lt1: HEX.white, dk2: HEX.navy, lt2: HEX.tint, accent1: HEX.navy, accent2: HEX.orange, accent3: HEX.teal,
            accent4: HEX.gray, accent5: "8C5BA8", accent6: HEX.muted, hlink: HEX.navy, folHlink: "8C5BA8" },
};

async function icon(Comp, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
  pres.title = "EvidEO: why it matters";
  pres.author = "Team Stardust";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;

  // ---------- layouts ----------
  const frame = [
    { text: { text: "Evid", options: { x: 8.25, y: 0.2, w: 0.8, h: 0.42, align: "right", valign: "middle", fontSize: 18, bold: true, color: C.accent1, fontFace: "Calibri", margin: 0 } } },
    { text: { text: "EO", options: { x: 9.05, y: 0.2, w: 0.65, h: 0.42, align: "left", valign: "middle", fontSize: 18, bold: true, color: C.accent2, fontFace: "Calibri", margin: 0 } } },
    { rect: { x: 0, y: 5.3, w: 10, h: 0.325, fill: { color: C.accent1 } } },
    { text: { text: "EvidEO  |  measured satellite answers you can check", options: { x: 0.3, y: 5.3, w: 7, h: 0.325, fontSize: 10, color: C.background1, valign: "middle", margin: 0 } } },
  ];

  // title placeholder for content slides
  pres.defineSlideMaster({
    title: "CONTENT_T", background: { color: HEX.white },
    objects: [...frame, { placeholder: { options: { name: "title", type: "title", x: 1.6, y: 0.14, w: 6.6, h: 0.56, align: "center", valign: "middle",
                fontSize: 26, bold: true, color: C.text1, fontFace: "Times New Roman", margin: 0, fit: "shrink" }, text: "" } }],
    slideNumber: { x: 9.2, y: 5.33, w: 0.5, h: 0.26, color: HEX.white, fontSize: 10, align: "right" },
  });
  pres.defineSlideMaster({
    title: "TITLE", background: { color: HEX.white },
    objects: [
      { rect: { x: 0, y: 5.3, w: 10, h: 0.325, fill: { color: C.accent1 } } },
      { text: { text: "Team Stardust  |  RV Institute of Technology and Management, Bengaluru", options: { x: 0.3, y: 5.3, w: 8, h: 0.325, fontSize: 10, color: C.background1, valign: "middle", margin: 0 } } },
    ],
  });

  const T = (s, text) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.3, y: 0.2, w: 1.15, h: 0.42, rectRadius: 0.21, fill: { color: C.background1 }, line: { color: C.accent1, width: 1.25 }, objectName: "team pill" });
    s.addText("Stardust", { x: 0.3, y: 0.2, w: 1.15, h: 0.42, align: "center", valign: "middle", fontSize: 12, color: C.text1, margin: 0, isTextBox: true });
    s.addText(text, { placeholder: "title" });
  };
  const box = (s, x, y, w, h, name, fill) => s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill || C.background1 }, line: { color: HEX.line, width: 1 }, objectName: name });
  const head = (s, x, y, w, text) => s.addText(text, { x, y, w, h: 0.32, fontSize: 14, bold: true, color: C.text1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  const vline = (s, x, y, h) => s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: HEX.ink, width: 1 } });

  const e1 = R.E1_test["v1.1"], e2 = R.E2_loeo, e3 = R.E3_india_local_calibration;
  const k8 = e3.strategies.intercept_only.find(r => r.k === 8);
  const pct = v => Math.round(v * 100);

  // ===== Slide 1: title =====
  pres.addSection({ title: "Why EvidEO" });
  let s = pres.addSlide({ masterName: "TITLE", sectionTitle: "Why EvidEO" });
  s.addImage({ path: path.join(ROOT, "paper/figures/fig_barpeta_map.png"), x: 5.75, y: 0.45, w: 3.85, h: 4.13, objectName: "Barpeta map", altText: "EvidEO map of Sentinel-1 water over Barpeta district, 11 July 2024" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 0.5, w: 1.15, h: 0.42, rectRadius: 0.21, fill: { color: C.background1 }, line: { color: C.accent1, width: 1.25 } });
  s.addText("Stardust", { x: 0.5, y: 0.5, w: 1.15, h: 0.42, align: "center", valign: "middle", fontSize: 12, margin: 0, isTextBox: true, color: C.text1 });
  s.addText([{ text: "Evid", options: { color: C.accent1 } }, { text: "EO", options: { color: C.accent2 } }],
            { x: 0.5, y: 1.15, w: 5, h: 0.9, fontSize: 48, bold: true, fontFace: "Times New Roman", margin: 0, isTextBox: true });
  s.addText("Evidence first, or no answer", { x: 0.5, y: 2.05, w: 5.1, h: 0.5, fontSize: 22, color: C.text1, fontFace: "Times New Roman", margin: 0, isTextBox: true });
  s.addText("Ask about floods in any Indian district in plain words. Get an area measured from the actual Sentinel-1 radar pass, with scene, date, map and a calibrated confidence, or an honest \"not enough evidence\".",
            { x: 0.5, y: 2.7, w: 5.0, h: 1.05, fontSize: 14, color: HEX.muted, margin: 0, isTextBox: true, valign: "top" });
  s.addText("Sai Bhuwan S  ·  Yashita Mandavilli  ·  Raj Venkat  ·  Nikhil S Rao  ·  Shashwat Mittal  ·  Sasanuru Anirudh",
            { x: 0.5, y: 4.15, w: 5.0, h: 0.6, fontSize: 11, color: C.text1, margin: 0, isTextBox: true });
  s.addText("Barpeta, Assam · Sentinel-1 · 11 Jul 2024 · live run", { x: 5.75, y: 4.62, w: 3.85, h: 0.3, fontSize: 10, color: HEX.muted, align: "right", margin: 0, isTextBox: true });
  s.addNotes("EvidEO in one line: plain-language flood questions answered with measured, checkable evidence, or an honest refusal. The map on the right is a real run on the Sentinel-1 pass over Barpeta on 11 July 2024. Note: that water figure includes the river and permanent wetlands; it is water extent, not verified flood extent.");

  // ===== Slide 2: problem =====
  s = pres.addSlide({ masterName: "CONTENT_T", sectionTitle: "Why EvidEO" });
  T(s, "The Problem That Does Not Go Away");
  head(s, 0.3, 0.82, 4.55, "WHO LOSES TIME TODAY");
  head(s, 5.15, 0.82, 4.55, "WHY TODAY'S AI DOES NOT FIX IT");
  vline(s, 5.0, 0.85, 4.3);
  const users = [
    [fa.FaUserTie, "District disaster officials", "Wait for central maps: about 300 flood products in 2024 for 700+ districts."],
    [fa.FaSeedling, "Crop insurance officers", "Claims stay pending while yield data and satellite checks arrive late."],
    [fa.FaNewspaper, "Journalists, fact-checkers", "Free tools assume you know which sensor and band to use."],
  ];
  for (let i = 0; i < users.length; i++) {
    const y = 1.25 + i * 0.78;
    s.addShape(pres.shapes.OVAL, { x: 0.35, y: y + 0.05, w: 0.5, h: 0.5, fill: { color: C.background2 }, line: { color: C.background2 } });
    s.addImage({ data: await icon(users[i][0], HEX.navy), x: 0.47, y: y + 0.17, w: 0.26, h: 0.26 });
    s.addText(users[i][1], { x: 1.0, y, w: 3.85, h: 0.27, fontSize: 13, bold: true, color: C.text1, margin: 0, isTextBox: true });
    s.addText(users[i][2], { x: 1.0, y: y + 0.27, w: 3.85, h: 0.42, fontSize: 11, color: HEX.muted, margin: 0, isTextBox: true, valign: "top" });
  }
  const stats = [["60%+", "monsoon cloud cover over most of India"], ["~10x", "gap: 25 to 50k trained GIS users vs 500k more needed"]];
  stats.forEach((st, i) => {
    const x = 0.35 + i * 2.3;
    box(s, x, 3.68, 2.15, 1.42, "stat " + i, HEX.tint);
    s.addText(st[0], { x: x + 0.1, y: 3.73, w: 1.95, h: 0.6, fontSize: 30, bold: true, color: C.accent1, fontFace: "Times New Roman", margin: 0, isTextBox: true });
    s.addText(st[1], { x: x + 0.1, y: 4.33, w: 1.95, h: 0.72, fontSize: 11, color: C.text1, margin: 0, isTextBox: true, valign: "top" });
  });
  s.addChart(pres.charts.BAR, [{ name: "Grounding at IoU 0.5 (%)", labels: ["GPT-4o", "GPT-4V", "GeoChat", "EarthDial", "Supervised specialist"], values: [0.9, 7.6, 10.6, 24.3, 76.8] }], {
    x: 5.15, y: 1.2, w: 4.55, h: 2.35, barDir: "bar", chartColors: [HEX.gray, HEX.gray, HEX.navy, HEX.navy, HEX.teal],
    showTitle: true, title: "Can it find the thing you asked about? (%)", titleFontSize: 11, titleColor: HEX.ink, titleFontFace: "+mn-lt",
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 9, dataLabelColor: HEX.ink, dataLabelFontFace: "+mn-lt",
    catAxisLabelColor: HEX.ink, catAxisLabelFontSize: 9, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valAxisMaxVal: 90,
    valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 45, objectName: "grounding chart",
  });
  s.addText("Sources: VLEO-Bench (GPT-4V, specialist), GEOBench-VLM (GPT-4o, EarthDial), GeoChat paper. Benchmarks differ.", { x: 5.15, y: 3.55, w: 4.55, h: 0.3, fontSize: 9, color: HEX.muted, margin: 0, isTextBox: true });
  box(s, 5.15, 3.92, 4.55, 1.18, "hallucination box", HEX.sand);
  s.addText([{ text: "32 to 64%", options: { bold: true, fontSize: 24, color: "8A4A0F", fontFace: "Times New Roman", breakLine: true } },
             { text: "of remote-sensing VLM answers contain hallucinations, judged by experts (RSHallu, 2026). None states when not to trust it.", options: { fontSize: 11, color: C.text1 } }],
            { x: 5.3, y: 3.97, w: 4.3, h: 1.08, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("Whose problem: district officials, insurance officers, fact-checkers. Why it lasts: questions are local and constant, answers are produced centrally; the skills gap is about tenfold; monsoon clouds return every year. Why chat AI does not fix it: it is fluent but cannot locate what you asked about, and it never tells you when to distrust it. Chart values are read from each paper's tables; benchmarks differ, so compare orders of magnitude.");

  // ===== Slide 3: solution =====
  s = pres.addSlide({ masterName: "CONTENT_T", sectionTitle: "Why EvidEO" });
  T(s, "Instruments Answer, AI Only Asks");
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.85, w: 9.4, h: 0.5, fill: { color: C.background1 }, line: { color: HEX.ink, width: 1 } });
  s.addText("Every number comes from a measured, versioned instrument on the real radar pass. The language model never makes a number up.", { x: 0.4, y: 0.85, w: 9.2, h: 0.5, fontSize: 13, align: "center", valign: "middle", color: C.text1, margin: 0, isTextBox: true });
  const steps = [["1", "Ask", "\"How much of Barpeta was under water on 11 July?\""], ["2", "Find the pass", "Public STAC catalogues; radar first in monsoon"],
                 ["3", "Measure", "SAR water instrument per 5 km tile, on CPU"], ["4", "Calibrate", "Score to probability, fitted on hand labels"]];
  steps.forEach((st, i) => {
    const y = 1.55 + i * 0.83;
    s.addShape(pres.shapes.OVAL, { x: 0.35, y: y + 0.06, w: 0.46, h: 0.46, fill: { color: C.accent1 }, line: { color: C.accent1 } });
    s.addText(st[0], { x: 0.35, y: y + 0.06, w: 0.46, h: 0.46, align: "center", valign: "middle", fontSize: 14, bold: true, color: C.background1, margin: 0, isTextBox: true });
    s.addText(st[1], { x: 0.95, y, w: 3.0, h: 0.28, fontSize: 13, bold: true, color: C.text1, margin: 0, isTextBox: true });
    s.addText(st[2], { x: 0.95, y: y + 0.28, w: 3.2, h: 0.42, fontSize: 11, color: HEX.muted, margin: 0, isTextBox: true, valign: "top" });
    if (i < 3) s.addShape(pres.shapes.LINE, { x: 0.58, y: y + 0.55, w: 0, h: 0.31, line: { color: HEX.line, width: 1.5 } });
  });
  vline(s, 4.45, 1.55, 3.6);
  // the two outcomes
  box(s, 4.7, 1.55, 2.4, 3.55, "card yes", C.background1);
  s.addText("CONFIDENCE ≥ 0.60", { x: 4.8, y: 1.62, w: 2.2, h: 0.28, fontSize: 10, bold: true, color: C.accent3, margin: 0, isTextBox: true });
  s.addText([{ text: "914 km²", options: { fontSize: 28, bold: true, fontFace: "Times New Roman", color: C.text1, breakLine: true } },
             { text: "water in Barpeta, 11 Jul 2024", options: { fontSize: 11, color: C.text1 } }], { x: 4.8, y: 1.92, w: 2.2, h: 0.92, margin: 0, isTextBox: true, valign: "top" });
  const chips = ["Sentinel-1 scene + date", "117 of 117 tiles", "confidence 0.62", "receipt re-runs identically"];
  chips.forEach((c, i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 4.8, y: 2.85 + i * 0.4, w: 2.2, h: 0.33, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2 } });
    s.addText(c, { x: 4.85, y: 2.85 + i * 0.4, w: 2.1, h: 0.33, fontSize: 10, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText("Water extent, includes the river and wetlands; not yet checked against NRSC maps.", { x: 4.8, y: 4.48, w: 2.2, h: 0.5, fontSize: 9, color: HEX.muted, margin: 0, isTextBox: true, valign: "top" });
  box(s, 7.3, 1.55, 2.4, 3.55, "card no", HEX.sand);
  s.addText("CONFIDENCE < 0.60", { x: 7.4, y: 1.62, w: 2.2, h: 0.28, fontSize: 10, bold: true, color: "8A4A0F", margin: 0, isTextBox: true });
  s.addText([{ text: "Not enough evidence", options: { fontSize: 18, bold: true, fontFace: "Times New Roman", color: C.text1, breakLine: true } },
             { text: "\"Did the flood spread?\" abstained at 0.23. EvidEO offered what would help instead: the two single-date extents (413 and 914 km²), each published with its own confidence.", options: { fontSize: 11, color: C.text1 } }],
            { x: 7.4, y: 1.92, w: 2.2, h: 3.05, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("The core design flip: in chat assistants the model produces the answer. In EvidEO a transparent instrument measures, a calibration fitted on hand-labelled flood chips turns its score into a probability, and the card is published only at 0.60 or above. Below that it says so and offers the next useful question. Both cards on this slide are from real runs on live Sentinel-1 data.");

  // ===== Slide 4: evidence =====
  s = pres.addSlide({ masterName: "CONTENT_T", sectionTitle: "Why EvidEO" });
  T(s, "It Works on Held-Out Data");
  head(s, 0.3, 0.82, 4.55, "WHAT A USER GETS");
  head(s, 5.15, 0.82, 4.55, "RISK VS COVERAGE (82 HELD-OUT CHIPS)");
  vline(s, 5.0, 0.85, 4.3);
  const big = [[`${pct(e1.error_always_answer)}% → ${pct(e1.error_when_published)}%`, "wrong area answers, always answering vs publishing only at 0.60"],
               [`${pct(e1["coverage_at_0.6"])}%`, "of questions answered; the rest honestly abstain"],
               ["8 / 8", "demo receipts re-ran to identical output hashes (713 tiles)"],
               ["77 to 98 s", "per whole district on 2 CPU cores, no GPU; 0.5 s cached"]];
  big.forEach((b, i) => {
    const x = 0.35 + (i % 2) * 2.3, y = 1.25 + Math.floor(i / 2) * 1.95;
    box(s, x, y, 2.15, 1.8, "stat " + i, HEX.tint);
    s.addText(b[0], { x: x + 0.1, y: y + 0.08, w: 1.95, h: 0.7, fontSize: i === 0 ? 22 : 26, bold: true, color: C.accent1, fontFace: "Times New Roman", margin: 0, isTextBox: true, valign: "middle" });
    s.addText(b[1], { x: x + 0.1, y: y + 0.82, w: 1.95, h: 0.9, fontSize: 11, color: C.text1, margin: 0, isTextBox: true, valign: "top" });
  });
  const [cv, rk] = R.E1_test.curve_v11, [cv0, rk0] = R.E1_test.curve_v10;
  s.addChart(pres.charts.SCATTER, [
    { name: "coverage", values: cv.map(v => +v.toFixed(3)) },
    { name: "EvidEO v1.1 (VV + VH)", values: rk.map(v => +(v * 100).toFixed(1)) },
    { name: "Always answer", values: cv.map(() => +(e1.error_always_answer * 100).toFixed(1)) },
  ], {
    x: 5.15, y: 1.2, w: 4.55, h: 3.3, lineSize: 2, lineDataSymbol: "none", chartColors: [HEX.navy, HEX.orange],
    valAxisTitle: "Wrong among answered (%)", showValAxisTitle: true, valAxisTitleFontSize: 9, valAxisTitleColor: HEX.muted, valAxisTitleFontFace: "+mn-lt",
    catAxisTitle: "Share of questions answered", showCatAxisTitle: true, catAxisTitleFontSize: 9, catAxisTitleColor: HEX.muted, catAxisTitleFontFace: "+mn-lt",
    valAxisMinVal: 0, valAxisMaxVal: 60, catAxisMinVal: 0, catAxisMaxVal: 1, valAxisLabelFontSize: 9, catAxisLabelFontSize: 9,
    valAxisLabelColor: HEX.ink, catAxisLabelColor: HEX.ink, valAxisLabelFontFace: "+mn-lt", catAxisLabelFontFace: "+mn-lt", catAxisLabelFormatCode: "0%",
    valGridLine: { color: "E6E6E6", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "b", legendFontSize: 9, legendFontFace: "+mn-lt", legendColor: HEX.ink, objectName: "risk coverage chart",
  });
  s.addText("Sen1Floods11 test split. Answer counted right if area is within ±20% of hand labels. Our detector itself is ordinary: per-chip IoU 0.36, same as the published Otsu baseline (0.36).", { x: 5.15, y: 4.5, w: 4.55, h: 0.62, fontSize: 9, color: HEX.muted, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes(`Always answering, 45% of area answers on held-out chips are wrong. Publishing only at calibrated confidence 0.60 or above, EvidEO answers 43% of questions and 26% of those are wrong (95% bootstrap interval 12 to 41%). We are clear that the detector is not better than published baselines: per-chip IoU 0.362 vs 0.359 for Otsu in the Sen1Floods11 paper. The contribution is how answers are gated, receipted and reproduced.`);

  // ===== Slide 5: the finding =====
  s = pres.addSlide({ masterName: "CONTENT_T", sectionTitle: "Why EvidEO" });
  T(s, "Trust Must Be Calibrated Locally");
  const evs = Object.keys(e2).sort((a, b) => e2[b].overconfidence - e2[a].overconfidence);
  s.addChart(pres.charts.BAR, [{ name: "Over-confidence (points)", labels: evs, values: evs.map(k => Math.round(e2[k].overconfidence * 100)) }], {
    x: 0.3, y: 0.85, w: 4.75, h: 4.3, barDir: "bar", chartColors: evs.map(k => ["India", "Pakistan", "Sri-Lanka"].includes(k) ? HEX.orange : HEX.navy),
    showTitle: true, title: "Confidence minus actual accuracy, region held out (points)", titleFontSize: 11, titleColor: HEX.ink, titleFontFace: "+mn-lt",
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 9, dataLabelColor: HEX.ink, dataLabelFontFace: "+mn-lt", dataLabelFormatCode: "+0;-0;0",
    catAxisLabelColor: HEX.ink, catAxisLabelFontSize: 9, catAxisLabelFontFace: "+mn-lt", catAxisOrientation: "maxMin", catAxisLabelPos: "low", valAxisHidden: true, valAxisMinVal: -40, valAxisMaxVal: 40,
    valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 40, objectName: "loeo chart",
  });
  vline(s, 5.2, 0.9, 4.25);
  s.addText([{ text: "South Asian floods fool a globally calibrated system.", options: { bold: true, breakLine: true } },
             { text: `Fitted on other regions, EvidEO would be over-confident on India by ${Math.round(e2.India.overconfidence * 100)} points and publish ${pct(e2.India.coverage)}% of Indian answers with ${pct(e2.India.error_when_published)}% of them wrong.`, options: {} }],
            { x: 5.4, y: 0.9, w: 4.3, h: 1.25, fontSize: 12, color: C.text1, margin: 0, isTextBox: true, valign: "top" });
  const fix = [["+20 → +1", "over-confidence after refitting on just 8 Indian chips"], [`${pct(e2.India.error_when_published)}% → ${pct(k8.err_pub_mean)}%`, "wrong among published Indian answers"], [`${pct(e2.India.coverage)}% → ${pct(k8.coverage_mean)}%`, "answered: the honest price of a weak instrument"]];
  fix.forEach((f, i) => {
    const y = 2.3 + i * 0.95;
    box(s, 5.4, y, 4.3, 0.82, "fix " + i, i === 2 ? HEX.sand : HEX.tint);
    s.addText(f[0], { x: 5.5, y, w: 1.75, h: 0.82, fontSize: 18, bold: true, color: i === 2 ? "8A4A0F" : C.accent1, fontFace: "Times New Roman", valign: "middle", margin: 0, isTextBox: true });
    s.addText(f[1], { x: 7.3, y, w: 2.3, h: 0.82, fontSize: 11, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addNotes("This is the result we think matters beyond our system. Leave one flood event out, fit the calibration on the rest, and test on the held-out event. All three South Asian events are over-confident; the USA is under-confident. Any assistant that states a confidence without local calibration has this problem. Refitting only the intercept on eight labelled Indian chips removes the over-confidence and cuts wrong published answers from 55% to 28%, but the honest system then answers only about 13% of Indian questions. Limitation: the 64 Indian chips come from one Sen1Floods11 event.");

  // ===== Slide 6: why it matters =====
  s = pres.addSlide({ masterName: "CONTENT_T", sectionTitle: "Why EvidEO" });
  T(s, "Why It Matters, and What Is Next");
  head(s, 0.3, 0.82, 5.3, "READ IN FULL: NO OTHER SYSTEM HAS MORE THAN ONE");
  const cols = ["", "EvidEO", "Copernicus GFM", "RSure-Agent", "EO-Gym", "Google Earth AI"];
  const rows = [["Calibrated confidence per answer", "●", "◐", "", "", ""], ["Abstains with a next step", "●", "◐", "◐", "", ""], ["Scene receipts that re-run", "●", "◐", "◐", "◐", ""],
                ["Radar chosen under cloud", "●", "", "", "◐", ""], ["CPU or offline", "●", "", "", "◐", ""], ["Plain-language questions", "●", "", "◐", "◐", "●"]];
  const cell = (t, i, j) => ({ text: t, options: { bold: j === 1 || i === 0, color: j === 1 ? HEX.navy : HEX.ink, align: j === 0 ? "left" : "center", fill: { color: i === 0 ? HEX.tint : HEX.white }, fontSize: j === 0 ? 10 : (i === 0 ? 9 : 12) } });
  s.addTable([cols.map((c, j) => cell(c, 0, j)), ...rows.map((r, i) => r.map((c, j) => cell(c, i + 1, j)))], {
    x: 0.3, y: 1.2, w: 5.3, colW: [1.85, 0.62, 0.74, 0.7, 0.62, 0.77], rowH: 0.36, border: { type: "solid", pt: 0.75, color: HEX.line }, fontFace: "Calibri", valign: "middle", margin: 0.04,
  });
  s.addText("● has it   ◐ partial form. Full-text reads of the 37 closest papers (NOVELTY.md 5.8).", { x: 0.3, y: 3.8, w: 5.3, h: 0.28, fontSize: 9, color: HEX.muted, margin: 0, isTextBox: true });
  box(s, 0.3, 4.15, 5.3, 0.98, "honest limits", HEX.sand);
  s.addText([{ text: "Honest limits: ", options: { bold: true } }, { text: "the detector is a classic split-based threshold chain; Indian labels come from one event; no user study yet; the 914 km² figure includes the river and wetlands." }],
            { x: 0.42, y: 4.2, w: 5.06, h: 0.88, fontSize: 11, color: C.text1, margin: 0, isTextBox: true, valign: "middle" });
  vline(s, 5.85, 0.9, 4.25);
  head(s, 6.05, 0.82, 3.65, "NEXT");
  const next = [["Better instrument", "Terrain (HAND) and permanent-water masks, per-pixel water probability"], ["Indian labels", "Label chips from Assam and Bihar events; test across events"],
                ["User study", "10 to 15 non-GIS users: cards vs map tools, timed"], ["Publish", "Workshop paper (draft ready, IEEE format) and open release"]];
  next.forEach((n, i) => {
    const y = 1.25 + i * 0.97;
    s.addText(n[0], { x: 6.05, y, w: 3.65, h: 0.3, fontSize: 13, bold: true, color: C.accent1, margin: 0, isTextBox: true });
    s.addText(n[1], { x: 6.05, y: y + 0.3, w: 3.65, h: 0.55, fontSize: 11, color: C.text1, margin: 0, isTextBox: true, valign: "top" });
  });
  s.addNotes("Why it matters: every ingredient exists somewhere in partial form, but after reading the 37 closest papers in full, no research system delivers more than one of these six in full, and none tells a non-expert when not to trust an answer. The bottleneck we found is local labels and instrument quality, not bigger language models. Next: improve the instrument, gather Indian labels across events, run a small user study, and submit the paper.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
