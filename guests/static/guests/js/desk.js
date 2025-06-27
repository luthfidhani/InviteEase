/* Desk page QR scanner */
(function () {
    const btn   = document.getElementById("btnScan");
    const input = document.querySelector("input[name='query']");
    const qrDiv = document.getElementById("qr-reader");
  
    if (!btn) return;          // wrong page safety
  
    let scanner = null;
    let isScanning = false;
  
    btn.addEventListener("click", () => {
      // toggling
      if (!isScanning) {
        startScanner();
      } else {
        stopScanner();
      }
    });
  
    function startScanner() {
      // Show QR reader with Tailwind classes
      qrDiv.classList.remove("hidden");
      qrDiv.classList.add("block");
      btn.innerHTML = "<i class='fa-solid fa-stop'></i> Stop Scan";
      btn.classList.remove("from-gray-500", "to-gray-600", "hover:from-gray-600", "hover:to-gray-700");
      btn.classList.add("from-red-500", "to-red-600", "hover:from-red-600", "hover:to-red-700");
      isScanning = true;
  
      scanner = new Html5Qrcode("qr-reader");
      scanner.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 250 },
        (decodedText) => {
          // Got a code!
          stopScanner();
          input.value = decodedText.trim();
          // Use the form's submit button to ensure CSRF token is included
          const submitBtn = document.querySelector('button[type="submit"]');
          if (submitBtn) {
            submitBtn.click();
          } else {
            // Fallback to form submission if button not found
            const form = document.querySelector('form');
            if (form) {
              form.submit();
            }
          }
        },
        (err) => console.debug(err)
      ).catch((err) => {
        console.error("Failed to start scanner:", err);
        stopScanner();
      });
    }
  
    function stopScanner() {
      if (scanner) {
        scanner.stop().then(() => {
          scanner.clear();
          scanner = null;
        }).catch((err) => {
          console.error("Error stopping scanner:", err);
        });
      }
      
      // Hide QR reader with Tailwind classes
      qrDiv.classList.add("hidden");
      qrDiv.classList.remove("block");
      btn.innerHTML = "<i class='fa-solid fa-qrcode'></i> Scan QR";
      btn.classList.remove("from-red-500", "to-red-600", "hover:from-red-600", "hover:to-red-700");
      btn.classList.add("from-gray-500", "to-gray-600", "hover:from-gray-600", "hover:to-gray-700");
      isScanning = false;
    }
  })();
  