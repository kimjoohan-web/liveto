(() => {
  const chatBody = document.getElementById("chatBody");
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const logoutBtn = document.getElementById("logoutBtn");
  const viewerBadge = document.getElementById("viewerBadge");

  function escapeHtml(str){
    return String(str)
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll('"',"&quot;")
      .replaceAll("'","&#039;");
  }

  function renderItem(item){
    const sys = item.type === "system";
    const wrap = document.createElement("div");
    wrap.className = "msg" + (sys ? " system" : "");
    wrap.innerHTML = `
      <div class="avatar" aria-hidden="true"></div>
      <div class="mtxt">
        <div class="mtop">
          <div class="nick">${escapeHtml(item.nick || "user")}</div>
          <div class="time">${escapeHtml(item.time || "")}</div>
        </div>
        <div class="body">${escapeHtml(item.body || "")}</div>
      </div>
    `;
    return wrap;
  }

  function scrollToBottom(){
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  async function init(){
    // 세션 체크(프론트 데모 수준)
    // 세션 강제할 경우 아래 주석 해제
    // if (!window.Services.getSession()) location.href = "./index.html";

    const res = await window.Services.fetchChat();
    const items = res.ok ? res.items : [];
    chatBody.innerHTML = "";
    items.forEach(it => chatBody.appendChild(renderItem(it)));
    scrollToBottom();

    // 접속자 더미(살짝 변동)
    const base = 128;
    const n = base + Math.floor(Math.random()*12);
    viewerBadge.textContent = `접속 ${n}`;
  }

  chatForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = (chatInput.value || "").trim();
    if (!msg) return;
    chatInput.value = "";
    const res = await window.Services.sendChat(msg);
    if (res.ok) {
      chatBody.appendChild(renderItem(res.item));
      scrollToBottom();
    }
  });

  logoutBtn?.addEventListener("click", async () => {
    await window.Services.logout();
    location.href = "./index.html";
  });

  init();
})();
