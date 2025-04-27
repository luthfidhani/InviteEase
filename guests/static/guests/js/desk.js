/* Desk page QR scanner */
(function () {
    const btn   = document.getElementById("btnScan");
    const input = document.querySelector("input[name='query']");
    const qrDiv = document.getElementById("qr-reader");
  
    if (!btn) return;          // wrong page safety
  
    let scanner = null;
  
    btn.addEventListener("click", () => {
      // toggling
      if (qrDiv.style.display === "none") startScanner();
      else stopScanner();
    });
  
    function startScanner() {
      qrDiv.style.display = "block";
      btn.innerHTML = "<i class='fa-solid fa-stop'></i> Stop Scan";
  
      scanner = new Html5Qrcode("qr-reader");
      scanner.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 250 },
        (decodedText) => {
          // Got a code!
          stopScanner();
          input.value = decodedText.trim();
          document.forms[0].submit();
        },
        (err) => console.debug(err)
      );
    }
  
    function stopScanner() {
      if (scanner) {
        scanner.stop().then(() => scanner.clear());
        scanner = null;
      }
      qrDiv.style.display = "none";
      btn.innerHTML = "<i class='fa-solid fa-qrcode'></i> Scan QR";
    }
  })();
  