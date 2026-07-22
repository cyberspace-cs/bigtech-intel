/* ===================== 大厂情报站 · 交互逻辑 ===================== */
(function () {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const esc = (s) =>
    String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );

  /* ---------- 顶部 / 导航 ---------- */
  function renderTop() {
    $("#brand-title").textContent = META.title;
    $("#brand-sub").textContent = META.subtitle;
    $("#upd").textContent = META.updated;
    $("#metanote").textContent = META.note;
  }

  /* ---------- 统计 ---------- */
  function renderStats() {
    const t1 = TIER1.length, t2 = TIER2.length, total = ALL_COMPANIES.length;
    const tech = LINEAGE.qinghua.members.length + LINEAGE.beida.members.length;
    const data = [
      { n: total, l: "覆盖大厂 / 团队" },
      { n: t1, l: "第一梯队 · 五大模型厂" },
      { n: t2, l: "第二梯队 · 典型中小厂" },
      { n: tech, l: "清华系 / 北大系 关键人物" },
    ];
    $("#stats").innerHTML = data
      .map((d) => `<div class="stat"><div class="n">${d.n}</div><div class="l">${d.l}</div></div>`)
      .join("");
  }

  /* ---------- 卡片 ---------- */
  function cardHTML(c) {
    const cls = c.tier === 1 ? (c.featured ? "card featured" : "card") : "card t2";
    const prCls = c.tier === 1 ? "priority" : "priority t2";
    const cap = c.jd.capability || "";
    return `
      <div class="${cls}" data-id="${c.id}">
        <div class="head">
          <div class="emoji">${c.emoji || "🏢"}</div>
          <div class="name">${esc(c.name)}</div>
          <div class="${prCls}">${esc(c.priority)}</div>
        </div>
        <div class="dir">${esc(c.direction)}</div>
        <div class="cap">${esc(cap)}</div>
        <div class="foot">
          <span class="badge">${c.tier === 1 ? "第一梯队" : "第二梯队"}</span>
          <span class="more">查看画像 →</span>
        </div>
      </div>`;
  }

  function renderGrid(list) {
    const grid = $("#grid");
    if (!list.length) {
      grid.innerHTML = `<div class="empty">没有匹配的公司，换个关键词试试～</div>`;
      return;
    }
    grid.innerHTML = list.map(cardHTML).join("");
    $$(".card", grid).forEach((el) =>
      el.addEventListener("click", () => openModal(el.dataset.id))
    );
  }

  /* ---------- 过滤 + 搜索 ---------- */
  let curTab = "all";
  let curQuery = "";

  function passTab(c) {
    if (curTab === "all") return true;
    if (curTab === "t1") return c.tier === 1;
    if (curTab === "t2") return c.tier === 2;
    return true;
  }
  function passQuery(c) {
    if (!curQuery) return true;
    const q = curQuery.toLowerCase();
    const hay = [
      c.name, c.direction, c.priority,
      c.jd.capability, c.jd.hook, c.jd.intent, (c.jd.stack || []).join(" "),
      (c.background && c.background.summary) || "",
      (c.background && c.background.keyPeople || []).map((p) => p.name + " " + p.detail).join(" "),
    ].join(" ").toLowerCase();
    return hay.includes(q);
  }

  function apply() {
    let list = ALL_COMPANIES.filter((c) => passTab(c) && passQuery(c));
    if (curTab === "all") {
      // 第一梯队优先、featured 置顶
      list = list.slice().sort((a, b) => {
        if (!!b.featured !== !!a.featured) return b.featured ? 1 : -1;
        return a.tier - b.tier;
      });
    }
    renderGrid(list);
  }

  /* ---------- 背景图谱 ---------- */
  function linItem(m) {
    return `
      <div class="lin-item">
        <div class="top">
          <span class="nm">${esc(m.name)}</span>
          <span class="co">${esc(m.company)}</span>
          <span class="sch">${esc(m.school)}</span>
        </div>
        <div class="rl">${esc(m.role)}</div>
        <div class="nt">${esc(m.note)}</div>
      </div>`;
  }
  function renderLineage() {
    $("#lin-qinghua").innerHTML =
      `<div class="lin-head"><h3>${esc(LINEAGE.qinghua.title)}</h3><p>${esc(LINEAGE.qinghua.desc)}</p></div>
       <div class="lin-body"><div class="lin-grid">${LINEAGE.qinghua.members.map(linItem).join("")}</div></div>`;
    $("#lin-beida").innerHTML =
      `<div class="lin-head"><h3>${esc(LINEAGE.beida.title)}</h3><p>${esc(LINEAGE.beida.desc)}</p></div>
       <div class="lin-body"><div class="lin-grid">${LINEAGE.beida.members.map(linItem).join("")}</div></div>`;
  }

  /* ---------- 简历区 ---------- */
  function renderResume() {
    $("#tips").innerHTML = RESUME_TIPS.map(
      (t, i) => `
      <div class="tip">
        <div class="num">${i + 1}</div>
        <div class="tt">${esc(t.t)}</div>
        <div class="dd">${esc(t.d)}</div>
      </div>`
    ).join("");

    $("#strategy").innerHTML = `
      <div class="table-wrap">
        <table>
          <thead><tr><th>公司</th><th>求职意向</th><th>技术栈置顶</th><th>项目 Phase 置顶</th></tr></thead>
          <tbody>
            ${RESUME_STRATEGY.map(
              (r) => `<tr>
                <td><b>${esc(r.company)}</b></td>
                <td>${esc(r.intent)}</td>
                <td>${esc(r.stack)}</td>
                <td>${esc(r.phase)}</td>
              </tr>`
            ).join("")}
          </tbody>
        </table>
      </div>`;
  }

  /* ---------- 招聘速查 ---------- */
  function renderRecruit() {
    $("#recruit").innerHTML = `
      <div class="table-wrap">
        <table>
          <thead><tr><th>梯队</th><th>公司</th><th>对应岗位方向</th><th>官方招聘入口</th></tr></thead>
          <tbody>
            ${RECRUIT_TABLE.map(
              (r) => `<tr class="recruit-row">
                <td><span class="tier-pill ${r.tier === 2 ? "t2" : ""}">${r.tier === 1 ? "第一梯队" : "第二梯队"}</span></td>
                <td><b>${esc(r.company)}</b></td>
                <td>${esc(r.dir)}</td>
                <td><a href="${r.url}" target="_blank" rel="noopener">${esc(r.url)} ↗</a></td>
              </tr>`
            ).join("")}
          </tbody>
        </table>
      </div>`;
  }

  /* ---------- 详情弹层 ---------- */
  function openModal(id) {
    const c = ALL_COMPANIES.find((x) => x.id === id);
    if (!c) return;
    const j = c.jd;
    const bg = c.background;
    let html = "";

    html += `<div class="block"><h4>JD 画像 · 代表岗位</h4><p class="kv">${(j.positions || []).map(esc).join(" / ")}</p></div>`;
    html += `<div class="block"><h4>能力画像</h4><p>${esc(j.capability)}</p></div>`;
    html += `<div class="block"><h4>适配钩子（简历重排）</h4><p>${esc(j.hook)}</p></div>`;
    html += `<div class="block"><h4>分厂定制 · 求职意向 / 技术栈 / Phase</h4>
      <p class="kv"><b>求职意向：</b>${esc(j.intent || "")}</p>
      <div class="tagline">${(j.stack || []).map((s) => `<span class="tag">${esc(s)}</span>`).join("")}</div>
      <p class="kv" style="margin-top:8px;"><b>Phase 置顶：</b>${esc(j.phaseFocus || "")}</p>
    </div>`;

    if (bg) {
      html += `<div class="block"><h4>团队 / 公司背景</h4><p>${esc(bg.summary)}</p></div>`;
      if (bg.keyPeople && bg.keyPeople.length) {
        html += `<div class="block"><h4>关键人物</h4>${bg.keyPeople
          .map(
            (p) => `<div class="person">
              <div class="pn">${esc(p.name)}</div>
              <div class="pr">${esc(p.role)}</div>
              <div class="pd">${esc(p.detail)}</div>
              ${p.school ? `<span class="ps">${esc(p.school)}</span>` : ""}
            </div>`
          )
          .join("")}</div>`;
      }
      if (bg.strategy) html += `<div class="block"><h4>战略方向</h4><p>${esc(bg.strategy)}</p></div>`;
      if (bg.product) html += `<div class="block"><h4>产品设计 / 架构</h4><p>${esc(bg.product)}</p></div>`;
      if (bg.sources && bg.sources.length) {
        html += `<div class="block"><h4>参考来源</h4><ul class="sources">${bg.sources.map((s) => `<li>${esc(s)}</li>`).join("")}</ul></div>`;
      }
    }

    html += `<div class="block"><h4>官方招聘入口</h4>
      <a class="recruit-cta" href="${j.recruit.url}" target="_blank" rel="noopener">${esc(j.recruit.label)} ↗</a>
    </div>`;

    $("#modal-title").textContent = c.name;
    $("#modal-emoji").textContent = c.emoji || "🏢";
    $("#modal-priority").textContent = `${c.priority} · ${c.direction}`;
    $("#modal-body").innerHTML = html;
    $("#modal").classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeModal() {
    $("#modal").classList.remove("open");
    document.body.style.overflow = "";
  }

  /* ---------- Tab 切换 ---------- */
  const VIEWS = ["overview", "lineage", "resume", "recruit"];
  function switchTab(tab, btn) {
    $$(".nav button").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    VIEWS.forEach((v) => $("#view-" + v).style.display = v === tab ? "" : "none");

    // search row 仅在与公司相关的视图显示
    $("#searchrow").style.display = tab === "overview" ? "" : "none";
    if (tab !== "overview") $("#searchbox").value = "";

    // 公司视图内的子 tab（全部/第一/第二）
    curTab = "all";
    $$("#subtabs button").forEach((b) => b.classList.toggle("active", b.dataset.tab === "all"));
    if (tab === "overview") apply();
  }

  /* ---------- 初始化 ---------- */
  function init() {
    renderTop();
    renderStats();
    renderLineage();
    renderResume();
    renderRecruit();

    // 视图
    $$(".nav button").forEach((b) =>
      b.addEventListener("click", () => switchTab(b.dataset.view, b))
    );
    // 公司子 tab
    $$("#subtabs button").forEach((b) =>
      b.addEventListener("click", () => {
        $$("#subtabs button").forEach((x) => x.classList.remove("active"));
        b.classList.add("active");
        curTab = b.dataset.tab;
        apply();
      })
    );
    // 搜索
    $("#searchbox").addEventListener("input", (e) => {
      curQuery = e.target.value.trim();
      apply();
    });
    // 关闭弹层
    $("#modal-close").addEventListener("click", closeModal);
    $("#modal-mask").addEventListener("click", (e) => {
      if (e.target.id === "modal-mask") closeModal();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeModal();
    });

    // 默认视图
    switchTab("overview", $('.nav button[data-view="overview"]'));
    apply();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
