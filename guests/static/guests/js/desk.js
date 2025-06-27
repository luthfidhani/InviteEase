/* Desk page QR scanner + autocomplete */
(function () {
    const btn   = document.getElementById("btnScan");
    const input = document.querySelector("input[name='query']");
    const qrDiv = document.getElementById("qr-reader");
    const acList = document.getElementById("autocomplete-list");
  
    if (!btn) return;          // wrong page safety
  
    let scanner = null;
    let isScanning = false;
    let acTimeout = null;
  
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

    // --- Autocomplete logic ---
    if (input && acList) {
      input.setAttribute('autocomplete', 'off');
      input.addEventListener('input', function() {
        const val = this.value.trim();
        if (acTimeout) clearTimeout(acTimeout);
        if (val.length < 2) {
          acList.innerHTML = '';
          acList.classList.add('hidden');
          return;
        }
        acTimeout = setTimeout(() => {
          fetch(`/api/guests/search/?q=${encodeURIComponent(val)}`)
            .then(r => r.json())
            .then(data => {
              acList.innerHTML = '';
              if (data.results && data.results.length > 0) {
                data.results.forEach(g => {
                  const opt = document.createElement('div');
                  opt.className = 'px-4 py-2 cursor-pointer hover:bg-blue-100 flex flex-col text-left';
                  opt.innerHTML = `<span class='font-semibold text-gray-800'>${g.name}</span><span class='text-xs text-gray-500'>${g.invitation_code} &middot; ${g.status}</span>`;
                  opt.addEventListener('mousedown', function(e) {
                    e.preventDefault();
                    input.value = g.invitation_code;
                    acList.innerHTML = '';
                    acList.classList.add('hidden');
                  });
                  acList.appendChild(opt);
                });
                acList.classList.remove('hidden');
              } else {
                acList.classList.add('hidden');
              }
            });
        }, 200);
      });
      // Hide dropdown on blur
      input.addEventListener('blur', function() {
        setTimeout(() => {
          acList.innerHTML = '';
          acList.classList.add('hidden');
        }, 150);
      });
    }
})();
  