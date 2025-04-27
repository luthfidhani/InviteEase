function initScreen(screenId) {
  const wsUrl = `ws://${location.host}/ws/screen/${screenId}/`;
  const socket = new WebSocket(wsUrl);

  const box = document.getElementById("welcomeBox");
  const nameEl = document.getElementById("guestName");
  const statusEl = document.getElementById("guestStatus");
  const notesEl = document.getElementById("guestNotes");

  // map warna DaisyUI utk status
  const colorMap = {
    vvip: "text-accent",
    vip: "text-warning",
    reguler: "text-info",
  };

  // Variabel untuk menyimpan timeout
  let animationTimeouts = [];

  socket.onmessage = (e) => {
    const data = JSON.parse(e.data); // {text, status, notes}

    // Bersihkan semua timeout yang ada
    animationTimeouts.forEach(timeout => clearTimeout(timeout));
    animationTimeouts = [];

    // Reset animasi dan tampilkan data baru
    box.classList.remove('animate__animated', 'animate__fadeIn', 'animate__fadeOut');
    box.style.opacity = '0';
    
    // Update konten
    nameEl.textContent = data.text;
    statusEl.textContent = (data.status || "").toUpperCase();
    notesEl.textContent = data.notes || "";

    statusEl.className = `text-3xl font-semibold ${
      colorMap[data.status] ?? "text-info"
    }`;

    // Fade in
    box.style.opacity = '1';
    box.classList.add('animate__animated', 'animate__fadeIn');
    
    // Setelah fade in selesai (1 detik)
    const fadeInTimeout = setTimeout(() => {
      // Hapus class fadeIn
      box.classList.remove('animate__fadeIn');
      
      // Tunggu 6 detik, lalu fade out
      const delayTimeout = setTimeout(() => {
        box.classList.add('animate__fadeOut');
        
        // Setelah fade out selesai (1 detik), sembunyikan elemen
        const fadeOutTimeout = setTimeout(() => {
          box.style.opacity = '0';
          box.classList.remove('animate__fadeOut');
        }, 1000);
        
        animationTimeouts.push(fadeOutTimeout);
      }, 6000);
      
      animationTimeouts.push(delayTimeout);
    }, 1000);
    
    animationTimeouts.push(fadeInTimeout);
  };

  socket.onopen = () => console.log("Screen WS connected");
  socket.onerror = (err) => console.error("WS error", err);
  socket.onclose = () => setTimeout(() => initScreen(screenId), 3000); // auto-reconnect
}