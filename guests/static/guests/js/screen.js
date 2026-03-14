function initScreen(screenId) {
  const proto  = location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl  = `${proto}//${location.host}/ws/screen/${screenId}/`;
  const socket = new WebSocket(wsUrl);

  const box      = document.getElementById("welcomeBox");
  const idleBox  = document.getElementById("idleBox");
  const nameEl   = document.getElementById("guestName");
  const statusEl = document.getElementById("guestStatus");
  const notesEl  = document.getElementById("guestNotes");

  const statusStyle = {
    vvip:    { color: "#e8c4e0" },   // soft rose
    vip:     { color: "#e8d5a3" },   // warm gold
    reguler: { color: "#a8c4a0" },   // sage green
  };

  let timers = [];

  function clearTimers() {
    timers.forEach(clearTimeout);
    timers = [];
  }

  function showIdle() {
    if (idleBox) idleBox.style.opacity = "1";
    box.style.opacity = "0";
    box.classList.remove("animate__fadeIn", "animate__fadeOut");
  }

  socket.onmessage = (e) => {
    const data = JSON.parse(e.data); // { text, status, notes }

    clearTimers();

    // Hide idle, reset welcome box
    if (idleBox) idleBox.style.opacity = "0";
    box.classList.remove("animate__fadeIn", "animate__fadeOut");
    box.style.opacity = "0";

    // Fill content
    nameEl.textContent  = data.text || "";
    notesEl.textContent = data.notes || "";

    const s = (data.status || "reguler").toLowerCase();
    statusEl.textContent  = s.toUpperCase();
    statusEl.style.color  = (statusStyle[s] ?? statusStyle.reguler).color;

    // Fade in
    const t1 = setTimeout(() => {
      box.style.opacity = "1";
      box.classList.add("animate__animated", "animate__fadeIn");
    }, 100);

    // After 7s: fade out welcome, fade in idle
    const t2 = setTimeout(() => {
      box.classList.remove("animate__fadeIn");
      box.classList.add("animate__fadeOut");

      const t3 = setTimeout(() => {
        showIdle();
      }, 1000);
      timers.push(t3);
    }, 7000);

    timers.push(t1, t2);
  };

  socket.onopen  = () => console.log("Screen WS connected:", screenId);
  socket.onerror = (err) => console.error("WS error", err);
  socket.onclose = () => setTimeout(() => initScreen(screenId), 3000);
}
