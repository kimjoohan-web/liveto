/**
 * services.stub.js
 * ----------------
 * 이 파일은 “연동 포인트(스텁)”입니다.
 * - 현재는 프론트 데모용(mock) 구현
 * - 개발자가 DB/API/WebSocket을 붙일 때 이 파일만 교체(또는 내부를 수정)하면 됩니다.
 */

window.Services = (() => {
  const SESSION_KEY = "oyvd_session";

  function setSession(session){
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }
  function getSession(){
    try { return JSON.parse(localStorage.getItem(SESSION_KEY) || "null"); }
    catch { return null; }
  }
  function clearSession(){
    localStorage.removeItem(SESSION_KEY);
  }

  // async function login(username, password){
  //   // TODO: 개발자가 실제 로그인 API로 교체
  //   if (username === "test" && password === "1234") {
  //     const session = { username, token: "demo-token", ts: Date.now() };
  //     setSession(session);
  //     return { ok:true, session };
  //   }
  //   return { ok:false, message:"아이디 또는 비밀번호가 올바르지 않습니다." };
  // }

  async function logout(){
    // TODO: 개발자가 실제 로그아웃 처리로 교체
    clearSession();
    return { ok:true };
  }

  async function fetchChat(){
    // TODO: 개발자가 실제 채팅 히스토리 API로 교체
    return { ok:true, items: (window.MockChat?.items || []) };
  }

  async function sendChat(message){
    // TODO: 개발자가 실제 채팅 전송 API / WebSocket emit으로 교체
    const now = new Date();
    return {
      ok:true,
      item: {
        type: "user",
        nick: (getSession()?.username || "guest"),
        time: now.toLocaleTimeString("ko-KR", { hour:"2-digit", minute:"2-digit" }),
        body: message
      }
    };
  }

  // return { login, logout, fetchChat, sendChat, getSession, clearSession };
})();
