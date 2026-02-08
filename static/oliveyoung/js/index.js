// (() => {
//   const form = document.getElementById("loginForm");
//   const err = document.getElementById("err");
//   const skip = document.getElementById("skipLink");

//   // 이미 로그인되어 있으면 live로
//   if (window.Services?.getSession?.()) {
//     // 필요 시 주석 해제
//     // location.href = "./live.html";
//   }

//   // 데모 편의: "바로 보기"는 세션 없이도 이동하도록 둠
//   skip?.addEventListener("click", (e) => {
//     // 기본 동작 유지
//   });

//   form?.addEventListener("submit", async (e) => {
//     e.preventDefault();
//     err.style.display = "none";
//     const fd = new FormData(form);
//     const username = String(fd.get("username") || "").trim();
//     const password = String(fd.get("password") || "").trim();

//     const res = await window.Services.login(username, password);
//     if (!res.ok) {
//       err.textContent = res.message || "로그인에 실패했습니다.";
//       err.style.display = "block";
//       return;
//     }
//     location.href = "./live.html";
//   });
// })();
